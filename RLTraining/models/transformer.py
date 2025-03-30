from ray.rllib.core.rl_module.rl_module import RLModule
from ray.rllib.utils.typing import TensorType
import tensorflow as tf
from typing import Dict, Tuple


class TransformerModelAdapter(RLModule):
    def __init__(
        self,
        obs_space,
        action_space,
        num_outputs,
        model_config,
        name,
        d_history_flat: int = 168 * 38,
        num_obs_in_history: int = 168,
        d_obs: int = 34,
        d_time: int = 2,
        d_account: int = 2,
        d_candlesticks_btc: int = 34,
        d_obs_enc: int = 64,
        num_attn_blocks: int = 3,
        num_heads: int = 4,
        dropout_rate: float = 0.1
    ):
        super(TransformerModelAdapter, self).__init__(
            obs_space, action_space, num_outputs, model_config, name
        )
        
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

        self.model = TransformerModel(
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

    def forward(
        self,
        input_dict: Dict[str, TensorType],
        state: List[Tensor2[float32, Batch, Depth]],
        seq_lens: Tensor1[int32, Batch],
    ) -> Tuple[
        Tensor2[float32, Batch, NOutputs],
        List[Tensor2[float32, Batch, Depth]]
    ]:
                
        obs_history_flat: Tensor2[float32, Batch, DFlatHistory] = input_dict["obs"]
        training: bool = input_dict["is_training"]
        
        logits: Tensor2[float32, Batch, NOutputs]
        values: Tensor2[float32, Batch, Const1]

        logits, values = self.model(inputs=obs_history_flat, training=training)

        self._value_out: Tensor2[float32, Batch, Const1]
        self._value_out = values

        return logits, []
    
    def value_function(self) -> Tensor1[float32, Batch]:
        return tf.reshape(self._value_out, [-1])

