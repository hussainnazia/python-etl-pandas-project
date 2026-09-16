import pandas as pd



df=pd.read_csv(r"C:\Users\acer\sales.csv")

def sales_transformation(df):
    df["quantity"]=pd.to_numeric(df["quantity"],errors="coerce")
    df=df.dropna(subset=["quantity"]).copy()

    df["total_amount"]=df["quantity"] * df["price"]

    df=df.groupby("customer_id").agg(total_sales=("total_amount","sum"),total_orders=("order_id", "count")).reset_index().query('total_sales>300')
    

    return df



result=sales_transformation(df)

max_sales=result["total_sales"].max()
top_cust=result.loc[result["total_sales"]==max_sales]

print(result)

print(top_cust)


top_cust.to_csv("top_customer.csv",index=False)


result.to_csv("customer_sales.csv",index=False)
