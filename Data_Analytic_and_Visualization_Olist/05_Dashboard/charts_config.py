"""
CHARTS_CONFIG — cấu hình toàn bộ biểu đồ của Dashboard, gom nhóm theo tab.

Cách mở rộng khi có thêm hình cho phần "Phân tích chẩn đoán" hoặc "Dự đoán":
  1. Copy file ảnh vào thư mục assets/
  2. Thêm 1 dict mới vào danh sách "charts" của group tương ứng
     (hoặc tạo group mới trong CHARTS_CONFIG nếu chủ đề chưa có).
  3. Điền đủ: title, file, x_label, y_label, legend (nếu có), insight (1-2 câu).

Mỗi chart-dict cần các khóa:
  title    : Tiêu đề biểu đồ (đã có trong ảnh, dùng lại làm subheader)
  file     : Tên file ảnh trong assets/
  x_label  : Nhãn trục X
  y_label  : Nhãn trục Y
  legend   : Chú thích / giải nghĩa các nhóm màu (None nếu không có nhiều nhóm)
  insight  : 1-2 câu nhận xét về nội dung biểu đồ
"""

CHARTS_CONFIG = {
    "revenue": {
        "tab_label": "💰 Doanh thu & Ngành hàng",
        "charts": [
            {
                "title": "Xu hướng Doanh thu Hàng tháng (01/2017 – 08/2018)",
                "file": "monthly_revenue_trend.png",
                "x_label": "Tháng (Year-Month)",
                "y_label": "Doanh thu (Nghìn R$)",
                "legend": "Đường đỏ đứt nét đánh dấu tháng Black Friday (11/2017), tăng trưởng +207.8% so với tháng liền trước.",
                "insight": (
                    "Doanh thu tăng trưởng khá ổn định trong năm 2017 và đạt đỉnh nhờ hiệu ứng Black Friday "
                    "(11/2017), sau đó phục hồi và lập đỉnh mới quanh tháng 4-5/2018. Tuy nhiên từ tháng 6-8/2018 "
                    "doanh thu có dấu hiệu chững lại và suy giảm nhẹ — phù hợp với nghi vấn ban đầu của Ban giám đốc."
                ),
            },
            {
                "title": "Top 10 Ngành hàng có Doanh thu Cao nhất",
                "file": "top10_categories.png",
                "x_label": "Tổng doanh thu (Triệu R$)",
                "y_label": "Tên ngành hàng",
                "legend": None,
                "insight": (
                    "cama_mesa_banho dẫn đầu doanh thu (R$0.91M), theo sau là beleza_saude (R$0.84M) và "
                    "esporte_lazer (R$0.74M). Đây là 3 ngành hàng chủ lực nên được ưu tiên nguồn lực giữ chân khách hàng."
                ),
            },
            {
                "title": "Biểu đồ Pareto Ngành hàng: Căn cứ Khoa học Giảm chiều & Gộp nhóm `cat_outros`",
                "file": "factor5_pareto_categories.png",
                "x_label": "Danh mục ngành hàng (Product Categories)",
                "y_label": "Số lượng mặt hàng bán ra (Frequency) — trục trái | Tỷ lệ tích lũy % — trục phải",
                "legend": "Đường đỏ: % tích lũy. Đường đứt nét đỏ: ngưỡng Top 10 ngành hàng được giữ lại làm đặc trưng one-hot cho mô hình; 64 ngành đuôi dài còn lại được gộp chung vào nhóm `cat_outros`.",
                "insight": (
                    "Top 10 ngành hàng (dẫn đầu bởi cama_mesa_banho, beleza_saude, esporte_lazer) chiếm 64.74% tổng "
                    "số lượt bán; 64 ngành hàng còn lại được gộp vào nhóm `cat_outros` để giảm chiều dữ liệu trước "
                    "khi đưa vào mô hình dự đoán, tránh việc one-hot encoding sinh ra quá nhiều cột đặc trưng thưa "
                    "(sparse features)."
                ),
            },
        ],
    },
    "customer": {
        "tab_label": "👥 Khách hàng & Thanh toán",
        "charts": [
            {
                "title": "Phân bố Chi tiêu Khách hàng (Skewness = 9.32)",
                "file": "aov_distribution.png",
                "x_label": "Tổng chi tiêu BRL (R$)",
                "y_label": "Số lượng khách hàng",
                "legend": "Đường đỏ: Median ($107.78). Đường cam: Mean ($165.94). Boxplot bên phải thể hiện các điểm ngoại lai.",
                "insight": (
                    "Phân phối chi tiêu lệch phải rất mạnh (skewness ≈ 9.32); trung vị ($107.78) thấp hơn nhiều so "
                    "với trung bình ($165.94) cho thấy đa số khách chi tiêu thấp trong khi một nhóm nhỏ khách VIP "
                    "kéo giá trị trung bình lên cao — cần chính sách giữ chân riêng cho nhóm VIP này."
                ),
            },
            {
                "title": "Tỷ trọng Phương thức Thanh toán",
                "file": "payment_methods_donut.png",
                "x_label": None,
                "y_label": None,
                "legend": "credit_card (74.0%) · boleto (19.0%) · voucher (5.4%) · debit_card (1.5%)",
                "insight": (
                    "Thẻ tín dụng áp đảo với 74% giao dịch, tiếp theo là boleto (19%); voucher chỉ chiếm 5.4%, cho "
                    "thấy dư địa để đẩy mạnh chiến dịch voucher/khuyến mãi giữ chân khách hàng còn khá lớn."
                ),
            },
        ],
    },
    "churn": {
        "tab_label": "🔄 Hành vi Mua lặp lại & Churn",
        "charts": [
            {
                "title": "Tỷ lệ Khách hàng Mua 1 lần vs Mua lặp lại & Tỷ lệ Churn",
                "file": "population_proportions.png",
                "x_label": None,
                "y_label": None,
                "legend": (
                    "Biểu đồ trái: Mua 1 lần (F=1) vs Mua lặp lại (F≥2), N=92,077. "
                    "Biểu đồ phải: Active (Recency<90 ngày) vs Churn (Recency≥90 ngày)."
                ),
                "insight": (
                    "Chỉ 2.98% khách hàng (2,747 người) từng mua lặp lại, trong khi tới 80.02% khách hàng đang ở "
                    "trạng thái churn (không mua lại quá 90 ngày) — con số này xác nhận trực tiếp nghi ngờ của Ban "
                    "giám đốc về tỷ lệ khách quay lại mua hàng đang suy giảm."
                ),
            },
            {
                "title": "Phân bố Chu kỳ Mua lặp lại: Trước và Sau khi lọc đơn cùng phiên",
                "file": "repeat_interval_distribution.png",
                "x_label": "Số ngày giữa 2 đơn / 2 phiên mua hàng",
                "y_label": "Tần suất",
                "legend": "Biểu đồ trái: dữ liệu thô (gồm 900 lượt <1 ngày do đặt nhiều đơn cùng phiên). Biểu đồ phải: đã lọc, thể hiện Median, Q3 và ngưỡng churn 90 ngày.",
                "insight": (
                    "Sau khi loại bỏ 900 đơn hàng phát sinh cùng phiên (không phản ánh hành vi quay lại thực sự), "
                    "chu kỳ mua lặp lại thực tế có trung vị 71 ngày — thấp hơn ngưỡng churn 90 ngày được thiết lập, "
                    "cho thấy phần lớn khách quay lại vẫn nằm trong vùng an toàn nếu được chăm sóc kịp thời."
                ),
            },
            {
                "title": "Phân bố Chu kỳ Mua lại Thực tế & Cửa sổ Vàng Giữ chân [90–180 ngày]",
                "file": "repeat_interval_filtered.png",
                "x_label": "Số ngày giữa 2 phiên mua hàng độc lập (Days)",
                "y_label": "Số lượng khách hàng tái mua",
                "legend": "Q1 = 23.1 ngày · Median (ngưỡng churn) = 71 ngày · Q3 (cửa sổ vàng) = 171.4 ngày · Vùng vàng tô sáng = 90–180 ngày.",
                "insight": (
                    "Phần lớn khách quay lại mua hàng trong vòng 23–71 ngày; khoảng 90–180 ngày ('cửa sổ vàng') là "
                    "giai đoạn then chốt để triển khai chiến dịch remarketing trước khi khách chính thức bị tính là churn."
                ),
            },
        ],
    },
    "delivery": {
        "tab_label": "🚚 Trải nghiệm Giao hàng",
        "charts": [
            {
                "title": "Phân bố Độ trễ Giao hàng theo Review Score",
                "file": "delivery_delay_vs_review.png",
                "x_label": "Review Score (1–5)",
                "y_label": "Độ trễ giao hàng (ngày; âm = giao sớm, dương = giao trễ)",
                "legend": "Đường đứt nét ngang: mốc đúng hẹn (0 ngày). Mỗi violin ứng với 1 mức review score.",
                "insight": (
                    "Nhóm khách đánh giá 1 sao có xu hướng nhận hàng trễ nhiều hơn rõ rệt so với nhóm 5 sao "
                    "(phân phối lệch hẳn về phía dương/trễ hạn), cho thấy giao hàng trễ là một nguyên nhân chính "
                    "dẫn đến trải nghiệm tiêu cực và có thể là yếu tố thúc đẩy churn."
                ),
            },
        ],
    },
}


