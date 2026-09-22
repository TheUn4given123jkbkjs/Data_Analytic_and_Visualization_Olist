"""
CHARTS_CONFIG - Cấu hình toàn bộ biểu đồ và nhận xét chuyên sâu của Dashboard.
Gom nhóm theo 4 giai đoạn phân tích học thuật:
  1. CHARTS_CONFIG: 01. Phân tích Mô tả (EDA)
  2. DIAGNOSTIC_CONFIG: 02. Phân tích Chẩn đoán (Diagnostic Hypotheses)
  3. MODEL_CONFIG: 03. Đánh giá Mô hình Dự báo (Baseline vs XGBoost Giai đoạn 2)
  4. PRESCRIPTIVE_CONFIG: 04. Chiến lược Chỉ định & Tối ưu hóa Ngân sách (Knapsack & Dual-Engine)
"""

# =============================================================================
# 01. PHÂN TÍCH MÔ TẢ (DESCRIPTIVE ANALYTICS - EDA)
# =============================================================================
CHARTS_CONFIG = {
    "revenue": {
        "tab_label": "Doanh thu & Ngành hàng",
        "charts": [
            {
                "title": "Xu hướng Doanh thu Hàng tháng (01/2017 – 08/2018)",
                "file": "monthly_revenue_trend.png",
                "x_label": "Tháng giao dịch (Year-Month)",
                "y_label": "Doanh thu (Nghìn R$)",
                "legend": "Đường đỏ đứt nét: Đỉnh Black Friday (11/2017), tăng trưởng +207.8% so với tháng trước.",
                "allowed_directions": ["bottom"],
                "insight": (
                    "Doanh thu tăng trưởng mạnh mẽ trong năm 2017 và đạt đỉnh nhờ Black Friday (11/2017), "
                    "tiếp tục lập đỉnh mới vào tháng 4-5/2018. Tuy nhiên từ tháng 6-8/2018 doanh thu có dấu hiệu "
                    "chững lại do tỷ lệ khách quay lại mua lần 2 cực kỳ thấp."
                ),
            },
            {
                "title": "Top 10 Ngành hàng có Doanh thu Cao nhất Toàn sàn",
                "file": "top10_categories.png",
                "x_label": "Tổng doanh thu (Triệu R$)",
                "y_label": "Tên ngành hàng",
                "legend": None,
                "allowed_directions": ["bottom"],
                "insight": (
                    "cama_mesa_banho dẫn đầu doanh thu (0.91M R$), theo sau là beleza_saude (0.84M R$) và "
                    "esporte_lazer (0.74M R$). Đây là 3 ngành hàng đầu tàu đóng góp phần lớn dòng tiền của sàn Olist."
                ),
            },
            {
                "title": "Biểu đồ Pareto Ngành hàng: Căn cứ Giảm chiều Dữ liệu (Quy tắc 80/20)",
                "file": "factor5_pareto_categories.png",
                "x_label": "Danh mục ngành hàng (Product Categories)",
                "y_label": "Số lượng bán ra (Trục trái) | % Tích lũy (Trục phải)",
                "legend": "Đường đỏ: % tích lũy. Đường đứt nét đỏ: Ngưỡng Top 15 ngành hàng chiếm 80.05% lượng bán.",
                "allowed_directions": ["bottom"],
                "insight": (
                    "Theo nguyên lý Pareto 80/20: Top 15 ngành hàng chủ lực chiếm đúng 80.05% tổng số lượng bán ra "
                    "(được giữ lại làm 15 cột One-Hot encoding). Toàn bộ 59 ngành hàng đuôi dài còn lại (chỉ chiếm 19.95%) "
                    "được gộp chung vào một biến đại diện duy nhất `cat_outros` nhằm tránh bùng nổ chiều dữ liệu (Curse of Dimensionality)."
                ),
            },
        ],
    },
    "customer_payment": {
        "tab_label": "Khách hàng & Thanh toán",
        "charts": [
            {
                "title": "Cơ cấu Phương thức Thanh toán (Payment Methods)",
                "file": "payment_methods_donut.png",
                "x_label": None,
                "y_label": None,
                "legend": "Credit Card (73.7%), Boleto (19.0%), Voucher (5.6%), Debit Card (1.7%).",
                "allowed_directions": ["right"],
                "img_scale": 0.60,
                "insight": (
                    "Thẻ tín dụng chiếm áp đảo (73.7%), cho thấy thói quen trả góp rất phổ biến tại Brazil. "
                    "Boleto chiếm 19.0% và thường gắn liền với các đơn hàng B2B giá trị lớn."
                ),
            },
            {
                "title": "Phân phối Giá trị Đơn hàng (AOV Distribution)",
                "file": "aov_distribution.png",
                "x_label": "Giá trị đơn hàng (R$)",
                "y_label": "Mật độ phân phối (Density)",
                "legend": "Đường cam: Trung vị AOV (107.78 R$). Đường đỏ: Trung bình AOV (165.94 R$).",
                "allowed_directions": ["right"],
                "insight": (
                    "Phân phối lệch phải mạnh (Right-skewed, Skewness = 9.32). Trung vị AOV (107.78 R$) "
                    "thấp hơn đáng kể so với trung bình (165.94 R$), đòi hỏi phải dùng trung vị hoặc chuẩn hóa "
                    "để tránh bị nhiễu bởi các đơn hàng ngoại lai."
                ),
            },
        ],
    },
    "retention_churn": {
        "tab_label": "Hành vi Mua lặp lại & Churn",
        "charts": [
            {
                "title": "Tỷ lệ Quần thể Khách hàng & Khoảng Tin cậy 95%",
                "file": "population_proportions.png",
                "x_label": "Phân loại Khách hàng",
                "y_label": "Tỷ lệ trong Quần thể (%)",
                "legend": "Mua 1 lần: 97.02% [96.91%, 97.13%]. Mua lặp lại: 2.98% [2.87%, 3.09%]. Churn: 80.02%.",
                "allowed_directions": ["bottom"],
                "insight": (
                    "97.02% khách hàng chỉ mua đúng 1 lần duy nhất trong toàn bộ vòng đời. Tỷ lệ giữ chân "
                    "tự nhiên chỉ đạt 2.98% toàn sàn và 1.48% trong cửa sổ 90 ngày — xác nhận bài toán Churn là "
                    "vấn đề sống còn của doanh nghiệp."
                ),
            },
            {
                "title": "Phân phối Khoảng cách Thời gian Mua lại (Đã lọc đơn cùng ngày ≤ 1 ngày)",
                "file": "repeat_interval_filtered.png",
                "x_label": "Số ngày giữa 2 lần mua liên tiếp (Repeat Interval > 1 ngày)",
                "y_label": "Số lượng khách hàng",
                "legend": "Đường đỏ: Ngưỡng 90 ngày (Căn cứ định nghĩa Churn trong nghiên cứu). Đã loại bỏ đơn cùng ngày (Interval ≤ 1).",
                "allowed_directions": ["right"],
                "insight": (
                    "Sau khi loại bỏ các giao dịch mua nhiều món cùng ngày (Interval ≤ 1), phần lớn khách hàng mua lặp lại "
                    "đều phát sinh đơn tiếp theo trong vòng 90 ngày đầu tiên. Sau 90 ngày, xác suất mua lại tiệm cận về 0, "
                    "chứng minh mốc cutoff 90 ngày là chuẩn mực khoa học chuẩn xác."
                ),
            },
        ],
    },
    "logistics": {
        "tab_label": "Trải nghiệm Giao hàng",
        "charts": [
            {
                "title": "Tương quan giữa Số ngày Giao trễ và Điểm Đánh giá (Review Score)",
                "file": "delivery_delay_vs_review.png",
                "x_label": "Độ lệch giao hàng (Số ngày trễ > 0 hoặc sớm < 0)",
                "y_label": "Điểm đánh giá trung bình (1 - 5 sao)",
                "legend": "Đường xanh: Giao đúng/sớm hạn (Review ~ 4.2 sao). Đường đỏ: Giao trễ hạn (Review tụt dốc < 2.0 sao).",
                "allowed_directions": ["right"],
                "insight": (
                    "Khi đơn hàng bị giao trễ quá 5 ngày, điểm đánh giá của khách hàng tụt dốc không phanh "
                    "từ 4.2 sao xuống dưới 1.8 sao — Logistics chính là điểm nghẽn trải nghiệm nghiêm trọng nhất."
                ),
            },
        ],
    },
}

