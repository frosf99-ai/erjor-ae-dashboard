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
    # Load main AE dataset
    ae_df = pd.read_csv('AEs.csv', encoding='latin-1')
    ae_df['Latest Decision Date'] = pd.to_datetime(ae_df['Latest Decision Date'], errors='coerce')
    
    # Load citations data
    citations_df = pd.read_excel('AE-citations-combined.xlsx', sheet_name='Sheet1')
    citations_df['Latest Decision Date'] = pd.to_datetime(
        citations_df['Latest Decision Date'], 
        unit='D', 
        origin=pd.Timestamp('1899-12-30')
    )
    
    # Merge on Manuscript ID to get citations
    merged = ae_df.merge(
        citations_df[['Manuscript ID - Original', 'Number of Citations']],
        on='Manuscript ID - Original',
        how='left'
    )
    # Fill missing citations with 0
    merged['Number of Citations'] = merged['Number of Citations'].fillna(0)
    
    return merged

df = load_data()

# Set time window: Aug 2022 - Aug 2024
cutoff_start = pd.Timestamp('2022-08-01')
cutoff_end = pd.Timestamp('2024-08-31')
df_filtered = df[
    (df['Latest Decision Date'] >= cutoff_start) & 
    (df['Latest Decision Date'] <= cutoff_end)
].copy()

# Compute AE metrics
# Count all papers reviewed (accepted + rejected)
review_counts = df_filtered.groupby('Editor Names').size().reset_index(name='review_count')

# Calculate citations metrics from ACCEPTED PAPERS ONLY
df_accepted = df_filtered[df_filtered['Accept or Reject Final Decision'] == 'Accept'].copy()
citation_metrics = df_accepted.groupby('Editor Names').agg({
    'Number of Citations': ['mean', 'median', 'sum'],
}).round(2)
citation_metrics.columns = ['avg_citations', 'median_citations', 'total_citations']
citation_metrics = citation_metrics.reset_index()

# Merge review counts with citation metrics
ae_metrics = review_counts.merge(citation_metrics, on='Editor Names', how='left')
ae_metrics = ae_metrics.sort_values('review_count', ascending=False).reset_index(drop=True)
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
st.markdown(f"**Data for the 2025 Journal Citation Report window** (Papers published in Aug 2022–Aug 2024)")

# Calculate pack totals (always needed for later sections)
total_accepts = len(df_filtered[df_filtered['Accept or Reject Final Decision'] == 'Accept'])
total_rejects = len(df_filtered[df_filtered['Accept or Reject Final Decision'] == 'Reject'])

# ============================================================================
# SECTION 1: Overall ERJ Open Research Statistics
# ============================================================================
st.divider()
st.subheader("📈 Overall ERJ Open Research Statistics")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total AEs", len(ae_metrics))
with col2:
    st.metric("Total Reviews (All)", int(ae_metrics['review_count'].sum()))
with col3:
    st.metric("Mean/AE", f"{ae_metrics['review_count'].mean():.1f}")
with col4:
    st.metric("Median/AE", f"{ae_metrics['review_count'].median():.0f}")

# Accept/Reject summary
col1, col2, col3 = st.columns(3)
total_all = total_accepts + total_rejects

with col1:
    st.metric("Total Accepts", total_accepts)
with col2:
    st.metric("Total Rejects", total_rejects)
with col3:
    accept_rate = (total_accepts / total_all * 100) if total_all > 0 else 0
    st.metric("Accept Rate", f"{accept_rate:.1f}%")

# Citations summary
col1, col2, col3 = st.columns(3)
total_cites = int(ae_metrics['total_citations'].sum())
mean_cites_per_ae = ae_metrics['avg_citations'].mean()

with col1:
    st.metric("Total Citations (All AEs)", total_cites)
with col2:
    st.metric("Mean Avg Citations/AE", f"{mean_cites_per_ae:.2f}")
with col3:
    st.metric("Median Avg Citations/AE", f"{ae_metrics['avg_citations'].median():.2f}")

# Manuscript Type breakdown across pack
st.subheader("📋 All Papers by Manuscript Type")
manuscript_all = df_filtered['Manuscript Type'].value_counts()

fig_types_all = go.Figure(data=[go.Pie(
    labels=manuscript_all.index,
    values=manuscript_all.values,
    marker_colors=['#0072B5', '#BC3C29', '#E18727', '#20854E', '#7876B1', '#FFC000', '#00B4D8', '#90E0EF'],
    textposition='inside',
    textinfo='label+percent',
    hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>'
)])

