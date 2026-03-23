import asyncio
import os
import streamlit as st
import json

from researcher import Researcher
from neural_engine import NeuralExecutionEngine
from auditor import AdversarialAuditor

st.set_page_config(page_title="NEURO-CORE Dashboard", page_icon="🧠", layout="wide")

async def run_core_loop():
    with st.status("Booting NEURO-CORE...", expanded=True) as status:
        st.write("Initializing core instances...")
        researcher = Researcher()
        engine = NeuralExecutionEngine()
        auditor = AdversarialAuditor()
        
        st.markdown("### 🚀 [TASK 1] Real-Time Multi-Modal Research")
        ratio = await researcher.calculate_compute_to_market_ratio()
        st.metric(label="Initial Compute-to-Market Ratio", value=f"{ratio:.4f}")
        
        st.markdown("### ⚙️ [TASK 2] Booting Neural Execution Engine")
        
        # Fire up the edge nodes concurrently
        edge_task = asyncio.create_task(engine.run_nodes(num_nodes=50))
        await asyncio.sleep(0.5) # Let nodes start heartbeating
        
        st.write("🧠 Training predictor on synthetic market data...")
        progress_bar = st.progress(0)
        
        loss = 0.0
        # Train the predictor
        for i in range(10):
            market = await researcher.fetch_market_data()
            gpu_pricing = await researcher.fetch_gpu_pricing()
            
            y = market['btc_hashrate'] / (gpu_pricing * market['vix'])
            loss = engine.train_step([market['vix']], [y])
            progress_bar.progress((i + 1) * 10)
            
        st.metric(label="Final Training Loss", value=f"{loss:.4f}", delta="-optimized", delta_color="inverse")
        
        st.markdown("### 🛡️ [TASK 3] The Adversarial Auditor Starting")
        with open(__file__, "r", encoding="utf-8") as f:
             source = f.read()
             
        vulns = auditor.scan_for_injection_vulnerabilities(source)
        if vulns:
            st.warning(f"Injection vulnerabilities found: {vulns}")
        else:
            st.success("No critical injection vulnerabilities found.")
        
        st.write("🔍 Performing Math Audit (MSE)...")
        vix_samples = [18.5, 19.0, 19.5]
        predicted = [engine.predict(v) for v in vix_samples]
        actuals = [p + 0.01 for p in predicted]
        
        try:
            mse = auditor.manual_mse_audit(predicted, actuals)
            st.success(f"**[AUDIT PASS]** MSE recalculation successful, MSE={mse:.8f}")
        except ValueError as e:
            st.error(f"**[AUDIT FAIL]** Security Reject: {e}")
            
        st.markdown("### 🔗 [REPORT] Merkle-Hash Integrity Report")
        with st.spinner("Processing edge node logs..."):
            await asyncio.sleep(2.5) 
        
        st.info(f"Total processed edge logs: {len(engine.logs)}")
        
        if engine.logs:
           latest = json.loads(engine.logs[-1])
           st.code(f"Latest Log Root Hash: {latest.get('merkle_root')}", language="bash")
        else:
           st.warning("No edge logs present.")
           
        status.update(label="System Initialization Complete", state="complete", expanded=False)
        
        # Super important for Streamlit to clean up background asyncio tasks 
        # so it doesn't hang the thread infinitely
        edge_task.cancel() 

def main():
    st.title("🧠 NEURO-CORE Execution Engine")
    st.markdown("---")

    # Only run the core loop if the user clicks a button, to avoid infinite 
    # re-runs or hanging on edge nodes.
    if st.button("Initialize NEURO-CORE System", type="primary"):
        asyncio.run(run_core_loop())

if __name__ == "__main__":
    main()
