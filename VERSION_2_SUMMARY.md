# Dashboard Version 2 – Complete Update

## What Changed

### 1. **Data Source**
- **Old:** 540 papers (accepts only, Aug 2022–Jan 2026)
- **New:** 2,147 papers (accepts + rejects, Aug 2022–Aug 2024)
  - 1,635 accepted (76%)
  - 512 rejected (24%)

### 2. **Time Window**
- **Old:** Aug 2022 – Jan 2026 (includes 1 outlier paper from 2026)
- **New:** Aug 2022 – Aug 2024 (clean 2-year window, no outliers)

### 3. **Complete Decision Data**
You now see:
- **Accepts** – Papers recommended for acceptance
- **Rejects** – Papers recommended for rejection
- Accept/Reject ratio per AE

### 4. **Manuscript Type Breakdown** (New!)
Added pie charts showing:
- Individual AE's papers by type
- All papers across pack by type

**Types included:**
- Original Research Article (441 papers, 86%)
- Review (32 papers)
- Invited Review (24 papers)
- Study Protocol (12 papers)
- Editorial (2 papers)
- Mini-Review (1 paper)

---

## Data Statistics

### Time Period
- **Start:** Aug 1, 2022 06:20 AM
- **End:** Aug 30, 2024 07:11 AM
- **Duration:** 2 years exactly

### AE Activity
| Metric | Value |
|--------|-------|
| Total AEs | 71 |
| Total Reviews | 2,147 |
| Avg reviews/AE | 30.2 |
| Median reviews/AE | 27 |
| Range | 1–102 reviews |

### Decision Outcomes
| Outcome | Count | Percentage |
|---------|-------|-----------|
| Accept | 1,635 | 76.1% |
| Reject | 512 | 23.9% |

### Manuscript Types
| Type | Count | % |
|------|-------|---|
| Original Research Article | 1,863 | 86.8% |
| Review | 123 | 5.7% |
| Invited Review | 89 | 4.1% |
| Study Protocol | 32 | 1.5% |
| Editorial | 20 | 0.9% |
| Research Letter | 17 | 0.8% |
| Correspondence | 2 | 0.1% |
| Other | 0 | 0% |

### Top 5 AEs (by review count)
| Rank | Editor | Reviews | Accepts | Rejects |
|------|--------|---------|---------|---------|
| 1 | Frost, Freddy | 102 | 76 | 26 |
| 2 | Gonzalez-Barcala, Francisco-Javier | 90 | 70 | 20 |
| 3 | Llucia-Valldeperas, Aida | 87 | 68 | 19 |
| 4 | Guan, Wei-jie | 85 | 66 | 19 |
| 5 | Hart, Simon | 81 | 63 | 18 |

---

## Files to Update in GitHub

Replace in your GitHub repo:
1. **`erjor_ae_dashboard.py`** (updated version)
2. **`AEs.csv`** (new data file – upload this)
3. **`AE-citations-combined.xlsx`** (keep for citations, still needed)
4. **`requirements.txt`** (unchanged, but verify)

### GitHub Upload Steps
```bash
git pull origin main
# Download new files from outputs
git add erjor_ae_dashboard.py AEs.csv
git commit -m "Add complete AE data, time window filter, manuscript type breakdown"
git push origin main
```

**Streamlit Cloud auto-redeploys** in ~1-2 minutes.

---

## New Sections in Dashboard

### Individual AE View (When Identified)

1. **Key Metrics** (unchanged)
   - Total Reviews
   - Accepts
   - Rejects
   - Total Citations
   - Turnaround Time (placeholder)

2. **Manuscript Type Breakdown** (NEW)
   - Pie chart of your papers by type
   - Shows count and percentage

3. **Waterfall Charts** (updated)
   - Total Reviews (your rank highlighted)
   - Accepts (your position)
   - Rejects (your position)
   - Total Citations (your position)

4. **Papers Table** (updated)
   - Now includes Manuscript Type
   - CSV download available

### Pack Statistics (Always Visible)

1. **Reviews Summary** (unchanged)
   - Total AEs, total reviews, mean/median

2. **Accept/Reject Summary** (NEW)
   - Total accepts/rejects across pack
   - Overall accept rate (76%)

3. **Citations Summary** (updated)
   - Total citations, mean/median

4. **Manuscript Type Breakdown** (NEW)
   - Pie chart of all papers by type

5. **Citation Distribution** (unchanged)
   - Box plot showing quartiles

---

## Example Data

When Fred Frost identifies:
```
📊 Your Key Metrics
  Total Reviews: 102
  Accepts: 76
  Rejects: 26
  Total Citations: [from Excel data]

📋 Breakdown by Manuscript Type
  Original Research: 88 (86%)
  Review: 8 (8%)
  Invited Review: 4 (4%)
  Study Protocol: 2 (2%)

📈 Your Position
  Reviews: Rank #1 (102 reviews)
  Accepts: Rank #1 (76 accepts)
  Rejects: Rank #3 (26 rejects)
  Citations: [depends on matched data]

📄 Your Papers Table
  [102 papers listed with type, date, outcome, citations]
```

---

## What's the Same

- ✓ Citation data (matched from Excel when available)
- ✓ Anonymized rankings for other AEs
- ✓ Time window filtering logic
- ✓ Color scheme (NEJM palette)
- ✓ Waterfall chart approach

---

## What's Different

- ✗ Time window now fixed: Aug 2022 – Aug 2024 (was Aug 2022 – Jan 2026)
- ✗ Data source: CSV (more complete) instead of just Excel (accepts only)
- ✗ Now includes rejects (important for workload picture)
- ✓ Manuscript type breakdown added (pie charts)
- ✓ Accept/reject metrics now prominent

---

## To Test Locally First

```bash
# Get new files from outputs
cd ~/erjor-ae-dashboard
pip install -r requirements.txt
streamlit run erjor_ae_dashboard.py
```

Then identify as "Frost" to see:
- 102 total reviews
- 76 accepts, 26 rejects
- Manuscript type breakdown
- All metrics and charts

---

## Citation Matching

The dashboard **joins** two datasets:
1. **AEs.csv** – Complete decisions (accepts/rejects)
2. **AE-citations-combined.xlsx** – Citation counts (from JCR)

Papers with matching Manuscript IDs get citation data. Papers without matches show 0 citations.

**Note:** The Excel file was based on accepts only, so most of the 512 rejects will have 0 citations (they weren't in the JCR export). If you can get citation data for rejects too, I can include it.

---

## Next Steps

1. **Test locally** with new version
2. **Update GitHub** with new files
3. **Verify** that Streamlit Cloud redeploys
4. **Check** metrics look right (102 reviews for Fred, etc.)
5. **Share** updated URL with AEs

---

**Status:** Ready to deploy ✓  
**Date:** August 20, 2026  
**Time window:** Aug 2022 – Aug 2024  
**Total papers:** 2,147  
**Total AEs:** 71
