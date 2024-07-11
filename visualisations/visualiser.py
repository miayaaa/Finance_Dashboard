import streamlit as st
import pandas as pd
import plotly.express as px
from sqlite3 import Error
import logging

class Visualiser:
    """Fetch transaction data and manage visualisations."""
    def __init__(self, connection):
        self.connection = connection

    def run_dashboard(self):
        """Run the main dashboard app."""
        df = self.fetch_transaction_data()
        if df.empty:
            st.write("No transaction data available to display.")
            return

        monthly_summary = self.prepare_monthly_summary(df)
        most_recent_month = monthly_summary.index[-1] if not monthly_summary.empty else None
        selected_month = self.select_month_to_view(monthly_summary, most_recent_month)
        self.display_pie_chart(df, selected_month)
        self.display_bar_chart(monthly_summary)
        self.display_transactions_table(df)

    def fetch_transaction_data(self):
        """Fetch transaction data from the database."""
        try:
            cursor = self.connection.cursor()
            query = "SELECT date, type, category, amount, description FROM transactions ORDER BY date ASC;"
            cursor.execute(query)
            records = cursor.fetchall()
            df = pd.DataFrame(records, columns=['Date', 'Type', 'Category', 'Amount', 'Remarks'])
            df['Amount'] = pd.to_numeric(df['Amount'])
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            logging.info("Transaction data fetched successfully.")
            return df
        except Error as e:
            logging.error(f"Failed to fetch transaction data: {e}")
            return pd.DataFrame()

    def prepare_monthly_summary(self, df):
        """Prepare a summary of transactions grouped by month and type."""
        df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
        monthly_summary = df.groupby(['Month', 'Type'])['Amount'].sum().unstack().fillna(0)
        monthly_summary.index = monthly_summary.index.astype(str)
        return monthly_summary

    def select_month_to_view(self, monthly_summary, default_month):
        """Select a month to view expenses breakdown."""
        month_options = list(monthly_summary.index)
        if default_month and default_month in month_options:
            default_index = month_options.index(default_month)
        else:
            default_index = 0
        selected_month = st.selectbox('Select Month to View Expenses Breakdown', options=month_options, index=default_index)
        return selected_month

    def display_transactions_table(self, df):
        """Display a table of all transactions."""
        st.dataframe(df.sort_values(by='Date', ascending=False), height=400, width=900)

    def display_bar_chart(self, monthly_summary):
        """Display a bar chart of monthly income and expenses."""
        fig_bar = px.bar(monthly_summary, x=monthly_summary.index, y=['Income', 'Expense'],
                         title='Monthly Income and Expense', labels={'value': 'Amount', 'Month': 'Date'},
                         barmode='group',
                         height=400)
        st.plotly_chart(fig_bar)

    def display_pie_chart(self, df, selected_month):
        """Display a pie chart of expenses for the selected month."""
        if selected_month:
            selected_month_expenses = df[(df['Type'] == 'Expense') & (df['Month'].astype(str) == selected_month)]
            if not selected_month_expenses.empty:
                fig_pie = px.pie(selected_month_expenses, names='Category', values='Amount',
                                 title=f'Expenses by Category for {selected_month}', width=660, height=435)
                st.plotly_chart(fig_pie)
            else:
                st.write(f"No expenses recorded for {selected_month}.")