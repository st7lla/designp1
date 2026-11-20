def complete_order(userid, product_list):
    """completes the order for a user. It adds up the prices of all valid products, applies a random discount between 5 and 50 percent then calculates the tax on it after its price is discounted. It then prints a receipt, saves the order to orders.csv."""
    #set up variables

    tax_rate = 0.13
    discount_percent = random.randint(5,50)
    subtotal = 0 #running total of all valid item prices
    valid_products = []


    #calculate subtotal

    for item in product_list:
        name = item[0] #first part of the item is the product name
        price_text = str(item[1]).strip() #second part is the text without extra spaces

        #valid price is at most one decimal point
        if price_text.count('.') <=1 and price_text.replace(".", "", 1).isdigit():
            price = float(price_text)
            subtotal += price
            valid_products.append({name, price})

        else:
            print("invalid order.")


    if not valid_products:
        print("cannot complete order")
        return


    #apply discount and tax (tax is charged after the discount)

    discount_amount = subtotal * (discount_percent / 100)
    discounted_total = subtotal - discount_amount
    tax_amount = discounted_total *tax_rate
    final_total = discounted_total + tax_amount

    #print receipt

    print("\n" + "=" * 40)
    print("         ORDER RECEIPT          ")
    print("=" * 40)
    print(f"User ID: {userid}")
    print("-" * 40)
    print("Item                 Price")
    print("-" * 40)


    for name,price in valid_products:
        print(f'{name} ${price:.2f}')


    print("-" * 40)
    print(f"Subtotal:       ${subtotal:.2f}")
    print(f"Discount ({discount_percent}%)       -${discount_amount:.2f}")
    print(f'Tax (13%):      ${tax_amount:.2f}')
    print("-" * 40)
    print(f"TOTAL:          ${final_total:.2f}")
    print("-" * 40)


    #save to orders.csv
    order_data = [userid, f"{final_total:.2f}"]
    for item in valid_products:
        order_data.append(item[0])


    #open orders.csv in append mode so the new row goes at the end of the file
    file = open("orders.csv", "a", newline = "")
    writer = csv.writer(file) #turns list into properly formatted csv file line
    writer.writerow(order_data) #write our list as one new row
    file.close()


    #count how many orders have been placed
    order_count = 0
    file = open("orders.csv", "r")
    for line in file:
        order_count += 1

    file.close()






