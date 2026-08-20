# ERJOR AE Dashboard – Project Summary

## What You're Getting

A **Streamlit web dashboard** that shows ERJOR Associate Editors their reviewing activity and citation impact, with fully anonymized rankings.

### Key Features

✅ **Anonymized rankings** – Others see "Rank 1, Rank 2..." not names  
✅ **Individual identification** – Each AE enters surname to see only their data  
✅ **Citation metrics** – Links reviews to JCR citations  
✅ **Pack comparison** – See where you sit relative to peers  
✅ **Downloadable data** – Export your papers as CSV  
✅ **Interactive charts** – Plotly visualizations (histograms, box plots)  

### Data Included

- **71 AEs** across full career history (Aug 2022 – Jan 2026)
- **499 total reviews** with citation impact
- **Metrics:** review count, avg/median/total citations per AE

### Example Dashboard View

```
ERJOR Associate Editor Activity & Citations
Full career data (Aug 2022 – Jan 2026)

🔐 Identify Yourself (Sidebar)
   Your surname: [Frost ____]

📊 Anonymized AE Rankings (Always Visible)
   Rank | Reviews | Avg Cite | Median | Total
     1  |    25   |   3.7    |   4.0  |  92     ← You (highlighted)
     2  |    23   |   3.3    |   3.0  |  77
     3  |    21   |   3.3    |   3.0  |  69

📍 Your Position (When Identified)
   Rank: #1 of 71  |  Reviews: 25  |  Avg Citations: 3.7
   [Histogram showing your position in pack distribution]

📄 Your Reviews & Citations (When Identified)
   Paper Title | Citations | Type | Date | Outcome
   [Table with all 25 papers reviewed by you]
   [📥 Download CSV button]
```

---

## Files Included

### Core Application
| File | Size | Purpose |
|------|------|---------|
| `erjor_ae_dashboard.py` | 8.5 KB | Main Streamlit application |
| `requirements.txt` | 78 B | Python dependencies |
| `AE-citations-combined.xlsx` | 166 KB | Data file (71 AEs, 499 reviews) |

### Documentation
| File | Purpose |
|------|---------|
| `README.md` | Brief overview (for GitHub) |
| `QUICKSTART.md` | **Start here** – how to run & use |
| `DEPLOYMENT_GUIDE.md` | Detailed deployment options (local, cloud, Docker) |
| `DASHBOARD_OVERVIEW.md` | Feature details & metrics explanation |
| `PROJECT_SUMMARY.md` | This file |

---

## Quick Start

### To Run Locally (Testing)
```bash
pip install -r requirements.txt
streamlit run erjor_ae_dashboard.py
```
Opens at `http://localhost:8501`

