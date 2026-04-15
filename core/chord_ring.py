import random
from core.node import Node

M = 6
MAX_ID = 2 ** M

class ChordRing:
    def __init__(self, n):
        self.node_ids = sorted(random.sample(range(MAX_ID), n))
        self.nodes = {nid: Node(nid) for nid in self.node_ids}
        self.build_ring()
        self.build_finger_tables()

    def build_ring(self):
        if not self.node_ids:
            return
        for i, nid in enumerate(self.node_ids):
            successor_id = self.node_ids[(i + 1) % len(self.node_ids)]
            predecessor_id = self.node_ids[(i - 1) % len(self.node_ids)]
            
            self.nodes[nid].set_successor(self.nodes[successor_id])
            self.nodes[nid].set_predecessor(self.nodes[predecessor_id])

    def find_successor(self, key):
        if not self.node_ids: return None
        for nid in self.node_ids:
            if key <= nid:
                return self.nodes[nid]
        return self.nodes[self.node_ids[0]]

    def build_finger_tables(self):
        for node in self.nodes.values():
            if not node.is_active: continue
            table = []
            for i in range(M):
                start = (node.id + 2 ** i) % MAX_ID
                succ = self.find_successor(start)
                table.append((start, succ.id))
            node.update_finger_table(table)

    def add_node(self, new_id):
        if new_id not in self.node_ids and len(self.node_ids) < MAX_ID:
            self.node_ids.append(new_id)
            self.node_ids.sort()
            self.nodes[new_id] = Node(new_id)
            self.build_ring()
            self.build_finger_tables()
            return True
        return False

    def remove_node(self, target_id):
        if target_id in self.node_ids:
            self.nodes[target_id].is_active = False
            self.node_ids.remove(target_id)
            del self.nodes[target_id]
            self.build_ring()
            self.build_finger_tables()
            return True
        return False

    def lookup(self, start_id, key):
        path = []
        if start_id not in self.nodes:
            return path
            
        current = self.nodes[start_id]

        while True:
            path.append(current.id)

            if current.successor is None or self.in_range(key, current.id, current.successor.id):
                if current.successor:
                    path.append(current.successor.id)
                break

            next_node = current
            for start, fid in reversed(current.finger_table):
                if self.in_range(fid, current.id, key) and fid in self.nodes:
                    next_node = self.nodes[fid]
                    break

            if next_node == current:
                next_node = current.successor

            if next_node is None or next_node.id in path: 
                break # Prevent infinite loops in unstable states

            current = next_node

        return path

    def in_range(self, val, start, end):
        if start < end:
            return start < val <= end
        return val > start or val <= end