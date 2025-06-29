from ray.rllib.core.rl_module.rl_module import RLModule
from ray.rllib.utils.typing import TensorType
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import NewType, Dict, Tuple, List
from tensor_annotations.tensorflow import Tensor0, Tensor1, Tensor2
from tensor_annotations.tensorflow import float32, int32
from tensor_annotations.axes import Batch, Depth, Axis

NOutputs = NewType('NOutputs', Axis)

class oneAssetTradeTransformer(RLModule):
    def __init__(
        self,
        observation_space,
        action_space,
        model_config,
        d_history_flat: int = 168 * 38,
        num_obs_in_history: int = 168,
        d_obs: int = 34,
        d_time: int = 2,
        d_account: int = 2,
        d_candlesticks_btc: int = 34,
        d_obs_enc: int = 64,
        num_attn_blocks: int = 3,
        num_heads: int = 4,
        dropout_rate: float = 0.1,
        **kwargs
    ):
        super().__init__()
        print("KWARGS:", kwargs)

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
        
        # Defining a simple feedforward layer as an example. Adjust as needed.
        self.fc1 = nn.Linear(self.d_history_flat, 512)
        self.fc2 = nn.Linear(512, self.d_obs_enc)
        self.fc3 = nn.Linear(self.d_obs_enc, self.d_obs)

    def forward(
        self,
        input_dict: Dict[str, TensorType],
        state: List[Tensor2[float32, Batch, Depth]],
        seq_lens: Tensor1[int32, Batch],
    ) -> Tuple[
        Tensor2[float32, Batch, NOutputs],
        List[Tensor2[float32, Batch, Depth]]
    ]:
        # Extract the observation from the input_dict (assumed to be a tensor).
        obs_history_flat = input_dict["obs"]
        
        # Apply the forward pass through the model (example: simple feed-forward layers)
        x = F.relu(self.fc1(obs_history_flat))
        x = F.relu(self.fc2(x))
        logits = self.fc3(x)
        
        # Example value function (for PPO)
        values = logits.mean(dim=1, keepdim=True)

        return logits, values

    def value_function(self) -> Tensor1[float32, Batch]:
        # Return the value output from the model (reshape for compatibility)
        return self._value_out.view(-1)

