import csv
import random
from time import sleep

import bcrypt


##

symbols = "!@#$%^&*()-_=+[]{};:'\"<>.?/\\|`~"

ROOK_POS = [0.5351460045577583, 0.06310454491140446, 0.12127944557182074]
BOTTLE_POS = [0.5415553600056415, 0.14232975533626466, 0.22013022259933934]
SPONGE_POS = [0.5563154741216328, 0.1871495748421237, 0.1278768754295184]
WITCHHAT_POS = [0.5271910841928377, -0.07120695997003954, 0.052176207437212185]
BOWL_POS = [0.5543423776840543, -0.12138974624720286, 0.01810995164858714]
D12_POS = [0.518854868200273, -0.0011941637511675499, 0.024168489690372386]
SHIPPING_POS = [0.05380281520840685, -0.31212749135838896, 0.42416930736250485]


def load_users():
    userids = []
    hashes = []

    ## opening in "a" first makes the file if it doesn't exist yet
    file = open("users.csv", "a")
    file.close()

    file = open("users.csv", "r")
    for line in file:
        row = line.strip().split(",")
        if len(row) == 2:
            userids.append(row[0])
            hashes.append(row[1])
    file.close()
    return userids, hashes


def sign_up():
    userids, hashes = load_users()

    while True:
        userid = input("Enter a new userid: ")

        if userid == "" or " " in userid or "," in userid:
            print("Invalid ID - no blanks, spaces or commas")
        elif userid in userids:
            print("ID already taken, try another")
        else:
            break

    while True:
        password = input("Enter a password: ")

        has_upper = False
        has_lower = False
        has_digit = False
        has_symbol = False

        for char in password:
            if char.isupper():
                has_upper = True
            elif char.islower():
                has_lower = True
            elif char.isdigit():
                has_digit = True
            elif char in symbols:
                has_symbol = True

        if len(password) >= 6 and has_upper and has_lower and has_digit and has_symbol:
            confirm = input("Re-enter password to confirm: ")

            if confirm == password:
                break
            else:
                print("Passwords do not match")
        else:
            print("Weak password. Your password must have:")
            print("at least 6 characters")
            print("at least one uppercase letter")
            print("at least one lowercase letter")
            print("at least one digit")
            print("at least one symbol from: " + symbols)

    hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    file = open("users.csv", "a")
    file.write(userid + "," + hash + "\n")
    file.close()

    print("Account created successfully")
    return userid


def authenticate():
    while True:
        userids, hashes = load_users()
        userid = input("Enter your userid: ")

        if userid not in userids:
            print("User ID not found")
            choice = input("Create a new account? (y/n): ")
            if choice.lower() == "y":
                return sign_up()
            continue

        hash = hashes[userids.index(userid)]
        attempts = 0

        while attempts < 3:
            password = input("Enter your password: ")

            if bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8")):
                print("Login successful. Welcome, " + userid + "!")
                return userid

            attempts = attempts + 1
            if attempts < 3:
                print("Incorrect password. " + str(3 - attempts) + " tries left")

        print("Too many failed attempts. Re-enter ID")


## placeholder until we get the actual scanner, just type the names in
def scan_barcode():
    return input("Scan / enter products (separated by spaces): ")


def lookup_products(products):
    found_products = []

    for item in products.split():
        found = False
        file = open("products.csv")
        for line in file:
            row = line.strip().split(",")
            if len(row) == 2 and row[0] == item:
                found_products.append([row[0], float(row[1])])
                found = True
        file.close()

        if not found:
            print(f"Warning: {item} not found in products.csv, skipping.")

    return found_products


def pack_products(product_list):
    for product in product_list:
        name = product[0].strip().lower()
        if name == "rook":
            position = ROOK_POS
        elif name == "bottle":
            position = BOTTLE_POS
        elif name == "sponge":
            position = SPONGE_POS
        elif name == "witchhat":
            position = WITCHHAT_POS
        elif name == "bowl":
            position = BOWL_POS
        elif name == "d12":
            position = D12_POS
        else:
            print("Error:", product[0], "is not a recognized product.")
            continue

        print("Packing " + product[0] + "...")
        arm.set_arm_position(position)
        sleep(4)
        arm.set_arm_position(SHIPPING_POS)
        sleep(4)

    arm.home()


