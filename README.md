# PHÂN TÍCH VÀ TRỰC QUAN HÓA DỮ LIỆU THƯƠNG MẠI ĐIỆN TỬ BRAZIL (OLIST E-COMMERCE)
## Tối Ưu Hóa Tỷ Lệ Giữ Chân Khách Hàng (Customer Retention Optimization)

---

## 1. TỔNG QUAN DỰ ÁN
Dự án tập trung giải quyết bài toán cốt lõi của sàn thương mại điện tử **Olist (Brazil)**:
* **Tỷ lệ khách hàng mua 1 lần rồi rời bỏ (Single-Purchase Rate):** Chiếm tới **$97.02\%$** ($89,333 / 92,077$ khách hàng), tỷ lệ mua lặp lại toàn vòng đời chỉ đạt **$2.98\%$** ($2,744$ khách hàng).
* **Tỷ lệ mua lại trong khung 90 ngày (90-day Retention Rate cho bài toán ML):** Cực kỳ khan hiếm, chỉ đạt **$1.48\%$** (dẫn đến tỷ lệ mất khách/churn trong 90 ngày lên tới **$98.52\%$**).

Bằng việc triển khai trọn vẹn chu trình phân tích chuẩn 4 bậc của Gartner:
1. **Descriptive Analytics (Mô tả):** Thực trạng hành vi mua hàng và chân dung khách hàng là gì?
2. **Diagnostic Analytics (Chẩn đoán):** Tại sao khách hàng rời bỏ sàn sau lần mua đầu tiên?
3. **Predictive Analytics (Dự báo):** Ai là người có tiềm năng giữ chân và xác suất quay lại là bao nhiêu?
4. **Prescriptive Analytics (Chỉ định):** Doanh nghiệp nên can thiệp bằng chính sách / ngân sách nào để tối đa hóa ROI?
5. **Interactive Dashboard:** Bảng điều khiển tích hợp suy luận thời gian thực và mô phỏng tài chính.

---

## 2. CẤU TRÚC THƯ MỤC DỰ ÁN (PROJECT ARCHITECTURE)

```text
Midterm/
├── requirements.txt                    # Danh sách toàn bộ thư viện cần thiết
├── README.md                           # Tài liệu hướng dẫn sử dụng tổng quan
│
├── 00_Data_Preparation/               # [BƯỚC 0] Tiền xử lý & Làm sạch dữ liệu
│   ├── raw/                            # 9 bảng dữ liệu thô gốc từ Olist
│   ├── cleaned/                        # 7 bảng dữ liệu sạch đã xử lý logic & quan hệ
│   ├── Data_Cleaning.ipynb             # Notebook thực thi làm sạch toàn diện
│   └── data_cleaning_report.md         # Báo cáo chi tiết phương pháp làm sạch
│
├── 01_Descriptive/                    # [BƯỚC 1] Phân tích Mô tả (Descriptive Analytics)
│   ├── assets/                         # Toàn bộ biểu đồ trực quan hóa EDA
│   ├── Descriptive_Analysis.ipynb      # Notebook phân tích doanh thu, AOV, Pareto, chu kỳ
│   └── descriptive_analysis_report.md  # Báo cáo phân tích mô tả
│
├── 02_Diagnostic/                     # [BƯỚC 2] Phân tích Chẩn đoán (Diagnostic Analytics)
│   ├── assets/                         # Toàn bộ biểu đồ phân tích tương quan & rủi ro
│   ├── Diagnostic_Analysis.ipynb       # Notebook bóc tách 6 nhân tố rủi ro dẫn đến Churn
│   └── diagnostic_analysis_report.md   # Báo cáo phân tích chẩn đoán chuyên sâu
│
├── 03_Predictive/                     # [BƯỚC 3] Phân tích Dự báo (Predictive Analytics)
│   ├── assets/                         # Biểu đồ ROC-PR curves, SHAP summary, phân bố thời gian
│   ├── data/train_test/                # Tập Train/Test phân chia theo Temporal Split (chống rò rỉ)
│   ├── models/                         # Scaler, Feature config và Mô hình ML đã huấn luyện
│   ├── 01_Feature_Engineering.ipynb    # Kỹ thuật tạo 33 đặc trưng (bao gồm 3 biến tương tác sâu)
│   ├── 02_Model_Baseline.ipynb         # Huấn luyện mô hình Baseline (Logistic Regression, 10 Runs)
│   ├── 03_Model_Advanced.ipynb         # Huấn luyện mô hình Advanced (XGBoost + SMOTE + TreeSHAP)
│   └── predictive_analysis_report.md   # Báo cáo phân tích hiệu năng mô hình
│
├── 04_Prescriptive/                   # [BƯỚC 4] Phân tích Chỉ định (Prescriptive Analytics)
│   ├── assets/                         # Biểu đồ phân bổ điểm nghẽn, ngân sách, hòa vốn
│   ├── data/                           # File kế hoạch hành động prescriptive_action_plan.csv
│   ├── Prescriptive_Analysis.ipynb     # Phân cụm 4 giải pháp can thiệp & Tối ưu hóa tài chính
│   └── prescriptive_analysis_report.md # Báo cáo kế hoạch hành động & kịch bản lợi nhuận
│
└── 05_Dashboard/                      # [BƯỚC 5] Bảng điều khiển Web Tương tác (Streamlit)
    ├── app.py                          # Ứng dụng Web Dashboard giao diện Dark Mode cao cấp
    ├── model_helper.py                 # Module nạp model, bóc tách SHAP và tính toán phân tầng
    ├── data_scaler.py                  # Module chuẩn hóa dữ liệu đầu vào người dùng
    ├── charts_config.py                # Cấu hình biểu đồ trực quan hóa Plotly
    └── README.md                       # Hướng dẫn chi tiết sử dụng Dashboard
```

