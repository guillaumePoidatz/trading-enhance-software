import gymnasium as gym
import numpy as np
import os

from ray.tune import registry
from ray.rllib.core.rl_module.rl_module import RLModuleSpec
from ray.rllib.algorithms.ppo import PPOConfig

from RLTraining.envs.training_env_long import LearningCryptoEnv
from RLTraining.models.oneAssetTradeTransformer import oneAssetTradeTransformer

registry.register_env(
    name='CryptoEnv',
    env_creator=lambda env_config: LearningCryptoEnv(**env_config)
)


# create RL agent
ppo_config = (
    PPOConfig()
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
            "logdir": os.getcwd()
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
    .rl_module(
            model_config=DefaultModelConfig(free_log_std=True),
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
        train_batch_size=2 * 2 * 168, # num_rollout_workers * num_envs_per_worker * rollout_fragment_length
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
        num_env_runners=2,
        num_envs_per_env_runner=2,
        rollout_fragment_length=168,
        batch_mode='complete_episodes',
        preprocessor_pref=None,
        gym_env_vectorize_mode=("ASYNC"),
    )
    .resources(
        num_gpus=1
    )
    .debugging(
        log_level='WARN' # DEBUG INFO WARN ERROR CRITICAL
    )
    .api_stack(enable_rl_module_and_learner=True, enable_env_runner_and_connector_v2=True)
)
