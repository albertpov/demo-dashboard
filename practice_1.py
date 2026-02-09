import streamlit as st
import polars as pl

st.set_page_config(
    page_title="Streamlit with Polars",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="auto",
)
# header
st.header("Streamlit with Polars")

# load data
df = pl.read_parquet("survey_data.parquet")

# create filters
unique_years = df.select(pl.col("wave").unique().sort()).to_series().to_list()
unique_genders = df.select(pl.col("gender").unique().sort()).to_series().to_list()
region_order = ["Northeast", "Midwest", "South", "West"]

print(unique_years, unique_genders)

# # single select filters
# col1, col2, col3 = st.columns(3)
# with col1:
#     selected_year = st.selectbox("Wave", options=["All"] + unique_years)
# with col2:
#     selected_gender = st.selectbox("Gender", options=["All"] + unique_genders)
# with col3:
#     selected_region = st.selectbox("Region", options=["All"] + region_order)

# # apply filters
# df_filtered = df.filter(
#     pl.col("wave").is_in(unique_years if selected_year == "All" else [selected_year])
#     & pl.col("gender").is_in(unique_genders if selected_gender == "All" else [selected_gender])
#     & pl.col("region").is_in(region_order if selected_region == "All" else [selected_region])
# )

# multi select filters
col1, col2, col3 = st.columns(3)
with col1:
    selected_years = st.multiselect("Wave", options=unique_years, default=unique_years)
with col2:
    selected_genders = st.multiselect("Gender", options=unique_genders, default=unique_genders)
with col3:
    selected_regions = st.multiselect("Region", options=region_order, default=region_order)

# apply filters
df_filtered = df.filter(
    pl.col("wave").is_in(selected_years or unique_years)
    & pl.col("gender").is_in(selected_genders or unique_genders)
    & pl.col("region").is_in(selected_regions or region_order)
)

# high level metric cards

col1, col2, col3 = st.columns(3)

total_n = df_filtered.height

# non-weighted gender pct
# gender_counts = (
#     df_filtered
#     .group_by("gender")
#     .agg(pl.len().alias("count"))
#     .with_columns((pl.col("count") / pl.col("count").sum()).alias("pct"))
#     .sort("gender")
# )

# weighted gender pct
gender_counts = (
    df_filtered
    .group_by("gender")
    .agg(pl.col("weight").sum().alias("weighted_count"))
    .with_columns((pl.col("weighted_count") / pl.col("weighted_count").sum()).alias("pct"))
    .sort("gender")
)

gender_pct = " / ".join(
    f"{row['gender']} {row['pct']:.0%}"
    for row in gender_counts.iter_rows(named=True)
)

avg_age = df_filtered.select(pl.col("age").mean()).item()

col1.metric("Total Respondents", f"{total_n:,}")
col2.metric("Gender", gender_pct)
col3.metric("Average Age", f"{avg_age:.1f}")


import altair as alt

# calculate region counts and percentages
region_stats = (
    df_filtered
    .group_by("region")
    .agg(pl.len().alias("count"))
    .with_columns(
        (pl.col("count") / pl.col("count").sum() * 100).round(1).alias("pct")
    )
)

chart = (
    alt.Chart(region_stats)
    # .mark_bar(cornerRadius=8)
    .mark_bar(cornerRadiusEnd=3)
    .encode(
        x=alt.X("pct:Q", title="Percentage (%)"),
        y=alt.Y("region:N", title="Region", sort=region_order),
        tooltip=["region", "pct"],
    )
    .properties(
        title="Region Breakdown",
        height=200,
        width=300,
    )
)

text = chart.mark_text(dx=15).encode(
    text=alt.Text("pct:Q", format=".1f")
)

# streamlit default if no chart height/width provided
st.altair_chart(chart + text, use_container_width=True)
# mannual override height/width
st.altair_chart(chart + text, use_container_width=False)
# display the filtered dataframe
st.dataframe(df_filtered)