# =============================================================================
# TAB 2 — PHÂN TÍCH CHẨN ĐOÁN (DIAGNOSTIC ANALYSIS)
# So sánh nhóm Active (<90 ngày) vs Churn (>=90 ngày) theo 6 yếu tố nghi vấn,
# mỗi yếu tố đều có kiểm định thống kê (Z-test / Mann-Whitney U / Chi-Square).
# =============================================================================

DIAGNOSTIC_CONFIG = {
    "factor1": {
        "tab_label": "🚚 Yếu tố 1: Giao hàng trễ",
        "charts": [
            {
                "title": "So sánh Tỷ lệ Giao trễ giữa Nhóm Active và Churn",
                "file": "factor1_late_delivery.png",
                "x_label": "Nhóm khách hàng",
                "y_label": "Tỷ lệ Đơn hàng Giao trễ (%)",
                "legend": "Xanh: Active (<90 ngày) · Cam: Churn (≥90 ngày). Z-test p < 0.001.",
                "insight": (
                    "Tỷ lệ đơn hàng giao trễ ở nhóm churn (6.25%) cao gấp ~1.8 lần nhóm active (3.54%), khác biệt "
                    "có ý nghĩa thống kê (Z-test p < 0.001) — giao hàng trễ là một yếu tố rủi ro churn rõ ràng."
                ),
            },
            {
                "title": "Tỷ lệ Giao trễ Nội bộ & Quy mô Thất thoát Tuyệt đối",
                "file": "factor1_late_delivery_count.png",
                "x_label": "Nhóm khách hàng",
                "y_label": "(A) Tỷ lệ Giao trễ (%) · (B) Số lượng khách hàng bị giao trễ",
                "legend": "(A) So sánh tỷ lệ trễ nội bộ từng nhóm, chênh lệch +2.05% (Z=14.17, p<0.001). (B) Quy mô tuyệt đối: trong toàn bộ khách từng bị giao trễ, 87.6% đã rời bỏ.",
                "insight": (
                    "Xét theo cách tính mở rộng, tỷ lệ giao trễ ở nhóm churn (7.50%) vẫn cao hơn có ý nghĩa so với "
                    "active (5.45%). Đáng chú ý nhất: trong toàn bộ khách từng bị giao hàng trễ, có tới 87.6% đã "
                    "rời bỏ — cho thấy chỉ một trải nghiệm giao trễ cũng để lại hậu quả churn rất lớn."
                ),
            },
        ],
    },
    "factor2": {
        "tab_label": "💸 Yếu tố 2: Tỷ trọng Phí ship",
        "charts": [
            {
                "title": "Boxplot Tỷ trọng Phí ship (freight_ratio) giữa 2 Nhóm",
                "file": "factor2_freight_ratio_hist.png",
                "x_label": "Nhóm khách hàng (is_churn)",
                "y_label": "Tỷ trọng Phí ship (freight_ratio = phí ship / giá trị đơn hàng)",
                "legend": "Xanh: Active (<90 ngày) · Cam: Churn (≥90 ngày). p < 0.001.",
                "insight": (
                    "Hai boxplot gần như chồng khít lên nhau về hình dạng phân phối, cho thấy khác biệt thực tế "
                    "giữa 2 nhóm rất nhỏ dù kiểm định cho kết quả có ý nghĩa thống kê."
                ),
            },
            {
                "title": "Phân bố Tỷ trọng Phí ship (%) giữa Nhóm Churn vs Active",
                "file": "factor2_freight_ratio.png",
                "x_label": "Tỷ trọng Phí ship trên Tổng giá trị Đơn hàng (%)",
                "y_label": "Mật độ Phân phối (Density)",
                "legend": "Active (<90 ngày) — Median: 19.2% · Churn (≥90 ngày) — Median: 18.3%. Mann-Whitney U p < 0.001.",
                "insight": (
                    "Trung vị tỷ trọng phí ship giữa 2 nhóm chỉ chênh lệch 0.9 điểm % (19.2% vs 18.3%); do cỡ mẫu "
                    "rất lớn (N≈92,077) nên kiểm định dễ đạt ý nghĩa thống kê dù độ lớn khác biệt thực tế nhỏ — "
                    "freight_ratio nhiều khả năng KHÔNG phải yếu tố dự báo churn mạnh."
                ),
            },
        ],
    },
    "factor3": {
        "tab_label": "📦 Yếu tố 3: Số ngày Giao trễ",
        "charts": [
            {
                "title": "So sánh Số ngày Giao trễ giữa 2 Nhóm",
                "file": "factor3_delivery_delay_hist.png",
                "x_label": "Nhóm khách hàng (is_churn)",
                "y_label": "Số ngày Giao trễ (Dương = Trễ, Âm = Sớm)",
                "legend": "Xanh: Active (<90 ngày) · Cam: Churn (≥90 ngày). Mann-Whitney U p = 0.7554 (không có ý nghĩa thống kê).",
                "insight": (
                    "Không có khác biệt có ý nghĩa thống kê về số ngày giao trễ giữa 2 nhóm (p = 0.7554 > 0.05); "
                    "phân phối 2 nhóm gần như trùng khít nhau."
                ),
            },
            {
                "title": "Phân bố Số ngày Giao trễ (Âm = Sớm, Dương = Trễ)",
                "file": "factor3_delivery_delay.png",
                "x_label": "Số ngày Giao hàng so với Hẹn ước (ngày)",
                "y_label": "Mật độ Phân phối (Density)",
                "legend": "Đường đỏ đứt nét: mốc hạn giao cam kết (0 ngày). Active — Median: -11.2 ngày · Churn — Median: -12.0 ngày.",
                "insight": (
                    "Cả 2 nhóm đều giao hàng sớm hơn hẹn ước trung bình 11-12 ngày và phân phối gần như trùng nhau "
                    "(p = 0.7554). Điều này cho thấy 'số ngày trễ tuyệt đối' không phải yếu tố phân biệt churn hiệu "
                    "quả — ngược lại, việc CÓ bị trễ hay không (xem Yếu tố 1) mới là tín hiệu quan trọng hơn."
                ),
            },
        ],
    },
    "factor4": {
        "tab_label": "⭐ Yếu tố 4: Đánh giá Xấu",
        "charts": [
            {
                "title": "Tỷ lệ Review Xấu Nội bộ & Quy mô Thất thoát Tuyệt đối",
                "file": "factor4_bad_review.png",
                "x_label": "Nhóm khách hàng",
                "y_label": "(A) Tỷ lệ Đánh giá Xấu 1-2 sao (%) · (B) Số lượng khách hàng đánh giá xấu",
                "legend": "(A) So sánh nội bộ: chênh lệch +2.97% (Z=11.02, p<0.001). (B) 84.0% khách từng đánh giá xấu đã churn.",
                "insight": (
                    "Tỷ lệ khách đánh giá xấu (1-2 sao) ở nhóm churn (12.45%) cao hơn có ý nghĩa so với active "
                    "(9.48%), chênh lệch +2.97 điểm % (p < 0.001). Đáng báo động hơn: 84% trong toàn bộ khách từng "
                    "đánh giá xấu đã rời bỏ — review xấu là tín hiệu cảnh báo churn rất mạnh, cần can thiệp ngay "
                    "bằng gói bồi thường trải nghiệm."
                ),
            },
            {
                "title": "So sánh Tỷ lệ và Quy mô Khách hàng Đánh giá Xấu (bản đối chiếu)",
                "file": "factor4_bad_review_count.png",
                "x_label": "Nhóm khách hàng",
                "y_label": "(A) Tỷ lệ Đánh giá Xấu (%) · (B) Số lượng Khách hàng Đánh giá 1-2 sao",
                "legend": "Kết quả tương đồng với biểu đồ bên trái (9.45% vs 12.38%; 1,738 vs 9,118 khách, 84.0%), dùng để đối chiếu chéo kết quả tính toán.",
                "insight": (
                    "Kết quả đối chiếu cho ra con số gần như trùng khớp với biểu đồ đầu tiên, củng cố độ tin cậy "
                    "của kết luận: đánh giá xấu là một trong những yếu tố dự báo churn mạnh và nhất quán nhất."
                ),
            },
        ],
    },
    "factor5": {
        "tab_label": "🏷️ Yếu tố 5: Ngành hàng",
        "charts": [
            {
                "title": "Tỷ lệ Churn theo Ngành hàng & Quy mô Đơn hàng Top 10",
                "file": "factor5_category_churn.png",
                "x_label": "(A) Tỷ lệ Churn (%) · (B) Tổng số Đơn hàng (Quy mô)",
                "y_label": "Top 10 Ngành hàng",
                "legend": "Đường xanh đứt nét: Churn trung bình toàn sàn (80.0%). Chi-Square p < 0.001.",
                "insight": (
                    "Tỷ lệ churn khác biệt rõ theo ngành hàng (Chi-Square p<0.001): brinquedos (87.1%), "
                    "moveis_decoracao (84.8%) và telefonia (84.6%) có churn cao nhất, vượt xa mức TB toàn sàn "
                    "(80.0%); ngược lại beleza_saude (73.8%) và utilidades_domesticas (74.5%) giữ chân khách tốt "
                    "hơn hẳn — các chiến dịch giữ chân nên ưu tiên nhóm ngành churn cao nhưng vẫn có quy mô doanh "
                    "thu lớn (như cama_mesa_banho, esporte_lazer)."
                ),
            },
            {
                "title": "Biểu đồ Pareto Ngành hàng: Top 15 chiếm 80.05%",
                "file": "pareto_categories.png",
                "x_label": "Danh mục Ngành hàng (đã sắp xếp giảm dần)",
                "y_label": "Số lượng Mặt hàng Bán ra — trục trái | Tỷ lệ Tích lũy % — trục phải",
                "legend": "Đường đỏ: % tích lũy. Đường xanh đứt nét: ngưỡng Pareto 80% (đạt tại rank 15: bebes).",
                "insight": (
                    "Theo góc nhìn Pareto cổ điển (ngưỡng 80%), cần tới 15 ngành hàng mới đạt 80.05% tổng sản "
                    "lượng bán ra — đây là căn cứ để đối chiếu với quyết định giảm chiều dữ liệu mô hình (chỉ giữ "
                    "Top 10 ngành + `cat_outros`, xem Tab Mô tả Dữ liệu) nhằm cân bằng giữa độ chính xác và độ "
                    "phức tạp của mô hình."
                ),
            },
        ],
    },
    "factor6": {
        "tab_label": "🗺️ Yếu tố 6: Vùng địa lý",
        "charts": [
            {
                "title": "Tỷ lệ Churn theo Bang Địa lý & Quy mô Khách hàng Top 10 Bang",
                "file": "factor6_state_churn.png",
                "x_label": "(A) Tỷ lệ Churn (%) · (B) Tổng số Khách hàng (Quy mô)",
                "y_label": "Top 10 Bang (State)",
                "legend": "Đường xanh đứt nét: Churn trung bình toàn sàn (80.0%). Chi-Square p < 0.001.",
                "insight": (
                    "Tỷ lệ churn dao động 77.6% (DF) đến 82.5% (SC) tùy theo bang (Chi-Square p<0.001). SP là bang "
                    "chiếm quy mô khách hàng lớn nhất (38,989 khách, ~42% tổng số) nhưng lại có tỷ lệ churn thấp "
                    "nhất nhì (78.1%), thấp hơn mức trung bình toàn sàn."
                ),
            },
            {
                "title": "Phân hóa Tỷ lệ Churn theo Vùng Địa lý: Lợi thế Tầng lớp Trung lưu Đô thị Đông Nam",
                "file": "factor6_state_socioeconomic.png",
                "x_label": "Bang Địa lý (State)",
                "y_label": "Tỷ lệ Churn (%)",
                "legend": "Xanh: Vùng kinh tế phát triển (DF, SP, PR) — churn thấp hơn TB. Cam: Vùng ngoại vi (BA, MG, ES, RJ, GO, RS, SC) — churn cao hơn TB. Đường đỏ đứt nét: Churn TB toàn sàn (80.02%).",
                "insight": (
                    "Các bang thuộc vùng kinh tế phát triển (DF, SP, PR) đều có tỷ lệ churn thấp hơn mức trung bình "
                    "toàn sàn (80.02%), trong khi toàn bộ các bang ngoại vi (BA, MG, ES, RJ, GO, RS, SC) đều churn "
                    "cao hơn mức trung bình — gợi ý yếu tố kinh tế-xã hội vùng miền có liên hệ với khả năng giữ "
                    "chân khách hàng, và ngân sách marketing giữ chân nên được phân bổ ưu tiên hơn cho các bang "
                    "ngoại vi."
                ),
            },
        ],
    },
}


