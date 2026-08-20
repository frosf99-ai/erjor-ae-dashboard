# Deploy Dashboard Edits (Version 2.1)

## What Changed

✅ Added side-by-side pie charts (manuscript type + decisions)  
✅ Replaced dual accept/reject waterfalls with single % accept waterfall  
✅ Added median citations per paper waterfall  
✅ Added top decile (% in top 10%) waterfall  
✅ Added filter buttons (All/Accepts/Rejects) for papers table  
✅ Removed confusing distribution box plot  

---

## To Deploy (2 Steps)

### Step 1: Download Updated File
From outputs above, download:
- **`erjor_ae_dashboard.py`** (the edited version)

### Step 2: Upload to GitHub
1. Go to your GitHub repo
2. Click on `erjor_ae_dashboard.py`
3. Click pencil (edit)
4. **Paste entire new file** (replace all)
5. Commit changes
   - Message: "Edit: add pie charts, median/decile waterfalls, paper filters"

**That's it!** Streamlit Cloud redeploys automatically (~1-2 min).

---

## Or via Command Line

```bash
cd ~/erjor-ae-dashboard

# Download new file into this folder
# (erjor_ae_dashboard.py)

git add erjor_ae_dashboard.py
git commit -m "Edit: pie charts, waterfalls, filters"
git push origin main
```

---

## What You'll See After Deploy

### Individual AE View (When Identified)

**Example: Fred Frost**

```
📋 Breakdown by Manuscript Type
  [Your papers]       |  [All journal papers]
  86% Orig Research   |  86% Orig Research
  8% Review           |  6% Review
  4% Invited Review   |  4% Invited Review
  2% Study Protocol   |  4% Other

📈 Your Position Across Key Metrics

  [Your Decisions]    |  [All Decisions]
  76 Accept (74.5%)   |  1,635 Accept (76.1%)
  26 Reject (25.5%)   |  512 Reject (23.9%)

  [Waterfall 1: Reviews]
  You: Rank #1 (102 reviews)

  [Waterfall 2: Accept Rate %]
  You: 74.5% (Rank #42 of 71)

  [Waterfall 3: Median Citations/Paper]
  You: 4 citations (Rank #5 of 71)

  [Waterfall 4: % Papers in Top Decile]
  You: 35% (Rank #8 of 71)

📄 Your Reviews & Citations
  [📋 All] [✅ Accepts] [❌ Rejects]
  [102 papers listed, sorted by citations]
```

---

## Testing Locally First (Optional)

```bash
streamlit run erjor_ae_dashboard.py
# Then identify as "Frost"
# Verify all charts appear and filters work
```

---

## Verify After Deploy

### Checklist
- [ ] Dashboard loads without errors
- [ ] Pie charts appear side-by-side (not stacked)
- [ ] Waterfall charts show all 4 (no box plot)
- [ ] Filter buttons work (click All/Accepts/Rejects)
- [ ] Your rank shows correctly (Fred = #1 reviews, #5 median)
- [ ] Top decile waterfall shows %

### If Something's Wrong
- **Error loading CSV?** Check both `AEs.csv` and `AE-citations-combined.xlsx` are in repo
- **Charts not rendering?** Hard refresh browser (Ctrl+Shift+R)
- **Still broken?** Click "Reboot app" in Streamlit Cloud settings

---

## Key Metrics Examples

**For Fred Frost (after deploy):**

| Metric | Fred | Journal | Fred's Rank |
|--------|------|---------|-------------|
| Total Reviews | 102 | 2,147 | #1 of 71 |
| Accept Rate | 74.5% | 76.1% | #42 of 71 |
| Median Citations | 4 | 3.6 | #5 of 71 |
| % Top Decile | 35% | ~10% | #8 of 71 |

---

## Questions?

See `EDITS_SUMMARY.md` for full feature breakdown.

---

**Status:** Ready to deploy ✓  
**Time to deploy:** ~3 min  
**Time to redeploy:** ~1-2 min
