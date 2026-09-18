# KẾ HOẠCH TRIỂN KHAI PHÂN TÍCH CHỈ ĐỊNH VÀ TỐI ƯU HÓA TÀI CHÍNH (PRESCRIPTIVE ANALYTICS & ROI OPTIMIZATION)

Dự án Phân tích Dữ liệu Thương mại Điện tử Brazil (Olist E-Commerce)  
Giai đoạn 04: Prescriptive Analytics

---

## 1. TỔNG QUAN VÀ MỤC TIÊU CỐT LÕI

Phân tích Chỉ định (Prescriptive Analytics) là giai đoạn cao nhất trong chuỗi giá trị phân tích dữ liệu:
$$\text{Descriptive (Mô tả)} \longrightarrow \text{Diagnostic (Chẩn đoán)} \longrightarrow \text{Predictive (Dự báo)} \longrightarrow \mathbf{\text{Prescriptive (Chỉ định)}}$$

Mục tiêu cốt lõi của giai đoạn này là chuyển hóa các dự báo xác suất và nguyên nhân giải thích từ Mô hình AI (XGBoost + TreeSHAP ở Module 03) thành **chính sách hành động cụ thể, cá nhân hóa cho từng khách hàng và tối ưu hóa phân bổ ngân sách marketing nhằm tối đa hóa Lợi nhuận Ròng (Net Profit) và Tỷ suất Hoàn vốn (ROI)**.

---

## 2. NGUYÊN TẮC PHƯƠNG PHÁP LUẬN: ĐIỀU HÀNH DỰA HOÀN TOÀN TRÊN DỮ LIỆU (DATA-DRIVEN FRAMEWORK)

Để đảm bảo tính chặt chẽ về mặt khoa học dữ liệu và kinh tế học, toàn bộ quá trình xây dựng kế hoạch hành động phải tuân thủ nghiêm ngặt 3 nguyên tắc sau:

1. **Không giả định trước tỷ lệ hay chi phí cố định**: Toàn bộ chi phí can thiệp ($c_k$) và hành động tiếp thị phải được xác lập dựa trên các chỉ số tài chính thực tế trích xuất từ dữ liệu của từng nhóm khách hàng (giá trị đơn hàng trung bình $\text{AOV}_k$, cước phí vận chuyển thực tế $\text{Freight}_k$, số kỳ trả góp).
2. **Khảo sát phân bổ tỷ trọng % điểm nghẽn thực tế trước khi phân cụm**: Quét toàn diện tệp khách hàng mục tiêu Tier 2 (Savable Customers) để định lượng chính xác cơ cấu điểm nghẽn (tỷ lệ trễ hạn giao hàng, tỷ lệ đánh giá thấp, tỷ lệ áp lực thanh khoản).
3. **Đo lường mức tăng trưởng phản thực tế bằng chính mô hình AI (Counterfactual Simulation via XGBoost)**: Thay vì gán một tỷ lệ cứu vãn cảm tính, mô hình XGBoost sẽ được dùng để dự báo xác suất mới khi các điểm nghẽn được khắc phục:
   $$\Delta P_i = P(Y=1 \mid X_i^{\text{counterfactual}}) - P(Y=1 \mid X_i^{\text{original}})$$

---

## 3. CẤU TRÚC THƯ MỤC VÀ TÀI LIỆU DỰ KIẾN CỦA MODULE 04

```text
fix/
├── 04_Prescriptive/
│   ├── prescriptive_analysis_plan.md        <-- Kế hoạch phương pháp luận chi tiết (Tài liệu này)
│   ├── Prescriptive_Analysis.ipynb          <-- Notebook thực thi toàn bộ luồng phân tích và tối ưu hóa
│   ├── prescriptive_analysis_report.md      <-- Báo cáo học thuật toàn diện cho Ban Giám Đốc
│   ├── data/
│   │   └── prescriptive_action_plan.csv     <-- Bảng dữ liệu gán hành động và chi phí cho từng khách hàng
│   └── figures/
│       ├── executive_friction_distribution.png <-- Phân bố tỷ trọng % điểm nghẽn thực tế
│       ├── executive_budget_donut.png          <-- Phân bổ ngân sách tối ưu
│       ├── executive_profit_frontier.png       <-- Đường cong Ngân sách vs Lợi nhuận ròng
│       ├── executive_scenario_comparison.png   <-- So sánh 3 kịch bản kinh tế
│       └── executive_break_even_heatmap.png    <-- Ma trận trực quan ngưỡng hòa vốn
```

---

## 4. QUY TRÌNH THỰC HIỆN CHI TIẾT (6 BƯỚC CHUẨN MỰC)

