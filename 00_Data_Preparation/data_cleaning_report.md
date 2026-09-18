# BÁO CÁO TIỀN XỬ LÝ & LÀM SẠCH DỮ LIỆU HỌC THUẬT (DATA CLEANING REPORT)
## PHÂN RÃ CẤU TRÚC ĐỊNH DANH, CHIẾN LƯỢC XỬ LÝ MISSING VALUE & BẢO TOÀN DỮ LIỆU GỐC
---

### 1. NGUYÊN TẮC BẤT BIẾN CỦA DỮ LIỆU GỐC (RAW DATA IMMUTABILITY)

Theo quy chuẩn kỹ thuật dữ liệu học thuật và thực tiễn doanh nghiệp:
* **Dữ liệu thô ban đầu (Raw Data - 8 tệp `olist_*.csv`):** Đóng vai trò là "Nguồn sự thật duy nhất" (*Single Source of Truth*).
* **Cam kết kỹ thuật:**
  1. Tuyệt đối **KHÔNG BAO GIỜ** sửa đổi, ghi đè hay xóa trực tiếp trên các tệp dữ liệu gốc.
  2. Mọi thao tác làm sạch được thực hiện trên bản sao bộ nhớ RAM (`df.copy()`).
  3. Kết quả làm sạch được xuất ra thư mục riêng (`fix/data/cleaned/clean_*.csv`) để phục vụ các bước phân tích tiếp theo mà không làm ảnh hưởng đến dữ liệu nguồn.

---

### 2. PHÂN RÃ ĐỊNH DANH KHÁCH HÀNG: `customer_id` (99k+) vs `customer_unique_id` (96k+) vs `delivered` (92,077)

Nhằm giải đáp chi tiết thắc mắc của Giảng viên về sự thay đổi của các con số qua từng bước:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. DỮ LIỆU GỐC BAN ĐẦU: 99,441 dòng 'customer_id'                                     │
│    └─ Bản chất: Mã phiên đặt hàng (Order Session Key). Mỗi đơn hàng sinh ra 1 ID mới.  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ (Gom nhóm theo mã căn cước khách hàng thực tế)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 2. KHÁCH HÀNG THỰC TẾ DUY NHẤT: 96,096 cá nhân 'customer_unique_id'                    │
│    └─ Chênh lệch 3,345 phiên phát sinh từ khách hàng mua lặp lại (Repeat Customers).  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ (Lọc đơn hàng hoàn tất chu trình 'delivered' = 95,137 đơn)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 3. QUẦN THỂ NGHIÊN CỨU HÀNH VI CHUẨN XÁC: N = 92,077 KHÁCH HÀNG DUY NHẤT               │
│    ├─ 89,333 khách hàng chỉ mua 1 lần (97.02%)                                         │
│    └─ 2,744 khách hàng mua lặp lại ≥ 2 lần (2.98%)                                     │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 📌 Vì sao bắt buộc phải dùng quần thể $N = 92,077$ khách hàng?
1. Để phân tích các chỉ số hành vi cốt lõi như: *Thời gian giao hàng thực tế (`delivery_time_days`), Điểm đánh giá trải nghiệm (`review_score`), Chu kỳ mua lặp lại (`repeat_interval_days`), Tỷ lệ rời bỏ (`Churn`)*, khách hàng bắt buộc phải **đã nhận được hàng thành công (`order_status == 'delivered'`)**.
2. Các đơn hàng có trạng thái `shipped`, `processing`, `invoiced` hoặc `canceled` chưa có mốc thời gian nhận hàng thực tế (`order_delivered_customer_date`), nếu đưa vào tính toán sẽ gây méo mó sai lệch các phân phối thống kê.
3. Gom nhóm $95,137$ đơn hàng `delivered` theo `customer_unique_id`, ta thu được đúng **$92,077$ khách hàng duy nhất**, đảm bảo tính đồng bộ $100\%$ từ Bước 1 (Mô tả), Bước 2 (Chẩn đoán) đến Bước 3 (Dự báo Train $67,678$ + Test $24,399 = 92,077$).

---

### 3. CHIẾN LƯỢC XỬ LÝ GIÁ TRỊ KHUYẾT (MISSING VALUES) THEO BẢN CHẤT DỮ LIỆU

Việc xử lý giá trị khuyết (Null) được chia làm 3 nhóm giải pháp riêng biệt, không áp dụng cào bằng:

