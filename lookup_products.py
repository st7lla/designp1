def lookup_products(products):

    found_products = []

    for item in products.split():
        found = False
        file = open("products.csv")
        for line in file:
            row = line.split(",")
            if len(row) == 2 and row[0] == item:
                found_products.append([row[0], float(row[1])])
                found = True
        file.close()

        if not found:
            print(f"Warning: {item} not found in products.csv, skipping.")

    return found_products


print(lookup_products("Sponge D12 Rook"))