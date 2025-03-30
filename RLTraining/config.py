import gymnasium as gym
import numpy as np

from ray.tune import registry
from ray.rllib.models.catalog import ModelCatalog
from ray.rllib.algorithms.ppo import PPOConfig

from envs.training_env_long import LearningCryptoEnv
from models.transformer import TransformerModelAdapter

# personalized model derived from Transformer and named TransformerModelAdapter
ModelCatalog.register_custom_model(
    model_name='TransformerModelAdapter',
    model_class=TransformerModelAdapter
)

registry.register_env(
    name='CryptoEnv',
    env_creator=lambda env_config: LearningCryptoEnv(**env_config)
)

# create RL agent
ppo_config = (
    PPOConfig()
    # .rl_module(_enable_rl_module_api=False)
    .framework('tf2')
    .environment(
        env='CryptoEnv',
        env_config={
            "dataset_name": "dataset",  # .npy files should be in ./data/dataset/
            "leverage": 2, # leverage for perpetual futures
            "episode_max_len": 168 * 2, # train episode length, 2 weeks
            "lookback_window_len": 168, 
            "train_start": [2000, 7000, 12000, 17000, 22000],
            "train_end": [6000, 11000, 16000, 21000, 26000], 
            "test_start": [6000, 11000, 16000, 21000, 26000],
            "test_end": [7000, 12000, 17000, 22000, 29377-1], 
            "order_size": 50, # dollars
            "initial_capital": 1000, # dollars
            "open_fee": 0.12e-2, # taker_fee
            "close_fee": 0.12e-2, # taker_fee
            "maintenance_margin_percentage": 0.012, # 1.2 percent
            "initial_random_allocated": 0, # opened initial random long/short position up to initial_random_allocated $
            "regime": "training",
            "record_stats": False, # True for backtesting
            # "cold_start_steps": 0, # do nothing at the beginning of the episode
        },
        observation_space=gym.spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(183 * 168,),
            dtype=np.float32
        ),
        action_space=gym.spaces.Discrete(4),
    )
    .training(
        lr=5e-5,
        gamma=0.995, # 1 recent reward are more important (discount factor).
        grad_clip=30., # max value of the gradient will be 30
        entropy_coeff=0.03, # for exploration of action space
        kl_coeff=0.05, # is set in order to slow down or speed up the training depending on kl_target
        kl_target=0.01, # target of the divergence between two policies
        num_epochs=10,
        use_gae=True, # Generalized Advantage Estimation
        # lambda=0.95,
        clip_param=0.3, # limit the difference between two successive policies
        vf_clip_param=10, #  limit the difference between two successive velue functions
        train_batch_size=15 * 8 * 168, # num_rollout_workers * num_envs_per_worker * rollout_fragment_length
        model={
            "vf_share_layers": False,
            "custom_model": "TransformerModelAdapter",
            "custom_model_config": {
                "d_history_flat": 168 * 38,
                "num_obs_in_history": 168,
                "d_obs": 38,
                "d_time": 2,
                "d_account": 2,
                "d_candlesticks_btc": 34, # TA indicators
                "d_obs_enc": 64,
                "num_attn_blocks": 3,
                "num_heads": 4,
                "dropout_rate": 0.1
            }
        }
    )
    .evaluation(
        evaluation_interval=1,
        evaluation_duration=8,
        evaluation_duration_unit='episodes',
        evaluation_parallel_to_training=False,
        evaluation_config={
            "explore": False,
            "env_config": {
                "regime": "evaluation",
                "record_stats": False, # True for backtesting
                "episode_max_len": 168 * 2, # validation episode length
                "lookback_window_len": 168, 
            }
        },
        evaluation_num_env_runners=4
    )
    .env_runners(
        num_env_runners=15,
        num_envs_per_env_runner=8,
        rollout_fragment_length=168,
        batch_mode='complete_episodes',
        preprocessor_pref=None
    )
    .resources(
        num_gpus=1
    )
    .debugging(
        log_level='WARN' # DEBUG INFO WARN ERROR CRITICAL
    )
)
