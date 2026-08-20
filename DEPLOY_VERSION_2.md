# How to Deploy Version 2 to Streamlit Cloud

## Quick Summary

You now have **2 new files**:
- `erjor_ae_dashboard.py` (updated)
- `AEs.csv` (new data)

You already have:
- `AE-citations-combined.xlsx` (keep it – needed for citations)
- `requirements.txt` (already correct)

---

## Option A: Upload via GitHub Web UI (Easiest)

### Step 1: Open Your Repo
1. Go to your GitHub repo: `github.com/your-username/erjor-ae-dashboard`

### Step 2: Upload New Dashboard
1. Click "Add file" → "Upload files"
2. Drag & drop `erjor_ae_dashboard.py` from outputs
3. Click "Commit changes"
   - Message: "Update: add manuscript type breakdown and complete AE data"

### Step 3: Upload New Data CSV
1. Click "Add file" → "Upload files"
2. Drag & drop `AEs.csv` from outputs
3. Click "Commit changes"
   - Message: "Add complete AE data with accepts/rejects (Aug 2022-Aug 2024)"

### Step 4: Wait for Streamlit Cloud
- Streamlit Cloud **auto-detects** the changes
- **~1-2 minutes** to redeploy
- Your URL stays the same, but app refreshes

### Step 5: Test
- Open your dashboard URL
- Try identifying as "Frost"
- Should see 102 reviews (was 25 before)
- Should see manuscript type pie chart

---

## Option B: Upload via Command Line (Terminal)

```bash
# Navigate to your project
cd ~/erjor-ae-dashboard

# Pull latest from GitHub
git pull origin main

# Copy new files from outputs
# (erjor_ae_dashboard.py and AEs.csv into this folder)

# Check status
git status
# Should show both files as untracked

# Add files
git add erjor_ae_dashboard.py AEs.csv

# Commit with message
git commit -m "Update: complete AE data, manuscript breakdown, Aug 2022-Aug 2024"

# Push to GitHub
git push origin main
```

Then **wait 1-2 minutes** for Streamlit Cloud to redeploy.

---

## What Changed

### Data
| Aspect | Before | After |
|--------|--------|-------|
| Papers | 540 | 2,147 |
| AEs | 71 | 71 |
| Period | Aug 2022–Jan 2026 | Aug 2022–Aug 2024 |
| Decision Types | Accepts only | Accepts + Rejects |
| Fred's Reviews | 25 | 102 |

### UI
- ✅ Added manuscript type pie chart
- ✅ Added accept/reject metrics
- ✅ Updated waterfall charts with new data
- ✅ Enhanced pack statistics

---

## Verify the Deployment

### Expected Changes
1. **Your metrics** (identify as "Frost")
   - Total Reviews: **102** (was 25)
   - Accepts: **76**
   - Rejects: **26**

2. **Pack statistics**
   - Total Reviews: **2,147** (was 499)
   - Accept Rate: **76.1%**

3. **New section**
   - Pie chart showing manuscript type breakdown

### If It Doesn't Work

**Check:**
1. Both files uploaded to GitHub (check repo directly)
2. No red error banner at bottom of Streamlit Cloud
3. Try clicking "Reboot app" in Streamlit Cloud settings

**If still broken:**
- Check Streamlit Cloud logs ("Manage app" → "View logs")
- Verify both CSV and XLSX files in the repo
- Verify requirements.txt has openpyxl>=3.0.0

---

## After Deployment

### Tell Your AEs
"We've updated the dashboard with complete data covering Aug 2022 – Aug 2024. You'll now see your full reviewing activity including accepts and rejects, plus a breakdown by paper type."

### Example Announcement
```
📊 ERJOR AE Dashboard Updated!

We've expanded the dashboard with complete reviewing data:
- 2,147 papers (up from 540)
- Includes accepts AND rejects
- Enhanced metrics and visualizations
- Time period: Aug 2022 – Aug 2024

Visit: [your-dashboard-url]
Enter your surname to see your activity!
```

---

## Files in Your Repository (After Update)

```
erjor-ae-dashboard/
├── erjor_ae_dashboard.py         ← UPDATED (now v2)
├── AEs.csv                       ← NEW (complete data)
├── AE-citations-combined.xlsx    ← Keep (citations)
├── requirements.txt              ← No change needed
├── README.md                     ← Optional
└── .gitignore                    ← Optional
```

---

## Troubleshooting

### "CSV not found" error
- ✓ Verify AEs.csv is in GitHub repo
- ✓ Check file is in root (same level as .py)

### "Excel file not found" error
- ✓ Verify AE-citations-combined.xlsx is in GitHub repo
- ✓ Dashboard needs BOTH files

### Wrong numbers (e.g., still shows 25 reviews for Fred)
- ✓ Streamlit cache needs to clear
- ✓ Try hard refresh: Ctrl+Shift+R (or Cmd+Shift+R)
- ✓ If still wrong, click "Reboot app" in Streamlit Cloud

### Charts not rendering
- ✓ Check browser console for errors (F12)
- ✓ Try different browser
- ✓ Clear cookies/cache

---

## Files to Download from Outputs

✅ `erjor_ae_dashboard.py`  
✅ `AEs.csv`  
✅ `VERSION_2_SUMMARY.md` (reference)

Keep:
✅ `AE-citations-combined.xlsx` (already in repo)  
✅ `requirements.txt` (already correct)

---

## Expected Timeline

| Step | Time |
|------|------|
| Upload files to GitHub | 2 min |
| Wait for Streamlit Cloud | 1-2 min |
| Test in browser | 1 min |
| **Total** | **~5 min** |

---

## Questions?

Refer to:
- `VERSION_2_SUMMARY.md` – Data & feature details
- `DEPLOYMENT_GUIDE.md` – General deployment help
- Streamlit Cloud docs – https://docs.streamlit.io/deploy

---

**Ready? Download the files and upload to GitHub!**
