import simpy


class LookupSimulation:
    def __init__(self, env, ring):
        self.env = env
        self.ring = ring

    def lookup_process(self, start, key):
        print(f"\n[Time {self.env.now}] Start lookup from Node {start}")

        path = self.ring.lookup(start, key)

        for node in path:
            yield self.env.timeout(1)
            print(f"[Time {self.env.now}] Visiting Node {node}")

        print(f"[Time {self.env.now}] Lookup Complete at Node {path[-1]}")