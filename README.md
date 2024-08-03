# Personal Finance Dashboard

## Overview

This dashboard is designed to track and analyse financial actives. 
Enter income and daily expense to see finances.

## Installation

1. Download the repository files.
2. Install the required packages:
   ```sh
   pip install -r requirements.txt
3. Run the Streamlit Web application:
   ```sh
   streamlit run main.py

## Project Structure

In the project directory, you will find the following files:

- `main.py`: The main script to run the application.
- `database/`: 
  - `db_manager.py`: Handles database operations.
- `transactions/`:
  - `transaction_manager.py`: Manages transaction records.
- `visualisations/`:
  - `visualiser.py`: Visualising transaction data.
- `finance_db.sqlite`: The SQLite database file.
- `requirements.txt`: Lists all the dependencies.
- `utils.py`: Utility functions for data validation.
- `log`: Daily log records files.