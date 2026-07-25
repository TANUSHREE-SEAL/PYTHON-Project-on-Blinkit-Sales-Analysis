"""
Blinkit Sales Dashboard
Built with: pandas, numpy, matplotlib, seaborn, streamlit
Run with:   streamlit run app.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ----------------------------------------------------------------------
# PAGE CONFIG & STYLE
# ----------------------------------------------------------------------
st.set_page_config(page_title="Blinkit Sales Dashboard", page_icon="🛒", layout="wide")
sns.set_theme(style="whitegrid")
plt.rcParams["figure.facecolor"] = "white"

st.markdown(
    """
    <style>
    .info-box-green {
        background-color: #16342b; color: #6fe3a3; padding: 14px 16px;
        border-radius: 8px; font-weight: 600; text-align: left; margin-bottom: 10px;
    }
    .info-box-blue {
        background-color: #16283f; color: #7fb6f5; padding: 14px 16px;
        border-radius: 8px; font-weight: 600; text-align: left; margin-bottom: 10px;
    }
    .side-label { font-weight: 700; font-size: 1.05rem; margin-top: 4px; }
    .chart-title { font-weight: 700; font-size: 1.05rem; margin-bottom: 6px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# LOAD & CLEAN DATA
# ----------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/blinkit_data.csv")

    fat_map = {
        "Low Fat": "Low Fat", "low fat": "Low Fat", "LF": "Low Fat",
        "Regular": "Regular", "reg": "Regular",
    }
    df["Item Fat Content"] = df["Item Fat Content"].map(fat_map)

    df["Item Weight"] = df.groupby("Item Type")["Item Weight"].transform(
        lambda x: x.fillna(x.mean())
    )

    df["Outlet Age"] = df["Outlet Establishment Year"].max() - df["Outlet Establishment Year"] + 1
    return df


df = load_data()

# ----------------------------------------------------------------------
# SECTION / CHART TITLES (short, no question numbers)
# ----------------------------------------------------------------------
sections = [
    {
        "title": "🏆 Item Type Performance",
        "charts": ["Top-Selling Item Types", "Lowest-Selling Item Types"],
    },
    {
        "title": "🏬 Outlet Performance",
        "charts": ["Sales by Outlet Type", "Sales by Outlet Size"],
    },
    {
        "title": "📍 Location & Fat Content",
        "charts": ["Sales by Location Tier", "Sales Share by Fat Content"],
    },
    {
        "title": "🔗 Sales Relationships",
        "charts": ["Item Visibility vs Sales", "Item Weight vs Sales"],
    },
    {
        "title": "🏅 Outlet Rankings & Trends",
        "charts": ["Top & Bottom Outlets", "Avg Sales by Establishment Year"],
    },
    {
        "title": "⭐ Ratings & Weight Distribution",
        "charts": ["Rating by Outlet Type", "Item Weight Distribution"],
    },
    {
        "title": "🥇 Best Combos & Top Items",
        "charts": ["Location Tier x Outlet Size Heatmap", "Top 10 Best-Selling Items"],
    },
]
anchor_titles = [c for s in sections for c in s["charts"]]

# ----------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🛒 Blinkit Dashboard")

    st.markdown('<div class="side-label">Created By</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box-green">TANUSHREE SEAL</div>', unsafe_allow_html=True)

    st.markdown('<div class="side-label">🛠️ Tools Used</div>', unsafe_allow_html=True)
    st.markdown("- Python\n- Pandas\n- NumPy\n- Matplotlib\n- Seaborn\n- Streamlit")

    st.markdown('<div class="side-label">📊 Dataset</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="info-box-blue">{df.shape[0]:,} Records</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("**Jump to a section:**")
    for i, s in enumerate(sections, start=1):
        st.markdown(f"- [{s['title']}](#sec{i})")

# ----------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------
st.markdown("# 🛒 Blinkit Sales Dashboard")
st.markdown("### Sales Performance & Customer Insights")
st.markdown("---")

# ----------------------------------------------------------------------
# FILTERS
# ----------------------------------------------------------------------
st.markdown("## 🔍 Filters")

f1, f2, f3, f4 = st.columns(4)
with f1:
    item_type_sel = st.selectbox("📦 Item Type", ["All"] + sorted(df["Item Type"].unique().tolist()))
with f2:
    outlet_type_sel = st.selectbox("🏬 Outlet Type", ["All"] + sorted(df["Outlet Type"].unique().tolist()))
with f3:
    outlet_size_sel = st.selectbox("📐 Outlet Size", ["All"] + sorted(df["Outlet Size"].dropna().unique().tolist()))
with f4:
    location_sel = st.selectbox("📍 Location Tier", ["All"] + sorted(df["Outlet Location Type"].unique().tolist()))

fdf = df.copy()
if item_type_sel != "All":
    fdf = fdf[fdf["Item Type"] == item_type_sel]
if outlet_type_sel != "All":
    fdf = fdf[fdf["Outlet Type"] == outlet_type_sel]
if outlet_size_sel != "All":
    fdf = fdf[fdf["Outlet Size"] == outlet_size_sel]
if location_sel != "All":
    fdf = fdf[fdf["Outlet Location Type"] == location_sel]

if fdf.empty:
    st.warning("No records match the selected filters. Showing full dataset instead.")
    fdf = df.copy()

# ----------------------------------------------------------------------
# KEY PERFORMANCE INDICATORS
# ----------------------------------------------------------------------
st.markdown("## 📈 Key Performance Indicators")

k1, k2, k3, k4 = st.columns(4)
k1.metric("📦 Total Records", f"{fdf.shape[0]:,}")
k2.metric("💰 Total Sales", f"₹{fdf['Sales'].sum():,.0f}")
k3.metric("🧾 Avg Sale / Record", f"₹{fdf['Sales'].mean():,.2f}")
k4.metric("🏬 Unique Outlets", f"{fdf['Outlet Identifier'].nunique()}")

k5, k6, k7, k8 = st.columns(4)
k5.metric("⭐ Avg Rating", f"{fdf['Rating'].mean():.2f}")
k6.metric("🏷️ Unique Items", f"{fdf['Item Identifier'].nunique():,}")
k7.metric("⚖️ Avg Item Weight", f"{fdf['Item Weight'].mean():.1f}")
top_item_type = fdf.groupby("Item Type")["Sales"].sum().idxmax() if not fdf.empty else "N/A"
k8.metric("🥇 Top Item Type", top_item_type)

st.markdown("---")


# ----------------------------------------------------------------------
# CHART FUNCTIONS — each returns (matplotlib_fig_or_None, insight_text)
# and may render its own dataframe if needed (table-based charts return None fig)
# ----------------------------------------------------------------------
def chart_top_item_types():
    s = fdf.groupby("Item Type")["Sales"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="viridis", legend=False, ax=ax)
    ax.set_xlabel("Total Sales")
    ax.set_ylabel("")
    insight = (f"**{s.idxmax()}** leads with total sales of ₹{s.max():,.0f} "
               f"({s.max()/s.sum()*100:.1f}% of overall sales).")
    return fig, insight


def chart_lowest_item_types():
    s = fdf.groupby("Item Type")["Sales"].sum().sort_values()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="rocket", legend=False, ax=ax)
    ax.set_xlabel("Total Sales")
    ax.set_ylabel("")
    insight = (f"**{s.idxmin()}** is weakest with ₹{s.min():,.0f} in sales, "
               f"~{s.max()/max(s.min(),1):.1f}x less than the top category.")
    return fig, insight


def chart_sales_by_outlet_type():
    s = fdf.groupby("Outlet Type")["Sales"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="mako", legend=False, ax=ax)
    ax.set_xlabel("Total Sales")
    ax.set_ylabel("")
    insight = f"**{s.idxmax()}** stores dominate total revenue (₹{s.max():,.0f})."
    return fig, insight


def chart_sales_by_outlet_size():
    order = [o for o in ["Small", "Medium", "High"] if o in fdf["Outlet Size"].unique()]
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(data=fdf, x="Outlet Size", y="Sales", order=order, hue="Outlet Size",
                palette="Set2", legend=False, ax=ax)
    ax.set_ylim(0, fdf["Sales"].quantile(0.98))
    avg = fdf.groupby("Outlet Size")["Sales"].mean().reindex(order)
    insight = f"**{avg.idxmax()}** outlets sell the most on average (₹{avg.max():,.1f})."
    return fig, insight


def chart_sales_by_location():
    order = [o for o in ["Tier 1", "Tier 2", "Tier 3"] if o in fdf["Outlet Location Type"].unique()]
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(data=fdf, x="Outlet Location Type", y="Sales", order=order, estimator=np.mean,
                hue="Outlet Location Type", palette="crest", legend=False, ax=ax, errorbar=None)
    ax.set_ylabel("Average Sales")
    avg = fdf.groupby("Outlet Location Type")["Sales"].mean()
    insight = f"**{avg.idxmax()}** cities have the highest average sales per item (₹{avg.max():,.1f})."
    return fig, insight


def chart_fat_content_share():
    s = fdf.groupby("Item Fat Content")["Sales"].sum()
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(s.values, labels=s.index, autopct="%1.1f%%", colors=sns.color_palette("pastel"), startangle=90)
    insight = f"**{s.idxmax()}** items account for {s.max()/s.sum()*100:.1f}% of total sales."
    return fig, insight


def chart_visibility_vs_sales():
    corr = fdf["Item Visibility"].corr(fdf["Sales"])
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.regplot(data=fdf.sample(min(2000, len(fdf)), random_state=1), x="Item Visibility", y="Sales",
                scatter_kws={"alpha": 0.3, "s": 15}, line_kws={"color": "red"}, ax=ax)
    insight = f"Correlation is **{corr:.3f}** — visibility alone is not a strong sales driver."
    return fig, insight


def chart_weight_vs_sales():
    corr = fdf["Item Weight"].corr(fdf["Sales"])
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.regplot(data=fdf.sample(min(2000, len(fdf)), random_state=1), x="Item Weight", y="Sales",
                scatter_kws={"alpha": 0.3, "s": 15}, line_kws={"color": "red"}, ax=ax)
    insight = f"Correlation is **{corr:.3f}** — item weight has essentially no linear influence on sales."
    return fig, insight


def chart_top_bottom_outlets():
    s = fdf.groupby("Outlet Identifier")["Sales"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x=s.values, y=s.index, hue=s.index, palette="flare", legend=False, ax=ax)
    ax.set_xlabel("Total Sales")
    ax.set_ylabel("")
    insight = (f"**{s.idxmax()}** leads (₹{s.max():,.0f}), **{s.idxmin()}** trails (₹{s.min():,.0f}) — "
               f"a {s.max()/max(s.min(),1):.1f}x gap.")
    return fig, insight


def chart_sales_by_year():
    s = fdf.groupby("Outlet Establishment Year")["Sales"].mean().sort_index()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.lineplot(x=s.index, y=s.values, marker="o", ax=ax, color="teal")
    ax.set_ylabel("Average Sales")
    insight = (f"Outlets from **{int(s.idxmax())}** show the highest average sales (₹{s.max():,.1f}); "
               "no clean linear trend with outlet age.")
    return fig, insight


def chart_rating_by_outlet_type():
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(data=fdf, x="Outlet Type", y="Rating", hue="Outlet Type",
                palette="coolwarm", legend=False, ax=ax)
    ax.tick_params(axis="x", rotation=15)
    avg = fdf.groupby("Outlet Type")["Rating"].mean()
    spread = avg.max() - avg.min()
    insight = (f"Ratings range {avg.min():.2f}–{avg.max():.2f} across outlet types "
               f"(spread {spread:.2f}) — " +
               ("fairly uniform overall." if spread < 0.1 else f"**{avg.idxmax()}** rated highest."))
    return fig, insight


def chart_weight_distribution():
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.histplot(fdf["Item Weight"], kde=True, bins=30, color="slateblue", ax=ax)
    ax.set_xlabel("Item Weight")
    insight = (f"Weight ranges {fdf['Item Weight'].min():.1f}–{fdf['Item Weight'].max():.1f}, "
               f"averaging {fdf['Item Weight'].mean():.1f}.")
    return fig, insight


def chart_tier_size_heatmap():
    pivot = fdf.pivot_table(index="Outlet Location Type", columns="Outlet Size", values="Sales", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
    best = pivot.stack().idxmax()
    insight = f"**{best[0]} + {best[1]}** outlets yield the highest average sales (₹{pivot.stack().max():,.1f})."
    return fig, insight


def chart_top10_items():
    top = (fdf.groupby(["Item Identifier", "Item Type"])["Sales"].sum()
             .sort_values(ascending=False).head(10).reset_index())
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(data=top, x="Sales", y="Item Identifier", hue="Item Type", dodge=False,
                palette="Spectral", ax=ax)
    ax.legend(fontsize=7, loc="lower right")
    insight = f"Top item is **{top.iloc[0]['Item Identifier']}** ({top.iloc[0]['Item Type']}), ₹{top.iloc[0]['Sales']:,.1f}."
    return fig, insight


chart_funcs = {
    "Top-Selling Item Types": chart_top_item_types,
    "Lowest-Selling Item Types": chart_lowest_item_types,
    "Sales by Outlet Type": chart_sales_by_outlet_type,
    "Sales by Outlet Size": chart_sales_by_outlet_size,
    "Sales by Location Tier": chart_sales_by_location,
    "Sales Share by Fat Content": chart_fat_content_share,
    "Item Visibility vs Sales": chart_visibility_vs_sales,
    "Item Weight vs Sales": chart_weight_vs_sales,
    "Top & Bottom Outlets": chart_top_bottom_outlets,
    "Avg Sales by Establishment Year": chart_sales_by_year,
    "Rating by Outlet Type": chart_rating_by_outlet_type,
    "Item Weight Distribution": chart_weight_distribution,
    "Location Tier x Outlet Size Heatmap": chart_tier_size_heatmap,
    "Top 10 Best-Selling Items": chart_top10_items,
}

# ----------------------------------------------------------------------
# RENDER — two charts side by side per section, like the reference dashboard
# ----------------------------------------------------------------------
for i, sec in enumerate(sections, start=1):
    st.markdown(f'<a name="sec{i}"></a>', unsafe_allow_html=True)
    st.markdown(f"## {sec['title']}")
    col1, col2 = st.columns(2)
    for col, chart_title in zip([col1, col2], sec["charts"]):
        with col:
            st.markdown(f'<div class="chart-title">{chart_title}</div>', unsafe_allow_html=True)
            fig, insight = chart_funcs[chart_title]()
            st.pyplot(fig)
            st.caption(insight)
    st.markdown("---")

with st.expander("🔍 View raw data sample"):
    st.dataframe(fdf.head(50))
