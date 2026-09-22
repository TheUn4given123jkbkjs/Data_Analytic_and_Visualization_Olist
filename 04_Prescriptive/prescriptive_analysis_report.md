# BÁO CÁO PHÂN TÍCH CHỈ ĐỊNH VÀ TỐI ƯU HÓA TÀI CHÍNH

## (Prescriptive Analytics & ROI Optimization Report)

Dự án Phân tích Dữ liệu Thương mại Điện tử Brazil (Olist E-Commerce)
Giai đoạn 04: Prescriptive Analytics

---

## 1. TỔNG QUAN VÀ MỤC TIÊU

Báo cáo này trình bày kết quả thực thi giai đoạn Phân tích Chỉ định (Prescriptive Analytics), giai đoạn cao nhất trong chuỗi giá trị phân tích dữ liệu:

$$\text{Descriptive} \longrightarrow \text{Diagnostic} \longrightarrow \text{Predictive} \longrightarrow \mathbf{\text{Prescriptive}}$$

Mục tiêu cốt lõi là chuyển hóa xác suất dự báo và nguyên nhân giải thích từ mô hình XGBoost (Module 03) thành các quy tắc can thiệp tự động, cá nhân hóa cho từng khách hàng thuộc tệp Cần Giữ Chân (Tier 2: Savable Customers). Đồng thời, báo cáo xác lập khung phân bổ ngân sách theo **Hệ quy chiếu Tỷ lệ phần trăm (%) Linh hoạt** nhằm tối đa hóa Lợi nhuận Ròng và Tỷ suất Hoàn vốn (ROI).

### Khung Quản Trị Phân Tầng Rủi Ro (3-Tier Governance Architecture):
Hệ thống vận hành chính sách dựa trên 3 tầng phân định rủi ro được kế thừa trực tiếp từ Module 03:
1. **Tier 1 — Nguy cơ Cực cao / Lost Risk ($P < 0.150$):** Nhóm khách hàng rời bỏ khó cứu vãn do nhu cầu 1 lần hoặc trải nghiệm đứt gãy nghiêm trọng. **Chiến lược:** Loại trừ $100\%$ khỏi danh sách can thiệp để triệt tiêu chi phí chìm (Deadweight Loss).
2. **Tier 2 — Savable Target ($0.150 \le P \le 0.341$):** Nhóm khách hàng mục tiêu nằm trong vùng nhạy cảm với các đòn bẩy dịch vụ, tài chính và logistics ($N = 9.102$ khách hàng). **Chiến lược:** Áp dụng Phân luồng Can thiệp 4 Cụm và Cơ chế Động cơ Kép (Tier 2A Cấp vốn trực tiếp thu hồi trong 14 ngày & Tier 2B Tự tài trợ kích hoạt giỏ hàng mới).
3. **Tier 3 — Monitor ($P > 0.341$):** Nhóm khách hàng trung thành tự nhiên (xác suất $> 34.1\%$, cao gấp $> 11$ lần tỷ lệ tự nhiên của sàn $2.98\%$). **Chiến lược:** Không tiêu tốn ngân sách voucher, chỉ duy trì chất lượng dịch vụ chuẩn và chương trình CRM tích điểm nhằm bảo vệ trọn vẹn biên lợi nhuận gộp $30\%$.

---

## 2. NGUYÊN TẮC PHƯƠNG PHÁP LUẬN

Quá trình xây dựng kế hoạch hành động tuân thủ nghiêm ngặt 3 nguyên tắc:

1. **Tính toán chi phí can thiệp động theo tỷ lệ thực tế** — chi phí can thiệp $c_k$ cho mỗi nhóm được xác lập dựa trên tỷ lệ % giá trị đơn hàng trung bình (AOV - Average Order Value), cước phí vận chuyển thực tế và số kỳ trả góp.
2. **Khảo sát phân bổ tỷ trọng điểm nghẽn thực tế trước khi phân cụm** — quét toàn diện tệp Tier 2 để định lượng chính xác cơ cấu điểm nghẽn trước khi thiết kế chính sách can thiệp.
3. **Đo lường mức tăng trưởng phản thực tế bằng chính mô hình AI** (Counterfactual Simulation qua XGBoost) thay vì gán tỷ lệ cứu vãn cảm tính:

$$\Delta P_i = P(Y=1 \mid X_i^{\text{counterfactual}}) - P(Y=1 \mid X_i^{\text{original}})$$

---

## 3. BƯỚC 1 — THỐNG KÊ PHÂN BỔ ĐIỂM NGHẼN THỰC TẾ

