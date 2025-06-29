import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple, Dict, NewType
from ray.rllib.core.rl_module.torch import TorchRLModule
from ray.rllib.core.rl_module.rl_module import RLModuleConfig
from ray.rllib.utils.typing import TensorType
from ray.rllib.core.columns import Columns
from torch.distributions import Categorical
from ray.rllib.models.torch.misc import SlimFC

# the input layer is transforminf a flat encoding vector in different features tensors to train the model
class InputSplit(nn.Module):
    def __init__(self, num_obs_in_history: int, d_obs: int, d_obs_logical_segments: List[int]):
        super(InputSplit, self).__init__()
        self.num_obs_in_history = num_obs_in_history  # one week hourlyis for example 24*7 = 168
        self.d_obs = d_obs                            # dimension of the observation space which is the number of features used for the asset management (38)
        self.d_obs_logical_segments = d_obs_logical_segments  # list with dimension of all the observational subspaces (2,2,34)

        assert sum(d_obs_logical_segments) == d_obs, \
            "La somme des dimensions des sous-espaces doit être égale à la dimension d'observation."

    def forward(self, obs_history_flat: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        :param obs_history_flat: Tensor [batch_size, time, d_flat], avec d_flat = num_obs_in_history * d_obs
        :return: tuple de 3 tensors séparés selon les segments logiques de l'observation
        """
        batch_size = obs_history_flat.shape[0]

        # reshape in [batch, time, d_obs] = [B, T=168, D=38]
        obs_history = obs_history_flat.view(batch_size, self.num_obs_in_history, self.d_obs)

        # split following observational subspace dimensions  (par ex. [2, 2, 34])
        obs_logical_segments = torch.split(obs_history, self.d_obs_logical_segments, dim=-1)

        obs_history_time = obs_logical_segments[0]
        obs_history_account = obs_logical_segments[1]
        obs_history_candlesticks_btc = obs_logical_segments[2]

        return obs_history_time, obs_history_account, obs_history_candlesticks_btc
    

# each time information is encoding in a higher dimensional space in order to have richer information
class TimeEncoding(nn.Module):
    def __init__(self, num_obs_in_history: int = 168, d_time_enc: int = 96 // 3):
        super(TimeEncoding, self).__init__()

        self.num_obs_in_history = num_obs_in_history
        self.d_time_enc = d_time_enc

        # input size is 2 with the date and its index 
        self.dense_time_encoding = nn.Linear(in_features=2, out_features=self.d_time_enc)
        self.layer_norm_time = nn.LayerNorm(self.d_time_enc)

    def forward(self, obs_history_time: torch.Tensor) -> torch.Tensor:
        # Shape: [batch_size, time, DObsTime], where DObsTime is typically 2 (e.g., hour_of_day, day_of_week)

        # Step 1: Create time_abs_scaled (normalized absolute time) tensor
        # the nn need to now the relative position of each time in the sequence
        b_size = obs_history_time.size(0)
        time_abs_scaled = torch.linspace(0., 1., self.num_obs_in_history, device=obs_history_time.device)
        time_abs_scaled = time_abs_scaled.view(1, self.num_obs_in_history, 1).repeat(b_size, 1, 1)

        # Step 2: Prepare the time_calendar_clock_scaled (the time features)
        time_calendar_clock_scaled = obs_history_time  

        # Step 3: Concatenate time_abs_scaled and time_calendar_clock_scaled
        time_concat = torch.cat([time_abs_scaled, time_calendar_clock_scaled], dim=-1)

        # Step 4: Pass through the dense layer
        obs_history_time_enc = self.dense_time_encoding(time_concat)

        # Step 5: Apply Layer Normalization
        obs_history_time_enc = self.layer_norm_time(obs_history_time_enc)

        return obs_history_time_enc

class AccountEncoding(nn.Module):
    def __init__(self, d_account_enc: int = 96 // 3):
        
        super(AccountEncoding, self).__init__()

        self.d_account_enc = d_account_enc

        self.dense_account_encoding = nn.Linear(in_features=1, out_features=self.d_account_enc)
        self.layer_norm_account = nn.LayerNorm(self.d_account_enc)

    def forward(self,obs_history_account: torch.Tensor) -> torch.Tensor:

        obs_history_account_enc = self.dense_account_encoding(obs_history_account)
        obs_history_account_enc = self.layer_norm_account(obs_history_account_enc)

        return obs_history_account_enc


class ObsEncodingInternal(nn.Module):
    def __init__(self,num_obs_in_history: int = 168, d_time_enc: int = 96 // 3, d_account_enc: int = 96 // 3):

        """
        obs_history_time:      shape [Batch, Time, DObsTime]
        obs_history_account:   shape [Batch, Time, DObsAccount]
        returns:               shape [Batch, Time, DTimeEnc + DAccountEnc]
        """
        
        super(ObsEncodingInternal, self).__init__()

        self.num_obs_in_history = num_obs_in_history
        self.d_time_enc = d_time_enc
        self.d_account_enc = d_account_enc

        self.time_encoding = TimeEncoding(num_obs_in_history=self.num_obs_in_history, d_time_enc=self.d_time_enc)
        self.account_encoding = AccountEncoding(d_account_enc=self.d_account_enc)

    def forward(self,obs_history_time: torch.Tensor,obs_history_account: torch.Tensor) -> torch.Tensor:
        
        obs_history_time_enc = self.time_encoding(obs_history_time=obs_history_time) # [B, T, DTimeEnc]
        
        obs_history_account_enc = self.account_encoding(obs_history_account=obs_history_account) # [B, T, DAccountEnc]

        obs_history_internal_enc = torch.cat([obs_history_time_enc, obs_history_account_enc], dim=-1)  # [B, T, DSum]

        return obs_history_internal_enc
    

class CandlesticksEncoding(nn.Module):
    def __init__(
            self,
            d_candlesticks_btc: int = 34,
            d_candlesticks_enc: int = 256 * 3 // 8,
            ):

        super(CandlesticksEncoding, self).__init__()

        self.d_candlesticks_btc = d_candlesticks_btc
        self.d_candlesticks_enc = d_candlesticks_enc

        self.d_candlesticks_enc_btc = self.d_candlesticks_enc * 4 // 3

        self.dense_candlesticks_btc = torch.nn.Sequential(
            torch.nn.Linear(in_features = self.d_candlesticks_btc, out_features = self.d_candlesticks_enc_btc),
            torch.nn.GELU()
            )        

        self.dense_candlesticks_encoding = nn.Linear(in_features=self.d_candlesticks_btc, out_features=self.d_candlesticks_enc)
        self.layer_norm_candlesticks = nn.LayerNorm(self.d_candlesticks_enc)

    def forward(self,obs_history_candlesticks_btc:torch.Tensor) -> torch.Tensor:

        obs_history_account_enc = self.dense_account_encoding(obs_history_account)
        obs_history_account_enc = self.layer_norm_account(obs_history_account_enc)

        obs_history_candlesticks_enc_btc = self.dense_candlesticks_btc(obs_history_candlesticks_btc)


        """
obs_history_candlesticks_enc_concat = tf.concat(
            [obs_history_ca
             ndlesticks_enc_btc, obs_history_candlesticks_enc_ftm], axis=-1
        )
        """

        obs_history_candlesticks_enc = self.dense_candlesticks_encoding(obs_history_candlesticks_enc_btc)
        
        obs_history_candlesticks_enc = self.layer_norm_candlesticks(obs_history_candlesticks_enc)

        return obs_history_candlesticks_enc



class ObsEncodingExternal(nn.Module):
    def __init__(
            self,
            d_candlesticks_btc: int = 34,
            d_candlesticks_enc: int = 256 * 3 // 8,
        ):

        super(ObsEncodingExternal, self).__init__()

        self.d_candlesticks_btc = d_candlesticks_btc
        self.d_candlesticks_enc = d_candlesticks_enc

        self.candlesticks_encoding = CandlesticksEncoding(
            d_candlesticks_btc=self.d_candlesticks_btc,
            d_candlesticks_enc=self.d_candlesticks_enc
            )

    def forward(self,obs_history_candlesticks_btc: torch.Tensor) -> torch.Tensor:
        
        obs_history_candlesticks_enc = self.candlesticks_encoding(obs_history_candlesticks_btc=obs_history_candlesticks_btc)
        
        obs_external_enc = obs_history_candlesticks_enc

        return obs_external_enc
    

class Stem(nn.Module):
    def __init__(
            self,
            num_obs_in_history: int = 168,
            d_time_enc: int = 256 // 8,
            d_account_enc: int = 256 // 8,
            d_candlesticks_btc: int = 34,
            d_candlesticks_enc: int = 256 * 3 // 8,
        ):

        super(Stem, self).__init__()

        self.num_obs_in_history = num_obs_in_history
        self.d_time_enc = d_time_enc
        self.d_account_enc = d_account_enc

        self.d_candlesticks_btc = d_candlesticks_btc
        self.d_candlesticks_enc = d_candlesticks_enc

        self.obs_encoding_internal = ObsEncodingInternal(
            num_obs_in_history=self.num_obs_in_history,
            d_time_enc=self.d_time_enc,
            d_account_enc=self.d_account_enc
        )
        
        self.obs_encoding_external = ObsEncodingExternal(
            d_candlesticks_btc=self.d_candlesticks_btc,
            d_candlesticks_enc=self.d_candlesticks_enc,
        )

    def forward(
            self,
            obs_history_time: torch.Tensor,
            obs_history_account: torch.Tensor,
            obs_history_candlesticks_btc: torch.Tensor,
        ) -> Tuple[torch.Tensor,torch.Tensor]:
        """Tensor3[float32, Batch, Time, DObsInternalEnc],
            Tensor3[float32, Batch, Time, DObsExternalEnc]
            """

        obs_history_internal_enc = self.obs_encoding_internal(
            obs_history_time=obs_history_time,
            obs_history_account=obs_history_account,
        )

        obs_history_external_enc = self.obs_encoding_external(obs_history_candlesticks_btc=obs_history_candlesticks_btc)

        return obs_history_internal_enc, obs_history_external_enc

class StemOutputConcatenation(nn.Module):
    def __init__(self):
        super(StemOutputConcatenation, self).__init__()

    # obs_history_internal_enc [Batch, Time, DObsInternalEnc],
    # obs_history_external_enc: [Batch, Time, DObsExternalEnc]
    def forward(
            self,
            obs_history_internal_enc,
            obs_history_external_enc
        ) -> torch.Tensor:

        obs_history_stem_enc = torch.cat([obs_history_internal_enc, obs_history_external_enc], dim=-1)

        return obs_history_stem_enc

class AttentionBlock(nn.Module):
    def __init__(
            self,
            num_heads: int = 4,
            dropout_rate: float = 0.1,
            d_obs_internal_enc: int = 256 // 4,
            d_obs_external_enc: int = 256 * 3 // 4,
            ):

        super(AttentionBlock, self).__init__()

        self.num_heads = num_heads
        self.dropout_rate = dropout_rate
        self.d_obs_internal_enc = d_obs_internal_enc
        self.d_obs_external_enc = d_obs_external_enc

        self.d_model = self.d_obs_internal_enc + self.d_obs_external_enc
        self.d_ff_intermediate = self.d_model * 3 // 2

        self.attn_mha = nn.MultiheadAttention(embed_dim=self.d_model, num_heads=self.num_heads, batch_first=True)
        self.attn_dense = nn.Linear(in_features = self.d_model, out_features = self.d_obs_external_enc)
        self.attn_layer_norm = nn.LayerNorm(self.d_obs_external_enc)

        self.ff_dense_1 = nn.Linear(in_features = self.d_model, out_features = self.d_ff_intermediate)
        self.ff_dense_2 = nn.Linear(in_features = self.d_ff_intermediate, out_features = self.d_obs_external_enc)
        self.ff_dropout = nn.Dropout(p = self.dropout_rate)
        self.ff_layer_norm = nn.LayerNorm(normalized_shape = self.d_obs_external_enc)
  
    def forward(
            self,
            obs_history_internal_enc: torch.Tensor,  # [B, T, D_int]
            obs_history_external_enc: torch.Tensor,  # [B, T, D_ext]
        ) -> torch.Tensor: # [float32, Batch, Time, DObsExternalEnc]

        # Multi-head attention (Self-attention)
        attn_block_input = obs_history_external_enc  # [B, T, D_ext]
        obs_history_enc = torch.cat([obs_history_internal_enc, attn_block_input], dim=-1)  # [B, T, D_model]
        attn_mha_output, attn_mha_output_weights = self.attn_mha(query = obs_history_enc, key = obs_history_enc, value = obs_history_enc)  # [B, T, DObsStemEnc]
        attn_dense_output = self.attn_dense(attn_mha_output)  # [B, T, D_ext]
        # addition + normalization
        attn_add_output = attn_block_input + attn_dense_output  # Residual
        attn_block_output = self.attn_layer_norm(attn_output)  # [B, T, D_ext]

        # Feedforward block
        ff_block_input = attn_block_output #[Batch, Time, D_ext]
        obs_history_enc = torch.cat([obs_history_internal_enc, ff_block_input], dim=-1)  # [B, T, D_model]
        ff_dense_1_output = F.gelu(self.ff_dense_1(obs_history_enc))  # [B, T, D_ff_inter]
        ff_dense_2_output = self.ff_dense_2(ff_dense_1_output)  # [B, T, D_ext]

        # dropout
        ff_dropout_output = self.ff_dropout(ff_dense_2_output) #[Batch, Time, D_ext]

        # addition + nprmalization
        ff_add_output = ff_block_input + ff_dropout_output
        ff_block_output = self.ff_layer_norm(ff_add_output) # [B, T, D_ext]
    
        return ff_block_output

class TransformerOutputTimePooling(nn.Module):
    def __init__(self):
        super(TransformerOutputTimePooling, self).__init__()

    def forward(self,obs_history_stem_enc: torch.Tensor, obs_history_transformer_enc: torch.Tensor) -> torch.Tensor:

        # obs_history_stem_enc [Batch, Time, D_model]
        # obs_history_transformer_enc [Batch, Time, D_ext]
        
        last_obs_stem_enc = obs_history_stem_enc[:, -1, :]
        last_obs_transformer_enc = obs_history_transformer_enc[:, -1, :]

        last_obs_enc = torch.cat([last_obs_stem_enc, last_obs_transformer_enc], dim=-1)

        return last_obs_enc

# layer connected to the output of the pool layer to take the decision
# input: [Batch, DObsTranfEnc = D_model + D_ext]
# output: [Batch, NOutputs (actions)]
class ActionBranch(nn.Module):
    def __init__(self, num_inputs: int, num_actions: int):
        super(ActionBranch, self).__init__()

        self.num_inputs = num_inputs
        self.num_actions = num_actions
        self.dense = nn.Linear(in_features = self.num_inputs, out_features = self.num_actions)

    def forward(self,inputs: torch.Tensor) -> torch.Tensor:

        act_logits = self.dense(inputs)

        return act_logits

# layer for computing the the value of taking some action
class ValueBranch(nn.Module):
    def __init__(self,num_actions):
        super(ValueBranch, self).__init__()

        self.num_actions = num_actions
        self.dense = nn.Linear(in_features = self.num_actions, out_features = 1)

    def forward(self,actions: torch.Tensor) -> torch.Tensor:

        value = self.dense(actions)

        return value

class Transformer(nn.Module):
    def __init__(
        self,
        d_history_flat: int = 168 * 38,
        num_obs_in_history: int = 168,
        d_obs: int = 38,
        d_time: int = 2,
        d_account: int = 2,
        d_candlesticks_btc: int = 34,
        d_obs_enc: int = 256,
        num_attn_blocks: int = 3,
        num_heads: int = 4,
        dropout_rate: float = 0.1,
        num_outputs: int = 4,
    ):
        
        super(Transformer, self).__init__()

        self.d_history_flat = d_history_flat
        self.num_obs_in_history = num_obs_in_history
        self.d_obs = d_obs

        self.d_time = d_time
        self.d_account = d_account
        self.d_candlesticks_btc = d_candlesticks_btc

        self.d_obs_enc = d_obs_enc
        self.num_attn_blocks = num_attn_blocks
        self.num_heads = num_heads
        self.dropout_rate = dropout_rate

        self.num_outputs = num_outputs

        self.d_time_enc = self.d_obs_enc // 8
        self.d_account_enc = self.d_obs_enc // 8
        self.d_candlesticks_enc = self.d_obs_enc * 3 // 8

        self.d_obs_internal_enc = self.d_time_enc + self.d_account_enc
        self.d_obs_external_enc = self.d_candlesticks_enc #+ self.d_santiment_enc

        self.d_obs_logical_segments = [
            self.d_time,
            self.d_account,
            self.d_candlesticks_btc,
        ]

        assert self.d_obs_enc % 8 == 0
        assert self.d_history_flat == self.num_obs_in_history * self.d_obs
        assert self.d_obs == sum(self.d_obs_logical_segments)

        self.input_split = InputSplit(
            num_obs_in_history=self.num_obs_in_history,
            d_obs=self.d_obs,
            d_obs_logical_segments=self.d_obs_logical_segments
        )

        self.stem = Stem(
            num_obs_in_history=self.num_obs_in_history,
            d_time_enc=self.d_time_enc,
            d_account_enc=self.d_account_enc,
            d_candlesticks_btc=self.d_candlesticks_btc,
            d_candlesticks_enc=self.d_candlesticks_enc,
        )

        self.stem_output_concatenation = StemOutputConcatenation()

        self.attention_blocks: List[AttentionBlock] = [
            AttentionBlock(
                num_heads=self.num_heads,
                dropout_rate=self.dropout_rate,
                d_obs_internal_enc=self.d_obs_internal_enc,
                d_obs_external_enc=self.d_obs_external_enc,
            ) for i in range(self.num_attn_blocks)
        ]

        self.transformer_output_time_pooling = TransformerOutputTimePooling()

        #self.action_branch = ActionBranch(num_inputs = 2 * self.d_obs_external_enc + self.d_obs_internal_enc, num_actions = self.num_outputs)
        self.action_branch = SlimFC(in_size=2 * self.d_obs_external_enc + self.d_obs_internal_enc, out_size=self.num_outputs)
        self.value_branch = ValueBranch(num_actions = self.num_outputs)

    def forward(self, obs_history_flat: torch.Tensor):

        # [Batch, DFlatHistory]
        obs_history_flat = obs_history_flat

        obs_logical_segments = self.input_split(obs_history_flat=obs_history_flat)

        # [Batch, Time, DObsTime]
        obs_history_time = obs_logical_segments[0]
        obs_history_account = obs_logical_segments[1] # [Batch, Time, DObsAccount]
        obs_history_candlesticks_btc = obs_logical_segments[2] # [Batch, Time, DObsCandlesticksBTC]

        obs_logical_segments_enc = self.stem(
            obs_history_time=obs_history_time,
            obs_history_account=obs_history_account,
            obs_history_candlesticks_btc=obs_history_candlesticks_btc,
        )
        
        obs_history_internal_enc = obs_logical_segments_enc[0] # [Batch, Time, DObsInternalEnc]
        obs_history_external_enc = obs_logical_segments_enc[1] # [Batch, Time, DObsExternalEnc]

        # [Batch, Time, DObsStemEnc]
        obs_history_stem_enc = self.stem_output_concatenation(
            obs_history_internal_enc=obs_history_internal_enc,
            obs_history_external_enc=obs_history_external_enc
        )

        # [Batch, Time, DObsExternalEnc]
        for i in range(self.num_attn_blocks):
            obs_history_external_enc = self.attention_blocks[i](
                obs_history_internal_enc=obs_history_internal_enc,
                obs_history_external_enc=obs_history_external_enc,
            )

        obs_history_transformer_enc = obs_history_external_enc # [Batch, Time, DObsExternalEnc]

        # [Batch, DObsTranfEnc]
        current_obs_transformer_enc: Tensor2 = self.transformer_output_time_pooling(
            obs_history_stem_enc = obs_history_stem_enc,
            obs_history_transformer_enc = obs_history_transformer_enc
        )

        logits = self.action_branch(inputs=current_obs_transformer_enc) # [Batch, NOutputs (actions)]
        values = self.value_branch(inputs=current_obs_transformer_enc) # [Batch, Const1]

        return logits, values
    

class oneAssetTradeTransformer(TorchRLModule):
        
    def setup(self):

        self.d_history_flat = self.model_config["d_history_flat"]
        self.num_obs_in_history = self.model_config["num_obs_in_history"]
        self.d_obs = self.model_config["d_obs"]
        self.d_time = self.model_config["d_time"]
        self.d_account = self.model_config["d_account"]
        self.d_candlesticks_btc = self.model_config["d_candlesticks_btc"]
        self.d_obs_enc = self.model_config["d_obs_enc"]

        self.num_attn_blocks = self.model_config["num_attn_blocks"]
        self.num_heads = self.model_config["num_heads"]
        self.dropout_rate = self.model_config["dropout_rate"]
        
        self.num_outputs = self.model_config["num_outputs"]
        
        self.model = Transformer(
            d_history_flat=self.d_history_flat,
            num_obs_in_history=self.num_obs_in_history,
            d_obs=self.d_obs,
            d_time=self.d_time,
            d_account=self.d_account,
            d_candlesticks_btc=self.d_candlesticks_btc,
            d_obs_enc=self.d_obs_enc,
            num_attn_blocks=self.num_attn_blocks,
            num_heads=self.num_heads,
            dropout_rate=self.dropout_rate,
            num_outputs=self.num_outputs
        )

    def _forward(
        self,
        input_dict: Dict[str, TensorType],
        **kwargs
    ) :

        print("okkkkkkkk")
        print(input_dict)

        # input_dict Dict[str, TensorType]
        # state List[Tensor2[float32, Batch, Depth]]
        # seq_lens Tensor1[int32, Batch]

        # output
        # Tuple[
        # Tensor2[float32, Batch, NOutputs],
        # List[Tensor2[float32, Batch, Depth]]]
        
        # [Batch, DFlatHistory]
        obs_history_flat = input_dict["obs"]
        
        # [Batch, NOutputs]
        logits: torch.Tensor
        # [float32, Batch, Const1]
        values: torch.Tensor

        action_logits, values = self.model(obs_history_flat=obs_history_flat)

        print("logits are")
        print(action_logits)

        # [Batch, Const1]
        self._value_out: torch.Tensor
        self._value_out = values

        dist = Categorical(logits=action_logits)
        actions = dist.sample()

        return {
            "actions": actions,
            "logits": action_logits,
        }, state

    # [Batch]
    def value_function(self) -> torch.Tensor:
        return self._value_out.view(-1)




