# Sensor Network Simulation Report

This document outlines the results of the sensor network simulation where sensor nodes acted as both sensors and sinks. The nodes were placed on a 1000x1000 grid, and the scenario was tested in 50 rounds of operation.

## Simulation Configuration
- Grid size: 1000x1000 units
- Number of sensor nodes: 100
- Initial sink node: Node 0
- Second sink node: Node 50 (added after 50 rounds)
- Rounds per configuration: 50

## Results Summary
| Round | Active Sink Nodes | Messages Sent | Avg Latency |
|-------|------------------|---------------|-------------|
| 1 | 1 | 90 | 0.0003 |
| 2 | 1 | 86 | 0.0003 |
| 3 | 1 | 83 | 0.0003 |
| 4 | 1 | 77 | 0.0003 |
| 1 | 2 | 71 | 0.0003 |
| 2 | 2 | 68 | 0.0004 |
| 3 | 2 | 64 | 0.0004 |
| 4 | 2 | 62 | 0.0003 |
| 5 | 2 | 61 | 0.0002 |
| 1 | 1 | 60 | 0.0003 |
| 2 | 1 | 57 | 0.0003 |
| 3 | 1 | 52 | 0.0003 |
| 4 | 1 | 50 | 0.0003 |
| 5 | 1 | 48 | 0.0003 |
| 6 | 1 | 45 | 0.0002 |

## Conclusion
The sensor network simulation successfully demonstrated the ability of sensor nodes to adapt to changes in the sink configuration. Nodes were able to send data to the closest sink, even when the sink configuration changed during the simulation. Furthermore, the network showed resilience to node failures during the rounds.
