# ERJOR Associate Editor Dashboard

Review your activity and citation impact at a glance.

## What This Does

A private, web-based dashboard for ERJOR Associate Editors showing:
- **Your position** in the reviewing pack (anonymized for others)
- **Your reviewing volume** over the past 12 months
- **Citation impact** of papers you reviewed
- **Comparison to peers** – see the distribution without identifying them

## How It Works

1. **Open the dashboard** (shared link from ERJOR)
2. **Enter your surname** in the sidebar
3. **See your stats:** rank, number of reviews, average citations
4. **Browse anonymized pack:** see where everyone sits without identities
5. **Download your data** as CSV if needed

Everything else stays private – no one else can see your details.

## Key Metrics

- **Reviews (12m)** – How many papers you reviewed in the last year
- **Avg Citations** – Mean citations per paper (reflects citation impact of accepted work)
- **Total Citations** – All citations to papers you reviewed
- **Rank** – Your position by review volume (1 = most reviews)
- **Percentile** – Top X% of the pack

## Privacy

Rankings are **anonymized**:
- Others see "Rank 1", "Rank 2", etc. – not names
- Only you see your surname and position
- You need your exact surname to identify yourself (case-insensitive)

## Running Locally

```bash
pip install -r requirements.txt
streamlit run erjor_ae_dashboard.py
```

## Deployment

See **DEPLOYMENT_GUIDE.md** for Streamlit Cloud, Docker, or self-hosted options.

---

**Questions?** Contact the ERJOR editorial office.