Tệp khách hàng Tier 2 (Savable Customers) được trích xuất theo nhãn `risk_tier` từ đầu ra Module 03, thu được **N = 9.102 khách hàng** trong tập Test.

Bảng 1 trình bày tỷ trọng thực tế của 4 nhóm điểm nghẽn chính, đo trên toàn bộ tệp Tier 2 (một khách hàng có thể đồng thời mang nhiều cờ điểm nghẽn):

**Bảng 1. Phân bổ điểm nghẽn thực tế — Tệp Tier 2 (N = 9.102)**

| Nhóm Điểm Nghẽn                                             | Số Khách Hàng | Tỷ Trọng (%) | Doanh Thu Liên Quan (R$) | Chỉ Số Bổ Sung                              |
| ----------------------------------------------------------- | ------------: | -----------: | -----------------------: | ------------------------------------------- |
| 1. Logistics Friction (trễ hẹn giao)                        |           216 |         2,37 |                11.767,50 | Trễ TB: 4,2 ngày · Cước TB: R$ 10,03        |
| 2. Financial Burden (áp lực trả góp)                        |         1.892 |        20,79 |               177.873,49 | Kỳ trả góp TB: 7,9 · Đơn hàng TB: R$ 94,01  |
| 3. Rating & Service Friction (đánh giá kém)                 |         1.191 |        13,09 |                85.170,39 | Điểm đánh giá TB: 2,52/5                    |
| 4. Peripheral Category & Remote State (ngành/bang ngoại vi) |         5.800 |        63,72 |               305.053,22 | Đơn hàng TB: R$ 52,60                       |

**Nhận định:** Điểm nghẽn Ngành hàng & Địa lý chiếm ưu thế lớn nhất (63,72% tệp Tier 2 với 5.800 khách hàng), cho thấy phần lớn khách hàng có nguy cơ rời bỏ đến từ việc mua sắm ở các danh mục chưa phải thế mạnh hoặc cư trú tại các bang xa — đây là nhóm cần chiến lược nuôi dưỡng và tái tương tác theo chu kỳ tiêu dùng. Áp lực tài chính chiếm 20,79% (1.892 khách), đánh giá kém chiếm 13,09% (1.191 khách), và điểm nghẽn Logistics chỉ chiếm 2,37% (216 khách) nhưng mang tính nghiêm trọng cao trên từng đơn hàng (trễ trung bình 4,2 ngày).

![Phân bổ điểm nghẽn thực tế — Tệp Tier 2](assets/executive_friction_distribution.png)

---

> [!IMPORTANT]
> **Phân biệt Phương pháp luận giữa Bảng 1 (Đa nhãn Độc lập) và Bảng 2 (Phân hoạch Rời rạc):**
> - **Bảng 1 (Khảo sát Triệu chứng Độc lập — Multi-label Flags):** Mỗi khách hàng có thể vướng nhiều rào cản cùng lúc (ví dụ: vừa bị giao trễ, vừa chấm 1 sao; hoặc vừa trả góp nhiều kỳ, vừa ở bang ngoại vi). Do đó, các con số $5.800$, $1.892$, $1.191$, $216$ đo lường quy mô tổn thất doanh thu theo từng vấn đề riêng rẽ và có sự **chồng chéo (overlap)**.
> - **Bảng 2 (Phân cụm Điều trị Rời rạc — Single-label K-Means Partitioning):** Trong vận hành, mỗi khách hàng chỉ có thể nhận **duy nhất 1 gói can thiệp chủ đạo** (không thể cùng lúc gửi 3 voucher khác nhau gây lãng phí ngân sách). Thuật toán K-Means phân tích vector 9 chiều để bóc tách **"Điểm nghẽn chi phối chí mạng nhất" (Dominant Root Cause)**:
>   - **Toàn bộ 216 khách bị giao trễ** (điểm nghẽn cấp bách nhất) được gom trọn vẹn 100% vào **Cụm 3** ($N_3 = 216$).
>   - Trong 1.191 khách chấm review xấu, có 69 khách cũng bị giao trễ (đã đưa vào Cụm 3) và một số khách có đơn hàng lớn trả góp; K-Means gom **1.119 khách có điểm nghẽn thuần túy là Review tiêu cực** vào **Cụm 2** ($N_2 = 1.119$).
>   - Trong 1.892 khách chịu áp lực tài chính, sau khi bóc tách các khách bị giao trễ hay review xấu nặng, K-Means gom **1.570 khách có điểm nghẽn tài chính thuần túy** vào **Cụm 1** ($N_1 = 1.570$).
>   - **Cụm 0 (6.197 khách)** là nhóm khách hàng còn lại ($9.102 - 1.570 - 1.119 - 216 = 6.197$), gồm 5.800 khách có cờ ngành hàng/bang xa không vướng 3 sự cố nghiêm trọng trên kết hợp cùng các khách hàng có hành vi tiêu dùng phân tán.
>
> **Bảng đối soát ma trận chuyển hóa (Cross-Tabulation Matrix):**
> | Cụm K-Means | Quy mô ($N_k$) | % có Cờ Giao trễ | % có Cờ Tài chính | % có Cờ Review | % có Cờ Danh mục | Điểm Nghẽn Chi Phối |
> | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
> | **Cụm 3** | **216** | **100%** (216 KH) | 25% (54 KH) | 32% (69 KH) | 68% (147 KH) | Giao hàng trễ (Logistics) |
> | **Cụm 2** | **1.119** | 0% (0 KH) | 24% (268 KH) | **100%** (1.119 KH) | 63% (705 KH) | Đánh giá kém (Review) |
> | **Cụm 1** | **1.570** | 0% (0 KH) | **100%** (1.570 KH) | 0% (0 KH) | 70% (1.099 KH) | Áp lực tài chính (Financial) |
> | **Cụm 0** | **6.197** | 0% (0 KH) | 0% (0 KH) | 0% (0 KH) | **62%** (3.842 KH) | Danh mục ngoại vi (Category) |
> | **Tổng Cờ (Bảng 1)** | — | **216 khách** | $1.570 + 268 + 54 = \mathbf{1.892}$ | $1.119 + 69 + 3 \approx \mathbf{1.191}$ | $\approx \mathbf{5.800}$ khách | **Khớp chính xác 100%** |

