# BGU Mart Management Software

## Overview
BGU Mart is a simple supermarket management solution written in Python (3.9+) using SQLite. It stores data about:
- Employees
- Suppliers
- Products
- Branches
- Activities (sales and supply arrivals)

## Files
1. **initiate.py**  
   **Usage**: `python initiate.py config.txt`  
   **Description**:  
   - Removes any existing `bgumart.db`.  
   - Creates a new SQLite database named `bgumart.db`.  
   - Creates the required tables.  
   - Reads a configuration file (e.g., `config.txt`) to populate the tables with initial data.

2. **action.py**  
   **Usage**: `python action.py actions.txt`  
   **Description**:  
   - Reads an actions file (e.g., `actions.txt`).  
   - Each line corresponds to a sale (negative quantity) or a supply (positive quantity).  
   - Valid actions update the product quantity and log a record in the `activities` table.  
   - If a sale action does not have enough stock, the action is ignored.

3. **printdb.py**  
   **Usage**: `python printdb.py`  
   **Description**:  
   - Prints the contents of all five tables in a specified order.  
   - Displays detailed reports for employees (including total sales income) and for activities (including seller or supplier info).

## Running the Project
1. **Create and Initialize the Database**

   `python initiate.py config.txt`


2. **Print the Initial Database State**

   `python printdb.py`


3. **Process Actions**

   `python action.py actions.txt`


4. **Print the Updated Database State**

   `python printdb.py`

## Requirements
- Python 3.9 or above
- sqlite3 (usually included by default)

## Notes
- The database file must be named bgumart.db.
- No partial sales are made if product stock is insufficient—such actions are silently ignored.
- The schema and printing format follow the assignment specifications exactly.