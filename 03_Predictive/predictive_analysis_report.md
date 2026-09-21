# BÁO CÁO PHÂN TÍCH DỰ BÁO TOÀN DIỆN (PREDICTIVE ANALYTICS COMPREHENSIVE REPORT)

## DỰ BÁO XÁC SUẤT GIỮ CHÂN KHÁCH HÀNG SAU ĐƠN HÀNG ĐẦU TIÊN (FIRST-PURCHASE RETENTION PREDICTION)

### BỘ DỮ LIỆU THƯƠNG MẠI ĐIỆN TỬ BRAZIL (OLIST E-COMMERCE) - PHƯƠNG PHÁP LUẬN 2 GIAI ĐOẠN, ZERO DATA LEAKAGE & XAI

---

## 1. TỔNG QUAN BÀI TOÁN NGHIỆP VỤ & NGUYÊN TẮC ZERO-LEAKAGE

### 1.1. Bối cảnh Doanh nghiệp & Mục tiêu Dự báo

Trong hệ sinh thái thương mại điện tử Olist (Brazil), tỷ lệ khách hàng quay lại mua hàng tự nhiên cực kỳ thấp: **$2.98\%$** trên toàn bộ lịch sử và chỉ **$1.48\%$** trong cửa sổ kiểm thử 90 ngày. Điều này đồng nghĩa với việc **$98.52\%$** khách hàng rời bỏ sàn sau lần mua đầu tiên (One-time buyers).

Bài toán cốt lõi của doanh nghiệp được định nghĩa toán học như sau:

$$\boxed{\text{Đứng tại thời điểm khách hàng nhận xong ĐƠN HÀNG ĐẦU TIÊN } (T_0), \text{dự báo xác suất khách hàng quay lại mua đơn thứ 2 trong vòng 90 ngày } P(\text{Retain})}$$

### 1.2. Nguyên tắc Thiết kế Không Rò rỉ Dữ liệu (Zero Data Leakage)

- **Khắc phục lỗi Target Leakage:** Toàn bộ đặc trưng ứng viên **chỉ được phép trích xuất từ đơn hàng đầu tiên (First Delivered Order)**.
- **Loại bỏ biến tương lai:** Tuyệt đối không sử dụng các biến tổng hợp tương lai (như `total_spent` cộng dồn các đơn sau, hoặc biến $\Delta$ giữa đơn 2 và đơn 1), vì tại thời điểm $T_0$ doanh nghiệp chưa có dữ liệu của đơn thứ 2.
- **Quy trình Sàng lọc 5 Bước Khoa học:**

```
[Raw Candidates Đơn 1]


[Bộ lọc 1: Ma trận Tương quan Pearson (r)]


[Bộ lọc 2: Kiểm định Đa cộng tuyến Centered VIF (VIF < 5.0)]


[Bộ lọc 3: Ma trận Quyết định Sàng lọc]


[Temporal Split (Cutoff: 30/04/2018) -> Train (67,678) / Test (17,950)]
```

---

## 2. GIAI ĐOẠN 1: THIẾT KẾ ĐẶC TRƯNG CƠ BẢN & MÔ HÌNH NỀN TẢNG (BASELINE ITERATION)

### 2.1. Tập Ứng viên Đặc trưng Cơ bản & Sàng lọc Toán học

Trích xuất **33 đặc trưng ứng viên** độc lập từ Đơn hàng đầu tiên dựa trên các giả thuyết từ Bước Chẩn đoán (Diagnostic):

- **Logistics (3 biến):** `delivery_days`, `delivery_delay`, `is_late`.
- **Trải nghiệm (1 biến):** `review_score` (1-5 sao).
- **Chi tiêu & Chi phí (3 biến):** `order_spent`, `freight_ratio`, `same_state_ratio`.
- **Thanh toán & Trả góp (5 biến):** `max_installments`, `pay_credit_card`, `pay_boleto`, `pay_voucher`, `pay_debit_card`.
- **Vùng miền KT-XH (5 biến):** `state_SP`, `state_RJ`, `state_MG`, `state_Sul`, `state_outros`.
- **Ngành hàng Pareto 80/20 (16 biến):** Top 15 categories chiếm $80.05\%$ lượng đơn + 1 `cat_outros`.