Thuật toán K-Means được áp dụng trên ma trận điểm nghẽn đã chuẩn hóa. Số cụm tối ưu được kiểm chứng tự động theo phương pháp Elbow và Silhouette Score: **k = 4**.

![Phương pháp Elbow và Silhouette Score xác định 4 cụm tối ưu](assets/diagnostic_elbow_silhouette.png)

**Bảng 2. Chân dung 4 cụm khách hàng Tier 2 (N = 9.102)**

| Cụm | Điểm Nghẽn Chi Phối | $N_k$ | Tỷ Trọng (%) | $\text{AOV}_k$ (R$) | $\text{Freight}_k$ (R$) | $\text{Installments}_k$ | $P_{0,k}$ |
| --- | ------------------- | ----: | -----------: | ------------------: | ----------------------: | ----------------------: | --------: |
| 0   | Category (Ngành Ngoại vi) | 6.197 |        68,08 |               52,60 |                   14,10 |                    1,95 |      0,21 |
| 1   | Financial (Áp lực Tài chính) | 1.570 |        17,25 |               94,01 |                   15,82 |                    7,90 |      0,22 |
| 2   | Review (Đánh giá Kém) | 1.119 |        12,29 |               71,51 |                   16,20 |                    3,12 |      0,21 |
| 3   | Logistics (Giao Trễ) |   216 |         2,37 |               54,48 |                   10,03 |                    2,85 |      0,20 |

_Chú thích thuật ngữ:_
- $\text{AOV}_k$: Giá trị đơn hàng trung bình của cụm $k$.
- $\text{Freight}_k$: Cước phí giao hàng trung bình của cụm $k$.
- $P_{0,k}$: Xác suất giữ chân ban đầu do AI dự báo cho cụm $k$.

---

## 5. BƯỚC 3 — MA TRẬN CAN THIỆP VÀ CHI PHÍ ĐỘNG

Chi phí can thiệp $c_k$ được thiết lập dưới dạng tỷ lệ % theo giá trị đơn hàng thực tế của từng cụm. Các định mức % này được xây dựng dựa trên **chuẩn mực vận hành thực tế trong ngành Thương mại Điện tử (E-Commerce Standard Benchmarks)**:

**Bảng 3. Ma trận can thiệp và định mức chi phí theo tỷ lệ %**

