import ray
from ray.rllib.algorithms.ppo import PPOConfig

ray.init(address="auto")

algo = (
    PPOConfig()
    .environment("CartPole-v1")
    .env_runners(num_env_runners=8)
    .build()
)

for i in range(10):
    result = algo.train()
    mean_return = result["env_runners"]["episode_return_mean"]
    tps = result["env_runners"]["sampled_timesteps_per_second"]
    print(i, mean_return, tps)

