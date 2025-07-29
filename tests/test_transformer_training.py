import pytest
import logging
import gymnasium as gym
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.core.rl_module.rl_module import RLModuleSpec
from ray import init, shutdown

from trading_enhance_software.rl_training.models.one_asset_trade_transformer import (
    oneAssetTradeTransformer,
)

logging.getLogger(__name__)


@pytest.fixture(scope="module", autouse=True)
def ray_setup_teardown():
    init(ignore_reinit_error=True)
    yield
    shutdown()


def test_transformer_trains():
    env_name = "CartPole-v1"
    env = gym.make(env_name)

    action_space = env.action_space

    d_time = 1
    d_account = 1
    d_candlesticks_btc = 2
    d_obs = d_time + d_account + d_candlesticks_btc
    num_obs_in_history = 1
    d_history_flat = num_obs_in_history * d_obs
    num_outputs = action_space.n

    model_config = {
        "d_history_flat": d_history_flat,
        "num_obs_in_history": num_obs_in_history,
        "d_obs": d_obs,
        "d_time": d_time,
        "d_account": d_account,
        "d_candlesticks_btc": d_candlesticks_btc,
        "d_obs_enc": 256,
        "num_attn_blocks": 3,
        "num_heads": 4,
        "dropout_rate": 0.1,
        "num_outputs": num_outputs,
    }

    config = (
        PPOConfig()
        .environment(env_name)
        .framework("torch")
        .rl_module(
            rl_module_spec=RLModuleSpec(
                module_class=oneAssetTradeTransformer,
                model_config=model_config,
            )
        )
        .training(use_critic=True, use_gae=True)
    )

    trainer = config.build()

    result = trainer.train()

    # Debug: affiche toutes les clés pour savoir ce qui est dispo
    logging.info("Training result keys:", result.keys())

    # Cherche la clé la plus fiable
    reward = result.get("episode_reward_mean") or result.get(
        "evaluation/episode_reward_mean"
    )

    assert reward is not None, "No episode reward found in result"
    assert isinstance(reward, (int, float)), f"Reward is not a number: {reward}"

    trainer.stop()