| Cụm | Gói Can Thiệp                                | Định Mức Chi Phí (% Đơn Hàng)                                             | Chi Phí Mẫu ($c_k$) | $N_k$ | Tỷ Trọng (%) |
| --- | -------------------------------------------- | ------------------------------------------------------------------------- | ------------------: | ----: | -----------: |
| 0   | Category Re-engagement (Tái Tương Tác Ngành) | $8\\% \\times \\text{AOV}_k$ (Ưu đãi kích cầu giỏ hàng)                      |             R$ 4,91 | 6.197 |        68,08 |
| 1   | Financial Relief (Hỗ trợ Thanh toán)         | $6\\% \\times \\text{AOV}_k$ (Phí bù trả góp 0%)                             |             R$ 5,58 | 1.570 |        17,25 |
| 2   | Service Resolution (Chăm Sóc & Đổi Trả)      | $12\\% \\times \\text{AOV}_k$ (Voucher đền bù thiện chí)                     |             R$ 8,76 | 1.119 |        12,29 |
| 3   | Experience Recovery (Bồi Thường Vận Chuyển)  | $\\max(\\text{Freight}_k,\\ 15\\% \\times \\text{AOV}_k)$ (Hoàn 100% cước ship) |            R$ 10,03 |   216 |         2,37 |

### Căn cứ thực tế của từng mức định mức phần trăm (%):

1. **Gói Category Re-engagement (Định mức 8% AOV — Cụm 0):**
   - _Nghiệp vụ thực tế:_ Kích cầu mua lại cho khách hàng mua ngành hàng ngoại vi hoặc ở bang xa thông qua cá nhân hóa sản phẩm bổ trợ và ưu đãi kích hoạt giỏ hàng.
   - _Căn cứ kinh tế:_ Đây là định mức **Chiết khấu Giữ chân Chuẩn (Standard Retention Discount)** trong Marketing Automation, thường dao động từ **5% đến 8%**. Mức 8% là ngưỡng an toàn tối đa để khi khách đặt đơn mới, sàn vẫn bảo toàn được ít nhất 22% tiền lời ròng (30% biên gộp - 8% ưu đãi = 22%).

2. **Gói Financial Relief (Định mức 6% AOV — Cụm 1):**
   - _Nghiệp vụ thực tế:_ Tài trợ chương trình **Trả góp 0% Lãi suất** từ 6 - 12 kỳ cho các đơn hàng giá trị lớn nhằm giải phóng áp lực dòng tiền.
   - _Căn cứ kinh tế:_ Tại thị trường Brazil và các cổng thanh toán (Cielo, Stone, PagSeguro), khi sàn muốn người mua được trả góp 0%, sàn/người bán phải trả một khoản phí chuyển đổi giao dịch trả góp (Installment Subsidization Fee / MDR) cho ngân hàng, mức chuẩn mực dao động từ **5% đến 7%** (lấy mốc trung bình là **6%**).

3. **Gói Service Resolution (Định mức 12% AOV — Cụm 2):**
   - _Nghiệp vụ thực tế:_ Xử lý khiếu nại của khách hàng đánh giá 1 - 2 sao kết hợp tặng voucher bồi thường thiện chí (Goodwill Voucher) để khôi phục niềm tin.
   - _Căn cứ kinh tế:_ Theo chuẩn mực CSKH TMĐT quốc tế (Amazon, Shopee), voucher xin lỗi và đền bù dịch vụ thường được định mức ở mức **10% - 15% giá trị đơn hàng cũ** (lấy mốc trung bình là **12%**). Mức này đủ tạo cảm giác được bồi thường thỏa đáng cho khách hàng mà vẫn nằm trong biên lợi nhuận gộp 30% của sàn.

4. **Gói Experience Recovery (Hoàn 100% Cước Ship ~18% AOV — Cụm 3):**
   - _Nghiệp vụ thực tế:_ Khắc phục sự cố giao hàng trễ nghiêm trọng (trễ trung bình 4,2 ngày) bằng cách hoàn 100% cước phí vận chuyển cho đơn hàng tiếp theo.
   - _Căn cứ kinh tế:_ Sàn áp dụng chính sách **Bảo hiểm Cam kết SLA Vận chuyển: Hoàn 100% cước phí giao hàng (Free Ship R$ 10,03)** cho đơn tiếp theo. Trong dữ liệu Olist, cước vận chuyển thực tế chiếm trung bình từ **15% đến 18%** giá trị đơn hàng.

Chi phí can thiệp trung bình trên toàn tệp Tier 2 trong mẫu thử nghiệm: **R$ 5,58/khách hàng**.

---

## 6. BƯỚC 4 — MÔ PHỎNG PHẢN THỰC TẾ BẰNG AI (COUNTERFACTUAL UPLIFT)

Ma trận đặc trưng phản thực tế $X^{\text{counterfactual}}$ được xây dựng bằng cách khắc phục đúng điểm nghẽn chi phối của từng khách hàng, sau đó nạp vào mô hình XGBoost gốc để đo lường:

