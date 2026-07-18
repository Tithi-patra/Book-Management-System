import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
root = tk.Tk()
root.title("Login")
root.geometry("600x450")
conn=mysql.connector.connect(
    host='localhost',
    user='root',
    password='kbpw1234',
    database='book_store_db')
cursor=conn.cursor()
cart_bill=[]
def login():
    usertype=entry_usertype.get()
    username=user_entry.get()
    password=pass_entry.get()
    query="select *from users where user_type=%s and user_name=%s and password=%s"
    cursor.execute(query,(usertype,username,password))
    result=cursor.fetchone()
    if result:
        messagebox.showinfo("Success","login successful")
        open_dashboard(usertype)
        root.withdraw()   
    else:
        messagebox.showinfo("error","invalid username or password")
def open_dashboard(usertype):
    dashboard=tk.Toplevel(root)
    dashboard.configure(bg="#f4f6f9")
    title = tk.Label(
    dashboard,
    text="Book Store Dashboard",
    font=("Segoe UI",15,"bold"),
    bg="#f4f6f9"
    )
    title.pack(pady=20)
    btn_style = {
    "font":("Segoe UI",10),
    "width":12,
    "height":1,
    "bg":"#2E86C1",
    "fg":"white",
    "relief":"flat"
    }
    dashboard.geometry("600x500")
    top_frame = tk.Frame(dashboard, bg="#f7f9fc")
    top_frame.pack(pady=10)
    tk.Button(dashboard,text='view items',command=view_items,**btn_style).pack(pady=5)
    if usertype.lower()=='admin':
        tk.Button(dashboard,text='Add Items',command=add_items,**btn_style).pack(pady=5)
        tk.Button(dashboard,text='Delete Items',command=del_items,**btn_style).pack(pady=5)
        tk.Button(dashboard,text='Update Stock',command=update_stock,**btn_style).pack(pady=5)
def add_items():
    view_win2=tk.Toplevel(root)
    view_win2.title("Add Item")
    view_win2.geometry("400x200")
    cho_label=tk.Label(view_win2,text='do you want to add a new item other than the existing ones?(y/n):')
    cho_label.pack()
    entry_cho=tk.Entry(view_win2,width=30)
    entry_cho.pack(pady=5)
    cho=entry_cho.get()
    def choi():
                name_label=tk.Label(view_win2,text='Enter the name of the item you want to add:')
                name_label.pack()
                entry_name=tk.Entry(view_win2,width=30)
                entry_name.pack(pady=5)
                stock_label=tk.Label(view_win2,text='Enter the stock :')
                stock_label.pack()
                entry_stock=tk.Entry(view_win2,width=30)
                entry_stock.pack(pady=5)
                price_label=tk.Label(view_win2,text='Enter the price')
                price_label.pack()
                entry_price=tk.Entry(view_win2,width=30)
                entry_price.pack(pady=5)
                def addi():
                    name=entry_name.get()
                    stock=entry_stock.get()
                    price=entry_price.get()
                    insert_qu='''INSERT INTO items (Items,Stock,Price)
                    VALUES (%s,%s,%s)'''
                    new_item=(
                        name,
                        stock,
                        price,
                        )
                    cursor.execute(insert_qu,new_item)
                    conn.commit()
                    messagebox.showinfo('Success',"item added successfully.")
                tk.Button(view_win2,text='Add the item in products list',command=addi).pack(pady=5)
    def handle_choice():
            choice = entry_cho.get().strip().lower()

            if choice == 'y':
                choi()
            elif choice == 'n':
                messagebox.showinfo("Info", "No item will be added")
            else:
                messagebox.showerror("Error", "Please enter y or n")

    tk.Button(view_win2, text='Submit Choice', command=handle_choice).pack(pady=5)
def del_items():
        view_win3=tk.Toplevel(root)
        view_win3.title("Delete Items")
        view_win3.geometry('650x550')
        cho_label=tk.Label(view_win3,text='do you want to delete an item existing in the list?(y/n):')
        cho_label.pack()
        entry_cho=tk.Entry(view_win3,width=20)
        entry_cho.pack(pady=5)
        cho=entry_cho.get()
        def choi():
                entry_icode=tk.Entry(view_win3,width=30)
                icode_label=tk.Label(view_win3,text='Enter the item code you want to delete:')
                icode_label.pack()
                entry_icode.pack(pady=5)
                def delete():
                    icode = entry_icode.get().strip()
                    cursor.execute("SELECT Item_code FROM items WHERE Item_code = %s",(icode,))

                    if cursor.fetchone() is None:
                        messagebox.showerror("Error", "Item not found")
                        return
                    
                    cursor.execute("delete from items where Item_code=%s",(icode,));
                    conn.commit()
                    messagebox.showinfo('Success', "Item deleted successfully.")
                tk.Button(view_win3,text='Delete the item from the products list',command=delete).pack(pady=5)
        def handle_choice():
            choice = entry_cho.get().strip().lower()

            if choice == 'y':
                choi()
            elif choice == 'n':
                messagebox.showinfo("Info", "No item will be deleted")
            else:
                messagebox.showerror("Error", "Please enter y or n")

        tk.Button(view_win3, text='Submit Choice', command=handle_choice).pack(pady=5)