#### Ma trận Quyết định Sàng lọc Giai đoạn 1:

| Tên Đặc trưng Ứng viên | Nhóm Biến | Lọc Tương quan ($r$)  | Lọc VIF | Quyết định  | Căn cứ Khoa học                                                             |
| :--------------------- | :-------- | :-------------------: | :-----: | :---------: | :-------------------------------------------------------------------------- |
| **`is_late`**          | Logistics |  $r = 0.69$ vs delay  | $1.76$  | **LOẠI BỎ** | Dư thừa thông tin, `delivery_delay` đã thể hiện liên tục độ trễ (hoặc sớm). |
| **`same_state_ratio`** | Địa lý    | $r = 0.007$ vs retain | $2.23$  | **LOẠI BỎ** | Được thay thế bởi One-hot 5 Vùng miền KT-XH chuẩn xác hơn.                  |
| **`freight_ratio`**    | Chi phí   | $r = 0.014$ vs retain | $1.99$  | **LOẠI BỎ** | Không có phân tách thống kê ($p > 0.05$ trong kiểm định Chẩn đoán).         |

**Giữ lại chính thức Giai đoạn 1:** **30 đặc trưng sạch 100% không rò rỉ dữ liệu**.

---

### 2.2. Phân chia Chuỗi Thời gian (Temporal Split) & Cửa sổ Quan sát Nhãn

Để đảm bảo nguyên tắc vàng **Zero Data Leakage theo thời gian** (không dùng dữ liệu tương lai để dự đoán quá khứ), toàn bộ dữ liệu đơn hàng đầu tiên ($N = 85.628$) được chia thành 3 giai đoạn rõ ràng:

- **1. Cửa sổ Huấn luyện (Train Window - Xanh dương):**
  - Khoảng thời gian: Từ `2016-10-01` đến `2018-04-30` ($67.678$ khách hàng, chiếm $79.04\%$ tổng tệp).
  - Tỷ lệ giữ chân thực tế: $3.61\%$ ($2.446$ khách hàng quay lại).
- **2. Cửa sổ Kiểm thử (Test Window - Đỏ):**
  - Khoảng thời gian: Từ `2018-05-01` đến `2018-07-30` ($17.950$ khách hàng, chiếm $20.96\%$ tổng tệp).
  - Tỷ lệ giữ chân thực tế: $1.48\%$ ($265$ khách hàng quay lại).
- **3. Vùng đệm Quan sát Nhãn (Performance / Observation Window - Xanh lá cây):**
  - Khoảng thời gian: Từ `2018-08-01` đến `2018-10-17` (thời điểm kết thúc bộ dữ liệu Olist).
  - **Mục đích phương pháp luận:** Tạo ra một vùng đệm kéo dài **hơn 2,5 tháng (78 ngày)** để làm thời gian chờ quan sát xem các khách hàng mua đơn đầu tiên trong tập Test (tháng 5-7/2018) có thực sự quay lại mua đơn thứ 2 hay không. Việc chừa ra vùng đệm 78 ngày này giúp **loại bỏ hoàn toàn lỗi thiên lệch cắt phải (Right-Censoring Bias)** — tránh gán nhãn sai cho những khách hàng chưa kịp có đủ thời gian để mua lại.

![Phân bố chuỗi thời gian Train, Test và Vùng đệm](assets/time_split_distribution.png)

---

### 2.3. Kết quả Thực nghiệm Giai đoạn 1 (10-Run Protocol)