def complete_order(userid, product_list):
    tax_rate = 0.13
    discount_percent = random.randint(5, 50)
    subtotal = 0
    valid_products = []

    for item in product_list:
        name = item[0]
        price_text = str(item[1]).strip()

        ## only allow numbers with at most one decimal point
        if price_text.count(".") <= 1 and price_text.replace(".", "", 1).isdigit():
            price = float(price_text)
            subtotal += price
            valid_products.append([name, price])
        else:
            print("invalid order.")

    if not valid_products:
        print("cannot complete order")
        return

    ## tax goes on after the discount
    discount_amount = subtotal * (discount_percent / 100)
    discounted_total = subtotal - discount_amount
    tax_amount = discounted_total * tax_rate
    final_total = discounted_total + tax_amount

    print("\n" + "=" * 40)
    print("             ORDER RECEIPT")
    print("=" * 40)
    print(f"User ID: {userid}")
    print("-" * 40)
    print("Item                 Price")
    print("-" * 40)

    for name, price in valid_products:
        print(f"{name} ${price:.2f}")

    print("-" * 40)
    print(f"Subtotal:       ${subtotal:.2f}")
    print(f"Discount ({discount_percent}%)  -${discount_amount:.2f}")
    print(f"Tax (13%):      ${tax_amount:.2f}")
    print("-" * 40)
    print(f"TOTAL:          ${final_total:.2f}")
    print("=" * 40)

    order_data = [userid, f"{final_total:.2f}"]
    for item in valid_products:
        order_data.append(item[0])

    file = open("orders.csv", "a", newline="")
    writer = csv.writer(file)
    writer.writerow(order_data)
    file.close()

    order_count = 0
    file = open("orders.csv", "r")
    for line in file:
        if line.strip() != "":
            order_count += 1
    file.close()

    print(f"Order saved. Total orders placed at the warehouse: {order_count}\n")


def customer_summary(userid):
    total_orders = 0
    total_spent = 0.0

    product_names = []
    product_counts = []

    file = open("orders.csv", "a")
    file.close()

    file = open("orders.csv", "r")
    for row in file:
        new_row = row.strip()

        if new_row == "":
            continue

        data = new_row.split(",")

        ## each row is userid, total, then the products
        if data[0] == userid:
            total_orders += 1
            total_spent += float(data[1])

            for i in range(2, len(data)):
                item = data[i]

                if item in product_names:
                    index = product_names.index(item)
                    product_counts[index] += 1
                else:
                    product_names.append(item)
                    product_counts.append(1)

    file.close()
    total_format = f"${total_spent:.2f}"

    print("\n" + "=" * 42)
    print("         CUSTOMER ORDER SUMMARY")
    print("=" * 42)
    print(f"User ID:      {userid:>28}")
    print(f"Total Orders: {total_orders:>28}")
    print(f"Total Spent: {total_format:>29}")
    print("-" * 42)
    print(f"{'Product Name':<28} | {'Qty':>9}")
    print("-" * 42)

    if len(product_names) == 0:
        print("No previous orders found.")
    else:
        for i in range(len(product_names)):
            name = product_names[i]
            qty = product_counts[i]
            print(f"{name:<28} | {qty:>9}")

    print("=" * 42 + "\n")


def main():
    print("Welcome to the wonderful warehouse of Friday-22!!")
    print("You are free to place orders and we will ship them to the container!\n")

    userid = authenticate()

    more_orders = input("Do you want to place an order? (yes/no): ").strip().lower()
    while more_orders == "yes":
        print("Scan a barcode to place your order")
        products = scan_barcode()
        product_list = lookup_products(products)

        if len(product_list) == 0:
            print("No valid products found. Order not placed.")
        else:
            pack_products(product_list)
            complete_order(userid, product_list)

        more_orders = input("Do you want to place another order? (yes/no): ").strip().lower()

    customer_summary(userid)
    print("Thanks for shopping at Friday-22!")


main()