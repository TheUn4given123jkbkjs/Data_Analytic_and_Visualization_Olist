# DASHBOARD INTEGRATION API REFERENCE

Tài liệu API và hướng dẫn chi tiết các module hỗ trợ tích hợp mô hình AI và thuật toán phân tích chỉ định vào Dashboard Streamlit.

---

## 1. Cài đặt Thư viện Phụ thuộc
Chạy lệnh sau tại terminal để cài đặt toàn bộ môi trường:
```bash
pip install -r requirement.txt
```

---

## 2. Module `data_scaler.py` (Tiền xử lý & Chuẩn hóa 33 Đặc trưng)

Chuyển đổi linh hoạt mọi nguồn dữ liệu nhập thô (từng Widget giao diện, Dictionary hoặc DataFrame) thành **DataFrame đúng 33 cột chuẩn 100%** theo cấu trúc huấn luyện `feature_columns.json`.

### 2.1. Signature hàm rút gọn: `prepare_input`
```python
from data_scaler import prepare_input

# Cách 1: Truyền trực tiếp từ các Widget giao diện Streamlit (Sliders / Selectboxes)
X = prepare_input(
    order_spent=150.0,                  # float: Tổng giá trị đơn hàng (BRL)
    delivery_days=8.0,                  # float: Số ngày giao hàng thực tế
    estimated_delivery_days=15.0,       # float: Số ngày giao hàng dự kiến
    payment_type="credit_card",         # str: 'credit_card', 'boleto', 'voucher', 'debit_card'
    customer_state="SP",                # str: 'SP', 'RJ', 'MG', 'Sul', 'outros'
    product_category="beleza_saude",    # str: Danh mục sản phẩm chuẩn hóa
    review_score=5,                     # int: Đánh giá từ 1 đến 5 sao
    max_installments=3,                 # int: Số kỳ trả góp
    scale=False                         # bool: True nếu muốn scale Z-Score (mặc định False cho Tree-based)
)

# Cách 2: Truyền Dictionary thô
raw_dict = {"order_spent": 350.0, "payment_type": "boleto", "delivery_days": 20.0, "customer_state": "RJ"}
X = prepare_input(raw_dict)

# Cách 3: Truyền toàn bộ DataFrame thô (Batch Processing)
X_batch = prepare_input(df_raw)
```

### 2.2. Trả về:
* `pandas.DataFrame`: Kích thước `(N, 33)`, tự động tính toán 4 biến tương tác phi tuyến (`delivery_delay`, `delivery_speed_ratio`, `monthly_installment_burden`, `is_b2b_profile`) và One-Hot Encoding cho Phương thức thanh toán, Bang (State) và Ngành hàng (Category).

---

## 3. Module `model_helper.py` (Dự báo, Giải thích XAI & Phân tích Chỉ định)

### 3.1. Khởi tạo đối tượng Predictor:
```python
from model_helper import OlistCustomerPredictor

predictor = OlistCustomerPredictor()  # Tự động nạp model XGBoost và TreeExplainer
```

---

### 3.2. Phương thức 1: `predictor.predict_and_prescribe(**kwargs)`
Dự báo xác suất giữ chân / rời bỏ, phân tầng rủi ro, phân bổ tỷ trọng SHAP theo 4 nhóm nguyên nhân và gán gói can thiệp kinh doanh chi tiết.

* **Input:** Nhận các tham số tương tự `prepare_input` hoặc `transform_input`.
* **Output:** `dict` chứa 12 trường dữ liệu chi tiết:

