from persistence import *

def main():
    """
        Prints the database contents in the following order:
          1) Activities (ordered by date)
          2) Branches   (ordered by id)
          3) Employees  (ordered by id)
          4) Products   (ordered by id)
          5) Suppliers  (ordered by id)

        Then prints:
          - Employees report (Name Salary Location total_sales_income), ordered by name
          - Activities report (date, item_description, quantity, seller_name, supplier_name),
            ordered by date.
        """
    # We can use direct SQL queries to get ordering, or we can do a normal
    # .find_all() and sort in Python. We'll use direct SQL for the custom order.

    conn = repo._conn  # direct handle to the DB connection

    # 1) Activities (by date)
    print("Activities\n")
    rows = conn.execute("SELECT product_id, quantity, activator_id, date FROM activities ORDER BY date ASC").fetchall()
    for r in rows:
        print(r, end='\n\n')

    # 2) Branches (by id)
    print("Branches\n")
    rows = conn.execute("SELECT * FROM branches ORDER BY id ASC").fetchall()
    for r in rows:
        print(r, end='\n\n')

    # 3) Employees (by id)
    print("Employees\n")
    rows = conn.execute("SELECT * FROM employees ORDER BY id ASC").fetchall()
    for r in rows:
        print(r, end='\n\n')

    # 4) Products (by id)
    print("Products\n")
    rows = conn.execute("SELECT * FROM products ORDER BY id ASC").fetchall()
    for r in rows:
        print(r, end='\n\n')

    # 5) Suppliers (by id)
    print("Suppliers\n")
    rows = conn.execute("SELECT * FROM suppliers ORDER BY id ASC").fetchall()
    for r in rows:
        print(r, end='\n\n')

    # -- Now the employees report --
    print("\n\nEmployees report\n")
    # We want: (Name, Salary, Location, total_sales_income)
    # total_sales_income = sum of (price * -quantity) for negative quantity
    # done by that employee.
    query_employees_report = """
        SELECT E.name,
               E.salary,
               B.location,
               IFNULL(SUM(CASE WHEN A.quantity < 0 THEN P.price * ( - A.quantity ) ELSE 0 END), 0) AS total_sales_income
        FROM employees E
        JOIN branches B ON E.branche = B.id
        LEFT JOIN activities A ON A.activator_id = E.id
        LEFT JOIN products P   ON A.product_id    = P.id
        GROUP BY E.id
        ORDER BY E.name ASC
        """
    rows = conn.execute(query_employees_report).fetchall()
    for (name, salary, location, total_sales) in rows:
        print(name, salary, location, total_sales, end='\n\n')

    # -- Now the activities report --
    # date, item description, quantity, seller name, supplier name
    # If quantity < 0 => sale => seller_name = employee, supplier_name = None
    # If quantity > 0 => supply => seller_name = None, supplier_name = supplier
    # We can do a join with employees and suppliers, see which is not null
    query_activities_report = """
        SELECT A.date,
               P.description,
               A.quantity,
               E.name AS employee_name,
               S.name AS supplier_name
        FROM activities A
        JOIN products P ON A.product_id = P.id
        LEFT JOIN employees E ON A.activator_id = E.id
        LEFT JOIN suppliers S ON A.activator_id = S.id
        ORDER BY A.date ASC
        """
    rows = conn.execute(query_activities_report).fetchall()
    if len(rows) > 0:
        print("\n\nActivities report\n")
        for r in rows:
            date_str, description, quantity, emp_name, sup_name = r
            if quantity < 0:
                # Sale
                seller = emp_name if emp_name else None
                supplier = None
            else:
                # Supply
                seller = None
                supplier = sup_name if sup_name else None
            print((date_str, description, quantity, seller, supplier), end='\n\n')


if __name__ == '__main__':
    main()