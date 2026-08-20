# ERJOR Associate Editor Dashboard – Deployment Guide

## Overview
A Streamlit app that shows ERJOR Associate Editors their reviewing activity and citation impact over the last 12 months, with **anonymized rankings** that only reveal individual data upon identification.

## Quick Start

### Local Development
```bash
pip install -r requirements.txt
streamlit run erjor_ae_dashboard.py
```
The app will open at `http://localhost:8501`.

### Cloud Deployment (Streamlit Cloud)

1. **Push to GitHub**  
   Create a GitHub repository with:
   - `erjor_ae_dashboard.py`
   - `requirements.txt`
   - `AE-citations-combined.xlsx`
   - `README.md` (optional)

2. **Deploy via Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repo
   - Set main file to `erjor_ae_dashboard.py`
   - Deploy

3. **Share the link**  
   Share the public URL with all AEs (e.g., `https://share.streamlit.io/your-username/repo-name`)

### Alternative: Self-Hosted (Docker)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "erjor_ae_dashboard.py"]
```

Then:
```bash
docker build -t erjor-ae-dashboard .
docker run -p 8501:8501 erjor-ae-dashboard
```

## Features

### Anonymization Strategy
- **Pack view (default):** Rankings shown as Rank 1–71 with metrics (review count, citations)
- **Individual identification:** AE enters surname to reveal only their own data
- **Highlight in ranking:** Their row in the anonymized table is highlighted so they can see their position

### Metrics Shown
Each AE sees:
- **Rank** – Position in the pack by review volume
- **Reviews (12m)** – Number of papers reviewed in last 12 months
- **Avg Citations** – Mean citations per paper they reviewed
- **Median Citations** – Typical citation count
- **Total Citations** – Sum across all their reviews
- **Percentile** – Where they sit relative to pack (top X%)

### Data in Individual View
When an AE identifies themselves:
1. **Summary card** showing rank, review count, avg citations, percentile
2. **Position in pack** histogram showing where they fall vs distribution
3. **Detailed table** of all their papers with:
   - Paper title
   - Citation count
   - Manuscript type (Original Research, Review, etc.)
   - Decision date
   - Outcome (Accept/Reject)
4. **CSV download** of their personal data

### Pack Statistics
Always visible:
- Total AEs
- Total reviews in period
- Mean/median reviews per AE
- Box plot of average citation distribution

## Data Updates

### Refreshing Data
1. Replace `AE-citations-combined.xlsx` with updated data
2. For Streamlit Cloud, push to GitHub
3. For local/self-hosted, restart Streamlit

### Data Expectations
The Excel file should have one sheet with columns:
- `Editor Names` (format: "Lastname, Firstname(Associate Editor)")
- `Number of Citations` (integer, JCR count)
- `Latest Decision Date` (date, Excel serial format)
- `Item Title`, `Manuscript ID - Original`, `Manuscript Type`, `Accept or Reject Final Decision`
- Other columns are optional

## Customization

### Change Metrics Computed
Edit the `ae_metrics` groupby in the `load_data()` section:
```python
ae_metrics = df_12m.groupby('Editor Names').agg({
    'Number of Citations': ['count', 'mean', 'median', 'sum'],
})
```

### Change Anonymization
To use tokens instead of surnames, replace the sidebar input with:
```python
token = st.sidebar.text_input("Enter your AE token:")
if token:
    identified_ae = ae_metrics[ae_metrics['token_col'] == token]
```

### Change Color Scheme
Update Plotly colors (default: NEJM palette):
```python
marker_color='#BC3C29'  # NEJM red
marker_color='#0072B5'  # NEJM blue
marker_color='#E18727'  # NEJM orange
```

### Change Time Window
Modify the cutoff date:
```python
cutoff_date = datetime.now() - timedelta(days=365)  # 12 months
# or
cutoff_date = datetime.now() - timedelta(days=180)  # 6 months
```

## Security & Privacy Notes

**Current design:**
- Surnames are case-insensitive match (no password/2FA)
- Anyone with surname match can identify themselves
- Individual data only shown if they know (or guess) their own surname
- This is sufficient if shared with closed AE community

**If stricter control needed:**
- Add a PIN/token system (store in separate file or config)
- Use Streamlit secrets for tokens (`st.secrets["ae_pins"]`)
- Implement 2FA (e.g., via email code)

## Troubleshooting

### "No match found" when I enter my surname
- Check spelling (exact as in database)
- Try first name instead
- Contact Fred if surname has diacritics or variant spellings

### Charts not rendering
- Ensure Plotly installed: `pip install plotly`
- Clear browser cache and refresh

### Data looks stale
- Check file modification date on `AE-citations-combined.xlsx`
- For Streamlit Cloud, wait ~2 min after GitHub push
- For local, Streamlit auto-reloads; if not, restart

## Support

For questions or updates, contact Fred Frost (Deputy Chief Editor, ERJOR).

---

**Last updated:** 2026-08-20
