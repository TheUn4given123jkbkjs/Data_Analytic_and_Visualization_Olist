# BỐI CẢNH NGHIỆP VỤ, QUẦN THỂ QUAN SÁT VÀ KHUNG GIẢ THUYẾT THỐNG KÊ (REVIEW_PROBLEM.MD)
## MÔN HỌC: DATA ANALYSIS AND VISUALIZATION (TDTU)

---

### 1. Bối cảnh Nghiệp vụ & Vấn đề Cốt lõi (Business Context & Core Problem)
* **Bối cảnh:** Ban Giám đốc nhận thấy doanh thu quý gần nhất có dấu hiệu chững lại dù ngân sách Marketing không đổi. Ban Giám đốc đặt nghi vấn tỷ lệ khách hàng quay lại mua hàng (Repeat Purchase Rate) đang sụt giảm mạnh và tỷ lệ rời bỏ (Churn Rate) tăng cao.
* **Mục tiêu của Data Analyst:** 
  1. Phân tích dữ liệu ở cấp độ định danh cá nhân thực tế (`customer_unique_id`).
  2. Thực hiện Phân tích Mô tả (Descriptive Analytics) và Phân tích Chẩn đoán (Diagnostic Analytics) để giải mã nguyên nhân gốc rễ dẫn đến tỷ lệ mua 1 lần lên tới 97.02%.
  3. Xây dựng Phân tích Dự đoán (Predictive Analytics) bằng mô hình Machine Learning được huấn luyện trên toàn bộ quần thể khách hàng để dự đoán xác suất Churn ($P(\text{Churn})$) với tiêu chí tối ưu hóa **RECALL ($\ge 85\%$)**.
  4. Thực hiện Phân tích Chỉ định (Prescriptive Analytics) bằng mô hình Phân cụm Hành vi (K-Means Clustering) trên tệp **"Còn cứu được"** (Winnable At-Risk Segment) để đề xuất phương án tái phân bổ ngân sách Marketing.

---

### 2. Quần thể Quan sát & Đơn vị Phân tích (Population of Interest & Unit of Analysis)
* **Quần thể Quan sát (Population $N$):** Toàn bộ $N = 92,077$ khách hàng có phát sinh giao dịch giao hàng thành công — xác định qua trạng thái đơn hàng `order_status = 'delivered'` trên tập dữ liệu Olist.
* **Đơn vị Phân tích (Unit of Analysis):** `customer_unique_id` (Mã định danh từng cá nhân thực tế, gom nhóm toàn bộ đơn hàng của cùng 1 người).

---

### 3. Định nghĩa Thống kê & Ngưỡng Quan sát (Operational Definitions)
* **Tệp Mua 1 lần (One-time Buyers):** Khách hàng có tần suất mua $F = 1$ đơn hàng.
* **Tệp Mua lặp (Repeat Buyers):** Khách hàng có tần suất mua $F \ge 2$ đơn hàng.
* **Hành vi Churn ($N \ge 90$ ngày):** Một khách hàng được coi là Churn nếu không phát sinh đơn hàng `delivered` nào tiếp theo trong khoảng thời gian $N \ge 90$ ngày tính từ lần mua gần nhất đến mốc chốt dữ liệu (Max Date: `2018-08-29`).
* **Tệp "Còn cứu được" (Winnable At-Risk Segment):** Khách hàng thoả mãn đồng thời 3 điều kiện:
  1. Recency chớm dừng mua trong 3–6 tháng ($90 \le R \le 180$ ngày).
  2. Chi tiêu tích lũy cao ($\text{Total Spent} \ge \text{Median}$ R\$ 89.90).
  3. Mức độ hài lòng trong quá khứ cao ($\text{Review Score} \ge 4.0$ sao).

---

### 4. Khung Phát biểu Giả thuyết Thống kê Chính thức ($H_0$ vs $H_a$)
Để đảm bảo tính chặt chẽ về mặt học thuật (TDTU Chapter 5 & 6), tất cả các phân tích chẩn đoán sẽ tiến hành kiểm định các bộ Giả thuyết Thống kê sau với mức ý nghĩa $\alpha = 0.05$:

#### 🔹 Bộ Giả thuyết 1: Gánh nặng Phí vận chuyển (`freight_ratio`)
* **$H_{01}$ (Giả thuyết Không):** Không có sự khác biệt có ý nghĩa thống kê về tỷ lệ phí ship/giá sản phẩm giữa nhóm khách mua 1 lần và nhóm khách mua lặp lại ($\mu_1 = \mu_2$).
* **$H_{a1}$ (Giả thuyết Đối):** Tỷ lệ phí ship/giá sản phẩm của nhóm khách mua 1 lần cao hơn nhóm khách mua lặp lại có ý nghĩa thống kê ($\mu_1 > \mu_2$).

