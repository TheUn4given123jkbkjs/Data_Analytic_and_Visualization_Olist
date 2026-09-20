# Olist Churn Dashboard

Dashboard Streamlit cho đề tài **Dự đoán rời bỏ khách hàng (Churn) trên sàn TMĐT Olist**.

## Cấu trúc thư mục

```
dashboard/
├── app.py                 # File chạy chính (streamlit run app.py)
├── charts_config.py       # Khai báo metadata cho toàn bộ biểu đồ EDA (data-driven)
├── requirements.txt
├── assets/                # Ảnh biểu đồ hiện có (phần Mô tả dữ liệu)
└── core/
    ├── data_scaler.py     # Chuẩn hóa dữ liệu thành 33 đặc trưng chuẩn
    └── model_helper.py    # Dự đoán, giải thích SHAP, đề xuất, mô phỏng ROI
```

## Cách chạy

```bash
cd dashboard
pip install -r requirements.txt
streamlit run 05_Dashboard\app.py
```

## Trạng thái hiện tại (3 tab)

| Tab | Nội dung | Trạng thái |
|---|---|---|
| 1. Mô tả Dữ liệu (EDA) | 9 biểu đồ, chia 4 nhóm chủ đề | ✅ Hoàn chỉnh |
| 2. Phân tích Chẩn đoán | 12 biểu đồ, chia 6 "Yếu tố tác động churn" (giao trễ, phí ship, ngày trễ, review xấu, ngành hàng, vùng địa lý) + bảng tổng kết khuyến nghị đặc trưng cho mô hình | ✅ Hoàn chỉnh |
| 3. Dự đoán Churn & Đề xuất | 7 biểu đồ mô hình (chuẩn bị dữ liệu, baseline, so sánh baseline vs advanced, SHAP) + form dự đoán tương tác wiring tới `core/model_helper.py` | ✅ Biểu đồ hoàn chỉnh · Form chạy được khi có đủ model artifacts |

## Để Tab 3 (Dự đoán) chạy được đầy đủ

`core/model_helper.py` cần các file theo đường dẫn mặc định (tương đối so với `core/`):

- `../03_Predictive/models/advanced/best_run/best_model.pkl`
- `../03_Predictive/models/feature_columns.json`
- `../03_Predictive/data/train_test/X_train.csv` (dùng để fit scaler nếu bật `scale=True`)

Nếu artifacts model đặt ở nơi khác, sửa `model_dir` khi khởi tạo `OlistCustomerPredictor(model_dir=...)`
trong `app.py`.

## Yêu cầu về so sánh mô hình (baseline vs nâng cao)

Phần này cần bổ sung khi có kết quả huấn luyện: nên hiển thị ít nhất 2 mô hình
(ví dụ Logistic Regression làm baseline, và một mô hình cây/ensemble như
XGBoost/LightGBM/Random Forest làm mô hình nâng cao), kèm bảng so sánh chỉ số
(Accuracy, Precision, Recall, F1, AUC) và biểu đồ ROC/Confusion Matrix tương ứng —
có thể thêm vào Tab 3 dưới dạng một `st.tabs(["Baseline", "Advanced", "So sánh"])` con.
