import pandas as pd
file_path='items.csv'
df=pd.read_csv(file_path)
def display(df):
    df=pd.read_csv(file_path)
    print(df)
import os
import time
def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
def search_item(IC):
 for index, row in df.iterrows():
    if row['ItemCode'] == IC:
        #print( df.loc[index,'Items']," is at index:", {index})
        return index
def purchase(df):
    cart={}
    while True:
        item_code=int(input("Enter the item code:"))
        qty=int(input("Enter quantity to buy:"))
        if item_code in cart:
                cart[item_code] +=qty
        else:
                cart[item_code] =qty
        ch=input('Do you want to add another item?(y/n):').lower()
        if ch!='y':
            break
    print(cart)
    total_value=0
    purchase_list=[]
    bill=[]
    for itemcode,qty in cart.items():
            if itemcode in df["ItemCode"].values:
                    ind=search_item(itemcode)
                    st=df.loc[ind,'Stock']
                    pr=df.loc[ind,'Price']
                    item_name=df.loc[ind,'Items']
                    if(st>=qty):
                            amt=pr*qty
                            total_value+=amt
                            bill.append([item_name,qty,pr,amt])
                            purchase_list.append((ind, qty))
                    else:
                        print("Sorry.Only available",st)
    return bill,purchase_list,total_value
def update_stock(df,purchase_list):
    for ind, qty in purchase_list:
        df.loc[ind, 'Stock'] -= qty
    df.to_csv(file_path, index=False)
    import pandas as pd
df=pd.read_csv("items.csv")
def add_item():
    df=pd.read_csv("items.csv")
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
    df=pd.read_csv("items.csv")
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

def main():
    file_path='items.csv'
    df=pd.read_csv(file_path)
    display(df)
    bill,purchase_list,total_value=purchase(df)
    print("Total Value:",total_value)
    bill_df=pd.DataFrame(
        bill,
        columns=["Item","Quantity","Rate","Amount"])
    choice=input(print("Do you want to continue?:")).lower()
    if choice=='yes':
        print("Purchased Items:\n",bill_df)
        print("Total Payable Amount:",total_value)
        print("Thank You.")
        update_stock(df,purchase_list)
    else:
        print("Ok.Come again later") 
        clear_screen()
        display()

users_df=pd.read_csv("users.csv")
utype=input("enter user type(admin/normal):")
name=input("enter user name:")
pwd=input("enter password:")
user=users_df[
    (users_df["user_name"]==name)&
    (users_df["password"]==pwd)&
    (users_df["user_type"]==utype)]
if user.empty:
    print("invalid")
else:
    if utype=='admin':
        print("welcome admin session")
        display(df)
        ch1=input("do you want to add item(add) or update price(pr):")
        if ch1=='add':
            add_item()
        elif ch1=='pr':
            update_price()
        display(df)
    elif utype=='normal':
        print(f"welcome {name}")
        main()
