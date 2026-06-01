import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="📚 Book Store Analytics",
    page_icon="📚",
    layout="wide"
)

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("products.csv")

# ---------------------------
# HEADER
# ---------------------------
st.title("📚 Book Store Analytics Dashboard")
st.markdown("### Analyze, Filter and Explore Book Data")

st.divider()

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("📊 Dashboard Filters")

search = st.sidebar.text_input(
    "🔍 Search Book Title"
)

rating = st.sidebar.slider(
    "⭐ Minimum Rating",
    1,
    5,
    1
)

price_range = st.sidebar.slider(
    "💰 Price Range",
    float(df["Price"].min()),
    float(df["Price"].max()),
    (
        float(df["Price"].min()),
        float(df["Price"].max())
    )
)

# ---------------------------
# FILTER DATA
# ---------------------------
filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["Title"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

filtered_df = filtered_df[
    filtered_df["Rating"] >= rating
]

filtered_df = filtered_df[
    (filtered_df["Price"] >= price_range[0])
    &
    (filtered_df["Price"] <= price_range[1])
]

# ---------------------------
# METRICS
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📚 Total Books",
    len(filtered_df)
)

col2.metric(
    "💰 Average Price",
    f"£{filtered_df['Price'].mean():.2f}"
)

col3.metric(
    "📈 Highest Price",
    f"£{filtered_df['Price'].max():.2f}"
)

col4.metric(
    "📉 Lowest Price",
    f"£{filtered_df['Price'].min():.2f}"
)

st.divider()

# ---------------------------
# DATA TABLE
# ---------------------------
st.subheader("📖 Books Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ---------------------------
# DOWNLOAD BUTTON
# ---------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered CSV",
    data=csv,
    file_name="filtered_books.csv",
    mime="text/csv"
)

st.divider()

# ---------------------------
# PRICE DISTRIBUTION
# ---------------------------
st.subheader("📈 Price Distribution")

fig1, ax1 = plt.subplots(figsize=(8, 4))

ax1.hist(
    filtered_df["Price"],
    bins=15
)

ax1.set_xlabel("Price (£)")
ax1.set_ylabel("Number of Books")
ax1.set_title("Book Price Distribution")

st.pyplot(fig1)

# ---------------------------
# RATING DISTRIBUTION
# ---------------------------
st.subheader("⭐ Rating Distribution")

rating_counts = (
    filtered_df["Rating"]
    .value_counts()
    .sort_index()
)

fig2, ax2 = plt.subplots(figsize=(8, 4))

ax2.bar(
    rating_counts.index,
    rating_counts.values
)

ax2.set_xlabel("Rating")
ax2.set_ylabel("Books Count")
ax2.set_title("Rating Distribution")

st.pyplot(fig2)

# ---------------------------
# SUMMARY STATS
# ---------------------------
st.subheader("📊 Summary Statistics")

st.dataframe(
    filtered_df.describe(),
    use_container_width=True
)

# ---------------------------
# TOP EXPENSIVE BOOKS
# ---------------------------
st.subheader("💰 Top 10 Most Expensive Books")

top_expensive = filtered_df.sort_values(
    by="Price",
    ascending=False
).head(10)

st.dataframe(
    top_expensive,
    use_container_width=True
)

# ---------------------------
# TOP RATED BOOKS
# ---------------------------
st.subheader("🏆 Top Rated Books")

top_rated = filtered_df.sort_values(
    by=["Rating", "Price"],
    ascending=False
).head(10)

st.dataframe(
    top_rated,
    use_container_width=True
)

# ---------------------------
# FIVE STAR BOOKS
# ---------------------------
st.subheader("⭐ 5-Star Books")

five_star_books = filtered_df[
    filtered_df["Rating"] == 5
]

st.dataframe(
    five_star_books,
    use_container_width=True
)

# ---------------------------
# FOOTER
# ---------------------------
st.divider()

st.caption(
    "🚀 Developed by Harsha Sri Sai Thummala | SkillCraft Technology Internship Project"
)