| Tên Trường (Key) | Kiểu Dữ Liệu | Ý Nghĩa / Giá Trị Mẫu |
| :--- | :--- | :--- |
| `transformed_features` | `DataFrame` | Bảng đặc trưng `(1, 33)` đã tiền xử lý để đưa vào model |
| `prob_retain` | `float` | Xác suất quay lại mua hàng ($0.0 \to 1.0$) |
| `prob_retain_pct` | `str` | Chuỗi hiển thị tỷ lệ giữ chân (vd: `"21.86%"`) |
| `prob_churn_pct` | `str` | Chuỗi hiển thị tỷ lệ rời bỏ (vd: `"78.14%"`) |
| `risk_tier` | `str` | Tên phân tầng rủi ro (`Tier 1`, `Tier 2`, `Tier 3`) |
| `tier_color` | `str` | Mã màu HEX hiển thị UI (`#e63946` Đỏ, `#f4a261` Cam, `#2a9d8f` Xanh) |
| `can_intervene` | `bool` | `True` nếu thuộc Tier 2 (Cần can thiệp Marketing), `False` nếu Tier 1 hoặc 3 |
| `pie_chart_data` | `DataFrame` | Bảng gồm `Nhóm Nguyên Nhân`, `Mức độ Tác động`, `Tỷ trọng (%)` để vẽ Donut/Pie Chart |
| `top_cause` | `str` | Tên nhóm nguyên nhân chiếm tỷ trọng tác động lớn nhất |
| `action_title` | `str` | Tiêu đề gói giải pháp can thiệp (Cụm 0, Cụm 1, Cụm 2, Cụm 3) |
| `action_desc` | `str` | Nội dung chính sách can thiệp chi tiết |
| `action_channel` | `str` | Kênh triển khai tiếp thị thực tế |
| `assigned_engine` | `str` | Luồng thực thi: Tier 2A (Cấp vốn) vs Tier 2B (Tự tài trợ) vs Không can thiệp |

---

### 3.3. Phương thức 2 (Static): `OlistCustomerPredictor.simulate_roi(...)`
Bộ công cụ giả lập bài toán tài chính & tỷ suất hoàn vốn ROI phục vụ tab Phân tích Kinh doanh tương tác.

#### Signature:
```python
roi_result = OlistCustomerPredictor.simulate_roi(
    target_customers=600,      # int: Quy mô tệp can thiệp (Mặc định 600 khách Tier 2A)
    cost_per_voucher=6.34,     # float: Chi phí voucher/incentive bình quân mỗi khách (BRL)
    expected_uplift_pct=25.0,  # float: Tỷ lệ cứu vãn thành công kỳ vọng (%)
    avg_order_value=140.0,     # float: Giá trị đơn hàng trung bình AOV (BRL)
    net_margin_pct=30.0,       # float: Biên lợi nhuận gộp ròng sàn (%)
    future_orders=1.5          # float: Số đơn hàng phát sinh thêm trong vòng 1 năm
)
```

#### Trả về (`dict`):
* `total_cost` (`float`): Tổng ngân sách thực chi (BRL).
* `retained_customers` (`float`): Số lượng khách hàng được giữ chân thành công.
* `total_retained_profit` (`float`): Tổng giá trị lợi nhuận kỳ vọng thu về từ tệp khách giữ chân (BRL).
* `net_profit` (`float`): Lợi nhuận ròng sau khi đã trừ toàn bộ chi phí vốn (BRL).
* `roi_pct` (`float`): Tỷ suất sinh lời hoàn vốn ROI (%).
* `is_profitable` (`bool`): Trạng thái chiến dịch có lãi (`True` nếu Lợi nhuận ròng > 0).

## 4. Sơ đồ cây 
```text
├── app.py                    # File chính khởi chạy giao diện Streamlit Dashboard
├── charts_config.py           # Cấu hình dữ liệu biểu đồ, hình ảnh & nhận xét cho 4 phân hệ
├── core/
│   ├── data_scaler.py         # Pipeline tiền xử lý & chuẩn hóa 33 đặc trưng
│   └── model_helper.py        # Module nạp model XGBoost, TreeSHAP & bài toán chỉ định
└── assets/                    # Thư mục lưu trữ biểu đồ và hình ảnh minh họa
```

## 5. Kiến trúc giao diện Apdative UI (Streamlit app.py)
### Architecture & Key Features (Giao Diện & Chức Năng Nổi Bật)

Giao diện `app.py` tích hợp hệ thống **Design System thông minh**, giải quyết triệt để lỗi mất chữ/chìm màu chữ khi chuyển đổi giữa Dark Mode và Light Mode:

1. **Biến CSS Động (`var(--st-color-text)`):** Tự động bắt mã màu chữ theo theme hệ thống Streamlit để đảm bảo độ tương phản 100%.
2. **Bộ Điều Chỉnh Tỷ Lệ Font Chữ (UI Scaling):** Tích hợp Radio Selector ở Sidebar cho phép chuyển đổi linh hoạt kích thước font giữa các mức `Chuẩn (1.0x)`, `Lớn (1.2x)`, và `Trình chiếu (1.4x)`.
3. **Bộ Giả Lập Tài Chính Kép (Dual-Engine Simulator):** Tích hợp hai luồng tính toán tài chính độc lập trên giao diện tương tác:
  * **Luồng Tier 2A (Khách VIP):** Tính toán điểm hòa vốn, ngân sách cấp trước và ROI từ chiến dịch Voucher trực tiếp.
  * **Luồng Tier 2B (Khách Nền Tảng):** Tính toán doanh số sinh ra từ cơ chế Min-Cart/Cross-selling tự tài trợ không tốn chi phí vốn.

  ---

## 6. Module `charts_config.py` (Cấu Hình Dữ Liệu & Giao Diện Biểu Đồ)

Module trung tâm đóng vai trò lưu trữ toàn bộ cấu hình hiển thị, tiêu đề, đường dẫn hình ảnh, chú thích trục và nội dung **Nhận xét Chiến lược & Bài học Nghiệp vụ (Strategic Insights)** cho 4 phân hệ của Dashboard.

### 4.1. Cấu trúc Quản lý Dữ liệu

`charts_config.py` phân tách dữ liệu thành 4 Dictionary chính tương ứng với 4 phân hệ chính:

* **`CHARTS_CONFIG`**: Quản lý các biểu đồ Phân tích Mô tả (Descriptive) gồm phân phối khách hàng, RFM, AOV và hành vi mua hàng.
* **`DIAGNOSTIC_CONFIG`**: Lưu trữ dữ liệu 6 giả thuyết kiểm định thống kê (Chi-Square, Mann-Whitney U) phục vụ Phân tích Chẩn đoán.
* **`MODEL_CONFIG`**: Cấu hình các số liệu so sánh hiệu năng kỹ thuật giữa mô hình Baseline (Logistic Regression) và Advanced (XGBoost).
* **`PRESCRIPTIVE_CONFIG`**: Quản lý hình ảnh và dữ liệu phân cụm K-Means, bài toán tối ưu ngân sách Knapsack ILP và matrix kiểm định rủi ro.

### 4.2. Khai báo Mẫu Dữ liệu (Structure Example)

```python
# Ví dụ cấu trúc khai báo biểu đồ trong charts_config.py
CHARTS_CONFIG = {
    "overview": {
        "tab_label": "Tổng Quan Tập Dữ Liệu",
        "charts": [
            {
                "title": "Phân Phối Tỷ Lệ Rời Bỏ (Churn) vs Giữ Chân (Retention)",
                "file": "01_churn_distribution.png",
                "x_label": "Trạng thái Khách hàng (Active / Churn)",
                "y_label": "Số lượng Khách hàng",
                "legend": "Phân loại theo quy định Churn >90 ngày",
                "img_scale": 0.85,
                "insight": "Tỷ lệ Churn ở mức 80.02% thể hiện đặc thù giao dịch đơn lẻ của sàn E-commerce. Cần tập trung ngân sách can thiệp vào nhóm khách hàng tiềm năng Tier 2."
            }
        ]
    }
}
```

### 4.3. Nguyên lý Tích hợp với `app.py`

Hàm `render_chart_group_sliding()` trong `app.py` sẽ nạp cấu hình từ `charts_config.py` để tự động render giao diện:
1. **Tìm kiếm Hình ảnh:** Hàm `find_image_path()` duyệt tìm tập tin ảnh trong `assets/` dựa trên tên file khai báo.
2. **Dynamic UI Rendering:** Tự động điều chỉnh kích thước ảnh (`img_scale`), hiển thị các nhãn chú thích (X/Y Labels) và render **Insight Card** chứa nhận xét chuyên sâu bằng HTML/CSS thích ứng.