#### 🔹 Bộ Giả thuyết 2: Trải nghiệm Giao hàng Trễ (`is_late`)
* **$H_{02}$ (Giả thuyết Không):** Tỷ lệ giao hàng trễ so với cam kết ở nhóm khách mua 1 lần không khác biệt so với nhóm mua lặp lại ($p_1 = p_2$).
* **$H_{a2}$ (Giả thuyết Đối):** Tỷ lệ giao hàng trễ ở nhóm khách mua 1 lần cao hơn nhóm mua lặp lại có ý nghĩa thống kê ($p_1 > p_2$).

#### 🔹 Bộ Giả thuyết 3: Mức độ Hài lòng & Khoảng trống Kích hoạt (`review_score`)
* **$H_{03}$ (Giả thuyết Không):** Mức độ hài lòng (`review_score`) của nhóm khách mua 1 lần thấp hơn đáng kể so với nhóm mua lặp ($Review_1 < Review_2$).
* **$H_{a3}$ (Giả thuyết Đối):** Nhóm mua 1 lần vẫn có điểm hài lòng cao ($Review \ge 4.0$) nhưng ngưng mua do thiếu chiến dịch giữ chân/nhắc nhở tự động (Reactivation Gap).

#### 🔹 Bộ Giả thuyết 4: Chu kỳ Mua lại Thực tế (`interval_days`)
* **$H_{04}$ (Giả thuyết Không):** Phân bố chu kỳ mua lại bị chi phối bởi các đơn hàng cùng phiên sắm ($Interval < 1$ ngày).
* **$H_{a4}$ (Giả thuyết Đối):** Sau khi loại bỏ nhiễu đơn cùng phiên ($Interval \ge 1$ ngày), chu kỳ mua lại thực tế của khách hàng tập trung trong khoảng $3 - 6$ tháng ($90 \le R \le 180$ ngày).

---

### 5. Metadata Bộ Dữ liệu Olist (52 Cột / 9 Bảng CSV)
Tập dữ liệu **Brazilian E-Commerce Public Dataset by Olist** gồm 9 bảng CSV nối với nhau qua các khóa chính/khóa ngoại:
1. `olist_customers_dataset.csv` (5 cột): `customer_id`, `customer_unique_id`, bưu chính, thành phố, bang.
2. `olist_orders_dataset.csv` (8 cột): `order_id`, `customer_id`, `order_status`, các mốc thời gian (purchase, approved, delivered, estimated).
3. `olist_order_items_dataset.csv` (7 cột): `order_id`, `order_item_id`, `product_id`, `seller_id`, `price`, `freight_value`.
4. `olist_order_payments_dataset.csv` (5 cột): `payment_type`, `payment_installments`, `payment_value`.
5. `olist_order_reviews_dataset.csv` (7 cột): `review_id`, `order_id`, `review_score`, `review_comment_message`.
6. `olist_products_dataset.csv` (9 cột): `product_id`, `product_category_name`, kích thước, cân nặng.
7. `olist_sellers_dataset.csv` (4 cột): `seller_id`, bưu chính, thành phố, bang.
8. `product_category_name_translation.csv` (2 cột): Dịch danh mục Portuguese $\rightarrow$ English.
9. `olist_geolocation_dataset.csv` (5 cột): Tọa độ địa lý mã bưu chính.

---

### 6. Khung Câu hỏi Phân tích 4 Cấp độ (Data-Driven Analytics Questions)
1. **Descriptive:** Tỷ lệ mua 1 lần, mua lặp lại và Churn Rate thực tế trên toàn bộ $N = 92,077$ khách hàng là bao nhiêu? Giá trị AOV và doanh thu theo tháng biến động ra sao?
2. **Diagnostic:** Có sự khác biệt có ý nghĩa thống kê nào ($\alpha = 0.05$) giữa nhóm mua 1 lần và mua lặp lại về thời gian giao trễ, phí ship, điểm review score, và chu kỳ mua lại hay không?
3. **Predictive:** Yếu tố nào ảnh hưởng mạnh nhất đến xác suất Churn của khách hàng? Mô hình Advanced (XGBoost + SMOTE) đạt chỉ số Recall và ROC-AUC là bao nhiêu khi dự đoán Churn trên toàn bộ quần thể?
4. **Prescriptive:** Cụm khách hàng "Còn cứu được" (7,629 khách) có những đặc trưng hành vi nào khi phân cụm bằng K-Means? Cần đề xuất tái phân bổ ngân sách Marketing cụ thể như thế nào để tối ưu hóa ROI và doanh thu khôi phục kỳ vọng?