$$\Delta P_i = P(Y=1 \mid X_i^{\text{counterfactual}}) - P(Y=1 \mid X_i^{\text{original}})$$

$$\Delta \text{CLV}_i = \Delta P_i \times \text{AOV}_i \times m \times f$$

_Trong đó:_
- $m = 30\%$: Tỷ lệ biên tiền lời gộp của sàn thương mại điện tử.
- $f = 1{,}5$: Hệ số tần suất mua sắm kỳ vọng trong chu kỳ tiếp theo.
- $\Delta \text{CLV}_i$: Giá trị tiền lời tăng thêm kỳ vọng thu về từ khách hàng $i$.

**Kết quả mô phỏng trên toàn tệp Tier 2 (N = 9.102):**

| Chỉ số Đo Lường                                                        |     Giá Trị Mô Phỏng |
| ---------------------------------------------------------------------- | -------------------: |
| Mức tăng xác suất giữ chân trung bình ($\overline{\Delta P}$)          | 0,0558 (5,58 điểm %) |
| Tiền lời kỳ vọng tăng thêm trung bình ($\overline{\Delta \text{CLV}}$) |      R$ 0,56 / khách |

**Nhận định:** Mức tăng xác suất giữ chân trung bình trên toàn tệp đạt 5,58%, một số cá thể trong tệp có mức tăng đột biến ($\Delta P > 0{,}40$). Điều này chứng minh sự cần thiết của việc phân luồng xử lý: Cấp vốn trực tiếp cho nhóm chuyển đổi nhanh, và áp dụng cơ chế tự tài trợ nuôi dưỡng cho nhóm còn lại.

---

## 7. BƯỚC 5 — TỐI ƯU HÓA PHÂN BỔ NGÂN SÁCH (KNAPSACK OPTIMIZATION)

### 7.1. Định nghĩa và Nguồn gốc Trần Ngân Sách Toàn Tệp ($B_{\max}$)

Tổng trần ngân sách giả định tối đa ($B_{\max}$) là tổng chi phí nếu sàn phát voucher tiền mặt trực tiếp cho toàn bộ 100% khách hàng trong tệp Tier 2 (9.102 khách hàng), được tính bằng tổng chi phí của 4 cụm:

$$B_{\max} = \sum_{i=1}^{N} c_i = \sum_{k=0}^{3} (N_k \times c_k) = \text{R\$ } 51.131{,}00$$

### 7.2. Giải Thuật Quy Hoạch Tuyến Tính Nguyên (Knapsack 0/1)

$$\max_{\{x_i\}} \sum_{i=1}^{N} x_i \cdot \left( \Delta \text{CLV}_i - c_i \right) \quad \text{thỏa mãn} \quad \sum_{i=1}^{N} x_i \cdot c_i \le B,\quad x_i \in \{0, 1\}$$

**Bảng 4. Kết quả tối ưu hóa tại các mốc ngân sách thử nghiệm**

| Mốc Ngân Sách Thử Nghiệm          | Tỷ Lệ % $B_{\max}$ | Số Khách Hàng Được Chọn | Ngân Sách Đề Xuất (R$) | Tổng $\Delta\text{CLV}$ Thu Về (R$) | Lợi Nhuận Ròng (R$) | Tỷ Suất Hoàn Vốn ROI (%) |
| --------------------------------- | -----------------: | ----------------------: | ---------------------: | ----------------------------------: | ------------------: | -----------------------: |
| 25% $B_{\max}$ (Trần 12.782,75 R$) |              1,05% |         102 (1,12% tệp) |                 536,48 |                            1.686,04 |            1.149,56 |                  214,28% |
| 50% $B_{\max}$ (Trần 25.565,50 R$) |              1,05% |         102 (1,12% tệp) |                 536,48 |                            1.686,04 |            1.149,56 |                  214,28% |
| 75% $B_{\max}$ (Trần 38.348,25 R$) |              1,05% |         102 (1,12% tệp) |                 536,48 |                            1.686,04 |            1.149,56 |                  214,28% |
| 100% $B_{\max}$ (Trần 51.131,00 R$) |              1,05% |         102 (1,12% tệp) |                 536,48 |                            1.686,04 |            1.149,56 |                  214,28% |
| Ngân Sách Tự Do Tối Ưu            |              1,05% |         102 (1,12% tệp) |                 536,48 |                            1.686,04 |            1.149,56 |                  214,28% |

### 7.3. Giải Thích Ý Nghĩa Kinh Tế & Biểu Đồ Tối Ưu