---

## 3. HƯỚNG DẪN CÀI ĐẶT & CHẠY DỰ ÁN

### Bước 1: Clone Repository về máy
```bash
git clone https://github.com/TheUn4given123jkbkjs/Data_Analytic_and_Visualization_Olist.git
cd <THU_MUC_DU_AN>
```

### Bước 2: Tạo môi trường ảo & Cài đặt thư viện
Khuyến nghị sử dụng Python **3.10**, **3.11** hoặc **3.12**:
```bash
# Tạo môi trường ảo (Virtual Environment)
python -m venv .venv

# Kích hoạt môi trường:
# - Trên Windows:
.venv\Scripts\activate
# - Trên macOS/Linux:
source .venv/bin/activate

# Cài đặt toàn bộ thư viện phụ thuộc:
pip install -r requirements.txt
```

---

## 4. HƯỚNG DẪN THỰC THI TOÀN BỘ PIPELINE (END-TO-END)

Dự án được thiết kế theo dạng **Single Source of Truth** và **Zero Hardcoded Paths**. Người dùng có thể mở từng Notebook bằng VS Code / Jupyter Lab và bấm `Run All`, hoặc chạy theo thứ tự:

### 🔹 Thứ tự thực thi chuẩn:
1. **Làm sạch dữ liệu:**
   * Mở `00_Data_Preparation/Data_Cleaning.ipynb` $\to$ `Run All`.
   * *Kết quả:* Dữ liệu thô từ `00_Data_Preparation/raw/` được làm sạch và xuất ra `00_Data_Preparation/cleaned/`.
2. **Phân tích mô tả:**
   * Mở `01_Descriptive/Descriptive_Analysis.ipynb` $\to$ `Run All`.
   * *Kết quả:* Trực quan hóa toàn cảnh phân phối đơn hàng và chu kỳ mua lặp lại vào `01_Descriptive/assets/`.
3. **Phân tích chẩn đoán:**
   * Mở `02_Diagnostic/Diagnostic_Analysis.ipynb` $\to$ `Run All`.
   * *Kết quả:* Kiểm định thống kê 6 nhân tố rủi ro và xuất biểu đồ vào `02_Diagnostic/assets/`.
4. **Kỹ thuật đặc trưng & Huấn luyện mô hình:**
   * Chạy `03_Predictive/01_Feature_Engineering.ipynb` (Tạo tập train/test theo Temporal Split).
   * Chạy `03_Predictive/02_Model_Baseline.ipynb` (Huấn luyện Baseline Logistic Regression 10 Runs).
   * Chạy `03_Predictive/03_Model_Advanced.ipynb` (Huấn luyện Advanced XGBoost + TreeSHAP 10 Runs).
   * *Kết quả:* Lưu weights tốt nhất tại `03_Predictive/models/` và xuất `test_predictions.csv`.
5. **Phân tích chỉ định & Tối ưu ngân sách:**
   * Mở `04_Prescriptive/Prescriptive_Analysis.ipynb` $\to$ `Run All`.
   * *Kết quả:* Phân cụm 4 gói can thiệp và xuất ma trận hòa vốn vào `04_Prescriptive/assets/`.

---

## 5. KHỞI CHẠY BẢNG ĐIỀU KHIỂN TƯƠNG TÁC (STREAMLIT DASHBOARD)

Sau khi cài đặt thư viện, bạn có thể khởi chạy Dashboard ngay lập tức mà không cần huấn luyện lại mô hình (mô hình đã được đóng gói sẵn):

```bash
streamlit run 05_Dashboard/app.py
```

### Các tính năng nổi bật trên Dashboard:
* **Giao diện Giám đốc Điều hành (Executive Overview):** Theo dõi tổng doanh thu rủi ro, số lượng khách hàng phân tầng theo 4 Tầng Rủi ro (`Tier 1` đến `Tier 4`), cơ cấu ngân sách tối ưu và đường cong lợi nhuận biên.
* **Bộ Giả lập Khách hàng Thời gian Thực (Real-time Customer Predictor):** Nhập thông số đơn hàng bất kỳ (giá trị, số kỳ trả góp, thời gian giao hàng, điểm đánh giá, bang, ngành hàng) $\to$ Mô hình XGBoost & TreeSHAP lập tức bóc tách nguyên nhân rủi ro dưới dạng Biểu đồ Tròn và đề xuất Gói can thiệp phù hợp nhất.
* **Bộ Giả lập Tài chính Chiến lược (Strategic ROI Simulator):** Kéo thả số lượng khách hàng mục tiêu, chi phí voucher, tỷ lệ nâng nhấc (Uplift) và biên lợi nhuận để tính toán Doanh thu, Chi phí, Lợi nhuận ròng và ROI kỳ vọng.

---