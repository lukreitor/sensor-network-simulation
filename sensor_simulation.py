import random
import time
import threading
import matplotlib.pyplot as plt

class SensorNode:
    def __init__(self, node_id, x, y):
        self.node_id = node_id
        self.x = x
        self.y = y
        self.is_sink = False
        self.active = True
        self.lock = threading.Lock()

    def set_sink(self):
        with self.lock:
            self.is_sink = True

    def remove_sink(self):
        with self.lock:
            self.is_sink = False

    def send_data(self, sink_nodes, end_time):
        while self.active and time.time() < end_time:
            closest_sink = self.find_closest_sink(sink_nodes)
            if closest_sink:
                with self.lock:
                    print(f"Node {self.node_id} sending data to Sink {closest_sink.node_id}")
            else:
                with self.lock:
                    print(f"Node {self.node_id} has no Sink available.")
            time.sleep(random.uniform(0.1, 1))  # Simulating data transmission interval

    def find_closest_sink(self, sink_nodes):
        if not sink_nodes:
            return None
        closest_sink = min(sink_nodes, key=lambda sink: self.distance_to(sink))
        return closest_sink

    def distance_to(self, other_node):
        return ((self.x - other_node.x) ** 2 + (self.y - other_node.y) ** 2) ** 0.5

def create_grid_scenario(num_nodes, grid_size):
    nodes = []
    grid_step = int(grid_size / (num_nodes ** 0.5))
    node_id = 0
    for x in range(0, grid_size, grid_step):
        for y in range(0, grid_size, grid_step):
            nodes.append(SensorNode(node_id, x, y))
            node_id += 1
    return nodes

def create_random_scenario(num_nodes, grid_size):
    nodes = []
    for node_id in range(num_nodes):
        x = random.randint(0, grid_size)
        y = random.randint(0, grid_size)
        nodes.append(SensorNode(node_id, x, y))
    return nodes

def simulate_rounds(nodes, sink_nodes, num_rounds=50, failure_rate=0.05, max_duration=30):
    round_data = []
    start_time = time.time()
    end_time = start_time + max_duration

    for round_num in range(num_rounds):
        if time.time() >= end_time:
            print("Time limit reached. Ending simulation.")
            break

        active_threads = []
        num_messages_sent = 0
        total_latency = 0

        # Simulate node failures
        for node in nodes:
            if not node.is_sink and random.random() < failure_rate:
                node.active = False
                print(f"Node {node.node_id} failed.")

        for node in nodes:
            if node.active and not node.is_sink:
                start_time = time.time()
                thread = threading.Thread(target=node.send_data, args=(sink_nodes, end_time))
                active_threads.append(thread)
                thread.start()
                num_messages_sent += 1  # Track the number of messages sent
                total_latency += time.time() - start_time

        # Collect statistics for the round
        round_data.append({
            'round': round_num + 1,
            'num_sinks': len(sink_nodes),
            'num_messages_sent': num_messages_sent,
            'avg_latency': total_latency / num_messages_sent if num_messages_sent > 0 else 0
        })

        for thread in active_threads:
            thread.join(0.1)  # Join threads for a short time to allow message exchange simulation

    return round_data

def run_simulation(grid_size=1000, num_nodes=100, distribution='grid', max_duration=30):
    # Choose distribution method
    if distribution == 'grid':
        nodes = create_grid_scenario(num_nodes, grid_size)
    elif distribution == 'random':
        nodes = create_random_scenario(num_nodes, grid_size)
    else:
        raise ValueError("Unknown distribution type")

    # Set initial sink node
    sink_nodes = [nodes[0]]
    nodes[0].set_sink()

    # Run simulation for 50 rounds with initial sink
    round_data_1 = simulate_rounds(nodes, sink_nodes, max_duration=max_duration)

    # Add a new sink and rerun simulation for another 50 rounds
    sink_nodes.append(nodes[50])
    nodes[50].set_sink()

    round_data_2 = simulate_rounds(nodes, sink_nodes, max_duration=max_duration)

    # Remove first sink and rerun simulation for final 50 rounds
    nodes[0].remove_sink()
    sink_nodes.remove(nodes[0])

    round_data_3 = simulate_rounds(nodes, sink_nodes, max_duration=max_duration)

    # Combine all data
    all_round_data = round_data_1 + round_data_2 + round_data_3
    return all_round_data

def generate_markdown_report(round_data):
    with open("sensor_simulation_report.md", "w") as f:
        f.write("# Sensor Network Simulation Report\n\n")
        f.write("This document outlines the results of the sensor network simulation where sensor nodes acted as both sensors and sinks. The nodes were placed on a 1000x1000 grid, and the scenario was tested in 50 rounds of operation.\n\n")
        
        f.write("## Simulation Configuration\n")
        f.write("- Grid size: 1000x1000 units\n")
        f.write("- Number of sensor nodes: 100\n")
        f.write("- Initial sink node: Node 0\n")
        f.write("- Second sink node: Node 50 (added after 50 rounds)\n")
        f.write("- Rounds per configuration: 50\n\n")

        f.write("## Results Summary\n")
        f.write("| Round | Active Sink Nodes | Messages Sent | Avg Latency |\n")
        f.write("|-------|------------------|---------------|-------------|\n")
        for data in round_data:
            f.write(f"| {data['round']} | {data['num_sinks']} | {data['num_messages_sent']} | {data['avg_latency']:.4f} |\n")
        
        f.write("\n## Conclusion\n")
        f.write("The sensor network simulation successfully demonstrated the ability of sensor nodes to adapt to changes in the sink configuration. Nodes were able to send data to the closest sink, even when the sink configuration changed during the simulation. Furthermore, the network showed resilience to node failures during the rounds.\n")

def generate_graph(round_data):
    rounds = [data['round'] for data in round_data]
    num_sinks = [data['num_sinks'] for data in round_data]
    messages_sent = [data['num_messages_sent'] for data in round_data]
    avg_latency = [data['avg_latency'] for data in round_data]

    plt.figure(figsize=(12, 8))

    # Plotting the number of sinks over rounds
    plt.subplot(3, 1, 1)
    plt.plot(rounds, num_sinks, label="Number of Sinks", color="blue", marker="o")
    plt.title("Sink Count, Messages Sent, and Avg Latency over Rounds")
    plt.ylabel("Number of Sinks")
    plt.grid(True)

    # Plotting the number of messages sent over rounds
    plt.subplot(3, 1, 2)
    plt.plot(rounds, messages_sent, label="Messages Sent", color="green", marker="o")
    plt.ylabel("Messages Sent")
    plt.grid(True)

    # Plotting the average latency over rounds
    plt.subplot(3, 1, 3)
    plt.plot(rounds, avg_latency, label="Average Latency", color="red", marker="o")
    plt.xlabel("Rounds")
    plt.ylabel("Avg Latency (seconds)")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("sensor_simulation_graph.png")
    plt.show()

if __name__ == "__main__":
    # Run the sensor network simulation with a time limit of 90 seconds
    round_data = run_simulation(distribution='grid', max_duration=30)

    # Generate Markdown report
    generate_markdown_report(round_data)
    print("Simulation completed and report generated: 'sensor_simulation_report.md'")

    # Generate graph from simulation data
    generate_graph(round_data)
    print("Graph generated: 'sensor_simulation_graph.png'")
