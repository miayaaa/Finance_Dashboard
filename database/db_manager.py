import sqlite3
from sqlite3 import Error
import pandas as pd
import logging


class DatabaseManager:
    """Manage database connections and operations."""
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None
        try:
            self.connection = self.connect_to_database()
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database {db_file}: {e}")

    def connect_to_database(self):
        """Connect to the SQLite database."""
        try:
            conn = sqlite3.connect(self.db_file)
            logging.info("Successfully connected to the database")
            return conn
        except Error as e:
            logging.error(f"Error connecting to the database: {e}")
        return None

    def execute_query(self, query, params=None):
        """Execute a given SQL query."""
        if self.connection:
            cursor = self.connection.cursor()
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                self.connection.commit()
                logging.info(f"Query executed successfully: {query}")
            except Error as e:
                logging.error(f"The error '{e}' occurred")

    def export_data_to_csv(self, query, csv_file_path):
        """Export data from the database to a CSV file using the provided SQL query."""
        if self.connection:
            try:
                df = pd.read_sql_query(query, self.connection)
                df.to_csv(csv_file_path, index=False)
                logging.info(f"Data exported successfully to {csv_file_path}")
            except Error as e:
                logging.error(f"Failed to export data: {e}")

    def create_tables(self):
        """Create a table if not exists in SQLite."""
        create_transactions_table = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        );
        """
        self.execute_query(create_transactions_table)