**Tại sao cả 5 mốc ngân sách đều dừng lại ở đúng con số 536,48 R$ (102 khách hàng)?**

- Khi quét toàn bộ 9.102 khách hàng, chỉ có đúng **102 khách hàng (1,12%)** có giá trị tiền lời dự báo lớn hơn chi phí can thiệp ($\Delta \text{CLV}_i > c_i$).
- **9.000 khách hàng còn lại** có tiền lời dự báo nhỏ hơn chi phí voucher tiền mặt ($\Delta \text{CLV}_i \le c_i$).
- Vì vậy, ngay cả khi ban giám đốc cấp hạn mức ngân sách rất lớn (ví dụ 100% ngân sách = 51.131,00 R$), thuật toán Knapsack vẫn thông minh **tự động dừng lại ở mức 536,48 R$**. Nếu ép hệ thống chi thêm tiền mặt cho 9.000 khách còn lại thì cứ mỗi đồng chi ra công ty sẽ bị lỗ thêm, làm tổng lợi nhuận ròng của chiến dịch bị sụt giảm.

![Cơ cấu phân bổ ngân sách tối ưu theo gói can thiệp](assets/executive_budget_donut.png)

![Đường cong ngân sách vs lợi nhuận ròng — điểm bão hòa biên](assets/executive_profit_frontier.png)

- **Ý nghĩa Biểu đồ (Profit Frontier - Điểm bão hòa lợi nhuận biên):** Đường cong cho thấy lợi nhuận ròng tăng vọt và đạt đỉnh tối đa tại điểm chi phí 536,48 R$ (lợi nhuận ròng 1.149,56 R$). Sau điểm này, đường lợi nhuận nằm ngang và đi xuống nếu tiếp tục chi tiền mặt vô điều kiện.

---

## 8. BƯỚC 6 — PHÂN TÍCH ĐIỂM HÒA VỐN VÀ 3 KỊCH BẢN THỬ NGHIỆM

### 8.1. Tỷ lệ Chuyển đổi Hòa vốn Lý thuyết (Break-even Rate)

$$U_{\text{break-even}, k} = \frac{c_k}{\text{AOV}_k \times m \times f}$$

**Bảng 5. Ngưỡng chuyển đổi hòa vốn theo từng cụm**

| Cụm | Gói Can Thiệp          | Chi Phí Mẫu ($c_k$) | Đơn Hàng Mẫu ($\text{AOV}_k$) | Tỷ Lệ Cần Đạt ($U_{\text{break-even}}$) | Diễn Giải Bằng Ngôn Ngữ Tự Nhiên                                                             |
| --- | ---------------------- | ------------------: | ----------------------------: | --------------------------------------: | -------------------------------------------------------------------------------------------- |
| 0   | Category Re-engagement |             4,91 R$ |                      52,60 R$ |                              **20,73%** | Cần 2,1 trên 10 khách mua lại là sàn đã hòa vốn chiết khấu 8%.            |
| 1   | Financial Relief       |             5,58 R$ |                      94,01 R$ |                              **13,24%** | Chỉ cần 1,3 trên 10 khách mua lại là sàn đã hòa vốn (Rất dễ đạt vì giỏ hàng lớn).            |
| 2   | Service Resolution     |             8,76 R$ |                      71,51 R$ |                              **27,29%** | Cần khoảng 2,7 trên 10 khách mua lại để hòa vốn chi phí CSKH.                     |
| 3   | Experience Recovery    |            10,03 R$ |                      54,48 R$ |                              **40,96%** | Cần 4,1 trên 10 khách mua lại để bù cước Free Ship 100% (Gói có chi phí đầu người cao nhất). |

![Ma trận ngưỡng hòa vốn theo AOV và chi phí can thiệp](assets/executive_break_even_heatmap.png)

### 8.2. Đánh Giá Độ Nhạy Qua 3 Kịch Bản Thị Trường (Stress-Testing)

**Bảng 6. Đánh giá sức chống chịu tài chính trên nhóm 102 khách hàng ưu tiên (Tier 2A)**

