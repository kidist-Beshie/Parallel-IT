import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import ray
from ray.rllib.algorithms.ppo import PPOConfig
import matplotlib.pyplot as plt

# Start Ray
ray.init(ignore_reinit_error=True)

# Configure PPO on CartPole-v1
config = (
    PPOConfig()
    .environment("CartPole-v1")
    .framework("torch")
    .env_runners(num_env_runners=1)
)

# Build the algorithm (new API uses build_algo())
algo = config.build_algo()

# Train for 5 iterations
rewards = []
for i in range(20):
    result = algo.train()
    # In new API, mean reward is under 'metrics.episode_reward_mean'
    mean_reward = result.get("metrics", {}).get("episode_reward_mean", 0)
    rewards.append(mean_reward)
    print(f"Iteration {i+1}, mean reward = {mean_reward:.2f}")
# Save reward plot
plt.plot(range(1, 6), rewards, marker="o")
plt.title("PPO Training on CartPole-v1")
plt.xlabel("Iteration")
plt.ylabel("Mean Reward")
plt.grid(True)
plt.savefig("training_plot.png")
print("Training plot saved as training_plot.png")

