# ERJOR AE Dashboard – Feature Overview

## Data Summary
- **Total AEs:** 71
- **Total reviews:** 499 across full period
- **Date range:** Aug 2022 – Jan 2026
- **Average reviews per AE:** 7.0
- **Median reviews per AE:** 6
- **Range:** 1–25 reviews per AE

## Top Reviewers (Example)
| Rank | Editor | Reviews | Avg Citations | Total Citations |
|------|--------|---------|----------------|-----------------|
| 1 | Frost, Freddy | 25 | 3.7 | 92 |
| 2 | Gonzalez-Barcala, Francisco-Javier | 23 | 3.4 | 77 |
| 3 | Llucia-Valldeperas, Aida | 21 | 3.3 | 69 |
| 4 | Guan, Wei-jie | 18 | 4.5 | 81 |
| 5 | Hart, Simon | 18 | 3.5 | 63 |

## Dashboard Sections

### 1. **Identify Yourself** (Sidebar)
- Enter surname to reveal your position and metrics
- Case-insensitive matching
- Private – only you see your name

### 2. **Your Position in the Pack** (When Identified)
**Metrics displayed:**
- **Rank** – your position by review volume (e.g., #1 of 71)
- **Total Reviews** – number of papers you reviewed
- **Avg Citations** – mean citations per paper
- **Median Citations** – typical citation count
- **Percentile** – top X% by review volume

**Visual:**
- Histogram of review counts across all AEs
- Your position highlighted with a red dashed line

### 3. **Your Reviews & Citations** (When Identified)
**Table showing all your papers:**
- Paper title (from published JCR article)
- Number of citations (from Web of Science)
- Manuscript type (Original Research, Review, etc.)
- Decision date
- Outcome (Accept/Reject)

**Download option:**
- CSV export of your papers for personal records

### 4. **Anonymized Rankings** (Always Visible)
**Full ranking table:**
- Rank (1–71)
- Reviews (count)
- Avg Citations
- Median Citations
- Total Citations

**Privacy:**
- Others see "Rank 1", "Rank 2", etc. – no names
- Your row is highlighted in light blue when you identify yourself
- No AE names visible to other users

### 5. **Pack Statistics** (Always Visible)
**Summary metrics:**
- Total AEs (71)
- Total reviews (499)
- Mean/median reviews per AE
- Distribution of average citations

**Visualization:**
- Box plot showing citation distribution across AE population
- Shows median, quartiles, and outliers

### 6. **Notes** (Always Visible)
Privacy and methodology disclaimers:
- Rankings are anonymized
- Full career data shown (not just recent period)
- JCR citations may include self-citations
- Tool is for reflection, not evaluation

---

## Example: If Fred Frost Identifies

**His card would show:**
```
Position in the Pack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Rank: #1 of 71
  Reviews: 25
  Avg Citations: 3.7

Your metrics:
  Total citations: 92
  Median citations: 4.0
  You're in the top 100%
```

**His papers (top 5 by citations):**
| Title | Citations | Type | Date | Outcome |
|-------|-----------|------|------|---------|
| [Paper A] | 12 | Original Research | Jan 2026 | Accept |
| [Paper B] | 8 | Original Research | Dec 2025 | Accept |
| [Paper C] | 7 | Review | Oct 2025 | Accept |
| ... | ... | ... | ... | ... |

---

## Security Notes

**Current design:**
- Surnames are case-insensitive (no 2FA)
- Reasonable for a closed AE community
- Assumes AEs know their own name!

**If stricter security needed:**
- Can add PIN/token system
- Can use Streamlit secrets for authentication
- Can implement email verification

---

## Usage Flow

### For Any User
1. Open dashboard (shared link)
2. See anonymized rankings (no identities)
3. See pack statistics and distribution

### For Individual AE
1. Open dashboard
2. Enter surname (e.g., "Frost")
3. System matches and reveals:
   - Their rank (#1 of 71)
   - Their metrics (25 reviews, 3.7 avg citations)
   - Their specific papers and citation counts
   - Where they sit in the distribution
4. Download CSV of their papers if needed

### For Editorial Leadership (Fred)
- Can monitor AE activity and citation impact
- Identify high-volume reviewers (potential for advancement)
- See which AEs' papers have highest citation impact
- Identify less-active AEs (potential recruitment/retention issue)
- Use for recognizing AE contributions at annual meetings

---

## Technical Details

**Stack:**
- Streamlit (frontend/backend)
- Pandas (data processing)
- Plotly (interactive charts)
- openpyxl (Excel I/O)

**Data source:**
- `AE-citations-combined.xlsx`
- Single sheet with editor names, citations, decision dates
- Linked to JCR via citation counts

**Deployment:**
- Streamlit Cloud (simplest, free tier available)
- Docker / self-hosted (full control)
- Local development (for testing/iteration)

---

## Next Steps

1. **Review dashboard locally:**
   ```bash
   streamlit run erjor_ae_dashboard.py
   ```

2. **Customize if needed:**
   - Adjust color scheme (NEJM palette by default)
   - Change metrics computed (add/remove citation aggregations)
   - Adjust time windows or filters

3. **Deploy:**
   - Push to GitHub + Streamlit Cloud, or
   - Self-host with Docker, or
   - Run on institutional server

4. **Share with AE community:**
   - Send public URL
   - Brief explanation of how to use (enter surname)
   - Note on privacy (anonymized rankings)

5. **Plan updates:**
   - Refresh data quarterly or annually
   - Monitor for new AEs joining
   - Gather feedback on utility

