# app.py
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="EV Charging Dashboard", layout="wide")
st.title("⚡ EV Charging Station Dashboard")

st.caption(
    "Expected columns (case-sensitive): "
    "`Start Date`, `Station Name`, `Energy (kWh)`, `Duration(mins)`, "
    "`Latitude`, `Longitude` (others are fine and will be ignored)."
)

# ===== 1) Upload data =====
with st.sidebar:
    st.header("Upload Data")
    file = st.file_uploader("Choose your CSV", type=["csv"])

if file is None:
    st.info("Upload your CSV to begin.")
    st.stop()

# Read + parse
df = pd.read_csv(file, low_memory=False)

# Require datetime column
if "Start Date" not in df.columns:
    st.error("Column `Start Date` is required.")
    st.stop()

# Parse datetime and clean
# utc=True handles both tz-aware and naive inputs and yields tz-aware UTC
df["Start Date"] = pd.to_datetime(df["Start Date"], errors="coerce", utc=True)
df = df.dropna(subset=["Start Date"]).copy()

# local-naive timestamp for display/filtering
df["local_start"] = df["Start Date"].dt.tz_convert(None)

# Column names used throughout (present in your file)
station_col = "Station Name" if "Station Name" in df.columns else None
kwh_col = "Energy (kWh)" if "Energy (kWh)" in df.columns else None
dur_col = "Duration(mins)" if "Duration(mins)" in df.columns else None

# ===== 2) Filters =====
left, right = st.columns(2)
with left:
    dmin, dmax = df["local_start"].min().date(), df["local_start"].max().date()
    date_range = st.date_input(
        "Date range", (dmin, dmax),
        min_value=dmin, max_value=dmax
    )

with right:
    if station_col:
        stations = sorted(df[station_col].dropna().astype(str).unique())
        chosen = st.multiselect(
            "Stations",
            stations,
            default=stations[: min(8, len(stations))]
        )
    else:
        chosen = None

# Normalize both sides to datetime.date to avoid Timestamp/date comparison errors
start_date = pd.to_datetime(date_range[0]).date()
end_date = pd.to_datetime(date_range[-1]).date()

mask = (df["local_start"].dt.date >= start_date) & (df["local_start"].dt.date <= end_date)
if station_col and chosen:
    mask &= df[station_col].astype(str).isin(chosen)

dff = df.loc[mask].copy()

if dff.empty:
    st.warning("No data in the selected range/filters.")
    st.stop()

# ===== 3) KPIs =====
total_sessions = len(dff)
total_kwh = dff[kwh_col].sum() if kwh_col in dff.columns else np.nan
avg_dur = dff[dur_col].mean() if dur_col in dff.columns else np.nan
peak_hour = dff["local_start"].dt.hour.value_counts().idxmax() if not dff.empty else None

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Sessions", f"{total_sessions:,}")
k2.metric("Total kWh", "—" if pd.isna(total_kwh) else f"{total_kwh:,.0f}")
k3.metric("Avg Duration (min)", "—" if pd.isna(avg_dur) else f"{avg_dur:.1f}")
k4.metric("Peak Hour", "—" if peak_hour is None else f"{int(peak_hour):02d}:00")

# ===== 4) Sessions over time =====
st.subheader("📈 Sessions Over Time")
daily = dff.set_index("local_start").resample("D").size().rename("sessions")
st.line_chart(daily)

# ===== 5) Top stations + Sessions by hour =====
colA, colB = st.columns(2)

with colA:
    st.subheader("🏆 Top Stations")
    if station_col and station_col in dff.columns:
        top_n = st.slider("Show top N", 5, 20, 10, key="topn")
        top = dff[station_col].astype(str).value_counts().head(top_n)
        st.bar_chart(top)
    else:
        st.caption("No `Station Name` column found.")

with colB:
    st.subheader("⏰ Sessions by Hour")
    by_hour = dff["local_start"].dt.hour.value_counts().sort_index()
    st.bar_chart(by_hour)

# ===== 6) Heatmap (Day of Week × Hour) via styled table =====
st.subheader("🔥 Demand Heatmap (Day × Hour)")
tmp = dff.copy()
tmp["Hour"] = tmp["local_start"].dt.hour
tmp["Day"] = tmp["local_start"].dt.day_name()
order_days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
heat = (
    tmp.groupby(["Day","Hour"])
       .size()
       .unstack(fill_value=0)
       .reindex(order_days)
       .rename_axis(index=None, columns=None)
)
st.dataframe(
    heat.style.background_gradient(cmap="Blues"),
    use_container_width=True
)

# ===== 7) Map view =====
st.subheader("🗺️ Station Map")
if {"Latitude", "Longitude"}.issubset(dff.columns):
    map_df = (
        dff[["Latitude","Longitude"]]
        .dropna()
        .astype(float)
        .drop_duplicates()
        .rename(columns={"Latitude":"lat","Longitude":"lon"})
    )
    if not map_df.empty:
        st.map(map_df)
    else:
        st.caption("No valid coordinates to map.")
else:
    st.caption("Columns `Latitude` and `Longitude` not found; skipping map.")

st.divider()
st.caption("Tip: Use the sidebar to filter by date and stations. Export charts via the built-in menu.")