| Nhóm Dữ liệu Khuyết | Trường Thông tin | Số lượng Null | Bản chất Nghiệp vụ | Chiến lược Xử lý | Rationale (Lý do Khoa học) |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **1. Null Hợp lệ / Thông tin** | `review_comment_title`<br>`review_comment_message` | $88,285$<br>$58,247$ | Khách hàng chỉ chấm điểm sao (1-5 sao) mà không gõ bình luận chữ. | **Điền chuỗi rỗng `""` (Impute Empty)** | **Tuyệt đối không drop dòng.** Điểm sao (`review_score`) vẫn đầy đủ $100\%$, nếu drop sẽ làm mất oan hàng chục nghìn review quý giá. |
| **1. Null Hợp lệ / Thông tin** | `order_delivered_customer_date` (ở đơn chưa giao) | $2,957$ | Đơn hàng đang vận chuyển (`shipped`, `processing`...), chưa giao tới tay khách. | **GIỮ NGUYÊN NULL trong bảng `orders`** | Đơn hàng đang vận hành bình thường, không phải lỗi hệ thống. |
| **2. Null Thuộc tính Sản phẩm** | `product_category_name` | $610$ | Người bán chưa gán danh mục cho sản phẩm. | **Điền nhãn `"unknown"`** | Giữ sản phẩm trong hệ thống để bảo toàn doanh thu đơn hàng. |
| **2. Null Thuộc tính Sản phẩm** | `product_weight_g`<br>Kích thước dài/rộng/cao | $2$ sp | Thiếu thông số vật lý của 2 sản phẩm. | **Điền Trung vị theo Ngành (`groupby(category).median()`)** | Bảo toàn phân phối trọng lượng riêng của từng ngành hàng (*Domain-Specific Imputation*). |
| **3. Null Mâu thuẫn Logic** | `order_delivered_customer_date` (khi `status='delivered'`) | **$8$ đơn** | Hệ thống báo đã giao thành công nhưng trường ngày giao lại rỗng. | **BẮT BUỘC DROP (8 dòng)** | Không thể tự suy đoán ngày nhận hàng thực tế, loại bỏ để tránh sai lệch thời gian giao hàng. |

---

### 4. BẢO ĐẢM TOÀN VẸN THAM CHIẾU (REFERENTIAL INTEGRITY) & KHÓA NGOẠI MỒ CÔI

* **Loại bỏ Khóa ngoại Mồ côi (Orphan Foreign Keys):**
  * Các dòng trong bảng con (`order_items`, `payments`) tham chiếu đến `order_id` không tồn tại trong bảng cha `orders` (do đơn hàng lỗi từ hệ thống nguồn) được lọc bỏ để tránh lỗi liên kết khi `JOIN`.
* **Bảo tồn Người bán chưa phát sinh đơn hàng:**
  * Toàn bộ **$211$ sellers** chưa có đơn hàng trong `order_items` **được giữ nguyên $100\%$**, vì đây là các đối tác mới lên sàn, không phải dữ liệu rác.

---

### 5. XỬ LÝ NGOẠI LAI THỐNG KÊ (CONSERVATIVE OUTLIER TREATMENT VIA IQR $k = 3.0$)

Theo lý thuyết phân phối xác suất (TDTU Chapter 3 & 4):
$$\text{Lower Bound} = Q_1 - 3.0 \times \text{IQR}, \quad \text{Upper Bound} = Q_3 + 3.0 \times \text{IQR}$$

* **Lý do chọn $k = 3.0$ (Bảo thủ - Conservative):**
  * Nếu dùng $k = 1.5$ thông thường, ta sẽ vô tình xóa bỏ các đơn hàng giá trị cao ($1,000 - 3,000\text{ BRL}$) của khách hàng VIP (doanh thu cốt lõi).
  * Với $k = 3.0$, mô hình **chỉ loại bỏ các điểm dị biệt phi thực tế** (ví dụ đơn hàng lỗi nhập liệu hoặc thời gian giao hàng kéo dài hàng trăm ngày do thất lạc bưu cục).

---

### 6. BẢNG TỔNG KẾT KIỂM TOÁN LÀM SẠCH DỮ LIỆU (DATA CLEANING AUDIT)

| Bảng Dữ liệu | Số Dòng Gốc (Raw) | Số Dòng Sau Làm Sạch (Cleaned) | Số Dòng Bị Loại | Tỷ lệ Loại Bỏ (%) | Tỷ lệ Bảo Tồn (%) | Đánh giá Học thuật |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`customers`** | **99,441** | **99,441** | **0** | **0.00%** | **100.00%** | **Bảo tồn nguyên vẹn $100\%$** |
| **`products`** | **32,951** | **32,951** | **0** | **0.00%** | **100.00%** | **Bảo tồn nguyên vẹn $100\%$** |
| **`sellers`** | **3,095** | **3,095** | **0** | **0.00%** | **100.00%** | **Bảo tồn nguyên vẹn $100\%$** (Giữ cả 211 seller mới) |
| **`reviews`** | **99,224** | **98,673** | **551** | **0.56%** | **99.44%** | Khử trùng lặp, giữ review mới nhất mỗi đơn |
| **`orders`** | **99,441** | **98,100** | **1,341** | **1.35%** | **98.65%** | Loại bỏ mâu thuẫn ngày giao và outlier giao hàng |
| **`payments`** | **103,886** | **102,460** | **1,426** | **1.37%** | **98.63%** | Đồng bộ khóa ngoại theo các đơn orders hợp lệ |
| **`order_items`**| **112,650** | **102,219** | **10,431** | **9.26%** | **90.74%** | Lọc theo đơn cha và khử giá/phí ship bất thường |

---

### 7. KẾT LUẬN CHUYÊN MÔN
1. Dữ liệu gốc được bảo tồn gần như trọn vẹn ($> 98.65\%$ ở hầu hết các bảng).
2. Mọi quyết định loại bỏ dòng hay điền khuyết đều có căn cứ lý thuyết thống kê và nghiệp vụ E-commerce rõ ràng, minh bạch.
3. Toàn bộ 7 bảng sạch `clean_*.csv` đã được đồng bộ chuẩn xác làm đầu vào cho toàn bộ chuỗi phân tích tiếp theo.
