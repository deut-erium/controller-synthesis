import argparse
import gym
from gym.spaces import Discrete, Box
import numpy as np
import os

import ray
from ray import tune
from ray.tune import grid_search
from ray.rllib.models import ModelCatalog
from ray.rllib.models.tf.tf_modelv2 import TFModelV2
from ray.rllib.models.tf.fcnet import FullyConnectedNetwork
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.models.torch.fcnet import FullyConnectedNetwork as TorchFC
from ray.rllib.utils.framework import try_import_tf, try_import_torch
from ray.rllib.utils.test_utils import check_learning_achieved

from ray.rllib.env.multi_agent_env import MultiAgentEnv, make_multi_agent

MultiAgentCartPole = make_multi_agent("CartPole-v0")


import ray
from ray.rllib import agents
ray.init() # Skip or set to ignore if already called
config = {'gamma': 0.9,
          'lr': 1e-2,
          'num_workers': 4,
          'train_batch_size': 1000,
          'model': {
              'fcnet_hiddens': [128, 128]
          }}
trainer = agents.ppo.PPOTrainer(env='CartPole-v0', config=config)
results = trainer.train()

if __name__ == "__main__":
    args = parser.parse_args()
    ray.init()

    # Can also register the env creator function explicitly with:
    # register_env("corridor", lambda config: SimpleCorridor(config))
    ModelCatalog.register_custom_model(
        "my_model", TorchCustomModel if args.torch else CustomModel)

    config = {
        "env": SimpleCorridor,  # or "corridor" if registered above
        "env_config": {
            "corridor_length": 5,
        },
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
        "num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "0")),
        "model": {
            "custom_model": "my_model",
            "vf_share_layers": True,
        },
        "lr": grid_search([1e-2, 1e-4, 1e-6]),  # try different lrs
        "num_workers": 1,  # parallelism
        "framework": "torch" if args.torch else "tf",
    }

    stop = {
        "training_iteration": args.stop_iters,
        "timesteps_total": args.stop_timesteps,
        "episode_reward_mean": args.stop_reward,
    }

    results = tune.run(args.run, config=config, stop=stop)

    if args.as_test:
        check_learning_achieved(results, args.stop_reward)
    ray.shutdown()