### Bước 1: Trích Xuất Dữ Liệu và Thống Kê Phân Bổ Điểm Nghẽn Thực Tế (Data Ingestion & Empirical Profiling)
* Trích xuất tệp khách hàng Tier 2 (Savable Customers: $0.189 \le P(\text{Retain}) \le 0.450$) từ file `fix/03_Predictive/data/train_test/test_predictions.csv`.
* Đo lường và lập bảng phân bổ tỷ trọng % thực tế của 4 nhóm điểm nghẽn chính:
  1. **Điểm nghẽn Vận chuyển (Logistics Friction)**: Tỷ lệ % đơn hàng bị trễ hẹn giao (`delivery_delay > 0`), số ngày trễ trung bình, cước vận chuyển trung bình (`freight_value`).
  2. **Điểm nghẽn Tài chính & Trả góp (Financial Burden)**: Tỷ lệ % đơn hàng giá trị cao mua trả góp nhiều kỳ (`order_spent > 300` hoặc `max_installments >= 6`), mức chi trả bình quân mỗi kỳ.
  3. **Điểm nghẽn Đánh giá & Sự cố (Rating & Service Friction)**: Tỷ lệ % khách hàng đánh giá tiêu cực (`review_score <= 3`).
  4. **Điểm nghẽn Ngành hàng & Địa lý (Peripheral Category & Remote State)**: Tỷ lệ % khách hàng ở bang ngoại vi hoặc mua ngành hàng không cốt lõi.

---

### Bước 2: Phân Cụm Điểm Nghẽn Trải Nghiệm (XAI-Driven Friction Sub-Clustering)
* Sử dụng thuật toán `K-Means` trên ma trận điểm nghẽn chuẩn hóa để phân rã tệp Tier 2 thành các cụm chân dung hành vi cụ thể.
* Trích xuất các tham số kinh tế thực tế cho từng phân cụm $k$:
  * Quy mô khách hàng ($N_k$) và Tỷ trọng (% trong tệp Tier 2).
  * Giá trị đơn hàng trung bình của cụm ($\text{AOV}_k$).
  * Cước phí vận chuyển trung bình của cụm ($\text{Freight}_k$).
  * Số kỳ trả góp trung bình của cụm ($\text{Installments}_k$).
  * Xác suất giữ chân cơ sở bình quân ($P_{0, k}$).

---

### Bước 3: Thiết Kế Ma Trận Can Thiệp và Tính Toán Chi Phí Động (Dynamic Treatment & Cost Formulation)
Chi phí tiếp thị $c_k$ cho mỗi khách hàng thuộc cụm $k$ được tính toán trực tiếp từ chỉ số tài chính của chính cụm đó:

| Nhóm Điểm Nghẽn | Gói Can Thiệp Đề Xuất | Hành Động Điều Hành Cụ Thể | Công Thức Xác Lập Chi Phí ($c_k$) | Cơ Chế Phản Thực Tế (Counterfactual) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Sốc Logistics** | Gói Bồi Thường Trải Nghiệm (Experience Recovery) | Email/SMS xin lỗi từ CSKH + Voucher đền bù cước vận chuyển (Hạn 30 ngày) | $c_1 = \text{Freight}_1$ (hoặc $15\% \times \text{AOV}_1$) | Giả lập triệt tiêu trễ hạn (`delivery_delay -> 0`, chuẩn hóa `delivery_speed_ratio`) |
| **2. Áp Lực Tài Chính** | Gói Kích Cầu Thanh Khoản (Financial Relief) | Hỗ trợ Lãi suất Trả góp 0% cho 10-12 kỳ + Đề xuất combo giảm áp lực giỏ hàng | $c_2 = 6\% \times \text{AOV}_2$ (Chi phí bù lãi suất cho ngân hàng) | Giả lập giảm áp lực trả góp tháng (`monthly_burden` giảm 50%) |
| **3. Đánh Giá Kém** | Gói Chăm Sóc & Đổi Trả (Service Resolution) | Đội ngũ CSKH liên hệ trực tiếp hỗ trợ kỹ thuật/đổi trả + Voucher thiện chí | $c_3 = 12\% \times \text{AOV}_3$ | Giả lập khôi phục niềm tin khách hàng (`review_score -> 5.0`) |
| **4. Ngành Ngoại Vi** | Gói Tái Tương Tác Ngành (Category Re-engagement) | Hệ thống cá nhân hóa đề xuất sản phẩm bổ trợ/tiêu hao định kỳ + Voucher kích hoạt | $c_4 = 8\% \times \text{AOV}_4$ | Giả lập kích hoạt ngành hàng cốt lõi |

---

### Bước 4: Mô Phỏng Phản Thực Tế Bằng AI (Counterfactual Uplift Simulation)
* Tạo lập ma trận đặc trưng phản thực tế $X^{\text{counterfactual}}$ sau khi đã can thiệp các điểm nghẽn tương ứng cho từng khách hàng.
* Nạp $X^{\text{counterfactual}}$ vào mô hình XGBoost tốt nhất (`best_model.pkl`) để tính toán mức tăng xác suất giữ chân cá nhân hóa:
  $$\Delta P_i = P(Y=1 \mid X_i^{\text{counterfactual}}) - P(Y=1 \mid X_i^{\text{original}})$$
