# DASHBOARD INTEGRATION API REFERENCE

Tài liệu API và hướng dẫn cài đặt các module hỗ trợ tích hợp mô hình vào Dashboard.

---

## 1. Cài đặt Thư viện
```bash
pip install streamlit xgboost shap joblib plotly scikit-learn
```

---

## 2. API: `data_scaler.py` (Chuẩn hóa dữ liệu nạp Model)

Chuyển đổi dữ liệu nhập thô thành **DataFrame 33 cột chuẩn 100%** để đưa vào `model.predict_proba()`.

### Signature:
```python
from data_scaler import prepare_input

X = prepare_input(
    order_spent=150.0,                  # float: Giá trị đơn hàng (BRL)
    delivery_days=8.0,                  # float: Số ngày giao hàng thực tế
    estimated_delivery_days=15.0,       # float: Số ngày giao hàng dự kiến
    payment_type="credit_card",         # str: 'credit_card', 'boleto', 'voucher', 'debit_card'
    customer_state="SP",                # str: 'SP', 'RJ', 'MG', 'Sul', 'outros'
    product_category="beleza_saude",    # str: Tên danh mục sản phẩm
    review_score=5,                     # int: 1 đến 5 sao
    max_installments=3,                 # int: Số kỳ trả góp
    scale=False                         # bool: True nếu muốn chuẩn hóa Z-score
)
# Hoặc truyền dict / DataFrame: X = prepare_input(raw_dict_or_df)
```

### Returns:
* `pandas.DataFrame`: Shape `(1, 33)`, đúng 33 cột theo `feature_columns.json`.

---

## 3. API: `model_helper.py` (Dự báo, Giải thích & ROI)

### Khởi tạo:
```python
from model_helper import OlistCustomerPredictor

predictor = OlistCustomerPredictor()  # Tự động nạp model và feature columns
```

### Method 1: `predictor.predict_and_prescribe(**kwargs)`
Dự báo xác suất, phân tầng rủi ro, phân bổ tỷ trọng Pie Chart và đề xuất can thiệp.

* **Input:** Nhận các tham số tương tự `prepare_input` ở trên.
* **Returns:** `dict` chứa các trường sau:

| Key | Kiểu | Ý nghĩa / Giá trị mẫu |
| :--- | :--- | :--- |
| `prob_retain` | `float` | Xác suất giữ chân ($0.0 \to 1.0$) |
| `prob_retain_pct` | `str` | Chuỗi hiển thị (vd: `"21.86%"`) |
| `risk_tier` | `str` | Tên tầng rủi ro (Tier 1, Tier 2, Tier 3) |
| `tier_color` | `str` | Mã màu hex gợi ý cho UI (`#e63946`, `#f4a261`, `#2a9d8f`) |
| `can_intervene` | `bool` | `True` nếu thuộc Tier 2 (Cần can thiệp Marketing) |
| `pie_chart_data` | `DataFrame` | Cột `Nhóm Nguyên Nhân` & `Tỷ trọng (%)` để vẽ Pie Chart |
| `action_title` | `str` | Tên gói can thiệp Marketing đề xuất |
| `action_desc` | `str` | Mô tả chi tiết hành động |
| `action_channel` | `str` | Kênh triển khai tiếp thị |

---

### Method 2 (Static): `OlistCustomerPredictor.simulate_roi(...)`
Bộ tính toán bài toán kinh tế và ROI tiếp thị.

### Signature:
```python
roi = OlistCustomerPredictor.simulate_roi(
    target_customers=4124,     # Quy mô tệp khách hàng Tier 2
    cost_per_voucher=20.0,     # Chi phí voucher / tiếp thị mỗi khách (BRL)
    expected_uplift_pct=20.0,  # Tỷ lệ cứu vãn thành công kỳ vọng (%)
    avg_order_value=160.0,     # Giá trị đơn hàng trung bình (BRL)
    net_margin_pct=30.0,       # Biên lợi nhuận ròng (%)
    future_orders=1.5          # Số đơn mua thêm kỳ vọng trong 1 năm
)
```

### Returns: `dict`
* `total_cost`: Tổng ngân sách chiến dịch (BRL).
* `retained_customers`: Số khách hàng giữ chân thành công.
* `net_profit`: Lợi nhuận ròng thu về sau khi trừ chi phí (BRL).
* `roi_pct`: Tỷ suất hoàn vốn ROI (%).
* `is_profitable`: `True` nếu ROI > 0%.
