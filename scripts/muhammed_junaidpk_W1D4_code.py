import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------------------
# Page Title and Description
# -------------------------------
st.title("🧾 Personal Expense Tracker")
st.write("Upload your expenses CSV file to analyse your spending.")

# -------------------------------
# File Uploader
# -------------------------------
uploaded_file = st.file_uploader(
    "Upload expenses.csv",
    type=["csv"]
)

if uploaded_file is not None:

    # -------------------------------
    # Read CSV
    # -------------------------------
    df = pd.read_csv(uploaded_file)

    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Clean Amount column (remove ₹ and commas)
    df["Amount"] = (
        df["Amount"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # -------------------------------
    # Sidebar Filters
    # -------------------------------
    with st.sidebar:
        st.header("Filters")

        # Date Range Filter
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime(2024, 1, 1), datetime(2024, 5, 31))
        )

        # Guard for single date selection
        if isinstance(date_range, tuple):
            start_date, end_date = date_range
        else:
            start_date = end_date = date_range

        # Category Filter
        categories = [
            "Food & Dining",
            "Transport",
            "Utilities",
            "Entertainment",
            "Shopping",
            "Healthcare"
        ]

        selected_categories = st.multiselect(
            "Select Categories",
            categories,
            default=categories
        )

        # Restore all if none selected
        if len(selected_categories) == 0:
            selected_categories = categories

        # Minimum Amount Slider
        min_amount = st.slider(
            "Minimum Amount (₹)",
            min_value=int(df["Amount"].min()),
            max_value=int(df["Amount"].max()),
            value=int(df["Amount"].min())
        )

    # -------------------------------
    # Apply Filters
    # -------------------------------
    filtered_df = df[
        (df["Date"] >= pd.to_datetime(start_date)) &
        (df["Date"] <= pd.to_datetime(end_date))
    ]

    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_categories)
    ]

    filtered_df = filtered_df[
        filtered_df["Amount"] >= min_amount
    ]

    # -------------------------------
    # KPI Calculations
    # -------------------------------
    if filtered_df.empty:
        total_spend = 0
        num_transactions = 0
        avg_transaction = 0
        largest_expense = 0
    else:
        total_spend = filtered_df["Amount"].sum()
        num_transactions = len(filtered_df)
        avg_transaction = filtered_df["Amount"].mean()
        largest_expense = filtered_df["Amount"].max()

    # -------------------------------
    # KPI Metrics
    # -------------------------------
    st.subheader("Expense Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Spend",
        f"₹{total_spend:.2f}"
    )

    col2.metric(
        "Transactions",
        num_transactions
    )

    col3.metric(
        "Average Transaction",
        f"₹{avg_transaction:.2f}"
    )

    col4.metric(
        "Largest Expense",
        f"₹{largest_expense:.2f}"
    )

    # -------------------------------
    # Filtered Data Table
    # -------------------------------
    st.subheader("Filtered Transactions")

    st.dataframe(
        filtered_df,
        hide_index=True,
        use_container_width=True
    )

    # -------------------------------
    # Download Button
    # -------------------------------
    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name=f"expenses_{start_date}_{end_date}.csv",
        mime="text/csv",
        type="primary"
    )

    # -------------------------------
    # Spend by Category Bar Chart
    # -------------------------------
    st.subheader("Spend by Category")

    bar_color = st.color_picker(
        "Choose Bar Colour",
        "#3B82F6"
    )

    st.write("Selected Colour:", bar_color)

    category_spend = (
        filtered_df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_spend)

else:
    st.info("Please upload expenses.csv to get started.")