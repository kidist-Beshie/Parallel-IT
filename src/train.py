import ray
from ray.rllib.algorithms.ppo import PPOConfig

ray.init()

algo = (
    PPOConfig()
    .environment("CartPole-v1")
    .env_runners(num_env_runners=2)
    .build()
)

for i in range(10):
    result = algo.train()
    print(i, result["env_runners"]["episode_return_mean"])
