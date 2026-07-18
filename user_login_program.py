import pandas as pd
users_df=pd.read_csv("users.csv")
print(users_df)
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
    print(f'welcome {name}')

    