# =============================================================================
# 02. PHÂN TÍCH CHẨN ĐOÁN (DIAGNOSTIC HYPOTHESES)
# =============================================================================
DIAGNOSTIC_CONFIG = {
    "factor2": {
        "tab_label": "1. Tỷ trọng Phí Ship (Freight Ratio)",
        "charts": [
            {
                "title": "Phân phối Tỷ trọng Phí Vận chuyển / Tổng Đơn hàng",
                "file": "factor2_freight_ratio_hist.png",
                "x_label": "Trạng thái Khách hàng",
                "y_label": "Tỷ trọng Phí vận chuyển (Freight Ratio)",
                "legend": "Churn: 18.3% vs Active: 19.2%. Mann-Whitney U p > 0.05.",
                "allowed_directions": ["right"],
                "insight": (
                    "Tỷ trọng phí ship giữa nhóm Churn và Active gần như không có sự khác biệt có ý nghĩa thống kê "
                    "(18.3% so với 19.2%). Phí ship không phải là rào cản chính gây rời bỏ."
                ),
            },
        ],
    },
    "factor3": {
        "tab_label": "2. Số ngày Trễ (Delivery Delay)",
        "charts": [
            {
                "title": "Phân phối Số ngày Giao trễ Tuyệt đối (Chỉ tính các đơn trễ)",
                "file": "factor3_delivery_delay_hist.png",
                "x_label": "Trạng thái Khách hàng",
                "y_label": "Số ngày giao trễ (Days)",
                "legend": "Mann-Whitney U p = 0.7554 (Không có ý nghĩa thống kê).",
                "allowed_directions": ["right"],
                "insight": (
                    "Khi đã bị giao trễ, số ngày trễ trung bình của nhóm Churn và Active là tương đương nhau. "
                    "Điều này cho thấy việc 'bị trễ hay không' quan trọng hơn là 'trễ bao nhiêu ngày'."
                ),
            },
            {
                "title": "Tỷ lệ Giao hàng Trễ: Nhóm Churn vs Nhóm Active",
                "file": "factor1_late_delivery.png",
                "x_label": "Trạng thái Khách hàng",
                "y_label": "Tỷ lệ Đơn hàng bị Giao trễ (%)",
                "legend": "Churn: 6.25% vs Active: 3.54%. Chi-Square p < 0.001.",
                "allowed_directions": ["right"],
                "insight": (
                    "Nhóm Churn có tỷ lệ giao trễ cao gần gấp đôi nhóm Active (6.25% so với 3.54%, p < 0.001). "
                    "Trải nghiệm giao hàng trễ là một trong những nguyên nhân hàng đầu khiến khách hàng rời bỏ sàn."
                ),
            },
        ],
    },
    "factor4": {
        "tab_label": "3. Đánh giá Xấu 1-2 Sao (Bad Review)",
        "charts": [
            {
                "title": "Tỷ lệ Đánh giá Xấu (1-2 sao): Nhóm Churn vs Nhóm Active",
                "file": "factor4_bad_review.png",
                "x_label": "Trạng thái Khách hàng",
                "y_label": "Tỷ lệ Đánh giá Xấu 1-2 sao (%)",
                "legend": "Churn: 12.45% vs Active: 9.48%. Chi-Square p < 0.001.",
                "allowed_directions": ["right"],
                "insight": (
                    "Đánh giá xấu là tín hiệu cảnh báo Churn mạnh mẽ nhất (p < 0.001). Khách hàng chấm 1-2 sao "
                    "có xác suất rời bỏ vĩnh viễn cao gấp 1.31 lần so với khách hàng hài lòng."
                ),
            },
        ],
    },
    "factor5": {
        "tab_label": "4. Ngành hàng (Category Impact)",
        "charts": [
            {
                "title": "Tỷ lệ Churn Phân hóa theo Top 10 Ngành hàng",
                "file": "factor5_category_churn.png",
                "x_label": "Ngành hàng (Category)",
                "y_label": "Tỷ lệ Churn (%)",
                "legend": "Đường đỏ đứt nét: Churn trung bình toàn sàn (80.02%). Chi-Square p < 0.001.",
                "allowed_directions": ["right"],
                "insight": (
                    "Tỷ lệ churn dao động từ 73.8% (beleza_saude) đến 87.1% (telefonia). Các ngành hàng tiêu dùng "
                    "nhanh và mỹ phẩm có tỷ lệ quay lại cao hơn hẳn đồ điện tử gia dụng lâu bền."
                ),
            },
        ],
    },
    "factor6": {
        "tab_label": "5. Vùng Địa lý & KT-XH (State Impact)",
        "charts": [
            {
                "title": "Phân hóa Tỷ lệ Churn theo Bang và Vùng Kinh tế - Xã hội",
                "file": "factor6_state_socioeconomic.png",
                "x_label": "Bang Địa lý (State)",
                "y_label": "Tỷ lệ Churn (%)",
                "legend": "Xanh: Vùng phát triển (DF, SP, PR - Churn thấp). Cam: Vùng ngoại vi (BA, MG, RJ, RS - Churn cao).",
                "allowed_directions": ["right"],
                "insight": (
                    "Các bang trung tâm kinh tế Đông Nam (SP, DF, PR) có tỷ lệ churn thấp hơn mức trung bình toàn sàn "
                    "nhờ hạ tầng logistics phát triển, trong khi các bang vùng xa có tỷ lệ churn vượt 82%."
                ),
            },
        ],
    },
}

