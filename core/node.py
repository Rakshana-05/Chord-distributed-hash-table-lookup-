class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.finger_table = []
        self.successor = None
        self.predecessor = None
        self.is_active = True

    def set_successor(self, node):
        self.successor = node

    def set_predecessor(self, node):
        self.predecessor = node

    def update_finger_table(self, table):
        self.finger_table = table

    def __repr__(self):
        status = "🟢" if self.is_active else "🔴"
        return f"Node({self.id}) {status}"