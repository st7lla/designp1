def customer_summary(userid):
    total_orders = 0
    total_spent = 0.0

    product_names = []
    product_counts = []

    #open the file orders.csv
    file = open("orders.csv", "r")

    for row in file:
        new_row = row.strip()

        # skip empty lines
        if new_row == "":
            continue

        # change rows into a list
        data = new_row.split(",")

        # look for userid at index zero
        if data[0] == userid:
            total_orders += 1
            total_spent += float(data[1]) #index for the price

        # loop through product starting at index 2
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

    # summary
    print("\n" + "=" * 42)
    print(f"         CUSTOMER ORDER SUMMARY")
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
