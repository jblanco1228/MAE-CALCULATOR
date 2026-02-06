"""
Super Analyst MAE Calculator - Web Interface
Simple, beautiful UI for calculating QA system accuracy
"""

import streamlit as st
import pandas as pd
from mae_calculator import calculate_mae, interpret_mae, calculate_batch_mae
import json

# Page configuration
st.set_page_config(
    page_title="Super Analyst MAE Calculator",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .excellent { color: #28a745; font-weight: bold; }
    .good { color: #5cb85c; font-weight: bold; }
    .acceptable { color: #ffc107; font-weight: bold; }
    .poor { color: #dc3545; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">📊 Super Analyst MAE Calculator</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar for mode selection
st.sidebar.title("⚙️ Settings")
mode = st.sidebar.radio(
    "Select Mode:",
    ["Single Chat", "Batch Upload (CSV)", "Quick Test"]
)

# KPI list
KPIS = [
    'IssueIdentification',
    'ResolutionCompliance',
    'Clarity',
    'Retention',
    'Sentiment',
    'CustomerCentricity'
]

def get_mae_color_class(mae):
    """Return CSS class based on MAE value"""
    if mae < 0.50:
        return "excellent"
    elif mae < 0.75:
        return "good"
    elif mae < 1.00:
        return "acceptable"
    else:
        return "poor"


# MODE 1: SINGLE CHAT
if mode == "Single Chat":
    st.header("🎯 Single Chat Evaluation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 AI Scores")
        chat_id = st.text_input("Chat ID:", value="27811316")
        
        ai_scores = {}
        for kpi in KPIS:
            ai_scores[kpi] = st.slider(
                f"{kpi}:",
                min_value=0,
                max_value=5,
                value=3,
                key=f"ai_{kpi}"
            )
    
    with col2:
        st.subheader("👤 Human Scores")
        st.write("")  # Spacing to align with chat_id input
        st.write("")
        
        human_scores = {}
        for kpi in KPIS:
            human_scores[kpi] = st.slider(
                f"{kpi}:",
                min_value=0,
                max_value=5,
                value=3,
                key=f"human_{kpi}"
            )
    
    # Calculate button
    if st.button("Calculate MAE", type="primary", use_container_width=True):
        result = calculate_mae(ai_scores, human_scores)
        
        st.markdown("---")
        st.header("📈 Results")
        
        # Main MAE metric
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("MAE Score", f"{result.mae:.2f}")
        with col_b:
            st.metric("Total Difference", f"{result.total_difference:.0f}")
        with col_c:
            mae_class = get_mae_color_class(result.mae)
            st.markdown(f'<p class="{mae_class}" style="font-size: 1.2rem; margin-top: 0.5rem;">{result.interpretation}</p>', 
                       unsafe_allow_html=True)
        
        # Detailed breakdown
        st.subheader("📋 KPI Breakdown")
        
        df_data = []
        for kpi in KPIS:
            df_data.append({
                'KPI': kpi,
                'AI Score': ai_scores[kpi],
                'Human Score': human_scores[kpi],
                'Difference': result.kpi_differences[kpi],
                'Match': '✅' if result.kpi_differences[kpi] == 0 else '❌'
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)


# MODE 2: BATCH UPLOAD
elif mode == "Batch Upload (CSV)":
    st.header("📁 Batch Chat Evaluation")
    
    st.info("Upload a CSV file with columns: chat_id, ai_IssueIdentification, ai_ResolutionCompliance, ai_Clarity, ai_Retention, ai_Sentiment, ai_CustomerCentricity, human_IssueIdentification, human_ResolutionCompliance, human_Clarity, human_Retention, human_Sentiment, human_CustomerCentricity")
    
    # Sample CSV download
    sample_data = {
        'chat_id': ['27811316', '27811317'],
        'ai_IssueIdentification': [4, 3],
        'ai_ResolutionCompliance': [3, 2],
        'ai_Clarity': [2, 3],
        'ai_Retention': [2, 3],
        'ai_Sentiment': [3, 4],
        'ai_CustomerCentricity': [4, 3],
        'human_IssueIdentification': [4, 4],
        'human_ResolutionCompliance': [3, 3],
        'human_Clarity': [2, 2],
        'human_Retention': [2, 3],
        'human_Sentiment': [4, 4],
        'human_CustomerCentricity': [3, 4]
    }
    sample_df = pd.DataFrame(sample_data)
    
    st.download_button(
        label="📥 Download Sample CSV Template",
        data=sample_df.to_csv(index=False),
        file_name="mae_sample_template.csv",
        mime="text/csv"
    )
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        st.subheader("Preview Data")
        st.dataframe(df.head(), use_container_width=True)
        
        if st.button("Calculate Batch MAE", type="primary"):
            # Process the data
            chats = []
            for _, row in df.iterrows():
                ai_scores = {
                    'IssueIdentification': int(row['ai_IssueIdentification']),
                    'ResolutionCompliance': int(row['ai_ResolutionCompliance']),
                    'Clarity': int(row['ai_Clarity']),
                    'Retention': int(row['ai_Retention']),
                    'Sentiment': int(row['ai_Sentiment']),
                    'CustomerCentricity': int(row['ai_CustomerCentricity'])
                }
                human_scores = {
                    'IssueIdentification': int(row['human_IssueIdentification']),
                    'ResolutionCompliance': int(row['human_ResolutionCompliance']),
                    'Clarity': int(row['human_Clarity']),
                    'Retention': int(row['human_Retention']),
                    'Sentiment': int(row['human_Sentiment']),
                    'CustomerCentricity': int(row['human_CustomerCentricity'])
                }
                chats.append({
                    'chat_id': str(row['chat_id']),
                    'ai_scores': ai_scores,
                    'human_scores': human_scores
                })
            
            avg_mae, results = calculate_batch_mae(chats)
            
            st.markdown("---")
            st.header("📊 Batch Results")
            
            # Overall metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average MAE", f"{avg_mae:.2f}")
            with col2:
                st.metric("Total Chats", len(chats))
            with col3:
                mae_class = get_mae_color_class(avg_mae)
                st.markdown(f'<p class="{mae_class}" style="font-size: 1.2rem; margin-top: 0.5rem;">{interpret_mae(avg_mae)}</p>', 
                           unsafe_allow_html=True)
            
            # Detailed results table
            st.subheader("Individual Chat Results")
            results_data = []
            for chat, result in zip(chats, results):
                results_data.append({
                    'Chat ID': chat['chat_id'],
                    'MAE': f"{result.mae:.2f}",
                    'Total Diff': result.total_difference,
                    'Interpretation': result.interpretation
                })
            
            results_df = pd.DataFrame(results_data)
            st.dataframe(results_df, use_container_width=True, hide_index=True)
            
            # Download results
            st.download_button(
                label="📥 Download Results CSV",
                data=results_df.to_csv(index=False),
                file_name=f"mae_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )


# MODE 3: QUICK TEST
else:
    st.header("⚡ Quick Test with Example Data")
    
    st.info("Testing with ChatID 27811316 (your example)")
    
    # Example data
    ai_scores = {
        'IssueIdentification': 4,
        'ResolutionCompliance': 3,
        'Clarity': 2,
        'Retention': 2,
        'Sentiment': 3,
        'CustomerCentricity': 4
    }
    
    human_scores = {
        'IssueIdentification': 4,
        'ResolutionCompliance': 3,
        'Clarity': 2,
        'Retention': 2,
        'Sentiment': 4,
        'CustomerCentricity': 3
    }
    
    if st.button("Run Quick Test", type="primary", use_container_width=True):
        result = calculate_mae(ai_scores, human_scores)
        
        st.markdown("---")
        st.success("✅ Test completed successfully!")
        
        # Display results
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("MAE Score", f"{result.mae:.2f}")
        with col2:
            st.metric("Expected", "0.33")
        with col3:
            if abs(result.mae - 0.33) < 0.01:
                st.success("✅ Match!")
            else:
                st.error("❌ Mismatch")
        
        st.subheader("Detailed Breakdown")
        df_data = []
        for kpi in KPIS:
            df_data.append({
                'KPI': kpi,
                'AI Score': ai_scores[kpi],
                'Human Score': human_scores[kpi],
                'Difference': result.kpi_differences[kpi]
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown(f"**Interpretation:** {result.interpretation}")


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>Super Analyst MAE Calculator</strong> | Platinum-CS-Collabs</p>
    <p style='font-size: 0.9rem;'>MAE < 0.50 = Excellent | MAE < 0.75 = Good | MAE < 1.00 = Acceptable | MAE > 1.00 = Poor</p>
</div>
""", unsafe_allow_html=True)