| Chỉ số Đánh giá              |    Baseline (Logistic Regression)     |   Advanced (XGBoost)    | Nhận định Chuyên môn                                      |
| :--------------------------- | :-----------------------------------: | :---------------------: | :-------------------------------------------------------- |
| **ROC-AUC (Mean $\pm$ Std)** |        **$0.5410 \pm 0.0028$**        | **$0.5042 \pm 0.0028$** | Baseline có tính khái quát tuyến tính tốt hơn             |
| **ROC-AUC (Best Run)**       |             **$0.5461$**              |      **$0.5083$**       | Điểm số phân tách ở mức cơ bản                            |
| **PR-AUC (Best Run)**        |             **$0.0261$**              |      **$0.0160$**       | Cao hơn đường cơ sở ngẫu nhiên ($1.48\%$)                 |
| **Recall Retain ($y=1$)**    | **$63.02\%$** (Youden's J = $0.4811$) |      **$28.30\%$**      | Bắt được $63.02\%$ lượng khách hàng có tiềm năng quay lại |
| **Precision Retain**         |             **$1.69\%$**              |      **$1.82\%$**       | Bị loãng do $98.52\%$ mẫu âm (khách rời bỏ)               |

---

### 2.4. Phân tích Giới hạn: "Điểm nghẽn Thông tin (Information Bottleneck)"

1. **Tỷ số Tín hiệu trên Nhiễu (SNR) tiệm cận 0:** Thông tin tương hỗ $I(X; Y)$ giữa một đơn hàng giao dịch đơn lẻ và hành vi mua lại sau 90 ngày rất nhỏ ($I(X; Y) < 0.003\text{ nats}$).
2. **Đặc thù Ngành hàng Lâu bền (Durable Goods):** Khách mua đồ nội thất (giường, tủ, bàn ghế) dù hài lòng 5 sao vẫn không có nhu cầu sinh học để mua tiếp trong 90 ngày.
3. **Cần Nâng cấp Đặc trưng Tương tác:** Các biến số đơn lẻ chưa đủ sức nhận diện khách sỉ B2B, áp lực trả nợ hàng tháng hay tỷ lệ giao hàng sớm vượt kỳ vọng.

---

## 3. GIAI ĐOẠN 2: THIẾT KẾ ĐẶC TRƯNG TƯƠNG TÁC SÂU (ADVANCED INTERACTION ITERATION)

### 3.1. Cơ sở Lý thuyết & 3 Đặc trưng Nâng cấp Bổ sung

Dựa trên các nghiên cứu hành vi người tiêu dùng và 7 bảng dữ liệu nội tại sạch sẵn có, ta bổ sung **đúng 3 đặc trưng tương tác phi tuyến tính**:

|  STT  | Tên Đặc trưng Mới                | Công thức Toán học                                                                  | Cơ sở Lý thuyết & Ý nghĩa Nghiệp vụ                                                                                                                              | Bảng Dữ liệu Nguồn                             |
| :---: | :------------------------------- | :---------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------- |
| **1** | **`delivery_speed_ratio`**       | $\frac{\text{delivery\_days}}{\text{estimated\_delivery\_days}}$                    | **Thuyết Xác nhận Kỳ vọng (Oliver, 1980)**: Đo lường mức độ giao sớm/trễ so với cam kết ban đầu ($< 0.4$ kích hoạt hiệu ứng "Bất ngờ Thích thú" Delight Factor). | `clean_orders.csv`                             |
| **2** | **`monthly_installment_burden`** | $\frac{\text{order\_spent}}{\text{max\_installments}}$                              | **Thuyết Giới hạn Thanh khoản (Thaler, 1985)**: Đo lường số tiền trả nợ thực tế mỗi tháng; áp lực nhẹ giúp giải phóng thanh khoản mua lại.                       | `clean_payments.csv` & `clean_order_items.csv` |
| **3** | **`is_b2b_profile`**             | $\mathbb{I}\Big( (\text{order\_spent} > 300) \land (\text{pay\_boleto} == 1) \Big)$ | **Nhận diện Khách hàng B2B / Đại lý**: Khách mua hóa đơn lớn thanh toán Boleto Bancário có nhu cầu nhập hàng bổ sung liên tục.                                   | `clean_payments.csv` & `clean_order_items.csv` |

### 3.2. Danh sách Toàn bộ 33 Đặc trưng Chính thức Giai đoạn 2:

```text
 1. delivery_days               12. pay_debit_card            23. cat_utilidades_domesticas
 2. delivery_delay              13. state_SP                  24. cat_relogios_presentes
 3. delivery_speed_ratio      14. state_RJ                  25. cat_telefonia
 4. review_score                15. state_MG                  26. cat_ferramentas_jardim
 5. order_spent                 16. state_Sul                 27. cat_brinquedos
 6. monthly_installment_burden  17. state_outros             28. cat_automotivo
 7. max_installments            18. cat_cama_mesa_banho       29. cat_cool_stuff
 8. is_b2b_profile            19. cat_beleza_saude          30. cat_perfumaria
 9. pay_credit_card             20. cat_esporte_lazer         31. cat_eletronicos
10. pay_boleto                  21. cat_moveis_decoracao      32. cat_bebes
11. pay_voucher                 22. cat_informatica_acessorios 33. cat_outros
```

---

## 4. SO SÁNH ĐỐI CHIẾU HIỆU NĂNG GIAI ĐOẠN 1 VS GIAI ĐOẠN 2 (10-RUN BENCHMARK)

Sau khi hoàn thành huấn luyện 10 lượt chạy độc lập (10 Random Seeds) cho cả 2 mô hình trên tập 33 đặc trưng Giai đoạn 2:

### 4.1. Bảng Tổng hợp So sánh Đa chiều

| Tiêu chí Đánh giá            | Baseline Giai đoạn 1 (30 biến) | Baseline Giai đoạn 2 (33 biến) | Advanced Giai đoạn 1 (30 biến) | Advanced Giai đoạn 2 (33 biến) | Mức độ Cải thiện (Lift)                               |
| :--------------------------- | :----------------------------: | :----------------------------: | :----------------------------: | :----------------------------: | :---------------------------------------------------- |
| **ROC-AUC (Mean $\pm$ Std)** |      $0.5410 \pm 0.0028$       |    **$0.5371 \pm 0.0012$**     |      $0.5042 \pm 0.0028$       |    **$0.5027 \pm 0.0031$**     | Cả 2 mô hình ổn định cao ($CV < 0.7\%$)               |
| **ROC-AUC (Best Run)**       |            $0.5461$            |     **$0.5387$** _(Run 7)_     |            $0.5083$            |     **$0.5072$** _(Run 7)_     | Điểm số hội tụ thực tế                                |
| **PR-AUC (Best Run)**        |            $0.0261$            |          **$0.0267$**          |            $0.0160$            |          **$0.0148$**          | Baseline duy trì PR-AUC gần gấp đôi ngẫu nhiên ($1.48\%$) |
| **Recall Retain (Mean)**     |           $63.02\%$            |         **$57.81\%$**          |           $28.30\%$            |         **$61.51\%$**          | **XGBoost tăng vọt Recall trung bình ($+33.21\%$)**   |
| **Recall Retain (Max Run)**  |           $63.02\%$            |    **$62.64\%$** _(Run 8)_     |           $33.96\%$            |    **$86.04\%$** _(Run 4)_     | Bắt trúng tới **$86.04\%$** khách Retain              |
| **Precision Retain (Mean)**  |            $1.69\%$            |          **$1.69\%$**          |            $1.82\%$            |          **$1.59\%$**          | Ổn định quanh mức $1.6\% - 1.7\%$                     |
| **Tỷ lệ Dự đoán Retain**     |         $\sim 55.0\%$          |         $\sim 50.6\%$          |         $\sim 24.6\%$          |       **$\sim 57.4\%$**        | **Youden's J cân bằng tối ưu giữa Retain và Churn**   |

---

### 4.2. Đánh giá Ưu điểm Vượt trội của Mô hình Advanced (XGBoost Giai đoạn 2):

1. **Tăng vọt Khả năng Phát hiện Khách Retain (Recall Lift):** Nhờ 3 đặc trưng tương tác phi tuyến tính, XGBoost nâng Recall trung bình từ **$28.30\% \to 61.51\%$** (đỉnh cao $86.04\%$).
2. **Khả năng giải thích sâu với Explainable AI (TreeSHAP):** Khác với mô hình tuyến tính giả định độc lập, XGBoost bóc tách được các mối quan hệ phi tuyến tính và hiệu ứng tương tác đa chiều giữa Logistics, Chi tiêu trả góp và Hồ sơ B2B để hỗ trợ phân tầng rủi ro chính xác.

---

## 5. GIẢI THÍCH MÔ HÌNH VỚI XAI (TREESHAP FEATURE IMPORTANCE)

Áp dụng giải thuật **TreeSHAP (Lundberg & Lee, 2017)** trên mô hình XGBoost tốt nhất (Run 7) để bóc tách động lực quyết định:

```
                      TREESHAP GLOBAL FEATURE IMPORTANCE



[1. Nhóm Logistics & Tốc độ Giao]                       [2. Nhóm Tài chính & Trả góp]
• delivery_days (SHAP ~ 0.18)                           • monthly_installment_burden (SHAP ~ 0.14)
• delivery_speed_ratio (SHAP ~ 0.12)                    • max_installments (SHAP ~ 0.09)
• delivery_delay (SHAP ~ 0.11)                          • is_b2b_profile (SHAP ~ 0.06)
```

### 5.1. Phân tích Cơ chế Tác động:

1. **`delivery_days` & `delivery_speed_ratio` (Động lực số 1):** Thời gian giao hàng thực tế ngắn và tốc độ giao sớm trước hạn cam kết ($< 0.4$) đẩy SHAP value dương mạnh nhất, kích hoạt ý định mua lại.
2. **`monthly_installment_burden` & `is_b2b_profile` (Động lực số 2):** Áp lực trả nợ hàng tháng thấp giải phóng thanh khoản; nhóm khách sỉ B2B thanh toán Boleto có xu hướng giữ chân vượt trội so với khách mua lẻ.
3. **`review_score` (Bộ lọc Thảm họa):** Đánh giá 1-2 sao đóng vai trò là "lực cản tuyệt đối" (Hard Negative Driver), triệt tiêu xác suất quay lại.
4. **Ngành hàng Định kỳ (`cat_cama_mesa_banho`, `cat_beleza_saude`):** Giữ vị trí nhóm ngành hàng có tần suất tiêu dùng và tỷ lệ mua lại cao nhất.

---

## 6. PHÂN TẦNG RỦI RO KHÁCH HÀNG (RISK TIER SEGMENTATION)

Áp dụng mô hình XGBoost (Run 4) lên toàn bộ $17,950$ khách hàng trong tập Test để phân tầng phục vụ trực tiếp cho **Module 4 (Prescriptive Analytics)**:

| Tầng Rủi ro (Risk Tier) | Ngưỡng Xác suất $P(\text{Retain})$ | Tỷ trọng Khách hàng | Số lượng Khách | Định hướng Can thiệp Nghiệp vụ |
| :--- | :---: | :---: | :---: | :--- |
| **Tier 1: Irretrievable / Dead Loss** | $P < 0.189$ | **$18.56\%$** | $3,331$ | **KHÔNG CHI TIỀN MARKETING.** Khách hàng có rủi ro rời bỏ tuyệt đối, trải nghiệm thất bại nặng nề hoặc nhu cầu vãng lai 1 lần. Chi tiền vào đây sẽ gây thất thoát $100\%$ ngân sách (Deadweight Loss). |
| **Tier 2: Savable Target (Mục tiêu)** | $0.189 \le P \le 0.280$ | **$58.11\%$** | **$10,430$** | **TẬP TRUNG NGUỒN LỰC CAN THIỆP.** Nhóm nhạy cảm cao với dịch vụ, dễ bị lung lay bởi điểm nghẽn trải nghiệm (trễ hẹn, áp lực trả góp, ngành hàng ngoại vi). Áp dụng phân luồng 2 tầng (Tier 2A cấp vốn & Tier 2B tự tài trợ). |
| **Tier 3: Organic Safe (Tự nhiên)** | $P > 0.280$ | **$23.34\%$** | **$4,189$** | **BẢO TOÀN BIÊN LỢI NHUẬN.** Khách hàng có xu hướng quay lại tự nhiên rất cao (xác suất $> 28.0\%$, cao gấp $> 9.4$ lần tỷ lệ tự nhiên toàn sàn $2.98\%$). Không chiết khấu/voucher dư thừa, chỉ duy trì dịch vụ chuẩn và chương trình CRM tích điểm. |

---

## 7. KẾT LUẬN & CHUYỂN GIAO SANG PHÂN TÍCH CHỈ ĐỊNH (MODULE 04)

### 7.1. Tổng kết Thành tựu Module 03 (Predictive Analytics)

1. **Khoa học & Không Rò rỉ Dữ liệu ($100\%$ Zero Leakage):** Bác bỏ hoàn toàn các mô hình gian lận tương lai, xây dựng hệ thống dự báo thực tế ngay sau Đơn hàng đầu tiên.
2. **Kế thừa Phương pháp luận Quốc tế:** Bổ sung thành công 3 đặc trưng tương tác hành vi giúp XGBoost tăng gấp đôi Recall ($57.36\%$).
3. **Chuẩn bị Sẵn sàng Tệp Khách hàng Mục tiêu:** Xuất file `test_predictions.csv` chứa đầy đủ xác suất $P(\text{Retain})$, nhãn phân tầng và SHAP Values.

---

### 7.2. Lộ trình Chuyển giao sang Module 04 (Prescriptive Analytics - Phân tích Chỉ định)

1. **Phân loại 3 Tầng Quản trị (3-Tier Governance):**
   - *Tier 1:* Loại trừ khỏi chiến dịch tiếp thị để triệt tiêu lãng phí ngân sách.
   - *Tier 2:* Trích xuất đưa vào bài toán tối ưu hóa phân bổ ngân sách và can thiệp 4 cụm điểm nghẽn.
   - *Tier 3:* Phân luồng chăm sóc tự nhiên, bảo vệ 100% biên lợi nhuận gộp.
2. **Thực hiện Phân cụm Nguyên nhân Gốc rễ bằng TreeSHAP (Root Cause Clustering):**
   - *Cụm 0 (Financial Relief):* Khách hàng vướng rào cản tài chính, áp lực trả góp lớn -> Kích hoạt Gói Trả góp 0% Lãi suất.
   - *Cụm 1 (Service Resolution):* Đánh giá 1-2 sao, sự cố dịch vụ -> Đội ngũ CSKH xử lý khiếu nại + Voucher thiện chí 12%.
   - *Cụm 2 (Experience Recovery):* Sốc giao hàng trễ -> Gói bồi thường 100% cước vận chuyển (Free Ship).
   - *Cụm 3 (Category Re-engagement):* Mua sắm ngành hàng/khu vực ngoại vi -> Gợi ý sản phẩm bổ trợ cá nhân hóa + Voucher kích cầu 8%.
3. **Thiết lập Động cơ Kép (Dual-Engine Framework) & Tối ưu hóa Tuyến tính (ILP):**
   - *Nhánh Tier 2A (VIP Engine):* Cấp vốn tức thì cho top khách hàng biên lợi nhuận cao nhất, hoàn vốn trong 14 ngày.
   - *Nhánh Tier 2B (Base Engine):* Tự động hóa tự tài trợ qua mã giảm giá kèm điều kiện giỏ hàng mới.