* Tính toán Giá trị Vòng đời Kỳ vọng Tăng thêm ($\Delta \text{CLV}_i$):
  $$\Delta \text{CLV}_i = \Delta P_i \times \text{AOV}_i \times m \times f$$
  Trong đó:
  * $m = 30\%$: Biên lợi nhuận ròng của sàn thương mại điện tử.
  * $f = 1.5$: Số đơn hàng kỳ vọng khách mua thêm trong vòng 1 năm tiếp theo.

---

### Bước 5: Mô Hình Tối Ưu Hóa Phân Bổ Ngân Sách Tuyến Tính (Integer Linear Programming)
* Xác định Tổng Ngân Sách Tối Đa Toàn Tệp:
  $$B_{\max} = \sum_{i=1}^{N} c_i$$
* Thiết lập bài toán quy hoạch nguyên (Knapsack Optimization) để tối đa hóa Lợi nhuận Ròng:
  $$\max_{\{x_i\}} \sum_{i=1}^{N} x_i \cdot \left( \Delta \text{CLV}_i - c_i \right)$$
  Thỏa mãn ràng buộc ngân sách:
  $$\sum_{i=1}^{N} x_i \cdot c_i \le B \quad \text{với } x_i \in \{0, 1\}$$
* Giải bài toán tối ưu trên các mốc ngân sách điều hành: $25\% B_{\max}, 50\% B_{\max}, 75\% B_{\max}, 100\% B_{\max}$ và mốc Ngân Sách Tự Do Tối Ưu (Unconstrained Optimal Budget).

---

### Bước 6: Phân Tích Điểm Hòa Vốn và 3 Kịch Bản Điều Hành (Executive Break-Even & Scenario Analysis)
* **Tính toán Tỷ lệ Chuyển đổi Hòa vốn Lý thuyết ($U_{\text{break-even}}$)**:
  $$U_{\text{break-even}, k} = \frac{c_k}{\text{AOV}_k \times m \times f}$$
* **Lập bảng Ma trận 3 Kịch bản Thị trường**:
  1. **Kịch bản Bi quan (Pessimistic)**: Hiệu quả thực tế chỉ đạt $50\%$ mức tăng dự báo từ AI $\to$ Xác định giới hạn an toàn vốn và mức độ chịu lỗ.
  2. **Kịch bản Cơ sở (Base Case)**: Hiệu quả bám sát mức tăng $\Delta P_i$ từ mô phỏng XGBoost $\to$ Kỳ vọng lợi nhuận ròng và ROI chuẩn.
  3. **Kịch bản Lạc quan (Optimistic)**: Hiệu quả vượt $20\%$ dự báo nhờ phối hợp truyền thông đa kênh $\to$ Tiềm năng doanh thu tối đa.

---

## 5. DANH MỤC BIỂU ĐỒ TRỰC QUAN HÓA CHO CẤP QUẢN LÝ (5 EXECUTIVE CHARTS)

Toàn bộ biểu đồ trong báo cáo và notebook được chuẩn hóa theo phong cách quản trị kinh doanh trực quan, quen thuộc:

1. **Biểu đồ Cột Ngang Phân Bổ Điểm Nghẽn (`executive_friction_distribution.png`)**: Thể hiện quy mô số lượng khách hàng, tỷ lệ % và quy mô doanh thu của từng nhóm điểm nghẽn thực tế.
2. **Biểu đồ Tròn Donut Cơ Cấu Ngân Sách (`executive_budget_donut.png`)**: Tỷ trọng % ngân sách tối ưu phân bổ cho 4 gói can thiệp.
3. **Biểu đồ Đường Lũy Tiến Ngân Sách vs Lợi Nhuận (`executive_profit_frontier.png`)**: Đường cong thể hiện mối quan hệ giữa tổng chi phí đầu tư và lợi nhuận ròng thu về, xác định điểm bão hòa lợi nhuận biên.
4. **Biểu đồ Cột So Sánh 3 Kịch Bản (`executive_scenario_comparison.png`)**: So sánh trực quan Doanh thu, Chi phí, Lợi nhuận ròng giữa 3 kịch bản: Bi quan, Cơ sở, Lạc quan.
5. **Bảng Heatmap Điểm Hòa Vốn (`executive_break_even_heatmap.png`)**: Ma trận màu trực quan thể hiện ngưỡng tỷ lệ cứu vãn tối thiểu theo Chi phí Voucher và Giá trị Đơn hàng.

---

## 6. KẾ HOẠCH BÀN GIAO VÀ KIỂM CHỨNG (DELIVERABLES & VERIFICATION)

* File dữ liệu đầu ra: `fix/04_Prescriptive/data/prescriptive_action_plan.csv` chứa đầy đủ danh sách khách hàng Tier 2, phân cụm gán, chi phí can thiệp động $c_i$, xác suất gốc $P_0$, xác suất phản thực tế $P_{\text{new}}$ và quyết định cấp ngân sách $x_i$.
* Báo cáo toàn diện: `fix/04_Prescriptive/prescriptive_analysis_report.md` tuân thủ tuyệt đối văn phong học thuật, không sử dụng biểu tượng cảm xúc (emoji), đầy đủ công thức toán học và bảng số liệu phục vụ báo cáo hội đồng.
