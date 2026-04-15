import matplotlib.pyplot as plt
from core.chord_ring import ChordRing
import random


def measure_latency():
    sizes = [5, 10, 15, 20, 25, 30]
    avg_hops = []

    for n in sizes:
        ring = ChordRing(n)
        hops_list = []

        for _ in range(10):
            start = random.choice(ring.node_ids)
            key = random.randint(0, 63)
            path = ring.lookup(start, key)
            hops_list.append(len(path) - 1)

        avg_hops.append(sum(hops_list) / len(hops_list))

    fig, ax = plt.subplots()

    ax.plot(sizes, avg_hops, marker='o')
    ax.set_xlabel("Number of Nodes (N)")
    ax.set_ylabel("Average Hops")
    ax.set_title("O(log N) Lookup Performance")

    return fig