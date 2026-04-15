import streamlit as st
import time
import simpy

from core.chord_ring import ChordRing
from visualization.plot_ring import draw_ring
from visualization.latency_plot import measure_latency
from core.simpy_env import LookupSimulation

st.set_page_config(page_title="Chord Simulator", page_icon="🔗", layout="wide")
st.title("🔗 Dynamic Chord Protocol Simulator")

# -------------------------
# SESSION STATE INIT
# -------------------------
if 'ring' not in st.session_state:
    st.session_state.ring = ChordRing(10)

ring = st.session_state.ring

# -------------------------
# DYNAMIC CHURN CONTROLS (JOIN/LEAVE)
# -------------------------
st.sidebar.header("⚡ Network Churn (Join/Leave)")

col1, col2 = st.sidebar.columns(2)
with col1:
    new_node_id = st.number_input("Join ID", 0, 63, 25)
    if st.button("➕ Add Node"):
        if ring.add_node(new_node_id):
            st.sidebar.success(f"Node {new_node_id} joined!")
        else:
            st.sidebar.warning("Node already exists or ring is full.")

with col2:
    leave_node_id = st.number_input("Leave ID", 0, 63, value=ring.node_ids[0] if ring.node_ids else 0)
    if st.button("❌ Fail/Leave"):
        if ring.remove_node(leave_node_id):
            st.sidebar.success(f"Node {leave_node_id} failed!")
        else:
            st.sidebar.error("Node not found.")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Entire Ring"):
    st.session_state.ring = ChordRing(10)
    st.rerun()

# -------------------------
# UI LAYOUT
# -------------------------
col_main, col_side = st.columns([2, 1])

with col_main:
    st.subheader("🔵 Active Ring Topology")
    if not ring.node_ids:
        st.warning("Ring is empty! Add nodes to continue.")
    else:
        fig = draw_ring(ring)
        st.pyplot(fig)

with col_side:
    st.subheader("📌 Node Directory")
    st.write(f"**Active Nodes ({len(ring.node_ids)}):**")
    st.write(ring.node_ids)

    if ring.node_ids:
        st.subheader("📊 Inspect Finger Table")
        inspect_node = st.selectbox("Select Node to Inspect", ring.node_ids)
        node = ring.nodes[inspect_node]
        
        table_data = [{"Start": start_val, "Successor": succ} for start_val, succ in node.finger_table]
        st.dataframe(table_data, use_container_width=True)

st.markdown("---")

# -------------------------
# LOOKUP + ANIMATION
# -------------------------
st.subheader("🔍 Route Lookup")
if ring.node_ids:
    c1, c2 = st.columns(2)
    start = c1.selectbox("Source Node", ring.node_ids)
    key = c2.number_input("Search Key", 0, 63, 15)

    if st.button("🚀 Run Lookup Animation"):
        path = ring.lookup(start, key)

        st.write(f"**Lookup Path:** {' ➔ '.join(map(str, path))}")
        
        st.subheader("🎬 Routing Animation")
        placeholder = st.empty()

        for i in range(len(path)):
            fig = draw_ring(ring, path[:i + 1])
            placeholder.pyplot(fig)
            time.sleep(0.7)

        st.success(f"✅ Key {key} resolved at **Node {path[-1]}** in **{len(path) - 1} hops**!")

        # SimPy execution tracking
        env = simpy.Environment()
        sim = LookupSimulation(env, ring)
        env.process(sim.lookup_process(start, key))
        env.run()

# -------------------------
# PERFORMANCE METRICS
# -------------------------
st.markdown("---")
with st.expander("📈 O(log N) Scalability Analysis"):
    st.write("This graph demonstrates the logarithmic efficiency of the Chord routing protocol as the network size scales.")
    fig = measure_latency()
    st.pyplot(fig)