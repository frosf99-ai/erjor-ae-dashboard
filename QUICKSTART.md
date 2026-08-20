# Quick Start: ERJOR AE Dashboard

## For Fred: Running the Dashboard

### Option 1: Run Locally (Testing & Development)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run erjor_ae_dashboard.py
```

Open browser → `http://localhost:8501`

**Test it:** Enter "Frost" in the sidebar to see your data (Rank #1, 25 reviews, 3.7 avg citations).

### Option 2: Deploy to Streamlit Cloud (Free, Public Sharing)

**Prerequisites:**
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

**Steps:**
1. Create a GitHub repository with these files:
   - `erjor_ae_dashboard.py`
   - `requirements.txt`
   - `AE-citations-combined.xlsx`
   - `README.md`

2. Go to [share.streamlit.io](https://share.streamlit.io)

3. Click "New app" → select your repo → select `erjor_ae_dashboard.py` as main file

4. Deploy! You'll get a public URL like: `https://share.streamlit.io/your-user/your-repo`

5. Share the URL with all AEs

### Option 3: Self-Hosted (Docker)

```bash
docker build -t erjor-ae .
docker run -p 8501:8501 erjor-ae
```

Open → `http://your-server:8501`

---

## For AEs: Using the Dashboard

### To See Your Data

1. **Open the link** (provided by Fred)
2. **Look at anonymized rankings** (on the page, no login needed)
3. **Enter your surname** in the left sidebar (e.g., "Frost")
4. **Your card appears** showing:
   - Your rank (e.g., #1 of 71)
   - Number of reviews
   - Average citations per review
   - Your full review list

### To Download Your Data

- Scroll down to "Your Reviews & Citations"
- Click **📥 Download your papers (CSV)**
- Opens in Excel or any spreadsheet app

---

## Data Overview

**What you'll see:**

```
ERJOR Associate Editor Activity & Citations
Full career data (Aug 2022 – Jan 2026)

[Sidebar]
🔐 Identify Yourself
  Your surname: [Frost ____]

[Main page – Anonymized, anyone can see]
📊 Anonymized AE Rankings
  Rank | Reviews | Avg Cite | Median | Total
    1  |    25   |   3.7    |   4.0  |  92
    2  |    23   |   3.3    |   3.0  |  77
    3  |    21   |   3.3    |   3.0  |  69
   ...

📈 Pack Statistics
  Total AEs: 71
  Total reviews: 499
  Mean/AE: 7.0
  [Box plot showing citation distribution]

[Individual view – Only if you identify yourself]
📍 Your Position in the Pack
  Rank: #1 of 71
  Total Reviews: 25
  Avg Citations: 3.7
  Top 100%

📄 Your Reviews & Citations
  [Table with all your papers]
  [Download button]
```

---

## Data Details

**Per AE, you'll see:**
- **Rank** – Position by # of reviews (1 = most)
- **Reviews** – Number of papers reviewed
- **Avg Citations** – Mean citations per paper
- **Median Citations** – Typical citation count
- **Total Citations** – Sum across all papers

**For your papers:**
- Paper title (from published JCR article)
- Citation count (from Web of Science)
- Type (Original Research, Review, etc.)
- Decision date
- Accept/Reject outcome

---

## Updating Data

When you have new data:

1. **Get fresh export** from Web of Science + ScholarOne
2. **Replace** `AE-citations-combined.xlsx`
3. **For Streamlit Cloud:** Push to GitHub (auto-redeploys)
4. **For local/self-hosted:** Restart Streamlit (Ctrl+C, re-run)

---

## Privacy Notes

✓ **Rankings are anonymized** – others see "Rank 1", "Rank 2", not names  
✓ **Your data is private** – only you can identify yourself  
✓ **No passwords/2FA** – assumes you know your own surname  
✓ **For ERJOR AE community only** – not public

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No match found" when I enter my surname | Check spelling; try first name or contact Fred |
| Charts aren't rendering | Refresh browser; check internet connection |
| Data looks old | Check file date on AE-citations-combined.xlsx |
| "streamlit not found" error | Run `pip install -r requirements.txt` |
| Port 8501 already in use | Use different port: `streamlit run app.py --server.port 8502` |

---

## Example Workflow

### As an AE
```
Open dashboard → See I'm ranked in the middle of pack
Enter "Hart" → Discover I've reviewed 18 papers
See my papers → Some have 8+ citations, some 0
Download CSV → Keep record of my editorial contributions
```

### As Fred (Editorial Leadership)
```
Run locally → Check AE activity before each editorial meeting
Notice Frost, Gonzalez-Barcala, Llucia-Valldeperas are top reviewers
See Suzuki and Jankowski have highest avg citations
Use for recognizing AE contributions at congresses
Share with AE community for transparency
```

---

## Files Included

```
erjor_ae_dashboard.py        ← Main Streamlit app
requirements.txt             ← Python dependencies
AE-citations-combined.xlsx   ← Data file
README.md                    ← For GitHub repo
DEPLOYMENT_GUIDE.md          ← Detailed deployment options
DASHBOARD_OVERVIEW.md        ← Features & metrics
QUICKSTART.md                ← This file
```

---

## Support

**Questions?** Check:
- `DEPLOYMENT_GUIDE.md` – how to deploy
- `DASHBOARD_OVERVIEW.md` – what metrics mean
- Streamlit docs – [docs.streamlit.io](https://docs.streamlit.io)

**Issues?** Contact Fred Frost (f.frost@liverpool.ac.uk).

---

**Ready to run?** → Start with **Option 1** (local test) or **Option 2** (Streamlit Cloud share)