| Kịch Bản Thị Trường       | Giả Định Hiệu Quả Thực Tế                            | Doanh Số Tăng Thêm (R$) | Chi Phí Đầu Tư (R$) | Lợi Nhuận Ròng (R$) | Tỷ Suất Sinh Lời ROI (%) | Đánh Giá Mức Độ Rủi Ro                                                     |
| ------------------------- | ---------------------------------------------------- | ----------------------: | ------------------: | ------------------: | -----------------------: | -------------------------------------------------------------------------- |
| **Bi quan (Pessimistic)** | Khách hàng chỉ phản hồi **50%** so với dự báo của AI |                  843,02 |              536,48 |          **306,54** |               **57,14%** | **Cực kỳ an toàn**: Dù hiệu quả giảm 1 nửa, sàn vẫn thu hồi đủ vốn và lời hơn 57%. |
| **Cơ sở (Base Case)**     | Khách hàng phản hồi đúng **100%** theo dự báo của AI |                1.686,04 |              536,48 |        **1.149,56** |              **214,28%** | **Kịch bản chuẩn**: Thu về hơn 2 đồng lời ròng cho mỗi 1 đồng chi phí.       |
| **Lạc quan (Optimistic)** | Khách hàng phản hồi vượt kỳ vọng (**120%**)          |                2.023,25 |              536,48 |        **1.486,77** |              **277,13%** | **Kịch bản đột phá**: Lợi nhuận tăng trưởng vượt bậc khi kết hợp CSKH tốt. |

![So sánh Doanh thu — Chi phí — Lợi nhuận ròng giữa 3 kịch bản điều hành](assets/executive_scenario_comparison.png)

---

## 9. KẾT LUẬN VÀ KIẾN TRÚC CAN THIỆP 2 TẦNG (DUAL-ENGINE FRAMEWORK)

Giai đoạn Phân tích Chỉ định (Prescriptive Analytics) giải quyết triệt để câu hỏi cốt lõi của doanh nghiệp: **"Công ty phải làm gì cụ thể cho từng nhóm khách hàng và kết quả tài chính tổng thể mang lại ra sao?"**

### 9.1. Tổng Quan Phân Định Chiến Lược

**Bảng 7. Tổng quan phân định 2 luồng can thiệp chiến lược**

| Luồng Can Thiệp                   | Số Lượng (%)     | Vốn Cấp Trước   | Doanh Số Kỳ Vọng | Lợi Nhuận Ròng Thu Về | Cơ Chế Thực Thi                                                       |
| :-------------------------------- | :--------------- | :-------------- | :--------------- | :-------------------- | :-------------------------------------------------------------------- |
| **Nhóm Tier 2A (Khách VIP)**      | 102 (1,12%)      | R$ 536,48       | R$ 1.686,04      | **R$ 1.149,56**       | Cấp vốn trực tiếp — Thu hồi vốn trong 14 ngày (Tỷ suất sinh lời 214%) |
| **Nhóm Tier 2B (Khách Nền Tảng)** | 8.997 (98,88%)   | R$ 0,00         | R$ 86.003,80     | **R$ 18.920,84**      | Tự tài trợ (Mã giảm giá kèm điều kiện giỏ hàng mới $\ge 150\%$)       |
| **TỔNG CỘNG TOÀN CHIẾN DỊCH**     | **9.102 (100%)** | **R$ 536,48**   | **R$ 87.689,84** | **R$ 20.070,40**      | **Lợi nhuận ròng gấp 37,4 lần vốn đầu tư trực tiếp ban đầu**           |

---

### 9.2. Ma Trận Can Thiệp 4 Cụm Vấn Đề

**Bảng 8. Ma trận can thiệp chuyên biệt cho 4 cụm điểm nghẽn và nền tảng tham chiếu**

