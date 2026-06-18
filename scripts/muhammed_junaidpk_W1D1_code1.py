import streamlit as st
import pandas as pd
from datetime import datetime

# Page Title
st.title("🧾 Personal Expense Tracker")
st.write("Upload your expenses CSV file to analyse your spending.")

# File Upload
uploaded_file = st.file_uploader("Upload expenses.csv", type=["csv"])

if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Clean Amount column (remove ₹ and commas if present)
    df["Amount"] = (
        df["Amount"]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # Sidebar Filters
    with st.sidebar:
        st.header("Filters")

        # Date Range Filter
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime(2024, 1, 1), datetime(2024, 5, 31))
        )

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

        # Restore all categories if none selected
        if len(selected_categories) == 0:
            selected_categories = categories

        # Minimum Amount Slider
        min_amount = st.slider(
            "Minimum Amount (₹)",
            min_value=int(df["Amount"].min()),
            max_value=int(df["Amount"].max()),
            value=int(df["Amount"].min())
        )

    # Apply Date Filter
    filtered_df = df[
        (df["Date"] >= pd.to_datetime(start_date)) &
        (df["Date"] <= pd.to_datetime(end_date))
    ]

    # Apply Category Filter
    filtered_df = filtered_df[
        filtered_df["Category"].isin(selected_categories)
    ]

    # Apply Minimum Amount Filter
    filtered_df = filtered_df[
        filtered_df["Amount"] >= min_amount
    ]

    # KPI Calculations
    total_spend = filtered_df["Amount"].sum()
    num_transactions = len(filtered_df)
    avg_transaction = filtered_df["Amount"].mean()
    largest_expense = filtered_df["Amount"].max()

    # Handle empty filtered data
    if filtered_df.empty:
        total_spend = 0
        num_transactions = 0
        avg_transaction = 0
        largest_expense = 0

    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Spend", f"₹{total_spend:.2f}")
    col2.metric("Transactions", num_transactions)
    col3.metric("Average Transaction", f"₹{avg_transaction:.2f}")
    col4.metric("Largest Expense", f"₹{largest_expense:.2f}")

    # Display Filtered Data
    st.subheader("Filtered Expenses")
    st.dataframe(filtered_df)

else:
    st.info("Please upload expenses.csv to get started.")