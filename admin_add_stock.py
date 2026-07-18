import pandas as pd
df=pd.read_csv("items.csv")
def add_item():
    icode=int(input("item code of the item you want to add:"))
    if icode not in df["ItemCode"].values:
        print("item not found")
        ch=input("do you want to add a new item other than the existing ones?(y/n):")
        if ch=='y':
            name=input("enter the name of the item:")
            stock=int(input("enter stock quantity:"))
            price=int(input("enter the price of the item:"))
            new_item={
                "ItemCode":icode,
                "Items":name,
                "Stock":stock,
                "Price":price,
                }
            df1=pd.DataFrame([new_item])
            df=pd.concat([df,df1])
            df.to_csv("items.csv", index=False)
            print("item added successfully.")
    else:
        add_qty=int(input("enter quantity to add:"))
        for index, row in df.iterrows():
            if row['ItemCode'] ==icode:
                ind=index
        df.loc[ind,'Stock']+=add_qty
        df.to_csv("items.csv", index=False)
        print("stock updated successfully.")
def update_price():
    icode=int(input("enter the code of the item:"))
    if icode not in df["ItemCode"].values:
        print("item not found")
    else:
        new_price=int(input("enter the new price:"))
        for index, row in df.iterrows():
            if row['ItemCode'] ==icode:
                ind=index
        df.loc[ind,'Price']=new_price
        df.to_csv("items.csv", index=False)
        print("price updated successfully.")
def del_item():
    icode=int(input("enter the item code of the item to be deleted"))
    if icode not in df["ItemCode"].values:
        print("item not found")
    else:
        for index, row in df.iterrows():
            if row['ItemCode'] ==icode:
                ind=index
    df.drop(ind,inplace=True)
    df.to_csv("items.csv",index=False)
del_item()
    
        
