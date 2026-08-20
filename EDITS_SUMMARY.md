# Dashboard Edits Summary

## Changes Made

### 1. **Manuscript Type Pie Charts – Side by Side**
**Location:** Individual AE View, "Breakdown by Manuscript Type" section

Now shows:
- **Left:** Your papers (individual breakdown)
- **Right:** All journal papers (overall context)

Both show percentages and counts, making it easy to see if your paper mix differs from the journal average.

---

### 2. **Accept/Reject Decision Pie Charts – Side by Side**
**Location:** Individual AE View, "Your Position Across Key Metrics" section

Now shows:
- **Left:** Your accept/reject breakdown with accept rate %
- **Right:** All journal decisions with overall accept rate %

Example:
- You: 76 Accept, 26 Reject (74.5% accept rate)
- Journal: 1,635 Accept, 512 Reject (76.1% accept rate)

---

### 3. **Waterfall Charts Reorganized**

#### **Waterfall 1: Total Reviews**
- All AEs ranked by review count
- Your bar highlighted in red
- Unchanged

#### **Waterfall 2: Accept Rate (%) – REPLACED**
- **Old:** Two separate charts for Accepts and Rejects
- **New:** Single chart showing % accept for each AE
- Ranked highest to lowest accept rate
- Shows you in context of the pack's acceptance standards

Example:
- You: 74.5% accept rate
- Range across pack: 55% – 90%

#### **Waterfall 3: Median Citations per Paper – NEW**
- Shows typical citation count for papers each AE reviewed
- Ranked highest to lowest median
- Useful for understanding which AEs review papers that typically get cited
- Your position highlighted in red

#### **Waterfall 4: % of Papers in Top Decile for Citations – NEW**
- Shows % of YOUR papers that are in the journal's top 10% most-cited
- Top decile threshold calculated from all papers (e.g., ≥4 citations)
- Ranked highest to lowest %
- Indicates review quality/impact

Example:
- You: 35% of your papers in top decile
- Range across pack: 8% – 55%

---

### 4. **Papers Table with Filter Buttons**
**Location:** "Your Reviews & Citations" section

**New:** Three toggle buttons
- 📋 **All Papers** – Shows all reviews (default)
- ✅ **Accepted Only** – Shows papers you recommended for accept
- ❌ **Rejected Only** – Shows papers you recommended for reject

**Note:** Rejected papers will show 0 citations (they weren't in the JCR export)

Example usage:
- Click "Accepted Only" to see your 76 accepted papers
- Click "Rejected Only" to see your 26 rejected papers
- Papers sorted by citation count (highest first)

---

### 5. **Removed: Box Plot Distribution Chart**
**Location:** Was in Pack Statistics section

**Removed:** Chart showing "Distribution of Average Citations per Review Across AEs"
- Not intuitive for editorial users
- Replaced focus with more actionable decile chart

---

## Visual Flow (Updated)

### Individual AE View (When Identified)

```
📊 Your Key Metrics
  [4 cards: Reviews, Accepts, Rejects, Citations]
  ⏱️ Turnaround Time (placeholder)

📋 Breakdown by Manuscript Type
  [Your pie chart]  |  [All journal pie chart]

📈 Your Position Across Key Metrics
  
  [Your decisions pie]  |  [All decisions pie]
  
  [Waterfall 1: Total Reviews]
  
  [Waterfall 2: Accept Rate %]
  
  [Waterfall 3: Median Citations per Paper]
  
  [Waterfall 4: % Papers in Top Decile]

📄 Your Reviews & Citations
  [📋 All] [✅ Accepts] [❌ Rejects] (filter buttons)
  [Table of papers, sorted by citations]
  [📥 Download CSV]
```

### Pack View (Always Visible)

```
📊 Anonymized AE Rankings
  [Table of all AEs – no names, numbers only]

📈 Pack Statistics
  [Summary metrics]
  
📋 All Papers by Manuscript Type
  [Pie chart]
```

---

## Key Metrics You'll See (Example: Fred Frost)

### Manuscript Type
- Your papers: 86% Original Research, 8% Review, 4% Invited Review, 2% Protocol
- Journal average: 86% Original Research, 6% Review, 4% Invited Review, 4% Other

### Accept Rate
- Your accept rate: 74.5% (76 accept, 26 reject)
- Journal average: 76.1%

### Median Citations
- Your median: 4 citations
- Rank: #5 of 71

### Top Decile
- Your % in top decile: 35% (of your 102 papers)
- Rank: #8 of 71
- (Journal's top 10% threshold: ≥5 citations)

---

## To Deploy

1. Download `erjor_ae_dashboard.py` from outputs
2. Upload to your GitHub repo (replace existing file)
3. Streamlit Cloud auto-redeploys (~1-2 min)

---

## Testing Checklist

When you test locally or see live version, verify:

✅ Manuscript type pie charts appear side-by-side (individual vs all)
✅ Accept/reject pie charts appear side-by-side (individual vs all)
✅ % Accept waterfall shows your percentage (should be ~74.5% for Fred)
✅ Median citations waterfall shows median values
✅ Top decile waterfall shows % of papers in top 10%
✅ Filter buttons work (All/Accepts/Rejects)
✅ No box plot distribution chart
✅ Rejected papers show 0 citations

---

## Notes

- All waterfall charts highlight your bar in red (#BC3C29)
- Other AEs shown in different colors (blue, green, orange, purple, gold)
- Pie charts use consistent NEJM palette
- Session state preserves filter selection while browsing

---

**Status:** Ready to deploy ✓  
**Version:** 2.1 (Edits edition)  
**Date:** August 20, 2026
