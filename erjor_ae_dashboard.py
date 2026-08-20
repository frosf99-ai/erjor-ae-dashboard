import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="ERJOR AE Activity & Citations",
    page_icon="📊",
    layout="wide"
)

# Load and cache data
@st.cache_data
def load_data():
    df = pd.read_excel('AE-citations-combined.xlsx', sheet_name='Sheet1')
    
    # Convert Excel date serial to datetime
    # Excel stores dates as serial numbers from 1900-01-01
    df['Latest Decision Date'] = pd.to_datetime(
        df['Latest Decision Date'], 
        unit='D', 
        origin=pd.Timestamp('1899-12-30')
    )
    
    return df

df = load_data()

# Use all available data (shows full career history at ERJOR)
df_12m = df.copy()

# Compute AE metrics
ae_metrics = df_12m.groupby('Editor Names').agg({
    'Number of Citations': ['count', 'mean', 'median', 'sum'],
    'Manuscript ID - Original': 'count'
}).round(2)

ae_metrics.columns = ['review_count', 'avg_citations', 'median_citations', 'total_citations', '_']
ae_metrics = ae_metrics.drop('_', axis=1)
ae_metrics = ae_metrics.sort_values('review_count', ascending=False).reset_index()
ae_metrics['rank'] = range(1, len(ae_metrics) + 1)
ae_metrics['Editor Name (Clean)'] = ae_metrics['Editor Names'].str.replace('(Associate Editor)', '').str.strip()

# ============================================================================
# SIDEBAR: Identification
# ============================================================================
st.sidebar.header("🔐 Identify Yourself")
st.sidebar.write("Enter your surname to see your position and activity.")

user_surname = st.sidebar.text_input(
    "Your surname:",
    placeholder="e.g., Frost",
    help="Your name as it appears in the ERJOR database"
).strip()

identified_ae = None
if user_surname:
    # Case-insensitive match on surname
    matches = ae_metrics[
        ae_metrics['Editor Name (Clean)'].str.contains(user_surname, case=False, na=False)
    ]
    if len(matches) == 1:
        identified_ae = matches.iloc[0]
    elif len(matches) > 1:
        st.sidebar.warning("⚠️ Multiple matches. Please be more specific.")
    else:
        st.sidebar.error("❌ No match found. Check spelling and try again.")

# ============================================================================
# MAIN PAGE
# ============================================================================
st.title("ERJOR Associate Editor Activity & Citations")
date_min = df['Latest Decision Date'].min()
date_max = df['Latest Decision Date'].max()
st.markdown(f"_Full career data ({date_min.strftime('%b %Y')} – {date_max.strftime('%b %Y')})_")

# ============================================================================
# SECTION 1: Individual AE View (if identified)
# ============================================================================
if identified_ae is not None:
    st.divider()
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.subheader("📍 Your Position in the Pack")
        
        rank_col, reviews_col, avg_cites_col = st.columns(3)
        with rank_col:
            st.metric(
                "Rank",
                f"#{identified_ae['rank']} of {len(ae_metrics)}"
            )
        with reviews_col:
            st.metric(
                "Total Reviews",
                int(identified_ae['review_count'])
            )
        with avg_cites_col:
            st.metric(
                "Avg Citations",
                f"{identified_ae['avg_citations']:.1f}"
            )
        
        # Pack comparison
        review_counts = ae_metrics['review_count'].values
        percentile = (sum(review_counts < identified_ae['review_count']) / len(review_counts) * 100)
        
        st.write(f"""
        **Your metrics:**
        - Total citations across reviews: {int(identified_ae['total_citations'])}
        - Median citations per review: {identified_ae['median_citations']:.1f}
        - You're in the **top {100 - percentile:.0f}%** by review volume
        """)
    
    with col2:
        # Histogram of review counts with your position highlighted
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=ae_metrics['review_count'],
            nbinsx=15,
            name='All AEs',
            marker_color='#0072B5',
            opacity=0.7
        ))
        
        fig.add_vline(
            x=identified_ae['review_count'],
            line_dash="dash",
            line_color="#BC3C29",
            annotation_text=f"You: {int(identified_ae['review_count'])} reviews",
            annotation_position="top right"
        )
        
        fig.update_layout(
            title="Your Position in Pack Distribution",
            xaxis_title="Total Reviews",
            yaxis_title="Count of AEs",
            height=300,
            showlegend=False,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Your papers
    st.subheader("📄 Your Reviews & Citations")
    user_papers = df_12m[
        df_12m['Editor Names'] == identified_ae['Editor Names']
    ][['Item Title', 'Number of Citations', 'Manuscript Type', 'Latest Decision Date', 'Accept or Reject Final Decision']].copy()
    
    user_papers['Latest Decision Date'] = user_papers['Latest Decision Date'].dt.strftime('%b %Y')
    user_papers = user_papers.sort_values('Number of Citations', ascending=False)
    user_papers.columns = ['Paper Title', 'Citations', 'Type', 'Decision Date', 'Outcome']
    
    st.dataframe(
        user_papers,
        use_container_width=True,
        height=400,
        hide_index=True
    )
    
    # Download
    csv = user_papers.to_csv(index=False)
    st.download_button(
        label="📥 Download your papers (CSV)",
        data=csv,
        file_name=f"ERJOR_my_reviews_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# ============================================================================
# SECTION 2: Anonymized Pack Rankings (always shown)
# ============================================================================
st.divider()
st.subheader("📊 Anonymized AE Rankings (All Data)")

# Ranking table
ranking_table = ae_metrics[[
    'rank', 'review_count', 'avg_citations', 'median_citations', 'total_citations'
]].copy()

ranking_table.columns = ['Rank', 'Reviews', 'Avg Citations', 'Median Citations', 'Total Citations']

# Highlight identified AE
if identified_ae is not None:
    def highlight_row(row):
        if row['Rank'] == identified_ae['rank']:
            return ['background-color: #E8F4F8'] * len(row)
        return [''] * len(row)
    
    styled_table = ranking_table.style.apply(highlight_row, axis=1)
else:
    styled_table = ranking_table.style

st.dataframe(
    styled_table,
    use_container_width=True,
    height=600,
    hide_index=True
)

# ============================================================================
# SECTION 3: Pack Statistics
# ============================================================================
st.divider()
st.subheader("📈 Pack Statistics")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total AEs", len(ae_metrics))
with col2:
    st.metric("Total Reviews (All)", int(ae_metrics['review_count'].sum()))
with col3:
    st.metric("Mean/AE", f"{ae_metrics['review_count'].mean():.1f}")
with col4:
    st.metric("Median/AE", f"{ae_metrics['review_count'].median():.0f}")

# Citation distribution across the pack
fig_citations = go.Figure()

fig_citations.add_trace(go.Box(
    y=ae_metrics['avg_citations'],
    name='Avg Citations per Review',
    marker_color='#0072B5',
    boxmean='sd'
))

fig_citations.update_layout(
    title="Distribution of Average Citations per Review Across AEs",
    yaxis_title="Average Citations",
    height=350,
    showlegend=False
)

st.plotly_chart(fig_citations, use_container_width=True)

# ============================================================================
# SECTION 4: Notes
# ============================================================================
st.divider()
st.markdown("""
**Notes on this dashboard:**
- Rankings are anonymized; only you can identify yourself
- Data covers all reviews processed through ERJOR (full career history)
- Citation counts are from Web of Science JCR (may include self-citations)
- "Avg/Median Citations" reflects papers you reviewed and their subsequent citation impact
- This is a tool for reflecting on editorial contribution and paper impact, not performance evaluation
""")