def update_stock():
    stock_win = tk.Toplevel(root)
    stock_win.title("Update Stock")
    stock_win.geometry("450x300")

    tk.Label(
        stock_win,
        text="Select Item",
        font=("Arial", 11)
    ).pack(pady=10)
    cursor.execute("SELECT Items FROM items")
    items = [row[0] for row in cursor.fetchall()]

    item_dropdown = ttk.Combobox(
        stock_win,
        values=items,
        state="readonly",
        width=30
    )
    item_dropdown.pack(pady=5)

    tk.Label(stock_win,text="Enter Quantity to Add").pack(pady=10)

    stock_entry = tk.Entry(stock_win, width=20)
    stock_entry.pack(pady=5)

    def save_stock():
        item_name = item_dropdown.get()
        new_stock = stock_entry.get()

        if not item_name:
            messagebox.showerror("Error", "Select an item")
            return

        if not new_stock.isdigit():
            messagebox.showerror("Error", "Enter a valid stock quantity")
            return

        cursor.execute("UPDATE items SET Stock = Stock + %s WHERE Items = %s",(int(new_stock), item_name))
        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Stock for '{item_name}' updated!!"
        )

    tk.Button(
        stock_win,
        text="Update Stock",
        command=save_stock
    ).pack(pady=20)
    
def view_items():
    view_win=tk.Toplevel(root)
    view_win.title("select an item")
    view_win.geometry("600x300")
    tk.Label(view_win,text="Available items:",font=("Arial",11)).pack(pady=11)
    cursor.execute("select Items from items")
    data = [row[0] for row in cursor.fetchall()]
    dropdown=ttk.Combobox(view_win,values=data,state='readonly',width=30)
    dropdown.pack(pady=10)
    qty_label=tk.Label(view_win,text='Enter the quantity you want to buy:',bg='light blue',fg='black')
    qty_label.pack()
    entry_qty = tk.Entry(view_win, width=30)
    entry_qty.pack(pady=5)
    def purchase():
        selected_text = dropdown.get()
        if not selected_text:
            messagebox.showwarning("Warning", "Please select a item first!")
            return

        qty = entry_qty.get()
        if not qty.isdigit():
            messagebox.showerror("Error", "Enter valid quantity")
            return
        qty = int(qty)
        cursor.execute("SELECT Item_code, Items, Price, Stock FROM items WHERE Items = %s", (selected_text,))
        item_data = cursor.fetchone()
        db_stock = int(item_data[2])
        db_price = float(item_data[3])
        db_code = item_data[0]
        db_name = item_data[1]
        
        if qty >db_stock:
          messagebox.showerror("Error", "Not enough stock")
          return

        cart_bill.append({ 
            'Item_code': db_code,
            'Item': db_name,
            'Price': db_price,
            'qty': qty
        })
        messagebox.showinfo("Success", f"{qty} {db_name} added to cart!")
    def show_bill():
            if not cart_bill:
                messagebox.showinfo("Info", "Cart is empty")
                return
            for item in cart_bill:
                insert_query = """
                    INSERT INTO bill (item_code, items, price, quantity) 
                    VALUES (%s, %s, %s, %s)
                """
                data_to_insert = (
                    item['Item_code'], 
                    item['Item'], 
                    item['Price'], 
                    item['qty']
                )
                cursor.execute(insert_query, data_to_insert)
                update_stock_query = """
                    UPDATE items 
                    SET Stock = Stock - %s 
                    WHERE Item_code = %s
                """
                cursor.execute(update_stock_query, (item['qty'], item['Item_code']))
            conn.commit()
            receipt_text = "============ RECEIPT ============\n\n"
            total_bill = 0
            
            for item in cart_bill:
                item_total = item['Price'] * item['qty']
                total_bill += item_total
                receipt_text += f"{item['Item']}"
                receipt_text += f"   {item['qty']} x {item['Price']:.2f} = {item_total:.2f}\n"
            
            receipt_text += "\n---------------------------------\n"
            receipt_text += f"TOTAL AMOUNT: rupees {total_bill:.2f}\n"
            receipt_text += "=================================\n"
            receipt_text += "Thank you for shopping with us!"

           
            messagebox.showinfo("Print Receipt", receipt_text)
            cart_bill.clear()
    tk.Button(view_win,text='Show Bill',command=show_bill,activebackground='blue').pack(pady=10)    
    tk.Button(view_win,text='Add to cart',command=purchase,activebackground='blue').pack(pady=10)
label_title=tk.Label(root,text='login',font=('Arial',20,'bold'),bg='light grey')
label_title.pack(pady=20)
frame = tk.Frame(root, bg="#f7f9fc")
frame.pack(pady=40)
tk.Label(frame,text='Usertype').grid(row=0,column=0,padx=10,pady=10)
entry_usertype=ttk.Entry(frame)
entry_usertype.grid(row=0,column=1,padx=10,pady=10)
tk.Label(frame,text='username',font=("Arial",10)).grid(row=1, column=0, padx=10, pady=10)
user_entry=ttk.Entry(frame)
user_entry.grid(row=1,column=1, padx=10, pady=10)
tk.Label(frame,text='password',font=("Arial",10)).grid(row=2, column=0, padx=10, pady=10)
pass_entry=ttk.Entry(frame,show="*")
pass_entry.grid(row=2, column=1, padx=10, pady=10)
ttk.Button(frame,text='Login',width=15,command=login).grid(row=3, column=0, columnspan=2, pady=20)
root.mainloop()