# =============================================================================
# 03. ĐÁNH GIÁ MÔ HÌNH DỰ BÁO (PREDICTIVE EVALUATION)
# =============================================================================
MODEL_CONFIG = {
    "data_prep": {
        "tab_label": "Feature Engineering",
        "charts": [
            {
                "title": "Phân bổ Chuỗi Thời gian Train, Test & Vùng đệm Tránh Right-Censoring",
                "file": "time_split_distribution.png",
                "x_label": "Tháng mua hàng đầu tiên (First Purchase Month)",
                "y_label": "Số lượng khách hàng mới",
                "legend": "Xanh: Train (10/2016 - 04/2018). Đỏ: Test (05/2018 - 07/2018). Xanh lá: Vùng đệm 78 ngày.",
                "allowed_directions": ["right"],
                "insight": (
                    "Chia tập theo thời gian (Temporal Split) với vùng đệm 78 ngày giúp triệt tiêu hoàn toàn "
                    "lỗi rò rỉ dữ liệu tương lai (Data Leakage) và lỗi cắt phải (Right-Censoring Bias)."
                ),
            },
            {
                "title": "Ma trận Tương quan Pearson & Sàng lọc Biến Rò rỉ Dữ liệu",
                "file": "corr_heatmap.png",
                "x_label": "Đặc trưng Đơn hàng Đầu tiên",
                "y_label": "Đặc trưng Đơn hàng Đầu tiên",
                "legend": "Đỏ: Tương quan dương. Xanh: Tương quan âm. Mục tiêu: is_retain.",
                "allowed_directions": ["left"],
                "insight": (
                    "Tất cả đặc trưng đơn lẻ đều có tương quan tuyến tính rất yếu với is_retain (|r| <= 0.02). "
                    "Điều này khẳng định bài toán giữ chân khách hàng có tính chất phi tuyến sâu sắc, đòi hỏi phải "
                    "kết hợp các biến tương tác hành vi."
                ),
            },
            {
                "title": "Kiểm định Đa cộng tuyến VIF của Bộ 33 Đặc trưng",
                "file": "vif_comparison.png",
                "x_label": "Hệ số Phóng đại Phương sai (VIF)",
                "y_label": "Danh sách Đặc trưng",
                "legend": "Đường cam: Ngưỡng an toàn lý tưởng (VIF=2.0). Đường đỏ: Ngưỡng cảnh báo (VIF=5.0).",
                "allowed_directions": ["right"],
                "insight": (
                    "Sau khi loại bỏ các biến trùng lặp thông tin, toàn bộ 33 đặc trưng đều đạt chuẩn an toàn VIF < 5.0. "
                    "Mô hình hoàn toàn miễn nhiễm với hiện tượng đa cộng tuyến nghiêm trọng."
                ),
            },
        ],
    },
    "model_evaluation": {
        "tab_label": "Đánh giá Hiệu năng: Baseline vs XGBoost Giai đoạn 2",
        "charts": [
            {
                "title": "Đối sánh Hiệu năng Recall: Baseline vs XGBoost Ver 1 vs XGBoost Ver 2",
                "file": "recall_comparison_3models.png",
                "x_label": "Ngưỡng Xác suất Quyết định (Trái) / % Tệp Khách hàng Nhắm tới (Phải)",
                "y_label": "Tỷ lệ Thu hồi Khách hàng Tiềm năng (Recall / Cumulative Gains %)",
                "legend": "Xanh nét đứt: Baseline Logit. Cam nét chấm gạch: XGBoost Ver 1. Đỏ nét liền: XGBoost Ver 2 (Phi tuyến).",
                "allowed_directions": ["right"],
                "insight": (
                    "Đường cong Recall và Thu hồi Lũy tiến (Cumulative Gains) chứng minh rõ: Nhờ bổ sung 3 đặc trưng "
                    "tương tác phi tuyến (delivery_speed_ratio, monthly_installment_burden, is_b2b_profile), XGBoost Ver 2 "
                    "vượt trội hoàn toàn so với Baseline và XGBoost Ver 1. Khi tập trung vào Top 23% khách hàng tiềm năng, "
                    "mô hình bắt trúng tới 28.30% (đỉnh 77.36% theo phân tầng), giúp tối ưu hóa ngân sách và giảm thiểu chi phí tiếp cận lãng phí."
                ),
            },
        ],
    },
    "shap_explainability": {
        "tab_label": "Giải thích Mô hình Toàn cục (TreeSHAP XAI)",
        "charts": [
            {
                "title": "Bóc tách Tầm quan trọng & Chiều Tác động Đặc trưng Toàn cục (Biểu đồ 2 Phía TreeSHAP)",
                "file": "feature_importance_shap.png",
                "x_label": "Mức độ Đóng góp Biên (|SHAP Value|): ◀ Tăng Nguy cơ Churn | Thúc đẩy Giữ chân ▶",
                "y_label": "Danh mục Đặc trưng Hành vi",
                "legend": "Đỏ (Trái): Yếu tố làm tăng rủi ro Rời bỏ (- Churn). Xanh dương (Phải): Yếu tố thúc đẩy Giữ chân (+ Retain).",
                "allowed_directions": ["bottom"],
                "insight": (
                    "Biểu đồ phân kỳ 2 phía TreeSHAP làm nổi bật rõ ràng ranh giới hành vi: "
                    "1. Phía Thúc đẩy Giữ chân (+ Phải): Bang São Paulo (SP +0.646) và miền Nam (Sul +0.388) cùng Điểm đánh giá cao "
                    "(Review +0.252) và nhóm hàng tiêu dùng nhanh (Phòng ngủ, Mỹ phẩm, Đồ tập) là lực hút khách hàng tái mua mạnh mẽ nhất. "
                    "2. Phía Tăng Nguy cơ Rời bỏ (- Trái): Các bang vùng xa ngoại vi (Norte/Nordeste -0.472, RJ -0.343), "
                    "áp lực trả góp hàng tháng cao (monthly burden -0.096) và ngành hàng cồng kềnh/bền lâu năm là các điểm nghẽn chính làm gia tăng churn."
                ),
            },
        ],
    },
}