# =============================================================================
# TAB 3 — DỰ ĐOÁN CHURN: CHUẨN BỊ DỮ LIỆU, MÔ HÌNH BASELINE VS ADVANCED, SHAP
# =============================================================================

MODEL_CONFIG = {
    "data_prep": {
        "tab_label": "🗂️ Chuẩn bị Dữ liệu cho Mô hình",
        "charts": [
            {
                "title": "Ma trận Tương quan Pearson: Sàng lọc Đặc trưng Giai đoạn 2",
                "file": "corr_heatmap.png",
                "x_label": "Đặc trưng (Feature)",
                "y_label": "Đặc trưng (Feature)",
                "legend": "Màu đỏ: tương quan dương mạnh. Màu xanh dương: tương quan âm. Hàng/cột `is_retain` là biến mục tiêu.",
                "insight": (
                    "Hầu hết đặc trưng có tương quan tuyến tính rất yếu với biến mục tiêu is_retain (|r| ≤ 0.02) — "
                    "cho thấy churn khó giải thích bằng quan hệ tuyến tính đơn giản, cần mô hình phi tuyến. Đồng "
                    "thời, delivery_speed_ratio tương quan rất cao với delivery_days/delivery_delay/is_late "
                    "(r > 0.7) nên cần loại bớt để tránh đa cộng tuyến trước khi đưa vào mô hình."
                ),
            },
            {
                "title": "Biểu đồ Kiểm định VIF của Đặc trưng sau khi Sàng lọc Toán học",
                "file": "vif_comparison.png",
                "x_label": "Hệ số Phóng đại Phương sai (VIF)",
                "y_label": "Đặc trưng (Feature)",
                "legend": "Đường chấm cam: ngưỡng an toàn lý tưởng (VIF=2.0). Đường đứt nét đỏ: ngưỡng cảnh báo đa cộng tuyến (VIF=5.0).",
                "insight": (
                    "Sau khi loại các đặc trưng tương quan cao ở bước trước, toàn bộ 12 đặc trưng còn lại đều có "
                    "VIF < 5.0; pay_credit_card (4.18) và pay_boleto (3.95) cao nhất nhưng vẫn trong ngưỡng chấp "
                    "nhận được — bộ đặc trưng đủ điều kiện đưa vào mô hình mà không gặp vấn đề đa cộng tuyến "
                    "nghiêm trọng."
                ),
            },
            {
                "title": "Phân bố Tập Huấn luyện (Train) và Tập Kiểm thử (Test) theo Thời gian",
                "file": "time_split_distribution.png",
                "x_label": "Tháng mua hàng đầu tiên (First Purchase Month)",
                "y_label": "Số lượng Khách hàng mới",
                "legend": "Xanh: Tập Train (10/2016 – 04/2018). Đỏ: Tập Test (05/2018 – 08/2018). Đường đứt nét: mốc cutoff split (30/04/2018).",
                "insight": (
                    "Dữ liệu được chia theo mốc thời gian (time-based split) tại 30/04/2018 thay vì chia ngẫu "
                    "nhiên, nhằm mô phỏng đúng bối cảnh dự báo thực tế (dùng quá khứ dự đoán tương lai) và tránh "
                    "rò rỉ dữ liệu (data leakage); tập test gồm khách hàng mua lần đầu trong 4 tháng gần nhất."
                ),
            },
            {
                "title": "Biểu đồ Pareto Ngành hàng (đối chiếu ở giai đoạn xây dựng mô hình)",
                "file": "pareto_categories_modelstage.png",
                "x_label": "Danh mục Ngành hàng (đã sắp xếp giảm dần)",
                "y_label": "Số lượng Mặt hàng Bán ra — trục trái | Tỷ lệ Tích lũy % — trục phải",
                "legend": "Đường đỏ: % tích lũy. Đường xanh đứt nét: ngưỡng Pareto 80% (đạt tại rank 15: bebes).",
                "insight": (
                    "Bản Pareto này được tính lại ở giai đoạn xây dựng mô hình để đối chiếu chéo với kết quả ở "
                    "Tab Phân tích Chẩn đoán — số liệu tương đồng (Top 15 ngành ≈ 80%), xác nhận tính nhất quán "
                    "của phân phối ngành hàng giữa các giai đoạn phân tích khác nhau trong dự án, trước khi áp "
                    "dụng quyết định giảm chiều cuối cùng (Top 10 + `cat_outros`, xem Tab Mô tả Dữ liệu)."
                ),
            },
        ],
    },
    "baseline": {
        "tab_label": "📉 Mô hình Baseline",
        "charts": [
            {
                "title": "Đường cong ROC & Precision-Recall — Mô hình Baseline (Logistic Regression)",
                "file": "baseline_roc_pr_curves.png",
                "x_label": "False Positive Rate / Recall",
                "y_label": "True Positive Rate / Precision",
                "legend": "Đường xám đứt nét (ROC): mốc đoán ngẫu nhiên. Đường xám đứt nét (PR): tỷ lệ nền (Baseline Chance = 1.48%).",
                "insight": (
                    "Mô hình baseline (Logistic Regression) chỉ đạt AUC-ROC = 0.5346 — gần như không tốt hơn đoán "
                    "ngẫu nhiên (0.5). AUC-PR = 0.0264, cao hơn tỷ lệ nền (1.48%) nhưng vẫn cho thấy khả năng phân "
                    "biệt khách 'giữ chân' rất yếu — đúng như kỳ vọng của một mô hình baseline đơn giản, dùng làm "
                    "mốc so sánh cho mô hình nâng cao."
                ),
            },
        ],
    },
    "comparison": {
        "tab_label": "⚖️ So sánh Baseline vs Advanced",
        "charts": [
            {
                "title": "Đối sánh Đường cong ROC & Precision-Recall: Baseline vs Advanced (XGBoost)",
                "file": "model_roc_pr_curves.png",
                "x_label": "False Positive Rate / Recall",
                "y_label": "True Positive Rate / Precision",
                "legend": "Xanh đứt nét: Baseline Logistic Regression (AUC-ROC=0.5346, AUC-PR=0.0264). Đỏ: Advanced XGBoost (AUC-ROC=0.5187, AUC-PR=0.0155).",
                "insight": (
                    "⚠️ Đáng chú ý: mô hình nâng cao XGBoost cho kết quả THẤP HƠN baseline trên cả 2 chỉ số "
                    "(ROC-AUC 0.5187 so với 0.5346; PR-AUC 0.0155 so với 0.0264). Điều này cho thấy mô hình phức "
                    "tạp hơn không tự động đảm bảo hiệu suất tốt hơn, đặc biệt khi tỷ lệ lớp dương rất mất cân "
                    "bằng (1.48%) và tín hiệu đặc trưng còn yếu (xem ma trận tương quan). Cần thử thêm: xử lý mất "
                    "cân bằng lớp (SMOTE/class_weight), tinh chỉnh hyperparameter, hoặc bổ sung đặc trưng hành vi "
                    "mới thay vì chỉ đổi thuật toán."
                ),
            },
        ],
    },
    "explainability": {
        "tab_label": "🔍 Diễn giải Mô hình (SHAP)",
        "charts": [
            {
                "title": "SHAP Summary Plot: Tầm quan trọng & Đóng góp biên của 23 Đặc trưng",
                "file": "feature_importance_shap.png",
                "x_label": "SHAP value (impact on model output)",
                "y_label": "Đặc trưng (Feature), sắp xếp theo mức độ quan trọng giảm dần",
                "legend": "Mỗi điểm là 1 khách hàng. Màu đỏ/hồng: giá trị đặc trưng cao. Màu xanh dương: giá trị đặc trưng thấp. Vị trí ngang: mức ảnh hưởng đến output mô hình.",
                "insight": (
                    "Các đặc trưng vùng địa lý (state_SP, state_outros, state_Sul, state_RJ, state_MG) có ảnh "
                    "hưởng lớn nhất đến dự đoán, tiếp theo là review_score và các nhóm ngành hàng (cat_*) — phù "
                    "hợp với phát hiện ở Tab 2 (Yếu tố 5 & 6). Tuy nhiên cần lưu ý: SHAP importance cao không đồng "
                    "nghĩa mô hình dự đoán chính xác (AUC vẫn thấp) — nó chỉ cho biết đặc trưng nào đóng góp nhiều "
                    "nhất vào output của mô hình hiện tại, không đảm bảo output đó đúng."
                ),
            },
        ],
    },
}
