##main function


print("welcome to the wonderful warehouse of friday-22!!/n You are free to place orders and we will ship it the container!")
#call autenticate
authenticate()

#scan barcode



more_orders = input("Do you want to place an orders?")
while more_orders == "yes":
    print("Scan a barcode to place your order")
    scan_barcode()

    #direct to look up products
    lookup_products()
    #call packpructs
    pack_products()
    #call complete (userid and product list)
    complete_order(userid,product_list)
    more_orders = input("Do you want to place an orders?")

#direct to customer summary
print(customer_summary(userid))




