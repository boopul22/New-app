import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from auth import check_password
from user_data import UserHistory

# Set page configuration
st.set_page_config(
    page_title="Usage Stats - Text Rewriter",
    page_icon="📊",
    layout="wide"
)

# Check authentication before showing anything
if check_password():
    # Add custom CSS
    st.markdown("""
        <style>
        .stat-card {
            background: var(--card-bg, #ffffff);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            text-align: center;
        }
        .stat-number {
            font-size: 32px;
            font-weight: bold;
            color: #2196F3;
            margin: 10px 0;
        }
        .stat-label {
            font-size: 16px;
            color: #666;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.title("📊 Usage Statistics")
    
    # Initialize user history
    user_history = UserHistory()
    stats = user_history.get_usage_stats()
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="stat-card">
                <div class="stat-label">Total Rewrites</div>
                <div class="stat-number">{:,}</div>
            </div>
        """.format(stats["total_rewrites"]), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="stat-card">
                <div class="stat-label">Total Characters Processed</div>
                <div class="stat-number">{:,}</div>
            </div>
        """.format(stats["total_characters"]), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="stat-card">
                <div class="stat-label">Average Text Length</div>
                <div class="stat-number">{:,.0f}</div>
            </div>
        """.format(stats["avg_text_length"]), unsafe_allow_html=True)
    
    # Daily usage chart
    st.subheader("Daily Usage")
    daily_usage = user_history.get_daily_usage()
    
    df = pd.DataFrame(list(daily_usage.items()), columns=['Date', 'Rewrites'])
    df['Date'] = pd.to_datetime(df['Date'])
    
    fig = px.line(df, x='Date', y='Rewrites',
                  title='Rewrites per Day',
                  line_shape='linear')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Rewrites",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Usage heatmap
    st.subheader("Usage Heatmap")
    history = user_history.get_history()
    
    # Convert timestamps to hour of day
    hours = [datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S").hour 
            for entry in history]
    
    # Create hour distribution
    hour_dist = pd.Series(hours).value_counts().sort_index()
    
    # Create heatmap data
    heatmap_data = [[hour_dist.get(hour, 0)] for hour in range(24)]
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        y=[f"{i:02d}:00" for i in range(24)],
        x=['Usage'],
        colorscale='Blues'
    ))
    
    fig.update_layout(
        title='Usage by Hour of Day',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True) 