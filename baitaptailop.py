import pandas as pd

# 1. Đọc file CSV (utf-8-sig để bỏ ký tự BOM ở đầu tên cột OrderID)
df = pd.read_csv("data2.csv", encoding="utf-8-sig")

# 2. 5 dòng đầu, kích thước, kiểu dữ liệu
print("=== 2. HEAD ===")
print(df.head())
print("\nSố dòng, số cột:", df.shape)
print("\nKiểu dữ liệu:")
print(df.dtypes)
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# 3. Dữ liệu thiếu
print("\n=== 3. DỮ LIỆU THIẾU ===")
print(df.isna().sum())

# 4. Chuẩn hóa chuỗi
df["Product"] = df["Product"].str.strip()
df["City"] = df["City"].str.strip()
print("\n=== 4. SAU KHI STRIP ===")
print("Sản phẩm:", sorted(df["Product"].unique()))
print("Thành phố:", sorted(df["City"].unique()))

# 5. Số lượng không hợp lệ: âm hoặc <= 0, và outlier theo IQR
print("\n=== 5. SỐ LƯỢNG KHÔNG HỢP LỆ ===")
neg = df[df["Quantity"] <= 0]
print("Số lượng <= 0:")
print(neg)

q = df["Quantity"].where(df["Quantity"] > 0)
q1, q3 = q.quantile(0.25), q.quantile(0.75)
iqr = q3 - q1
# Dùng 3*IQR (ngoại lệ cực đoan) thay vì 1.5*IQR: với tập chỉ 20 dòng,
# 1.5*IQR đánh dấu nhầm đơn 10 USB Drive là bất thường.
upper = q3 + 3 * iqr
print(f"\nIQR: Q1={q1}, Q3={q3}, ngưỡng trên={upper}")
out = df[df["Quantity"] > upper]
print("Số lượng bất thường (quá lớn):")
print(out)

# 6. Xử lý thiếu / không hợp lệ
# Đánh dấu giá trị sai là NaN rồi điền chung một cách
df.loc[df["Quantity"] <= 0, "Quantity"] = float("nan")
df.loc[df["Quantity"] > upper, "Quantity"] = float("nan")

# Quantity: median theo sản phẩm (bền với outlier), nếu sản phẩm không có dữ liệu thì dùng median toàn bộ
df["Quantity"] = df["Quantity"].fillna(df.groupby("Product")["Quantity"].transform("median"))
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())

# UnitPrice: median theo sản phẩm vì giá gắn với sản phẩm
df["UnitPrice"] = df["UnitPrice"].fillna(df.groupby("Product")["UnitPrice"].transform("median"))

print("\n=== 6. SAU KHI XỬ LÝ ===")
print(df.isna().sum())
print(df.loc[df["OrderID"].isin(["O011", "O012", "O013", "O016"]),
             ["OrderID", "Product", "Quantity", "UnitPrice"]])

# 7. Revenue
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# 8. Doanh thu theo sản phẩm
by_product = df.groupby("Product")["Revenue"].sum()
print("\n=== 8. DOANH THU THEO SẢN PHẨM ===")
print(by_product)

# 9. Thống kê theo thành phố
by_city = df.groupby("City")["Revenue"].agg(["sum", "mean", "count"]).rename(
    columns={"sum": "TongDoanhThu", "mean": "TrungBinhDon", "count": "SoDon"})
print("\n=== 9. THỐNG KÊ THEO THÀNH PHỐ ===")
print(by_city.sort_values("TongDoanhThu", ascending=False))

# 10. Sắp xếp giảm dần
ranked = by_product.sort_values(ascending=False)
print("\n=== 10. SẢN PHẨM THEO DOANH THU GIẢM DẦN ===")
print(ranked)

# 11. Xuất file
df.to_csv("sales_clean.csv", index=False, encoding="utf-8-sig")
print("\nĐã xuất sales_clean.csv")