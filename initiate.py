from prompt_toolkit.shortcuts import input_dialog

from persistence import *

import sys
import os


def add_branch(split_line: list[str]):
    # split_line = [id, location, number_of_employees]
    branch_id = int(split_line[0])
    location = split_line[1]
    number_of_employees = int(split_line[2])
    b = Branche(branch_id, location, number_of_employees)
    repo.branches.insert(b)


def add_supplier(split_line: list[str]):
    # split_line = [id, name, contact_information]
    supplier_id = int(split_line[0])
    sup_name = split_line[1]
    contact_info = split_line[2]
    s = Supplier(supplier_id, sup_name, contact_info)
    repo.suppliers.insert(s)


def add_product(split_line: list[str]):
    # split_line = [id, description, price, quantity]
    product_id = int(split_line[0])
    description = split_line[1]
    price = float(split_line[2])
    quantity = int(split_line[3])
    p = Product(product_id, description, price, quantity)
    repo.products.insert(p)


def add_employee(split_line: list[str]):
    # split_line = [id, name, salary, branche]
    employee_id = int(split_line[0])
    name = split_line[1]
    salary = float(split_line[2])
    branche_id = int(split_line[3])
    e = Employee(employee_id, name, salary, branche_id)
    repo.employees.insert(e)


adders = {"B": add_branch,
          "S": add_supplier,
          "P": add_product,
          "E": add_employee}


def main(args: list[str]):
    if len(args) < 2:
        print("Usage: python initiate.py <config file>")
        return

    input_file_name = "config.txt"

    repo._close()

    if os.path.isfile("bgumart.db"):
        os.remove("bgumart.db")

    repo.__init__()
    repo.create_tables()

    with open(input_file_name) as input_file:
        for line in input_file:
            line = line.strip()
            if not line:
                continue
            split_line: list[str] = line.split(",")
            record_type = split_line[0].strip()
            data_parts = [x.strip() for x in split_line[1:]]
            adders[record_type](data_parts)

if __name__ == '__main__':
    main(sys.argv)
