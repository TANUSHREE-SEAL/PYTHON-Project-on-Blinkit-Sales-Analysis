# PYTHON-Project-on-Blinkit-Sales-Analysis
# 🛒 Blinkit Sales Dashboard

An interactive sales analytics dashboard for Blinkit's grocery item sales data, built with Python and Streamlit.

🔗 **Live Dashboard:** https://python-project-on-blinkit-sales-analysis-9zuvtaxcyqkusndah4s47.streamlit.app/

---

## 📊 Overview

This dashboard explores item-outlet sales data across multiple stores, answering key business questions like:

- Which item categories and outlets drive the most revenue?
- How do sales vary by outlet size, type, and location tier?
- Does item visibility, weight, or shelf placement affect sales?
- Which individual products and outlets are the top performers?

It includes live filters, KPI cards, and 14 charts grouped into 7 analysis sections, each with a short data-driven insight.

---

## 🛠️ Tools Used

- **Python**
- **Pandas** — data cleaning & aggregation
- **NumPy** — numerical operations
- **Matplotlib** & **Seaborn** — data visualization
- **Streamlit** — interactive web app framework

---

## ✨ Features

- 🔍 **Filters** — Item Type, Outlet Type, Outlet Size, Location Tier
- 📈 **KPIs** — total records, total sales, average sale, unique outlets, average rating, unique items, average item weight, top item type
- 📊 **7 chart sections** (2 charts per section):
  - Item Type Performance
  - Outlet Performance
  - Location & Fat Content
  - Sales Relationships
  - Outlet Rankings & Trends
  - Ratings & Weight Distribution
  - Best Combos & Top Items
- 🧹 Automatic data cleaning: standardizes inconsistent `Item Fat Content` labels, imputes missing `Item Weight` by item-type average

---

## 📁 Project Structure

```
blinkit-sales-dashboard/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
└── data/
    └── blinkit_data.csv    # Dataset
```

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/<your-username>/blinkit-sales-dashboard.git
cd blinkit-sales-dashboard
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

If `streamlit` isn't recognized directly on Windows, use:
```bash
python -m streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## ☁️ Deployment

This app is deployed on [Streamlit Community Cloud](https://share.streamlit.io):

1. Push the project to a public GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select the repo, branch (`main`), and main file (`app.py`)
4. Click **Deploy**

---

## 📌 Dataset

`blinkit_data.csv` contains item-outlet level sales records including item type, fat content, visibility, weight, outlet type, size, location tier, establishment year, sales value, and customer rating.

---

## 👤 Author

**Tanushree Seal**