fig_types_all.update_layout(
    title=f"All Papers by Manuscript Type ({len(df_filtered)} total)",
    height=400,
)
st.plotly_chart(fig_types_all, use_container_width=True)

# ============================================================================
# SECTION 2: Individual AE View (if identified)
# ============================================================================
if identified_ae is not None:
    st.divider()
    
    # ===== YOUR METRICS CARDS =====
    st.subheader("📊 Your Key Metrics")
    
    # Turnaround time placeholder
    st.info("⏱️ **Turnaround Time** – Data not yet available. Will be added when submission-to-decision dates are included in the dataset.")
    
    st.divider()
    
    # Calculate metrics for identified AE
    user_reviews = int(identified_ae['review_count'])
    user_citations = int(identified_ae['total_citations'])
    user_avg_citations = identified_ae['avg_citations']
    
    # Count accepts/rejects
    user_papers = df_filtered[df_filtered['Editor Names'] == identified_ae['Editor Names']]
    user_accepts = len(user_papers[user_papers['Accept or Reject Final Decision'] == 'Accept'])
    user_rejects = len(user_papers[user_papers['Accept or Reject Final Decision'] == 'Reject'])
    
    metric1, metric2, metric3, metric4 = st.columns(4)
    with metric1:
        st.metric("Total Reviews", user_reviews)
    with metric2:
        st.metric("Accepts", user_accepts)
    with metric3:
        st.metric("Rejects", user_rejects)
    with metric4:
        st.metric("Total Citations", user_citations)
    
    # ===== MANUSCRIPT TYPE BREAKDOWN =====
    st.subheader("📋 Breakdown by Manuscript Type")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Your manuscript type breakdown
        manuscript_breakdown = user_papers['Manuscript Type'].value_counts()
        
        fig_types = go.Figure(data=[go.Pie(
            labels=manuscript_breakdown.index,
            values=manuscript_breakdown.values,
            marker_colors=['#0072B5', '#BC3C29', '#E18727', '#20854E', '#7876B1', '#FFC000'],
            textposition='inside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>'
        )])
        
        fig_types.update_layout(
            title=f"Your Papers ({user_reviews} total)",
            height=350,
        )
        st.plotly_chart(fig_types, use_container_width=True)
    
    with col2:
        # Overall manuscript type breakdown
        manuscript_all = df_filtered['Manuscript Type'].value_counts()
        
        fig_types_all = go.Figure(data=[go.Pie(
            labels=manuscript_all.index,
            values=manuscript_all.values,
            marker_colors=['#0072B5', '#BC3C29', '#E18727', '#20854E', '#7876B1', '#FFC000'],
            textposition='inside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>'
        )])
        
        fig_types_all.update_layout(
            title=f"All Journal Papers ({len(df_filtered)} total)",
            height=350,
        )
        st.plotly_chart(fig_types_all, use_container_width=True)
    
    # ===== WATERFALL PLOTS =====
    st.subheader("📈 Your Position Across Key Metrics")
    
    # Filter by manuscript type for decisions pie charts
    st.write("**Filter by Manuscript Type:**")
    col_filter1, col_filter2, col_filter3, col_filter4, col_filter5 = st.columns(5)
    
    with col_filter1:
        btn_all = st.button("📋 All Types", use_container_width=True, key='btn_all_types')
    with col_filter2:
        btn_orig = st.button("📊 Original Research", use_container_width=True, key='btn_orig')
    with col_filter3:
        btn_review = st.button("📚 Review", use_container_width=True, key='btn_review')
    with col_filter4:
        btn_letter = st.button("✉️ Research Letter", use_container_width=True, key='btn_letter')
    
    # Track button state
    if 'type_filter_state' not in st.session_state:
        st.session_state.type_filter_state = 'All Types'
    
    if btn_all:
        st.session_state.type_filter_state = 'All Types'
    elif btn_orig:
        st.session_state.type_filter_state = 'Original Research Article'
    elif btn_review:
        st.session_state.type_filter_state = 'Review'
    elif btn_letter:
        st.session_state.type_filter_state = 'Research Letter'
    
    selected_type = st.session_state.type_filter_state
    
    # Filter data based on selection
    if selected_type == 'All Types':
        user_papers_filtered_type = user_papers
        df_filtered_type = df_filtered
        type_label = "All Types"
    else:
        user_papers_filtered_type = user_papers[user_papers['Manuscript Type'] == selected_type]
        df_filtered_type = df_filtered[df_filtered['Manuscript Type'] == selected_type]
        type_label = selected_type
    
    # Recalculate accept/reject for selected type
    type_accepts = len(user_papers_filtered_type[user_papers_filtered_type['Accept or Reject Final Decision'] == 'Accept'])
    type_rejects = len(user_papers_filtered_type[user_papers_filtered_type['Accept or Reject Final Decision'] == 'Reject'])
    type_total_accepts = len(df_filtered_type[df_filtered_type['Accept or Reject Final Decision'] == 'Accept'])
    type_total_rejects = len(df_filtered_type[df_filtered_type['Accept or Reject Final Decision'] == 'Reject'])
    
    st.divider()
    
    # Accept/Reject Pie Charts (filtered by type)
    col1, col2 = st.columns(2)
    
    with col1:
        # Your accept/reject breakdown (filtered)
        your_decisions_type = pd.Series({
            'Accept': type_accepts,
            'Reject': type_rejects
        })
        
        fig_your_decisions_type = go.Figure(data=[go.Pie(
            labels=your_decisions_type.index,
            values=your_decisions_type.values,
            marker_colors=['#20854E', '#E18727'],
            textposition='inside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>'
        )])
        
        type_accept_pct = (type_accepts / (type_accepts + type_rejects) * 100) if (type_accepts + type_rejects) > 0 else 0
        fig_your_decisions_type.update_layout(
            title=f"Your Decisions – {type_label}<br>({type_accepts + type_rejects} papers)<br>Accept Rate: {type_accept_pct:.1f}%",
            height=350,
        )
        st.plotly_chart(fig_your_decisions_type, use_container_width=True)
    
    with col2:
        # Overall accept/reject breakdown (filtered)
        overall_decisions_type = pd.Series({
            'Accept': type_total_accepts,
            'Reject': type_total_rejects
        })
        
        fig_overall_decisions_type = go.Figure(data=[go.Pie(
            labels=overall_decisions_type.index,
            values=overall_decisions_type.values,
            marker_colors=['#20854E', '#E18727'],
            textposition='inside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>'
        )])
        
        type_overall_accept_pct = (type_total_accepts / (type_total_accepts + type_total_rejects) * 100) if (type_total_accepts + type_total_rejects) > 0 else 0
        fig_overall_decisions_type.update_layout(
            title=f"All Journal Decisions – {type_label}<br>({type_total_accepts + type_total_rejects} papers)<br>Accept Rate: {type_overall_accept_pct:.1f}%",
            height=350,
        )
        st.plotly_chart(fig_overall_decisions_type, use_container_width=True)
    
    st.divider()
    
    # Waterfall 1: Total Reviews
    fig_reviews = go.Figure()
    ae_sorted_reviews = ae_metrics.sort_values('review_count', ascending=False).reset_index(drop=True)
    
    colors = ['#0072B5' if name != identified_ae['Editor Names'] else '#BC3C29' 
              for name in ae_sorted_reviews['Editor Names']]
    
    fig_reviews.add_trace(go.Bar(
        x=ae_sorted_reviews.index + 1,
        y=ae_sorted_reviews['review_count'],
        marker_color=colors,
        text=ae_sorted_reviews['review_count'].astype(int),
        textposition='outside',
        hovertemplate='<b>Rank %{x}</b><br>Reviews: %{y}<extra></extra>',
        showlegend=False
    ))
    
    fig_reviews.update_layout(
        title=f"Total Reviews – Your Rank: #{identified_ae['rank']} ({user_reviews} reviews)",
        xaxis_title="AE Rank (Highest to Lowest)",
        yaxis_title="Number of Reviews",
        height=350,
        hovermode='x unified',
        bargap=0.2
    )
    st.plotly_chart(fig_reviews, use_container_width=True)
    
    # Waterfall 2: % Accept
    ae_decisions = df_filtered.groupby('Editor Names').apply(
        lambda x: pd.Series({
            'accepts': len(x[x['Accept or Reject Final Decision'] == 'Accept']),
            'total': len(x),
        })
    ).reset_index()
    ae_decisions['pct_accept'] = (ae_decisions['accepts'] / ae_decisions['total'] * 100).round(1)
    ae_decisions = ae_decisions.sort_values('pct_accept', ascending=False).reset_index(drop=True)
    ae_decisions['rank'] = range(1, len(ae_decisions) + 1)
    
    colors_pct = ['#20854E' if name != identified_ae['Editor Names'] else '#BC3C29' 
                  for name in ae_decisions['Editor Names']]
    
    your_pct_accept = (user_accepts / (user_accepts + user_rejects) * 100) if (user_accepts + user_rejects) > 0 else 0
    
    fig_pct_accept = go.Figure()
    fig_pct_accept.add_trace(go.Bar(
        x=ae_decisions.index + 1,
        y=ae_decisions['pct_accept'],
        marker_color=colors_pct,
        text=ae_decisions['pct_accept'].astype(str) + '%',
        textposition='outside',
        hovertemplate='<b>Rank %{x}</b><br>Accept Rate: %{y:.1f}%<extra></extra>',
        showlegend=False
    ))
    
    fig_pct_accept.update_layout(
        title=f"Accept Rate (%) – You: {your_pct_accept:.1f}%",
        xaxis_title="AE Rank (Highest to Lowest Accept Rate)",
        yaxis_title="Accept Rate (%)",
        height=350,
        hovermode='x unified',
        bargap=0.2,
        yaxis=dict(range=[0, 100])
    )
    st.plotly_chart(fig_pct_accept, use_container_width=True)
    
    # Waterfall 3: Median Citations per Paper (with filter)
    st.write("**Filter Median Citations by Type:**")
    col_med1, col_med2, col_med3, col_med4 = st.columns(4)
    
    with col_med1:
        btn_med_combo = st.button("📊 Orig & Reviews", use_container_width=True, key='btn_med_combo')
    with col_med2:
        btn_med_orig = st.button("📄 Original Only", use_container_width=True, key='btn_med_orig')
    with col_med3:
        btn_med_review = st.button("📚 Reviews Only", use_container_width=True, key='btn_med_review')
    with col_med4:
        btn_med_all = st.button("📋 All Types", use_container_width=True, key='btn_med_all')
    
    # Track median filter state
    if 'median_filter_state' not in st.session_state:
        st.session_state.median_filter_state = 'Orig Research & Reviews'
    
    if btn_med_combo:
        st.session_state.median_filter_state = 'Orig Research & Reviews'
    elif btn_med_orig:
        st.session_state.median_filter_state = 'Original Research Article'
    elif btn_med_review:
        st.session_state.median_filter_state = 'Review'
    elif btn_med_all:
        st.session_state.median_filter_state = 'All Types'
    
    median_filter = st.session_state.median_filter_state
    
    # Filter data for median calculation
    if median_filter == 'Orig Research & Reviews':
        df_median_filtered = df_accepted[df_accepted['Manuscript Type'].isin(['Original Research Article', 'Review'])]
        ae_median_filtered = df_median_filtered.groupby('Editor Names').agg({
            'Number of Citations': ['median'],
        }).round(2)
        ae_median_filtered.columns = ['median_citations']
        ae_median_filtered = ae_median_filtered.reset_index()
        ae_median_filtered = ae_median_filtered.sort_values('median_citations', ascending=False).reset_index(drop=True)
        median_label = "Original Research & Reviews"
    elif median_filter == 'Original Research Article':
        df_median_filtered = df_accepted[df_accepted['Manuscript Type'] == 'Original Research Article']
        ae_median_filtered = df_median_filtered.groupby('Editor Names').agg({
            'Number of Citations': ['median'],
        }).round(2)
        ae_median_filtered.columns = ['median_citations']
        ae_median_filtered = ae_median_filtered.reset_index()
        ae_median_filtered = ae_median_filtered.sort_values('median_citations', ascending=False).reset_index(drop=True)
        median_label = "Original Research"
    elif median_filter == 'Review':
        df_median_filtered = df_accepted[df_accepted['Manuscript Type'] == 'Review']
        ae_median_filtered = df_median_filtered.groupby('Editor Names').agg({
            'Number of Citations': ['median'],
        }).round(2)
        ae_median_filtered.columns = ['median_citations']
        ae_median_filtered = ae_median_filtered.reset_index()
        ae_median_filtered = ae_median_filtered.sort_values('median_citations', ascending=False).reset_index(drop=True)
        median_label = "Reviews"
    else:  # All Types
        df_median_filtered = df_accepted
        ae_median_filtered = df_median_filtered.groupby('Editor Names').agg({
            'Number of Citations': ['median'],
        }).round(2)
        ae_median_filtered.columns = ['median_citations']
        ae_median_filtered = ae_median_filtered.reset_index()
        ae_median_filtered = ae_median_filtered.sort_values('median_citations', ascending=False).reset_index(drop=True)
        median_label = "All Types"
    
    # Create waterfall
    fig_median = go.Figure()
    colors_median = ['#7876B1' if name != identified_ae['Editor Names'] else '#BC3C29' 
                     for name in ae_median_filtered['Editor Names']]
    
    fig_median.add_trace(go.Bar(
        x=ae_median_filtered.index + 1,
        y=ae_median_filtered['median_citations'],
        marker_color=colors_median,
        text=ae_median_filtered['median_citations'].astype(str),
        textposition='outside',
        hovertemplate='<b>Rank %{x}</b><br>Median Citations: %{y}<extra></extra>',
        showlegend=False
    ))
    
    # Find your rank in filtered data
    your_row_filtered = ae_median_filtered[ae_median_filtered['Editor Names'] == identified_ae['Editor Names']]
    if len(your_row_filtered) > 0:
        your_median_rank = your_row_filtered.index[0] + 1
        your_median_value = your_row_filtered['median_citations'].values[0]
    else:
        your_median_rank = "N/A"
        your_median_value = "N/A"
    
    fig_median.update_layout(
        title=f"Median Citations per Paper – {median_label} – Your Rank: #{your_median_rank} ({your_median_value:.2f} citations)",
        xaxis_title="AE Rank (Highest to Lowest Median)",
        yaxis_title="Median Citations",
        height=350,
        hovermode='x unified',
        bargap=0.2
    )
    st.plotly_chart(fig_median, use_container_width=True)
    
    # Waterfall 4: % of Papers in Top Decile for Citations
    # Calculate top decile threshold
    top_decile_threshold = df_filtered['Number of Citations'].quantile(0.90)
    
    ae_top_decile = df_filtered.groupby('Editor Names').apply(
        lambda x: pd.Series({
            'in_top_decile': len(x[x['Number of Citations'] >= top_decile_threshold]),
            'total': len(x),
        })
    ).reset_index()
    ae_top_decile['pct_top_decile'] = (ae_top_decile['in_top_decile'] / ae_top_decile['total'] * 100).round(1)
    ae_top_decile = ae_top_decile.sort_values('pct_top_decile', ascending=False).reset_index(drop=True)
    ae_top_decile['rank'] = range(1, len(ae_top_decile) + 1)
    
    colors_decile = ['#FFC000' if name != identified_ae['Editor Names'] else '#BC3C29' 
                     for name in ae_top_decile['Editor Names']]
    
    your_pct_decile = ae_top_decile[ae_top_decile['Editor Names'] == identified_ae['Editor Names']]['pct_top_decile'].values
    your_pct_decile = your_pct_decile[0] if len(your_pct_decile) > 0 else 0
    
    fig_decile = go.Figure()
    fig_decile.add_trace(go.Bar(
        x=ae_top_decile.index + 1,
        y=ae_top_decile['pct_top_decile'],
        marker_color=colors_decile,
        text=ae_top_decile['pct_top_decile'].astype(str) + '%',
        textposition='outside',
        hovertemplate='<b>Rank %{x}</b><br>Top Decile: %{y:.1f}%<extra></extra>',
        showlegend=False
    ))
    
    fig_decile.update_layout(
        title=f"% of Papers in Top Decile for Citations (>{top_decile_threshold:.0f} cites) – You: {your_pct_decile:.1f}%",
        xaxis_title="AE Rank (Highest to Lowest %)",
        yaxis_title="% of Papers in Top Decile",
        height=350,
        hovermode='x unified',
        bargap=0.2,
        yaxis=dict(range=[0, 100])
    )
    st.plotly_chart(fig_decile, use_container_width=True)
    
    # Waterfall 5: Your Accepted Articles by Citations
    st.subheader("📄 Your Accepted Articles – Citation Impact")
    
    your_accepted = user_papers[user_papers['Accept or Reject Final Decision'] == 'Accept'].copy()
    your_accepted = your_accepted.sort_values('Number of Citations', ascending=False).reset_index(drop=True)
    
    if len(your_accepted) > 0:
        # Create color map for manuscript types
        type_colors = {
            'Original Research Article': '#0072B5',
            'Review': '#BC3C29',
            'Invited Review': '#E18727',
            'Study Protocol': '#20854E',
            'Editorial': '#7876B1',
            'Research Letter': '#FFC000',
            'Correspondence': '#00B4D8'
        }
        
        colors_articles = [type_colors.get(mtype, '#7876B1') for mtype in your_accepted['Manuscript Type']]
        
        # Truncate titles for display
        article_labels = [title[:40] + '...' if len(title) > 40 else title 
                         for title in your_accepted['Manuscript Title']]
        
        fig_accepted = go.Figure()
        fig_accepted.add_trace(go.Bar(
            x=list(range(1, len(your_accepted) + 1)),
            y=your_accepted['Number of Citations'],
            marker_color=colors_articles,
            text=your_accepted['Number of Citations'].astype(int),
            customdata=your_accepted['Manuscript Type'],
            textposition='outside',
            hovertemplate='<b>%{customdata}</b><br>Citations: %{y}<extra></extra>',
            showlegend=False
        ))
        
        fig_accepted.update_layout(
            title=f"Your {len(your_accepted)} Accepted Articles – Citations",
            xaxis_title="",
            yaxis_title="Citations",
            height=400,
            hovermode='x unified',
            bargap=0,
            showlegend=False
        )
        st.plotly_chart(fig_accepted, use_container_width=True)
    else:
        st.info("No accepted articles to display.")
    
    # Your papers
    st.subheader("📄 Your Reviews & Citations")
    
    # Filter buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        show_all = st.button("📋 All Papers", use_container_width=True, key='all_papers')
    with col2:
        show_accepts = st.button("✅ Accepted Only", use_container_width=True, key='accepts')
    with col3:
        show_rejects = st.button("❌ Rejected Only", use_container_width=True, key='rejects')
    
    # Determine filter state
    if 'filter_type' not in st.session_state:
        st.session_state.filter_type = 'all'
    
    if show_accepts:
        st.session_state.filter_type = 'accepts'
    elif show_rejects:
        st.session_state.filter_type = 'rejects'
    elif show_all:
        st.session_state.filter_type = 'all'
    
    # Apply filter
    if st.session_state.filter_type == 'accepts':
        user_papers_filtered = user_papers[user_papers['Accept or Reject Final Decision'] == 'Accept'].copy()
    elif st.session_state.filter_type == 'rejects':
        user_papers_filtered = user_papers[user_papers['Accept or Reject Final Decision'] == 'Reject'].copy()
    else:
        user_papers_filtered = user_papers.copy()
    
    # Display table
    user_papers_display = user_papers_filtered[['Manuscript Title', 'Number of Citations', 'Manuscript Type', 'Latest Decision Date', 'Accept or Reject Final Decision']].copy()
    
    user_papers_display['Latest Decision Date'] = user_papers_display['Latest Decision Date'].dt.strftime('%b %Y')
    user_papers_display = user_papers_display.sort_values('Number of Citations', ascending=False)
    user_papers_display.columns = ['Paper Title', 'Citations', 'Type', 'Decision Date', 'Outcome']
    
    st.dataframe(
        user_papers_display,
        use_container_width=True,
        height=400,
        hide_index=True
    )
    
    # Download
    csv = user_papers_display.to_csv(index=False)
    st.download_button(
        label="📥 Download your papers (CSV)",
        data=csv,
        file_name=f"ERJOR_my_reviews_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# ============================================================================
# SECTION 3: Notes
# ============================================================================
st.divider()
st.markdown("""
**Notes on this dashboard:**
- Rankings are anonymized; only you can identify yourself
- Data covers decisions from Aug 2022 to Aug 2024
- Citation counts are from Web of Science JCR (may include self-citations)
- **"Mean/Median/Total Citations"** metrics show citations for **accepted papers only** (rejected papers have 0 citations and aren't included)
- "Total Reviews" = all papers reviewed (accepted + rejected)
- "Accepts/Rejects" = count of decisions for each outcome
- This is a tool for reflecting on editorial contribution and paper impact, not performance evaluation
""")
