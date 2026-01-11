import json
import matplotlib.pyplot as plt
import glob
import math

# File generated with the help of gemini

# 1. Collect all files first to know how many subplots we need
files = sorted(glob.glob("results_*nodes.json"))
num_node_tests = len(files)

# We create a layout: 
# Top row: The main Scaling (Time) plot
# Bottom row(s): Individual Learning plots for each node test
fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(2, num_node_tests)

ax_time = fig.add_subplot(gs[0, :]) # Main time plot spans the whole top row

# 2. Iterate through files to plot
for i, file in enumerate(files):
    with open(file, "r") as f:
        data = json.load(f)
        nodes = data["nodes"]
        
        # --- PART 1: TIME SCALING (Main Top Graph) ---
        counts = []
        times = []
        for w_count, details in data["results"].items():
            counts.append(int(w_count))
            times.append(details["time"])
        
        # Sort for clean lines
        sorted_time = sorted(zip(counts, times))
        s_counts, s_times = zip(*sorted_time)
        ax_time.plot(s_counts, s_times, marker='o', label=f"{nodes} Nodes")

        # --- PART 2: INDIVIDUAL LEARNING PLOTS (Bottom Row) ---
        ax_reward = fig.add_subplot(gs[1, i])
        
        for w_count, details in data["results"].items():
            rewards = details["rewards"]
            ax_reward.plot(range(len(rewards)), rewards, label=f"{w_count} Workers")
        
        ax_reward.set_title(f"Learning: {nodes} Node Cluster")
        ax_reward.set_xlabel("Iteration")
        ax_reward.set_ylabel("Mean Reward")
        ax_reward.set_ylim(0, 520) # Keep scale consistent
        ax_reward.grid(True, alpha=0.3)
        ax_reward.legend(fontsize='small')

# --- FINAL FORMATTING ---
ax_time.set_title("Overall Scaling Efficiency")
ax_time.set_xlabel("Total Workers")
ax_time.set_ylabel("Seconds (10 Iterations)")
ax_time.grid(True, linestyle='--', alpha=0.6)
ax_time.legend()

plt.tight_layout()
plt.savefig("master_report_plots.png")
print(f"\n[SUCCESS] Master plot with {num_node_tests} sub-graphs saved.")
plt.show()
