import pandas as pd
import numpy as np

# 1. doc file csv (utf-8-sig de bo ky tu BOM o dau file)
df = pd.read_csv("data2.csv", encoding="utf-8-sig")

# 2. xem du lieu tong quan
# xem 5 dong dau tien
print(df.head())

# xem 5 dong cuoi cung
print(df.tail())

# xem kich thuoc du lieu (so dong, so cot)
print(df.shape)

# xem ten cot
print(df.columns)

# xem thong tin tong quat
df.info()

# xem kieu du lieu
print(df.dtypes)
print(df.describe())

# chuyen OrderDate tu chuoi sang kieu ngay
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# 3. phat hien du lieu bi thieu
print(df.isna().sum())
print("Tong so o bi thieu: ", df.isna().sum().sum())

# loc cac dong bi thieu
missing_row = df[df.isna().any(axis=1)]
print(missing_row)

# 4. chuan hoa du lieu (xoa khoang trang thua)
df["Product"] = df["Product"].str.strip()
df["City"] = df["City"].str.strip()
print(df["Product"].unique())
print(df["City"].unique())

# kiem tra du lieu bi trung lap
print(df.duplicated().sum())
print(df[df.duplicated(subset=["OrderID"], keep=False)])

# 5. phat hien du lieu sai - du lieu bat thuong
'''
So luong ban (Quantity): 1 - 100
Don gia (UnitPrice): > 0
'''
invalid_quantity = df[
    ((df["Quantity"] < 1) | (df["Quantity"] > 100))
]
print(invalid_quantity)

invalid_price = df[df["UnitPrice"] <= 0]
print(invalid_price)

# lam sach du lieu bi sai: chuyen ve NaN de xu ly chung voi du lieu thieu
df.loc[
    (df["Quantity"] < 1) | (df["Quantity"] > 100), "Quantity"
] = np.nan

df.loc[df["UnitPrice"] <= 0, "UnitPrice"] = np.nan

print(df.isna().sum())

# 6. xu ly du lieu bi thieu
# neu xoa dong (dropna) se mat 4 don hang -> khong xoa vi chi co 20 dong
df_drop = df.dropna()
print(df_drop.shape)

# dien bang median CUA TUNG SAN PHAM:
# - median khong bi keo lech boi gia tri cuc doan nhu mean
# - don gia gan voi san pham (Keyboard luon 650000), nen dien theo san pham
#   chinh xac hon dien theo ca cot (se gan gia laptop cho ban phim)
df["Quantity"] = df["Quantity"].fillna(
    df.groupby("Product")["Quantity"].transform("median")
)
df["UnitPrice"] = df["UnitPrice"].fillna(
    df.groupby("Product")["UnitPrice"].transform("median")
)

# kiem tra lai
print(df.isna().sum())

# 7. tao cot Revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]
print(df)

# 8. tong doanh thu theo tung san pham
revenue_by_product = df.groupby("Product")["Revenue"].sum()
print(revenue_by_product)

# 9. thong ke doanh thu theo tung thanh pho
revenue_by_city = df.groupby("City")["Revenue"].agg(["sum", "mean", "count"])
print(revenue_by_city)

# 10. sap xep san pham theo doanh thu giam dan
product_sorted = revenue_by_product.sort_values(ascending=False)
print(product_sorted)

# thong ke tong quan
print("Tong doanh thu: ", df["Revenue"].sum())
print("San pham doanh thu cao nhat: ", product_sorted.idxmax())
print("San pham doanh thu thap nhat: ", product_sorted.idxmin())
print("Thanh pho doanh thu cao nhat: ", revenue_by_city["sum"].idxmax())

# 11. xuat du lieu sau khi xu ly
df.to_csv("sales_clean.csv", index=False, encoding="utf-8-sig")