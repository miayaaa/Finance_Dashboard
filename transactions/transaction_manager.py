import streamlit as st
import logging
from sqlite3 import Error


class TransactionManager:
    """Manage transaction inputs and insert provided transactions into database."""
    def __init__(self, connection):
        self.connection = connection
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize session state variables."""
        if 'amount' not in st.session_state:
            st.session_state.amount = 0.00

    def input_transaction(self):
        """Collect user input for transactions, either income or expense."""
        st.sidebar.subheader('Enter your transaction')
        transaction_type = st.sidebar.radio("Select the transaction type", ('Income', 'Expense'))
        amount, amount_valid = self.get_transaction_amount()
        category = self.get_transaction_category(transaction_type)
        transaction_date, remarks = self.get_transaction_details()
        if st.sidebar.button(f'Add {transaction_type}'):
            st.sidebar.write(f'{transaction_type} of {amount} added for {category} on {transaction_date}')
            return transaction_type, category, amount, transaction_date, remarks


    def get_transaction_amount(self):
        """Get and validate the transaction amount from user input."""
        amount_input = st.sidebar.text_input('Enter the amount', value='')
        try:
            amount = float(amount_input)
            if amount > 0:
                return amount, True
            else:
                st.sidebar.error('Please enter a number greater than 0.')
                return 0.00, False
        except ValueError:
            st.sidebar.error('Please enter a valid number.')
            return 0.00, False

    def get_transaction_category(self, transaction_type):
        """Get the transaction category."""
        if transaction_type == 'Income':
            category = st.sidebar.selectbox('Select income source', [
                'Salary', 'Business', 'Investments', 'Other'])
        else:
            category = st.sidebar.selectbox('Select expense category', [
                'Groceries', 'Rent', 'Utilities', 'Transportation', 'Education', 'Entertainment', 'Other'])
        return category

    def get_transaction_details(self):
        """Get the transaction date and remarks."""
        transaction_date = st.sidebar.date_input('Date of transaction')
        remarks = st.sidebar.text_area('Remarks (optional)', '')
        return transaction_date, remarks

    def add_transaction_to_db(self, connection, transaction_type, category, amount, transaction_date, remarks):
        """Insert user-provided transaction into the database."""
        insert_transaction_query = '''
        INSERT INTO transactions (type, category, amount, date, description) VALUES (?, ?, ?, ?, ?);
        '''
        params = (transaction_type, category, amount, transaction_date, remarks)
        try:
            cursor = connection.cursor()
            cursor.execute(insert_transaction_query, params)
            connection.commit()
            st.sidebar.success(f'{transaction_type} added successfully!')
            logging.info(f'{transaction_type} added to database successfully.')
        except Error as e:
            st.sidebar.error(f'Error: {e}')
            logging.error(f'Error adding transaction to database: {e}')
        finally:
            cursor.close()