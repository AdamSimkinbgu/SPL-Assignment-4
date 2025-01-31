from persistence import *

import sys

def main(args: list[str]):
    if len(args) < 2:
        print("Usage: python action.py <actions file>")
        return

    input_file_name: str = args[1]
    with open(input_file_name) as input_file:
        for line in input_file:
            split_line: list[str] = line.strip().split(", ")
            line = line.strip()
            if not line:
                continue

            # Format: product_id, quantity, activator_id, date
            split_line: list[str] = line.split(",")
            product_id = int(split_line[0].strip())
            quantity = int(split_line[1].strip())
            activator_id = int(split_line[2].strip())
            date_str = split_line[3].strip()

            # quantity == 0 => ignore
            if quantity == 0:
                continue

            # Check product existence/quantity
            product_list = repo.products.find(id=product_id)
            if len(product_list) == 0:
                # No such product, ignore
                continue

            product = product_list[0]
            current_qty = product.quantity

            if quantity < 0:
                # Sale
                needed = abs(quantity)
                if current_qty < needed:
                    # Not enough in stock -> ignore
                    continue
                # Enough => proceed
                product.quantity = current_qty + quantity  # quantity is negative
                repo.products.delete(id=product_id)  # remove old record
                repo.products.insert(product)  # insert updated product
                # Add an activity row
                a = Activitie(product_id, quantity, activator_id, date_str)
                repo.activities.insert(a)

            else:
                # Supply (quantity > 0)
                product.quantity = current_qty + quantity
                repo.products.delete(id=product_id)
                repo.products.insert(product)
                # Insert activity
                a = Activitie(product_id, quantity, activator_id, date_str)
                repo.activities.insert(a)


if __name__ == '__main__':
    main(sys.argv)