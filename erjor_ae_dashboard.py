"""
ERJOR Associate Editor Activity & Citations Dashboard

Shows anonymised reviewing activity and JCR citation data for ERJOR
Associate Editors. AEs identify themselves by surname to see their own
position; all other AEs remain anonymous ranks.

Data window: decisions Aug 2022 - Aug 2024 (2025 JCR window).
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# ============================================================================
# CONFIGURATION
# ============================================================================
CONFIG = {
    'page_title': 'ERJOR AE Activity & Citations',
    'date_start': pd.Timestamp('2022-08-01'),
    'date_end': pd.Timestamp('2024-08-31'),
    'csv_encoding': 'latin-1',
    'top_decile_quantile': 0.90,
    'zero_bar_height': 0.2,
}

# Global colour palette (NEJM-derived)
PALETTE = {
    'primary': '#0072B5',
    'highlight': '#BC3C29',
    'success': '#20854E',
    'warning': '#E18727',
    'info': '#7876B1',
    'gold': '#FFC000',
    'cyan': '#00B4D8',
    'text_dark': '#1a1a1a',
    'axis': '#1a1a1a',
}

# Consistent manuscript-type colours used by every chart
MANUSCRIPT_COLORS = {
    'Original Research Article': PALETTE['primary'],
    'Review': PALETTE['highlight'],
    'Invited Review': PALETTE['warning'],
    'Mini-Review': PALETTE['warning'],
    'Study Protocol': PALETTE['success'],
    'Editorial': PALETTE['info'],
    'Research Letter': PALETTE['gold'],
    'Correspondence': PALETTE['cyan'],
}

DECISION_COLORS = {
    'Accept': PALETTE['success'],
    'Reject': PALETTE['warning'],
}

st.set_page_config(
    page_title=CONFIG['page_title'],
    page_icon="chart_with_upwards_trend",
    layout="wide",
)

# ============================================================================
# GLOBAL STYLING
# ============================================================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', Arial, sans-serif; }
h1 { font-size: 30px !important; font-weight: 700 !important; color: #1a1a1a !important; letter-spacing: -0.5px; }
h2, h3 { font-weight: 600 !important; color: #2c2c2c !important; margin-top: 8px !important; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%); border-right: 1px solid #e8e8e8; }
[data-testid="stMetricValue"] { font-size: 26px; font-weight: 600; }
[data-testid="stMetricLabel"] { font-size: 13px; color: #555; }
div[role="radiogroup"] { gap: 6px; padding: 2px 0 8px 0; }
div[role="radiogroup"] label { font-size: 14px; }
.dataframe { font-size: 13px; }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# CHART STYLING HELPERS
# ============================================================================
def style_bar_chart(fig, title, xaxis_title="", yaxis_title="",
                    height=350, yaxis_range=None, bargap=0.2):
    """Apply house style to a bar/waterfall chart.

    Left-aligned title, no gridlines, black axes, unified hover.
    """
    fig.update_layout(
        title=dict(text=title, x=0.0, xanchor='left',
                   font=dict(size=15, color=PALETTE['text_dark'])),
        template='plotly_white',
        font=dict(family="Inter, Arial, sans-serif", size=11),
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        height=height,
        hovermode='x unified',
        bargap=bargap,
        margin=dict(l=55, r=25, t=60, b=45),
        showlegend=False,
    )
    fig.update_xaxes(showgrid=False, linecolor=PALETTE['axis'], ticks='outside')
    fig.update_yaxes(showgrid=False, linecolor=PALETTE['axis'], ticks='outside')
    if yaxis_range:
        fig.update_yaxes(range=yaxis_range)
    return fig


def style_pie_chart(fig, title, height=350):
    """Apply house style to a pie chart."""
    fig.update_layout(
        title=dict(text=title, x=0.0, xanchor='left',
                   font=dict(size=14, color=PALETTE['text_dark'])),
        height=height,
        font=dict(family="Inter, Arial, sans-serif", size=11),
        margin=dict(l=25, r=25, t=90, b=25),
    )
    return fig


def type_colors_for(labels):
    """Map manuscript-type labels to their consistent colours."""
    return [MANUSCRIPT_COLORS.get(label, PALETTE['info']) for label in labels]


def decision_colors_for(labels):
    """Map Accept/Reject labels to their consistent colours."""
    return [DECISION_COLORS.get(label, PALETTE['info']) for label in labels]


def rank_colors(names, your_name, base_color):
    """Base colour for the pack, highlight red for the identified AE."""
    return [base_color if n != your_name else PALETTE['highlight']
            for n in names]


def median_by_ae(frame):
    """Median citations per AE, sorted highest to lowest with clean index."""
    out = (frame.groupby('Editor Names')['Number of Citations']
           .median().round(2).reset_index(name='median_citations'))
    return out.sort_values('median_citations',
                           ascending=False).reset_index(drop=True)


# ============================================================================
# DATA LOADING
# ============================================================================
@st.cache_data
def load_data():
    """Load and merge AE activity (CSV) and citation (Excel) data.

    Returns:
        pd.DataFrame: one row per manuscript, with decision and citation count.
    """
    ae_df = pd.read_csv('AEs.csv', encoding=CONFIG['csv_encoding'])
    ae_df['Latest Decision Date'] = pd.to_datetime(
        ae_df['Latest Decision Date'], errors='coerce')

    citations_df = pd.read_excel('AE-citations-combined.xlsx',
                                 sheet_name='Sheet1')
    citations_df['Latest Decision Date'] = pd.to_datetime(
        citations_df['Latest Decision Date'],
        unit='D',
        origin=pd.Timestamp('1899-12-30'),
    )

    merged = ae_df.merge(
        citations_df[['Manuscript ID - Original', 'Number of Citations']],
        on='Manuscript ID - Original',
        how='left',
    )
    merged['Number of Citations'] = merged['Number of Citations'].fillna(0)
    return merged


df = load_data()

df_filtered = df[
    (df['Latest Decision Date'] >= CONFIG['date_start']) &
    (df['Latest Decision Date'] <= CONFIG['date_end'])
].copy()

# review_count = ALL papers handled; citation metrics = ACCEPTED papers only
review_counts = (df_filtered.groupby('Editor Names').size()
                 .reset_index(name='review_count'))

df_accepted = df_filtered[
    df_filtered['Accept or Reject Final Decision'] == 'Accept'].copy()
citation_metrics = df_accepted.groupby('Editor Names').agg(
    {'Number of Citations': ['mean', 'median', 'sum']}).round(2)
citation_metrics.columns = ['avg_citations', 'median_citations',
                            'total_citations']
citation_metrics = citation_metrics.reset_index()

ae_metrics = review_counts.merge(citation_metrics, on='Editor Names',
                                 how='left')
ae_metrics = ae_metrics.sort_values(
    'review_count', ascending=False).reset_index(drop=True)
ae_metrics['rank'] = range(1, len(ae_metrics) + 1)
ae_metrics['Editor Name (Clean)'] = (
    ae_metrics['Editor Names']
    .str.replace('(Associate Editor)', '', regex=False).str.strip())

# ============================================================================
# SIDEBAR
# ============================================================================
st.sidebar.markdown("### Identify Yourself")
st.sidebar.markdown(
    "_Enter your surname to see your own position. "
    "All other editors stay anonymous._")
st.sidebar.markdown("")

user_surname = st.sidebar.text_input(
    "Your surname:",
    placeholder="e.g., Frost",
    help="Your name as it appears in the ERJOR database",
).strip()

identified_ae = None
if user_surname:
    matches = ae_metrics[
        ae_metrics['Editor Name (Clean)'].str.contains(
            user_surname, case=False, na=False)]
    if len(matches) == 1:
        identified_ae = matches.iloc[0]
        st.sidebar.success(
            f"Identified: {identified_ae['Editor Name (Clean)']}")
    elif len(matches) > 1:
        st.sidebar.warning("Multiple matches. Please be more specific.")
    else:
        st.sidebar.error("No match found. Check spelling and try again.")

# ============================================================================
# MAIN PAGE
# ============================================================================
st.title("ERJOR Associate Editor Activity & Citations")
st.markdown(
    "**Data for the 2025 Journal Citation Report window** "
    "(Papers published in Aug 2022 to Aug 2024)")

total_accepts = len(df_filtered[
    df_filtered['Accept or Reject Final Decision'] == 'Accept'])
total_rejects = len(df_filtered[
    df_filtered['Accept or Reject Final Decision'] == 'Reject'])

# ============================================================================
# SECTION 1: Overall journal statistics
# ============================================================================
st.divider()
st.subheader("Overall ERJ Open Research Statistics")
st.markdown("")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total AEs", len(ae_metrics))
with col2:
    st.metric("Total Reviews (All)", int(ae_metrics['review_count'].sum()))
with col3:
    st.metric("Mean/AE", f"{ae_metrics['review_count'].mean():.1f}")
with col4:
    st.metric("Median/AE", f"{ae_metrics['review_count'].median():.0f}")

col1, col2, col3 = st.columns(3)
total_all = total_accepts + total_rejects
with col1:
    st.metric("Total Accepts", total_accepts)
with col2:
    st.metric("Total Rejects", total_rejects)
with col3:
    accept_rate = (total_accepts / total_all * 100) if total_all > 0 else 0
    st.metric("Accept Rate", f"{accept_rate:.1f}%")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Citations (All AEs)",
              int(ae_metrics['total_citations'].sum()))
with col2:
    st.metric("Mean Avg Citations/AE",
              f"{ae_metrics['avg_citations'].mean():.2f}")
with col3:
    st.metric("Median Avg Citations/AE",
              f"{ae_metrics['avg_citations'].median():.2f}")

st.markdown("")
st.subheader("All Papers by Manuscript Type")
manuscript_all = df_filtered['Manuscript Type'].value_counts()

fig_types_all = go.Figure(data=[go.Pie(
    labels=manuscript_all.index,
    values=manuscript_all.values,
    marker_colors=type_colors_for(manuscript_all.index),
    textposition='inside',
    textinfo='label+percent',
    hovertemplate='<b>%{label}</b><br>Count: %{value}'
                  '<br>Percent: %{percent}<extra></extra>',
)])
fig_types_all = style_pie_chart(
    fig_types_all,
    f"All Papers by Manuscript Type ({len(df_filtered)} total)", height=400)
st.plotly_chart(fig_types_all, use_container_width=True)

# ============================================================================
# SECTION 2: Individual AE view
# ============================================================================
if identified_ae is not None:
    st.divider()

    st.subheader("Your Key Metrics")
    st.info("**Turnaround Time** - Data not yet available. Will be added "
            "when submission-to-decision dates are included in the dataset.")
    st.markdown("")

    user_reviews = int(identified_ae['review_count'])
    user_citations = int(identified_ae['total_citations'])

    user_papers = df_filtered[
        df_filtered['Editor Names'] == identified_ae['Editor Names']]
    user_accepts = len(user_papers[
        user_papers['Accept or Reject Final Decision'] == 'Accept'])
    user_rejects = len(user_papers[
        user_papers['Accept or Reject Final Decision'] == 'Reject'])

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Reviews", user_reviews)
    with m2:
        st.metric("Accepts", user_accepts)
    with m3:
        st.metric("Rejects", user_rejects)
    with m4:
        st.metric("Total Citations", user_citations)

    # ===== Total reviews waterfall =====
    st.markdown("")
    st.subheader("Your Total Reviews")

    ae_sorted_reviews = ae_metrics.sort_values(
        'review_count', ascending=False).reset_index(drop=True)
    fig_reviews = go.Figure(go.Bar(
        x=(ae_sorted_reviews.index + 1).tolist(),
        y=ae_sorted_reviews['review_count'],
        marker_color=rank_colors(ae_sorted_reviews['Editor Names'],
                                 identified_ae['Editor Names'],
                                 PALETTE['primary']),
        text=ae_sorted_reviews['review_count'].astype(int),
        textposition='outside',
        hovertemplate='<b>Rank %{x}</b><br>Reviews: %{y}<extra></extra>',
    ))
    fig_reviews = style_bar_chart(
        fig_reviews,
        f"Total Reviews - Your Rank: #{identified_ae['rank']} "
        f"({user_reviews} reviews)",
        xaxis_title="AE Rank (Highest to Lowest)",
        yaxis_title="Number of Reviews")
    st.plotly_chart(fig_reviews, use_container_width=True)

    # ===== Manuscript type breakdown =====
    st.divider()
    st.subheader("Breakdown by Manuscript Type")

    col1, col2 = st.columns(2)
    with col1:
        manuscript_breakdown = user_papers['Manuscript Type'].value_counts()
        fig_types = go.Figure(data=[go.Pie(
            labels=manuscript_breakdown.index,
            values=manuscript_breakdown.values,
            marker_colors=type_colors_for(manuscript_breakdown.index),
            textposition='inside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}'
                          '<br>Percent: %{percent}<extra></extra>',
        )])
        fig_types = style_pie_chart(
            fig_types, f"Your Papers ({user_reviews} total)")
        st.plotly_chart(fig_types, use_container_width=True)

    with col2:
        fig_types_all2 = go.Figure(data=[go.Pie(
            labels=manuscript_all.index,
            values=manuscript_all.values,
            marker_colors=type_colors_for(manuscript_all.index),
            textposition='inside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}'
                          '<br>Percent: %{percent}<extra></extra>',
        )])
        fig_types_all2 = style_pie_chart(
            fig_types_all2, f"All Journal Papers ({len(df_filtered)} total)")
        st.plotly_chart(fig_types_all2, use_container_width=True)

    # ===== Editorial decisions =====
    st.divider()
    st.subheader("Your Editorial Decisions")

    TYPE_FILTER_OPTIONS = {
        "All Types": None,
        "Original Research": "Original Research Article",
        "Review": "Review",
        "Research Letter": "Research Letter",
    }
    selected_label = st.radio(
        "Filter by manuscript type:",
        list(TYPE_FILTER_OPTIONS.keys()),
        horizontal=True,
        key='decisions_type_filter',
    )
    selected_type = TYPE_FILTER_OPTIONS[selected_label]

    if selected_type is None:
        user_papers_type = user_papers
        df_type = df_filtered
    else:
        user_papers_type = user_papers[
            user_papers['Manuscript Type'] == selected_type]
        df_type = df_filtered[
            df_filtered['Manuscript Type'] == selected_type]

    type_accepts = len(user_papers_type[
        user_papers_type['Accept or Reject Final Decision'] == 'Accept'])
    type_rejects = len(user_papers_type[
        user_papers_type['Accept or Reject Final Decision'] == 'Reject'])
    type_total_accepts = len(df_type[
        df_type['Accept or Reject Final Decision'] == 'Accept'])
    type_total_rejects = len(df_type[
        df_type['Accept or Reject Final Decision'] == 'Reject'])

    col1, col2 = st.columns(2)
    with col1:
        your_dec = pd.Series({'Accept': type_accepts, 'Reject': type_rejects})
        fig_your_dec = go.Figure(data=[go.Pie(
            labels=your_dec.index,
            values=your_dec.values,
            marker_colors=decision_colors_for(your_dec.index),
            textposition='inside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}'
                          '<br>Percent: %{percent}<extra></extra>',
        )])
        n_you = type_accepts + type_rejects
        pct_you = (type_accepts / n_you * 100) if n_you > 0 else 0
        fig_your_dec = style_pie_chart(
            fig_your_dec,
            f"Your Decisions - {selected_label}<br>"
            f"({n_you} papers) - Accept Rate: {pct_you:.1f}%")
        st.plotly_chart(fig_your_dec, use_container_width=True)

    with col2:
        all_dec = pd.Series({'Accept': type_total_accepts,
                             'Reject': type_total_rejects})
        fig_all_dec = go.Figure(data=[go.Pie(
            labels=all_dec.index,
            values=all_dec.values,
            marker_colors=decision_colors_for(all_dec.index),
            textposition='inside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}'
                          '<br>Percent: %{percent}<extra></extra>',
        )])
        n_all = type_total_accepts + type_total_rejects
        pct_all = (type_total_accepts / n_all * 100) if n_all > 0 else 0
        fig_all_dec = style_pie_chart(
            fig_all_dec,
            f"All Journal Decisions - {selected_label}<br>"
            f"({n_all} papers) - Accept Rate: {pct_all:.1f}%")
        st.plotly_chart(fig_all_dec, use_container_width=True)

    # ===== Performance metrics =====
    st.divider()
    st.subheader("Your Performance Metrics")

    # Only rows with a recorded decision count toward accept rate
    df_decided = df_filtered[
        df_filtered['Accept or Reject Final Decision'].isin(
            ['Accept', 'Reject'])]
    ae_decisions = df_decided.groupby('Editor Names').apply(
        lambda x: pd.Series({
            'accepts': len(
                x[x['Accept or Reject Final Decision'] == 'Accept']),
            'total': len(x),
        })
    ).reset_index()
    ae_decisions['pct_accept'] = (
        ae_decisions['accepts'] / ae_decisions['total'] * 100).round(1)
    ae_decisions = ae_decisions.sort_values(
        'pct_accept', ascending=False).reset_index(drop=True)

    your_pct_accept = (user_accepts / (user_accepts + user_rejects) * 100) \
        if (user_accepts + user_rejects) > 0 else 0

    fig_pct = go.Figure(go.Bar(
        x=(ae_decisions.index + 1).tolist(),
        y=ae_decisions['pct_accept'],
        marker_color=rank_colors(ae_decisions['Editor Names'],
                                 identified_ae['Editor Names'],
                                 PALETTE['success']),
        text=ae_decisions['pct_accept'].astype(str) + '%',
        textposition='outside',
        hovertemplate='<b>Rank %{x}</b><br>Accept Rate: '
                      '%{y:.1f}%<extra></extra>',
    ))
    fig_pct = style_bar_chart(
        fig_pct,
        f"Accept Rate (%) - You: {your_pct_accept:.1f}%",
        xaxis_title="AE Rank (Highest to Lowest Accept Rate)",
        yaxis_title="Accept Rate (%)",
        yaxis_range=[0, 108])
    st.plotly_chart(fig_pct, use_container_width=True)

    # ===== Median citations (filtered) =====
    st.markdown("")
    REVIEW_TYPES = ['Review', 'Invited Review', 'Mini-Review']
    MEDIAN_FILTER_OPTIONS = {
        "Orig Research & Reviews": ['Original Research Article'] + REVIEW_TYPES,
        "Original Research Only": ['Original Research Article'],
        "Reviews Only": REVIEW_TYPES,
        "All Types": None,
    }
    median_label = st.radio(
        "Filter median citations by type:",
        list(MEDIAN_FILTER_OPTIONS.keys()),
        horizontal=True,
        key='median_type_filter',
    )
    median_types = MEDIAN_FILTER_OPTIONS[median_label]

    if median_types is None:
        ae_median = median_by_ae(df_accepted)
    else:
        ae_median = median_by_ae(
            df_accepted[df_accepted['Manuscript Type'].isin(median_types)])

    your_row = ae_median[
        ae_median['Editor Names'] == identified_ae['Editor Names']]
    if len(your_row) > 0:
        your_median_rank = f"#{your_row.index[0] + 1}"
        your_median_value = f"{your_row['median_citations'].values[0]:.2f}"
    else:
        your_median_rank = "N/A"
        your_median_value = "N/A"

    fig_median = go.Figure(go.Bar(
        x=(ae_median.index + 1).tolist(),
        y=ae_median['median_citations'],
        marker_color=rank_colors(ae_median['Editor Names'],
                                 identified_ae['Editor Names'],
                                 PALETTE['info']),
        text=ae_median['median_citations'].astype(str),
        textposition='outside',
        hovertemplate='<b>Rank %{x}</b><br>Median Citations: '
                      '%{y}<extra></extra>',
    ))
    fig_median = style_bar_chart(
        fig_median,
        f"Median Citations per Paper - {median_label} - "
        f"Your Rank: {your_median_rank} ({your_median_value} citations)",
        xaxis_title="AE Rank (Highest to Lowest Median)",
        yaxis_title="Median Citations")
    st.plotly_chart(fig_median, use_container_width=True)

    # ===== Top decile =====
    # Threshold and denominator use ACCEPTED papers only, consistent with
    # every other citation metric on this page. Including rejected papers
    # (all zero citations) would drag the threshold down and pad the
    # denominator with papers that can never be in the top decile.
    top_decile_threshold = df_accepted['Number of Citations'].quantile(
        CONFIG['top_decile_quantile'])

    ae_top_decile = df_accepted.groupby('Editor Names').apply(
        lambda x: pd.Series({
            'in_top_decile': len(
                x[x['Number of Citations'] >= top_decile_threshold]),
            'total': len(x),
        })
    ).reset_index()
    ae_top_decile['pct_top_decile'] = (
        ae_top_decile['in_top_decile'] / ae_top_decile['total'] * 100
    ).round(1)
    ae_top_decile = ae_top_decile.sort_values(
        'pct_top_decile', ascending=False).reset_index(drop=True)

    your_pct_decile = ae_top_decile[
        ae_top_decile['Editor Names'] == identified_ae['Editor Names']
    ]['pct_top_decile'].values
    your_pct_decile = your_pct_decile[0] if len(your_pct_decile) > 0 else 0

    fig_decile = go.Figure(go.Bar(
        x=(ae_top_decile.index + 1).tolist(),
        y=ae_top_decile['pct_top_decile'],
        marker_color=rank_colors(ae_top_decile['Editor Names'],
                                 identified_ae['Editor Names'],
                                 PALETTE['gold']),
        text=ae_top_decile['pct_top_decile'].astype(str) + '%',
        textposition='outside',
        hovertemplate='<b>Rank %{x}</b><br>Top Decile: '
                      '%{y:.1f}%<extra></extra>',
    ))
    fig_decile = style_bar_chart(
        fig_decile,
        f"% of Accepted Papers in Top Decile for Citations "
        f"({top_decile_threshold:.0f}+ cites) - You: {your_pct_decile:.1f}%",
        xaxis_title="AE Rank (Highest to Lowest %)",
        yaxis_title="% of Accepted Papers in Top Decile",
        yaxis_range=[0, 108])
    st.plotly_chart(fig_decile, use_container_width=True)

    # ===== Accepted articles =====
    st.divider()
    st.subheader("Your Accepted Articles - Citation Impact")

    your_accepted = user_papers[
        user_papers['Accept or Reject Final Decision'] == 'Accept'].copy()
    your_accepted = your_accepted.sort_values(
        'Number of Citations', ascending=False).reset_index(drop=True)

    if len(your_accepted) > 0:
        y_display = your_accepted['Number of Citations'].replace(
            0, CONFIG['zero_bar_height'])

        present_types = list(your_accepted['Manuscript Type'].unique())
        legend_bits = "&nbsp;&nbsp;&nbsp;".join(
            f"<span style='color:{MANUSCRIPT_COLORS.get(t, PALETTE['info'])};"
            f"font-size:15px'>&#9632;</span> {t}"
            for t in present_types)
        st.markdown(
            f"<div style='font-size:12px;color:#555;padding-bottom:4px'>"
            f"{legend_bits}</div>", unsafe_allow_html=True)

        fig_accepted = go.Figure(go.Bar(
            x=list(range(1, len(your_accepted) + 1)),
            y=y_display,
            marker_color=type_colors_for(your_accepted['Manuscript Type']),
            text=your_accepted['Number of Citations'].astype(int),
            customdata=your_accepted['Manuscript Type'],
            textposition='outside',
            hovertemplate='<b>%{customdata}</b><br>Citations: '
                          '%{text}<extra></extra>',
        ))
        fig_accepted = style_bar_chart(
            fig_accepted,
            f"Your {len(your_accepted)} Accepted Articles - Citations",
            yaxis_title="Citations",
            height=400, bargap=0)
        st.plotly_chart(fig_accepted, use_container_width=True)
    else:
        st.info("No accepted articles to display.")

    # ===== Papers table =====
    st.divider()
    st.subheader("Your Reviews & Citations")

    table_filter = st.radio(
        "Show:",
        ["All Papers", "Accepted Only", "Rejected Only"],
        horizontal=True,
        key='table_filter',
    )

    if table_filter == "Accepted Only":
        table_papers = user_papers[
            user_papers['Accept or Reject Final Decision'] == 'Accept']
    elif table_filter == "Rejected Only":
        table_papers = user_papers[
            user_papers['Accept or Reject Final Decision'] == 'Reject']
    else:
        table_papers = user_papers

    display = table_papers[[
        'Manuscript Title', 'Number of Citations', 'Manuscript Type',
        'Latest Decision Date', 'Accept or Reject Final Decision']].copy()
    display['Latest Decision Date'] = (
        display['Latest Decision Date'].dt.strftime('%b %Y'))
    display = display.sort_values('Number of Citations', ascending=False)
    display.columns = ['Paper Title', 'Citations', 'Type',
                       'Decision Date', 'Outcome']

    st.dataframe(display, use_container_width=True, height=400,
                 hide_index=True)

    csv = display.to_csv(index=False)
    st.download_button(
        label="Download your papers (CSV)",
        data=csv,
        file_name=f"ERJOR_my_reviews_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

# ============================================================================
# SECTION 3: Notes
# ============================================================================
st.divider()
st.markdown("""
**Notes on this dashboard:**
- Rankings are anonymised; only you can identify yourself
- Data covers decisions from Aug 2022 to Aug 2024
- Citation counts are from Web of Science JCR (may include self-citations)
- **Mean/Median/Total Citations** metrics show citations for **accepted papers only** (rejected papers have 0 citations and are not included)
- **Total Reviews** = all papers reviewed (accepted + rejected)
- **Accepts/Rejects** = count of decisions for each outcome
- This is a tool for reflecting on editorial contribution and paper impact, not performance evaluation
""")