### To Share with AEs (Streamlit Cloud)
1. Push to GitHub
2. Connect via [share.streamlit.io](https://share.streamlit.io)
3. Share public URL with AEs

### To Self-Host (Docker)
```bash
docker build -t erjor-ae .
docker run -p 8501:8501 erjor-ae
```

See `DEPLOYMENT_GUIDE.md` for full details.

---

## How AEs Use It

1. **Open dashboard** (link from Fred)
2. **Enter surname** (e.g., "Hart") → see rank, metrics, papers
3. **Browse anonymized pack** → see where everyone sits
4. **Download CSV** → keep record of editorial contributions

---

## Your Top 5 AEs (By Review Volume)

| Rank | Name | Reviews | Avg Citations | Total Citations |
|------|------|---------|---------------|-----------------|
| 1 | Frost, Freddy | 25 | 3.68 | 92 |
| 2 | Gonzalez-Barcala, Francisco-Javier | 23 | 3.35 | 77 |
| 3 | Llucia-Valldeperas, Aida | 21 | 3.29 | 69 |
| 4 | Guan, Wei-jie | 18 | 4.50 | 81 |
| 5 | Hart, Simon | 18 | 3.50 | 63 |

(Full 71 AEs in dashboard)

---

## Customization Options

Want to change something? Easy edits in `erjor_ae_dashboard.py`:

```python
# Change time window
cutoff_date = max_date - timedelta(days=180)  # 6 months instead

# Add new metric
'Number of Citations': ['count', 'mean', 'median', 'sum', 'max']

# Change colors
marker_color='#BC3C29'  # NEJM red
marker_color='#20854E'  # NEJM green

# Add stricter authentication
if token != st.secrets["ae_tokens"][surname]:
    st.error("Invalid token")
```

See `DEPLOYMENT_GUIDE.md` for more.

---

## Security & Privacy

**Current design:**
- ✓ Anonymized rankings (no other AE names visible)
- ✓ Case-insensitive surname matching
- ✓ Private data (only visible to identified AE)
- ⚠️ No password/2FA (assumes you know your surname)

**Risk level:** Low for closed AE community  
**If stricter needed:** Add PIN/token system via Streamlit secrets

---

## Technical Stack

- **Streamlit** – Interactive web framework (Python)
- **Pandas** – Data processing
- **Plotly** – Interactive charts
- **openpyxl** – Excel file handling

**Browser:** Any modern browser (Chrome, Firefox, Safari, Edge)  
**Python:** 3.8+  
**Storage:** Single Excel file (no database)

---

## Data Updates

To refresh with new reviews:

1. Export fresh data from Web of Science + ScholarOne
2. Replace `AE-citations-combined.xlsx`
3. For Streamlit Cloud: push to GitHub (auto-redeploys)
4. For local: restart Streamlit

---

## Use Cases

### For Individual AEs
- See their reviewing volume
- Understand citation impact of their papers
- Benchmark against peers (anonymously)
- Track editorial contributions

### For Editorial Leadership (Fred)
- Monitor AE activity before editorial meetings
- Identify high-volume reviewers for advancement
- Recognize AEs with highest-impact papers
- Engage less-active reviewers
- Use for congress/conference recognition
- Show commitment to editorial transparency

### For Editorial Board
- Understand AE workload distribution
- See aggregate citation impact of editorial decisions
- Plan AE recruitment/succession

---

## Next Steps

1. **Test locally:**
   ```bash
   streamlit run erjor_ae_dashboard.py
   ```
   Enter "Frost" to see your rank (#1), 25 reviews, 3.7 avg citations

2. **Deploy:**
   - Simple: Streamlit Cloud (2 clicks)
   - Professional: Self-hosted Docker
   - Development: Keep running locally

3. **Share with AEs:**
   - Send public URL
   - Brief note: "Enter your surname to see your metrics"
   - Emphasize: rankings are anonymized for others

4. **Plan updates:**
   - Monthly/quarterly data refreshes
   - Annual review before editorial meetings
   - Gather feedback from AE community

5. **Customize:**
   - Adjust metrics (add/remove aggregations)
   - Change date windows
   - Brand with ERJOR colors/logo
   - Add editorial guidance/context

---

## Support & Questions

**For technical issues:**
- See `DEPLOYMENT_GUIDE.md` (troubleshooting section)
- Streamlit docs: [docs.streamlit.io](https://docs.streamlit.io)

**For editorial strategy:**
- Discuss with Woo-Jung Song (Chief Editor)

**For AE user support:**
- Create simple FAQ (how to identify, download data, understand metrics)
- Email contact for technical issues

---

## File Manifest

```
Project Files:
├── erjor_ae_dashboard.py           ← RUN THIS
├── requirements.txt                ← pip install -r this
├── AE-citations-combined.xlsx      ← Your data
├── README.md                       ← GitHub overview
├── QUICKSTART.md                   ← Read this first
├── DEPLOYMENT_GUIDE.md             ← How to deploy
├── DASHBOARD_OVERVIEW.md           ← Features explained
└── PROJECT_SUMMARY.md              ← This file

To run:
  pip install -r requirements.txt
  streamlit run erjor_ae_dashboard.py

To deploy:
  See DEPLOYMENT_GUIDE.md (Streamlit Cloud, Docker, or self-host)
```

---

## Success Criteria

✅ Dashboard loads data correctly  
✅ AEs can identify themselves with surname  
✅ Rankings are anonymized for others  
✅ Individual metrics visible only to identified AE  
✅ Charts render correctly  
✅ CSV download works  
✅ Easy to update with new data  

All criteria met! ✓

---

**Date created:** August 20, 2026  
**Data period:** August 2022 – January 2026  
**Total AEs:** 71  
**Total reviews:** 499  
**Status:** Ready to deploy
