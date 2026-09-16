import csv

with open(r"C:\Users\acer\sales.csv", "r") as file:
    reader = csv.DictReader(file)

    def calculate_total(quantity,price):
        total_amount = quantity * price
        return  total_amount

    total_sales = 0

    customer_sales={}
    
    for row in reader:
        customer_id=row["customer_id"]
        try:
            quantity=int(row["quantity"])
            price=int(row["price"])
        except ValueError:
             print("invalid  data ",row["order_id"]," — skipping row")
             
             continue
        
        total=calculate_total(quantity,price)
        if customer_id in customer_sales:
            customer_sales[customer_id]=customer_sales[customer_id]+total
        else:
            customer_sales[customer_id]=total
          
    #print(customer_sales)
        total_sales=total_sales+total
    #print(row["order_id"],row["customer_id"],row["product"],total)
print("Total sales:", total_sales)




        
           
with open("customer_sales.csv", "w", newline="") as file:
    writer = csv.DictWriter(file,fieldnames=["customer_id", "total_sales"])
    writer.writeheader()
    for customer_id, total_sales in customer_sales.items():
                writer.writerow({
                "customer_id":customer_id,
                "total_sales": total_sales
})
    