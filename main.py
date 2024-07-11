import streamlit as st
from database.db_manager import DatabaseManager
from transactions.transaction_manager import TransactionManager
from visualisations.visualiser import Visualiser
from utils import setup_logging
import logging


def main():
    """The main entry point of the Personal Finance Dashboard."""
    setup_logging()
    logging.info("Application started.")

    st.title('Personal Finance Dashboard')
    st.markdown("""
    This dashboard helps you track and analyse your financial activities. Enter your monthly income and daily expenses
    to see a summary and chart of your financial health.
    """)
    st.sidebar.header('User Inputs')

    db_manager = DatabaseManager(db_file="finance_db.sqlite")
    db_manager.create_tables()

    transaction_manager = TransactionManager(db_manager.connection)
    transaction_data = transaction_manager.input_transaction()
    if transaction_data:
        transaction_type, category, amount, transaction_date, remarks = transaction_data
        transaction_manager.add_transaction_to_db(db_manager.connection, transaction_type, category, amount,
                                                  transaction_date, remarks)

    visualiser = Visualiser(db_manager.connection)
    visualiser.run_dashboard()

    if st.button('Export Transactions to CSV'):
        csv_file_path = 'transactions.csv'
        db_manager.export_data_to_csv('SELECT * FROM transactions', csv_file_path)
        st.success(f'Transactions exported successfully to {csv_file_path}')

    logging.info("Application ended.")


if __name__ == "__main__":
    main()
