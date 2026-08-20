# Updated Dashboard Features

## New Sections Added

### **Individual AE View (When Identified)**

#### 1. **Key Metrics Cards**
When you identify yourself, you now see 4 metric cards:
- **Total Reviews** – Number of papers reviewed
- **Accepts** – Number of papers you recommended for acceptance
- **Rejects** – Number of papers you recommended for rejection
- **Total Citations** – Sum of all citations to papers you reviewed

**Placeholder:**
- **Turnaround Time** – ⏱️ Currently blank (waiting for submission-to-decision dates in dataset)

---

#### 2. **Waterfall Charts** (New)
Three ordered bar charts showing your position relative to all 71 AEs:

**Chart 1: Total Reviews**
- All AEs ranked highest to lowest by review count
- **Your bar highlighted in red** (#BC3C29)
- Other AEs in blue (#0072B5)
- Shows exact number above each bar
- Title includes your rank (e.g., "Rank #1") and your count

**Chart 2a: Accepted Reviews** (left side)
- All AEs ranked highest to lowest by accept count
- **Your bar highlighted in red**
- Other AEs in green (#20854E)
- Shows exact numbers

**Chart 2b: Rejected Reviews** (right side)
- All AEs ranked highest to lowest by reject count
- **Your bar highlighted in red**
- Other AEs in orange (#E18727)
- Shows exact numbers

**Chart 3: Total Citations**
- All AEs ranked highest to lowest by total citations
- **Your bar highlighted in red**
- Other AEs in purple (#7876B1)
- Shows your rank in the title

---

#### 3. **Papers Table**
(Unchanged from before)
- All papers you reviewed with:
  - Paper title
  - Citation count
  - Manuscript type
  - Decision date
  - Outcome (Accept/Reject)

---

### **Pack Statistics Section (Always Visible)**

#### **Summary Metrics** (All new)

**Row 1: Reviews**
- Total AEs
- Total Reviews (All AEs combined)
- Mean reviews per AE
- Median reviews per AE

**Row 2: Accept/Reject** (New)
- Total Accepts (across all papers reviewed by all AEs)
- Total Rejects
- Accept Rate (as percentage)

**Row 3: Citations** (New)
- Total Citations (sum across all AEs' papers)
- Mean average citations per AE
- Median average citations per AE

**Chart: Citation Distribution**
(Unchanged – box plot showing quartiles and outliers)

---

## Color Scheme (NEJM Palette)

| Metric | Color | Hex |
|--------|-------|-----|
| Reviews | Blue | #0072B5 |
| Accepts | Green | #20854E |
| Rejects | Orange | #E18727 |
| Citations | Purple | #7876B1 |
| Your Bars | Red | #BC3C29 |

---

## Data Requirements

### **Currently Available** ✓
- Editor Names
- Number of Citations (from JCR)
- Manuscript Type
- Accept/Reject Decision
- Decision Date

### **Needed for Turnaround Time** ⏱️
To populate the turnaround time section, add:
- **Submission Date** (when manuscript first received)
- **Final Decision Date** (already have this)

Once you add submission dates to the export, I can:
- Calculate decision time per manuscript (in days)
- Show your average turnaround time
- Rank all AEs by speed
- Create a waterfall chart showing your position

---

## How to Update the Export

When you export fresh data from Web of Science + ScholarOne, include:
```
Editor Names | Item Title | Number of Citations | 
Accept or Reject | Latest Decision Date | 
[NEW] Submission Date | [OPTIONAL] Manuscript Type
```

Then:
1. Update `AE-citations-combined.xlsx` in GitHub
2. Streamlit Cloud auto-redeploys (~1 min)
3. Turnaround time section populates automatically

---

## To Deploy the Updated Dashboard

### Option A: Update GitHub Repo
1. Replace `erjor_ae_dashboard.py` in your GitHub repo
2. Streamlit Cloud auto-redeploys in ~1 minute

### Option B: If Running Locally
```bash
# Update the file and restart:
streamlit run erjor_ae_dashboard.py
```

---

## Visual Layout (When Identified)

```
🔐 Your Position in the Pack
  Rank #1 of 71 | Reviews: 25 | Avg Citations: 3.7

⏱️ Turnaround Time
  [Placeholder – data not yet available]

📊 Your Key Metrics
  [4 metric cards: Total Reviews, Accepts, Rejects, Total Citations]

📈 Your Position Across Key Metrics
  [Waterfall 1: Total Reviews – ranked highest to lowest]
  
  [Waterfall 2a: Accepts]  [Waterfall 2b: Rejects]
  
  [Waterfall 3: Total Citations – ranked highest to lowest]

📄 Your Reviews & Citations
  [Table of all your papers with citations]
  [📥 Download CSV]

────────────────────────────────────────────

📊 Anonymized AE Rankings (All Data)
  [Ranking table – no names, numbers only]

📈 Pack Statistics
  [Summary metrics: Total AEs, Reviews, Accepts, Rejects, Accept Rate, Citations]
  [Box plot showing citation distribution]

📝 Notes
  [Privacy and methodology disclaimers]
```

---

## Example: If Fred Frost Identifies

**Metrics:**
- Total Reviews: **25**
- Accepts: **25** (100% accept rate)
- Rejects: **0**
- Total Citations: **92**

**Charts:**
- Bar 1 (Reviews): Frost's bar at #1 position, highest at 25 reviews
- Bar 2a (Accepts): Frost's bar shows 25 (tied with others or #1)
- Bar 2b (Rejects): Frost's bar shows 0 (lowest)
- Bar 3 (Citations): Frost's bar position among all 71 AEs

**Pack sees (anonymized):**
```
Rank | Reviews | Accepts | Rejects | Total Cites
  1  |   25    |   25    |    0    |    92
  2  |   23    |   23    |    0    |    77
  3  |   21    |   21    |    0    |    69
 ...
```

No names visible to other users.

---

## Known Limitations

1. **Turnaround Time** – Requires submission dates (not in current dataset)
2. **Waterfall charts** – Currently show rank order, not actual waterfall (stacked) format
   - If you want actual waterfall/cascade effect, let me know – easy to change

---

## Feedback & Customization

Want to:
- Change chart types (e.g., actual waterfall/cascade)?
- Add more metrics?
- Change the order of sections?
- Adjust colors?

Just let me know!

---

**Updated:** August 20, 2026  
**Status:** Ready to deploy