# =============================================================================
# 04. CHIẾN LƯỢC CHỈ ĐỊNH & TỐI ƯU HÓA (PRESCRIPTIVE STRATEGY & ROI)
# =============================================================================
PRESCRIPTIVE_CONFIG = {
    "clustering": {
        "tab_label": "1. Phân cụm Điểm nghẽn (K-Means)",
        "charts": [
            {
                "title": "Xác định Số Cụm Tối ưu: Phương pháp Khuỷu tay (Elbow) & Điểm Silhouette",
                "file": "diagnostic_elbow_silhouette.png",
                "x_label": "Số lượng Cụm (k)",
                "y_label": "Inertia (Trục trái) | Silhouette Score (Trục phải)",
                "legend": "Đường đỏ: Ngưỡng k=4 tối ưu hóa độ phân tách hành vi người dùng.",
                "allowed_directions": ["right"],
                "insight": (
                    "Tại k=4, đồ thị Silhouette đạt đỉnh phân tách rõ rệt nhất, chia tệp khách hàng cần cứu vãn "
                    "thành đúng 4 nhóm điểm nghẽn riêng biệt không bị trùng lặp."
                ),
            },
            {
                "title": "Phân bổ Quy mô 4 Cụm Điểm nghẽn Hành vi Khách hàng",
                "file": "executive_friction_distribution.png",
                "x_label": "Cụm Điểm nghẽn (Friction Cluster)",
                "y_label": "Số lượng Khách hàng Mục tiêu",
                "legend": "Cụm 0 (Tài chính: 2,319 khách), Cụm 1 (Review xấu: 2,086 khách), Cụm 2 (Giao trễ: 1,987 khách), Cụm 3 (Ngành hàng: 7,133 khách).",
                "allowed_directions": ["left"],
                "insight": (
                    "Cụm 3 (Ngành hàng) chiếm quy mô lớn nhất (52.74%), nhưng Cụm 0, 1, 2 là những nhóm có điểm nghẽn "
                    "trải nghiệm cấp bách cần can thiệp chính sách khẩn cấp để ngăn chặn rời bỏ."
                ),
            },
        ],
    },
    "knapsack_budget": {
        "tab_label": "2. Tối ưu Knapsack & Phân bổ Vốn",
        "charts": [
            {
                "title": "Đường biên Lợi nhuận Bão hòa (Diminishing Returns Frontier - Knapsack ILP)",
                "file": "executive_profit_frontier.png",
                "x_label": "Ngân sách Cấp trước (R$)",
                "y_label": "Lợi nhuận Ròng Kỳ vọng (R$)",
                "legend": "Điểm bão hòa kinh tế tại 3,803.95 R$ (3.59% tổng ngân sách tối đa), tối đa hóa Lợi nhuận Ròng đạt 10,925.85 R$.",
                "allowed_directions": ["right"],
                "insight": (
                    "Quy luật hiệu suất giảm dần (Diminishing Returns) xuất hiện rõ rệt: Đầu tư vượt mốc 3,803.95 R$ "
                    "sẽ làm giảm hiệu quả biên ROI. Do đó 3,803.95 R$ là điểm cân bằng tài chính tối ưu hoàn hảo cho 600 khách VIP Tier 2A."
                ),
            },
            {
                "title": "Cơ cấu Phân bổ Ngân sách Tối ưu giữa 4 Cụm Khách hàng",
                "file": "executive_budget_donut.png",
                "x_label": None,
                "y_label": None,
                "legend": "Cụm 0 (Áp lực tài chính: 50.9%), Cụm 1 (Đánh giá kém: 24.5%), Cụm 2 (Giao hàng: 24.6%), Cụm 3 (Tự tài trợ: 0.0%).",
                "allowed_directions": ["left"],
                "insight": (
                    "50.9% vốn cấp trước được dồn vào Cụm 0 (Tài trợ trả góp 0% cho đơn to), 49.1% còn lại chia đều "
                    "cho Cụm 1 (Đền bù thiện chí) và Cụm 2 (Hoàn phí ship SLA). Cụm 3 tự vận hành bằng cơ chế Tự tài trợ."
                ),
            },
        ],
    },
    "risk_scenarios": {
        "tab_label": "3. Điểm Hòa vốn & Kiểm định Kịch bản",
        "charts": [
            {
                "title": "Ma trận Tỷ lệ Giữ chân Hòa vốn (Break-even Retention Rate Heatmap)",
                "file": "executive_break_even_heatmap.png",
                "x_label": "Biên Lợi nhuận Ròng Doanh nghiệp (%)",
                "y_label": "Cụm Can thiệp Marketing",
                "legend": "Tỷ lệ hòa vốn dao động từ 1.83% đến 14.71% tùy thuộc biên lợi nhuận và cước phí can thiệp.",
                "allowed_directions": ["right"],
                "insight": (
                    "Tại biên lợi nhuận chuẩn 30%, toàn bộ 4 cụm đều có điểm hòa vốn cực thấp (< 6.5%), "
                    "chứng minh chiến dịch giữ chân có biên độ an toàn tài chính (Safety Margin) rất rộng."
                ),
            },
            {
                "title": "Kiểm định Stress-Test Tài chính qua 3 Kịch bản Thị trường",
                "file": "executive_scenario_comparison.png",
                "x_label": "Kịch bản Thị trường",
                "y_label": "Lợi nhuận Ròng Thu về (R$)",
                "legend": "Bi quan (Lợi nhuận +1,650 R$), Cơ sở (+10,926 R$), Lạc quan (+20,201 R$).",
                "allowed_directions": ["left"],
                "insight": (
                    "Ngay cả trong kịch bản Bi quan nhất (Uplift giảm 40%), chiến dịch Tier 2A vẫn bảo toàn lợi nhuận "
                    "dương (+1,650 R$), loại bỏ hoàn toàn nguy cơ thua lỗ vốn đầu tư ban đầu."
                ),
            },
        ],
    },
}