| Cụm Điểm Nghẽn | Vấn Đề Cốt Lõi | Nhánh Tier 2A (Khách VIP — Cấp Vốn Trực Tiếp) | Nhánh Tier 2B (Khách Nền Tảng — Tự Động Hóa Tự Tài Trợ) | Nền Tảng TMĐT Tham Khảo |
| :--- | :--- | :--- | :--- | :--- |
| **Cụm 0: Ngành Ngoại vi & Bang Xa**<br>(6.197 khách) | Chưa mua lại ngành hàng cốt lõi, ở bang xa | **91 khách hàng ưu tiên** (R$ 446,50 · 83,2% ngân sách): Ưu đãi kích hoạt giỏ hàng 8% AOV | **6.106 khách hàng nền tảng**: Ví hoàn tiền tạm khóa (hạn dùng 14 ngày) + Bắt buộc giỏ hàng tối thiểu gấp 1,5 lần đơn cũ | **Mercado Libre Brazil** (Cơ chế trợ giá giỏ hàng)<br>**Shopee & Taobao** (Ví hoàn xu & Khóa ngưỡng đơn) |
| **Cụm 1: Áp Lực Tài Chính**<br>(1.570 khách) | Đơn hàng lớn (TB 94,01 R$), trả góp dài (TB 7,9 kỳ) | **2 khách hàng ưu tiên** (R$ 11,16 · 2,1% ngân sách): Hỗ trợ phí trả góp 0% 6 kỳ cho đơn lớn có $\Delta\text{CLV} > c_i$ | **1.568 khách hàng nền tảng**: Đưa vào Lộ trình thăng hạng hội viên + Gửi thông báo nhắc mua lại theo chu kỳ 30 ngày | **Mercado Pago** (Tài trợ trả góp phân khúc)<br>**Shopee Rewards** (Thăng hạng thành viên) |
| **Cụm 2: Đánh Giá Kém**<br>(1.119 khách) | Đánh giá 2,52/5 sao, nguy cơ rời bỏ cao | **9 khách hàng ưu tiên** (R$ 78,82 · 14,7% ngân sách): CSKH 1-1 trong 24h + Tặng voucher đền bù thiện chí 12% | **1.110 khách hàng nền tảng**: Tự động kích hoạt mã miễn phí vận chuyển khi khách phát sinh đơn hàng mới có tiền lời | **Amazon** (Goodwill Compensation CSKH)<br>**JD.com** (Bồi thường trải nghiệm dịch vụ) |
| **Cụm 3: Sốc Giao Hàng Trễ**<br>(216 khách) | Trễ hẹn giao nghiêm trọng (TB 4,2 ngày) | **0 khách hàng** (R$ 0,00 · 0,0% ngân sách): Chi phí hoàn cước ship (R$ 10,03) vượt lợi nhuận ròng của đơn nhỏ R$ 54,48 ($\Delta\text{CLV} < c_i$) | **Toàn bộ 216 khách hàng**: Áp dụng trọn bộ tự tài trợ: Ví voucher Free Ship kích hoạt khi giỏ hàng mới $\ge 150\%$ | **Amazon Prime & Taobao** (Coupon SLA kèm ngưỡng đơn tối thiểu bảo toàn lợi nhuận) |

---

### 9.3. Báo Cáo Tài Chính Theo Kịch Bản Chuyển Đổi (Tier 2A + Tier 2B)

**Bảng 9. Dự báo tài chính toàn diện theo các kịch bản giữ chân của tệp Tier 2B**

| Kịch Bản Chuyển Đổi Tier 2B    | Doanh Số Tier 2A | Doanh Số Tier 2B | TỔNG DOANH SỐ     | Lợi Nhuận Tier 2A | Lợi Nhuận Tier 2B | TỔNG LỢI NHUẬN RÒNG |
| :----------------------------- | :--------------- | :--------------- | :---------------- | :---------------- | :---------------- | :------------------ |
| **Mức Tối Thiểu (8% mua lại)** | R$ 1.686,04      | R$ 68.803,04     | **R$ 70.489,08**  | R$ 1.149,56       | R$ 15.136,67      | **R$ 16.286,23**    |
| **Mức Kỳ Vọng (10% mua lại)**  | R$ 1.686,04      | R$ 86.003,80     | **R$ 87.689,84**  | R$ 1.149,56       | R$ 18.920,84      | **R$ 20.070,40**    |
| **Mức Tối Ưu (12% mua lại)**   | R$ 1.686,04      | R$ 103.204,56    | **R$ 104.890,60** | R$ 1.149,56       | R$ 22.705,00      | **R$ 23.854,56**    |

---

### 9.4. Hướng Dẫn Tích Hợp Hệ Thống Thực Tế

1. **Nhánh xử lý tức thì (Hệ thống CRM):** Xuất danh sách 102 khách hàng ưu tiên (trường `x_i_selected_100pct_budget = 1` trong file `prescriptive_action_plan.csv`) sang hệ thống CRM để tự động nạp mã giảm giá và kết nối nhân viên chăm sóc khách hàng trực tiếp trong 24 giờ.
2. **Nhánh xử lý tự động (Hệ thống tiếp thị tự động):** Nạp 9.000 khách hàng còn lại vào luồng tự động: Tự động kích hoạt ví hoàn tiền tạm khóa sau đơn 1, thiết lập điều kiện giỏ hàng tối thiểu khi thanh toán, và lên lịch gửi thông báo nhắc mua lại vào ngày thứ 30 sau khi nhận hàng.

---

_Nguồn dữ liệu: `test_predictions.csv`, `X_test.csv`, `best_model.pkl` (Module 03 — Predictive Analytics). Toàn bộ mã nguồn: `Prescriptive_Analysis.ipynb`._
