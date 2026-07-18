import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
top=tk.Tk()
users_df=pd.read_csv("users.csv")
df=pd.read_csv('items.csv')
def login():
    username=entry_username.get()
    password=entry_password.get()
    usertype=entry_usertype.get()
    user=users_df[
    (users_df["user_name"]==username)&
    (users_df["password"]==password)&
    (users_df["user_type"]==usertype)]
    if user.empty:
        messagebox.showinfo('login failed',"invalid user name or password")
    else:
        messagebox.showinfo("login success",'welcome')
        open_dashboard()
def open_dashboard():
    dashboard=tk.Toplevel(top)
    dashboard.title("Store Dashboard")
    dashboard.geometry('850x650')
    tk.Label(top,text='select items',font=('Arial',14))
    items_list=df['Items'].tolist()
    top_frame = tk.Frame(dashboard, bg="#f7f9fc")
    top_frame.pack(pady=10)
    ttk.Label(top_frame, text="Item").grid(row=0, column=0)
    item_box = ttk.Combobox(top_frame, values=items_list)
    item_box.grid(row=0, column=1, padx=5)
    ttk.Label(top_frame,text='Quantity').grid(row=0,column=2)
    entry_qty = ttk.Entry(top_frame, width=10)
    entry_qty.grid(row=0, column=3, padx=5)
    quantity_label = ttk.Label(dashboard, text="Stock: ")
    quantity_label.pack()
    price_label = ttk.Label(dashboard, text="Price: ")
    price_label.pack()
    status_label = ttk.Label(dashboard, text="")
    status_label.pack()
    bill_label = tk.Label(dashboard, text="")
    bill_label.pack()
    cart_bill=[]
    qty_label=tk.Label(dashboard,text='Enter the quantity you want to buy:',bg='light blue',fg='black')
    qty_label.pack()
    entry_qty = tk.Entry(dashboard, width=30)
    entry_qty.pack(pady=5)
    total_value_label=tk.Label(dashboard,text='')
    total_value_label.pack()
    total_value=0
    def purchase():
        selected_item = item_box.get()
        nonlocal total_value
        qty = entry_qty.get()
        if not qty.isdigit():
            messagebox.showerror("Error", "Enter valid quantity")
            return
        qty = int(qty)
        result = df[df['Items'] == selected_item]
        if result.empty:
            messagebox.showerror("Error", "Item not found")
            return
        stock = result['Stock'].values[0]
        price = result['Price'].values[0]
        if qty > stock:
            messagebox.showerror("Error", "Not enough stock")
            return

        amount = price * qty
        print(amount)
        total_value+=amount
        total_value=int(total_value)

        cart_bill.append([selected_item, qty, price, amount])
        messagebox.showinfo("Success", "Item added to cart")
    
    def update_stock():
        for selected_item, qty, price, amount in cart_bill:
            row_index = df[df['Items'] == selected_item].index[0]
            df.loc[row_index, 'Stock'] -= qty
            df.to_csv("items.csv", index=False)
    def show_bill():
        if not cart_bill:
            messagebox.showinfo("Info", "Cart is empty")
            return

        bill_df = pd.DataFrame(
            cart_bill,
            columns=["Item", "Quantity", "Rate", "Amount"]
        )
        bill_label.config(text=f"purchased items:\n{bill_df}")
        total_value_label.config(text=f"Total Payable Amount is:{total_value} ")
        update_stock()
    def open_dash():
        dashboard=tk.Toplevel(top)
        dashboard.title("Add Items")
        dashboard.geometry('850x650')
        cho_label=tk.Label(dashboard,text='do you want to add a new item other than the existing ones?(y/n):')
        cho_label.pack()
        entry_cho=tk.Entry(dashboard,width=30)
        entry_cho.pack(pady=5)
        cho=entry_cho.get()
        def choi():
                global df
                entry_icode=tk.Entry(dashboard,width=30)
                icode_label=tk.Label(dashboard,text='Enter the item code you want to add:')
                icode_label.pack()
                entry_icode.pack(pady=5)
                name_label=tk.Label(dashboard,text='Enter the name of the item you want to add:')
                name_label.pack()
                entry_name=tk.Entry(dashboard,width=30)
                entry_name.pack(pady=5)
                stock_label=tk.Label(dashboard,text='Enter the stock :')
                stock_label.pack()
                entry_stock=tk.Entry(dashboard,width=30)
                entry_stock.pack(pady=5)
                price_label=tk.Label(dashboard,text='Enter the price')
                price_label.pack()
                entry_price=tk.Entry(dashboard,width=30)
                entry_price.pack(pady=5)
                def addi():
                    global df
                    name=entry_name.get()
                    stock=entry_stock.get()
                    price=entry_price.get()
                    icode=entry_icode.get()
                    new_item={
                        "ItemCode":icode,
                        "Items":name,
                        "Stock":stock,
                        "Price":price,
                        }
                    df1=pd.DataFrame([new_item])
                    df=pd.concat([df,df1])
                    df.to_csv("items.csv", index=False)
                    messagebox.showinfo('Success',"item added successfully.")
                tk.Button(dashboard,text='Add the item in products list',command=addi).pack(pady=5)
        def handle_choice():
            choice = entry_cho.get().strip().lower()

            if choice == 'y':
                choi()
            elif choice == 'n':
                messagebox.showinfo("Info", "No item will be added")
            else:
                messagebox.showerror("Error", "Please enter y or n")

        tk.Button(dashboard, text='Submit Choice', command=handle_choice).pack(pady=5)
   
    def op_dash():
        dashboard=tk.Toplevel(top)
        dashboard.title("Delete Items")
        dashboard.geometry('650x550')
        cho_label=tk.Label(dashboard,text='do you want to delete an item existing in the list?(y/n):')
        cho_label.pack()
        entry_cho=tk.Entry(dashboard,width=20)
        entry_cho.pack(pady=5)
        cho=entry_cho.get()
        def choi():
                global df
                entry_icode=tk.Entry(dashboard,width=30)
                icode_label=tk.Label(dashboard,text='Enter the item code you want to delete:')
                icode_label.pack()
                entry_icode.pack(pady=5)
                def delete():
                    global df
                    icode = entry_icode.get().strip()

                    if icode not in df["ItemCode"].astype(str).values:
                        messagebox.showerror("Error", "Item not found")
                        return

                    df = df[df["ItemCode"].astype(str) != icode]
                    df.to_csv("items.csv", index=False)

                    messagebox.showinfo('Success', "Item deleted successfully.")
                tk.Button(dashboard,text='Delete the item from the products list',command=delete).pack(pady=5)
        def handle_choice():
            choice = entry_cho.get().strip().lower()

            if choice == 'y':
                choi()
            elif choice == 'n':
                messagebox.showinfo("Info", "No item will be deleted")
            else:
                messagebox.showerror("Error", "Please enter y or n")

        tk.Button(dashboard, text='Submit Choice', command=handle_choice).pack(pady=5)
    def check_avdl():
        df = pd.read_csv("items.csv")

        icode_label = tk.Label(dashboard, text='Enter the item code:')
        icode_label.pack()
        entry_icode = tk.Entry(dashboard, width=30)
        entry_icode.pack(pady=5)

        def search_item():
            icode = entry_icode.get().strip()
            print('value of ->', icode, '<-')
            if icode not in df["ItemCode"].astype(str).values:
                messagebox.showinfo('Error', "item not found")
            else:
                messagebox.showinfo('Success', "Item found")
                op_dash()
        tk.Button(dashboard, text="Search", command=search_item).pack(pady=5)
    def check_av():
        df = pd.read_csv("items.csv")
        icode_label = tk.Label(dashboard, text='Enter the item code:')
        icode_label.pack()
        entry_icode = tk.Entry(dashboard, width=30)
        entry_icode.pack(pady=5)

        def search_item():
            icode = entry_icode.get().strip()
            print('value of ->', icode, '<-')
            if icode not in df["ItemCode"].astype(str).values:
                messagebox.showinfo('Error', "item not found")
                open_dash()
            else:
                messagebox.showinfo('Success', "Item found")
        tk.Button(dashboard, text="Search", command=search_item,bg="light green",activebackground='blue').pack(pady=5)
    def del_item():
        df=pd.read_csv("items.csv")
        entry_icode=tk.Entry(dashboard,width=30)
        icode_label=tk.Label(dashboard,text='Enter the item code you want to delete:')
        icode_label.pack()
        entry_icode.pack(pady=5)
        tk.Button(dashboard,text='Check if item is present',command=check_avdl).pack(pady=5)

    def add_item():
        df=pd.read_csv("items.csv")
        entry_icode=tk.Entry(dashboard,width=30)
        icode_label=tk.Label(dashboard,text='Enter the item code you want to add:')
        icode_label.pack()
        entry_icode.pack(pady=5)
        tk.Button(dashboard,text='Check if item is present',command=check_av).pack(pady=5)
    def check_item():
        selected_item=item_box.get()
        code=df[df['Items']==selected_item]
        if not code.empty:
            item_code=code['ItemCode'].values[0]
            result=df[df['ItemCode']==item_code]
            quantity=result['Stock'].values[0]
            price=result['Price'].values[0]
            quantity_label.config(text=f"Stock:{quantity}")
            price_label.config(text=f"price:{price}")
            if quantity>0:
                status_label.config(text='Item Available')
            else:
                status_label.config(text='Out of Stock')
        else:
            quantity_label.config(text='')
            price_label.config(text='')
            status_label.config(text='Item not found',font=('Arial',14))
    def all_items():
        items_list=df['Items'].tolist()
    
    btn_frame = tk.Frame(dashboard, bg="light grey")
    btn_frame.pack(pady=10)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton",
    font=("Arial", 11),
    padding=6)
    style.configure("TCombobox",
    padding=5)
    ttk.Button(btn_frame,text='Check Availability',command=check_item).grid(row=0,column=0,padx=10)
    ttk.Button(btn_frame , text='Add to Cart', command=purchase).grid(row=0,column=1,padx=10)
    ttk.Button(btn_frame,text='Bill',command=show_bill).grid(row=1,column=0,padx=10)

    tk.Button(dashboard,text='Add Items',command=add_item,bg='light green',activebackground='blue').pack(pady=5)
    tk.Button(dashboard,text='Delete Items',command=del_item,bg='light green',activebackground='blue').pack(pady=5)
    top.title('login screen')
top.geometry('750x550')
top.resizable(False,False)
label_title=tk.Label(top,text='login',font=('Arial',20,'bold'),bg='light grey')
label_title.pack(pady=20)
frame = tk.Frame(top, bg="#f7f9fc")
frame.pack(pady=40)
tk.Label(frame,text='Usertype').grid(row=0,column=0,padx=10,pady=10)
entry_usertype=ttk.Entry(frame)
entry_usertype.grid(row=0,column=1,padx=10,pady=10)
tk.Label(frame, text="Username").grid(row=1, column=0, padx=10, pady=10)
entry_username = ttk.Entry(frame)
entry_username.grid(row=1,column=1, padx=10, pady=10)
tk.Label(frame,text='Password').grid(row=2, column=0, padx=10, pady=10)
entry_password = ttk.Entry(frame,show='*')
entry_password.grid(row=2, column=1, padx=10, pady=10)
ttk.Button(frame, text="Login",command=login).grid(row=3, column=0, columnspan=2, pady=20)
top.mainloop()
