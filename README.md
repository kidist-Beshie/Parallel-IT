# Distributed PPO on Grid5000

This project runs distributed PPO training using Ray RLlib on the Grid5000 cluster.

## Structure
- src/: training scripts
- cluster/: Ray cluster setup
- results/: logs, plots, metrics

## How to run
Launch ray on diffrent nodes:
- head:
    cluster/setup_head.sh
- worker:
    setup_worker.sh <HEAD-IP>


# REPORT: Distributed RL Benchmarking on Grid'5000

## Section: Scaling Observations

Our results demonstrate **Amdahl's Law** in practice. While we increased the computational resources (nodes and workers), we observed a significant performance penalty when moving from a single-node to a multi-node configuration. 

The table below highlights the "Network Tax" paid when distributing the same workload across the cluster:

| Nodes | Workers | Total Time (s) | Latency Penalty vs. 1-Node |
| :--- | :--- | :--- | :--- |
| **1 (Local)** | 2 | 94.03s | 0% (Baseline) |
| **2 (Dist.)** | 2 | 136.81s | **+45.5%** |
| **3 (Dist.)** | 2 | 138.28s | **+47.1%** |
| **4 (Dist.)** | 2 | 135.42s | **+44.0%** |

The table below compares the performance of each cluster at its **highest tested worker capacity**:

| Nodes | Max Workers Tested | Total Time (s) | Efficiency vs. 1-Node |
| :--- | :--- | :--- | :--- |
| **1 (Local)** | 8 | **81.61s** | **100% (Fastest)** |
| **2 (Dist.)** | 48 | 113.90s | 71.6% (Slower) |
| **3 (Dist.)** | 64 | 115.18s | 70.8% (Slower) |
| **4 (Dist.)** | 64 | 115.95s | 70.4% (Slower) |

The table below highlights the **fastest execution time** achieved for each node configuration:

| Nodes | Fastest Worker Config | Total Time (s) | Efficiency vs. 1-Node |
| :--- | :--- | :--- | :--- |
| **1 (Local)** | 8 Workers | **81.61s** | **100% (Baseline)** |
| **2 (Dist.)** | 24 Workers | 113.34s | 72.0% |
| **3 (Dist.)** | 32 Workers | 113.52s | 71.9% |
| **4 (Dist.)** | 2 Workers | 135.42s | 60.2% |

**Analysis:** The data shows a "Scaling Wall." The fastest execution occurred on a single node with 8 workers. As soon as the workload was distributed (2+ nodes), the execution time jumped by ~30 seconds and stayed there, regardless of how many more nodes or workers were added. This proves that the **Inter-node Latency** (TCP/IP communication) is the primary bottleneck, not the number of CPUs.



## Section: Efficiency Bottlenecks

The **CartPole-v1** environment is computationally "light." Consequently, the "worker coordination overhead" dominates the execution time. This is evident across all multi-node tests:

* **3-Node Test:** 24 to 64 workers → ~114s to ~115s.
* **4-Node Test:** 24 to 64 workers → ~116s to ~115s.

The system is bottlenecked by the **Head node's ability to aggregate results** (the sequential portion of the task). Adding more nodes or workers beyond a certain point yields **zero speedup**, as the time saved by parallel physics simulation is entirely consumed by the overhead of managing a larger number of remote heartbeats and data buffers.



## Section: Learning Performance

Contrary to intuition, higher worker counts did not lead to higher rewards within our 10-iteration window. In fact, the most distributed configurations (e.g., 4 nodes with 64 workers) often showed slower reward growth compared to the single-node baseline.

This is likely due to the **increased effective batch size**. With 64 workers, the agent collects a massive amount of data before each policy update. For simple environments, this makes the learning updates "coarse" and less efficient than the frequent, nimble updates possible on a single node. This represents a classic trade-off in RL between **throughput** (samples collected per second) and **sample efficiency** (how much the agent learns from each sample).

## Conclusion

This experiment highlights that horizontal scaling is not a "magic button" for performance. For small-scale problems like CartPole, the communication latency between nodes on the Grid'5000 cluster creates a performance floor. Distributed computing is most effective when the environment is computationally heavy, where the time spent calculating physics outweighs the time spent sending data over the network.

---

### Final Visualization
![Benchmark scaling and learning curves](./results/master_report_plots.png)
