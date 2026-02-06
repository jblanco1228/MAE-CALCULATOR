# 📊 Super Analyst MAE Calculator - Quick Start Guide

Beautiful web interface for calculating Mean Absolute Error between AI and Human QA scores.

## 🚀 Installation (One-Time Setup)

### Step 1: Install Python
Make sure you have Python 3.8+ installed. Check by running:
```bash
python --version
```

### Step 2: Install Required Packages
Open your terminal/command prompt and navigate to the folder with these files, then run:

```bash
pip install -r requirements.txt
```

That's it! Installation complete ✅

---

## 🎯 How to Run the App

### Simple Method:
1. Open terminal/command prompt
2. Navigate to the folder containing `mae_app.py`
3. Run this command:

```bash
streamlit run mae_app.py
```

4. Your browser will automatically open with the app! 🎉

If it doesn't open automatically, look in the terminal for a URL like:
```
Local URL: http://localhost:8501
```
Copy and paste that into your browser.

---

## 🎨 Features

### 1. **Single Chat Mode** 
- Enter ChatID and scores manually using sliders
- Instant MAE calculation
- Visual breakdown by KPI
- Perfect for testing individual chats

### 2. **Batch Upload Mode**
- Upload CSV with multiple chats
- Calculate MAE for all chats at once
- Download results as CSV
- Includes sample template download

### 3. **Quick Test Mode**
- Test with your example (ChatID 27811316)
- Verify calculator is working correctly
- Expected result: MAE = 0.33

---

## 📝 CSV Format for Batch Upload

Your CSV file should have these columns:

| Column Name | Description |
|------------|-------------|
| `chat_id` | Chat identifier |
| `ai_IssueIdentification` | AI score (0-5) |
| `ai_ResolutionCompliance` | AI score (0-5) |
| `ai_Clarity` | AI score (0-5) |
| `ai_Retention` | AI score (0-5) |
| `ai_Sentiment` | AI score (0-5) |
| `ai_CustomerCentricity` | AI score (0-5) |
| `human_IssueIdentification` | Human score (0-5) |
| `human_ResolutionCompliance` | Human score (0-5) |
| `human_Clarity` | Human score (0-5) |
| `human_Retention` | Human score (0-5) |
| `human_Sentiment` | Human score (0-5) |
| `human_CustomerCentricity` | Human score (0-5) |

**Tip:** Use the "Download Sample CSV Template" button in the app to get the correct format!

---

## 📊 MAE Interpretation

| MAE Range | Rating | Meaning |
|-----------|--------|---------|
| < 0.50 | 🟢 Excellent | Matches human analyst very closely |
| < 0.75 | 🟢 Good | Production-ready |
| < 1.00 | 🟡 Acceptable | Needs minor calibration |
| > 1.00 | 🔴 Poor | Needs major fixes |

---

## 🛠️ Troubleshooting

**Problem:** "streamlit: command not found"
- **Solution:** Try `python -m streamlit run mae_app.py`

**Problem:** Browser doesn't open automatically
- **Solution:** Look for the URL in terminal (usually `http://localhost:8501`) and open it manually

**Problem:** Port already in use
- **Solution:** Stop other Streamlit apps or use: `streamlit run mae_app.py --server.port 8502`

**Problem:** Module not found error
- **Solution:** Make sure `mae_calculator.py` is in the same folder as `mae_app.py`

---

## 💡 Tips

1. **Keyboard Shortcuts in the App:**
   - Press `/` to focus search
   - Press `R` to rerun the app
   - Press `C` to clear cache

2. **Customization:**
   - Change colors by editing the CSS in `mae_app.py`
   - Adjust KPI names in the `KPIS` list
   - Modify interpretation thresholds in the `interpret_mae()` function

3. **Stopping the App:**
   - Press `Ctrl + C` in the terminal

---

## 📂 File Structure

```
your-folder/
├── mae_calculator.py     # Core calculation logic
├── mae_app.py           # Web interface
├── requirements.txt     # Dependencies
└── README.md           # This file
```

---

## 🎯 Quick Example

1. Run: `streamlit run mae_app.py`
2. Go to "Quick Test" mode
3. Click "Run Quick Test"
4. See MAE = 0.33 ✅

---

## 📧 Support

Having issues? The app shows helpful error messages. Make sure:
- All files are in the same folder
- Python 3.8+ is installed
- Requirements are installed (`pip install -r requirements.txt`)

---

**Happy Analyzing! 🚀**
