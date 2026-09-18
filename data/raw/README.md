# THƯ MỤC DỮ LIỆU GỐC (RAW DATA) - OLIST E-COMMERCE

Bộ dữ liệu gốc từ Kaggle (Brazilian E-Commerce Public Dataset by Olist) gồm 8 bảng dữ liệu quan hệ:
1. `olist_customers_dataset.csv`
2. `olist_orders_dataset.csv`
3. `olist_order_items_dataset.csv`
4. `olist_order_payments_dataset.csv`
5. `olist_order_reviews_dataset.csv`
6. `olist_products_dataset.csv`
7. `olist_sellers_dataset.csv`
8. `olist_geolocation_dataset.csv`

Toàn bộ quy trình làm sạch (Xử lý null, chuẩn hóa kiểu datetime, loại bỏ đơn hủy/trùng lặp) được thực thi bởi notebook:
`fix/00_Data_Preparation/Data_Cleaning.ipynb`

Dữ liệu sạch đầu ra được lưu tại:
`fix/data/cleaned/` (gồm 7 bảng sạch đã loại bỏ nhiễu).
