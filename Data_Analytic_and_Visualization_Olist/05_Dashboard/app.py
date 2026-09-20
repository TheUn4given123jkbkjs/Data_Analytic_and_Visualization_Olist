"""
DASHBOARD PHÂN TÍCH & DỰ ĐOÁN RỜI BỎ KHÁCH HÀNG (CUSTOMER CHURN)
Sàn Thương mại điện tử Brazil (Olist E-commerce)

Cấu trúc:
  Tab 1  - Mô tả Dữ liệu (EDA)          : 9 biểu đồ, chia theo 4 chủ đề
  Tab 2  - Phân tích Chẩn đoán           : 12 biểu đồ, chia theo 6 yếu tố tác động churn
  Tab 3  - Dự đoán Churn & Đề xuất       : 7 biểu đồ mô hình (chuẩn bị dữ liệu, baseline,
                                           so sánh baseline vs advanced, SHAP) + form dự đoán
                                           tương tác wiring tới core/model_helper.py (chạy được
                                           ngay khi có đủ model artifacts: best_model.pkl,
                                           feature_columns.json, X_train.csv)

Chạy thử: streamlit run app.py
"""

import os
import sys
import streamlit as st
import pandas as pd

from charts_config import CHARTS_CONFIG, DIAGNOSTIC_CONFIG, MODEL_CONFIG

# ---------------------------------------------------------------------------
# CẤU HÌNH TRANG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Olist Churn Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CORE_DIR = os.path.join(BASE_DIR, "core")
sys.path.insert(0, CORE_DIR)

# Đường dẫn tới thư mục chứa model artifacts (best_model.pkl, feature_columns.json...).
# Tính TƯƠNG ĐỐI theo cấu trúc thư mục dự án thay vì gắn cứng ổ đĩa (D:\...), để
# không bị hỏng khi chạy trên máy khác (máy đồng đội, máy giảng viên chấm bài...).
# Cấu trúc giả định: <project_root>/05_Dashboard/ (chứa app.py này)
#                     <project_root>/03_Predictive/models/...
# Nếu cấu trúc máy bạn khác, chỉ cần sửa MỘT dòng DEFAULT_MODEL_DIR này.
DEFAULT_MODEL_DIR = os.path.join(os.path.dirname(BASE_DIR), "03_Predictive", "models")

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("Olist Churn Dashboard")
    st.markdown(
        "**Đề tài:** Dự đoán rời bỏ khách hàng (Churn) trên sàn TMĐT\n\n"
        "**Bối cảnh:** Doanh thu quý gần đây tăng trưởng chậm lại dù ngân sách "
        "marketing không đổi. Ban giám đốc nghi ngờ tỷ lệ khách quay lại mua hàng "
        "(repeat purchase) đang giảm."
    )
    st.divider()
    st.markdown("**Quần thể nghiên cứu:** N = 92,077 khách hàng `delivered`, 01/2017 – 08/2018")
    st.caption(
        "Dữ liệu đã được làm sạch theo nguyên tắc bảo toàn dữ liệu gốc "
        "(raw data immutability) — xem chi tiết trong báo cáo tiền xử lý."
    )

# ---------------------------------------------------------------------------
# HEADER + CHỈ SỐ NHANH
# ---------------------------------------------------------------------------
st.title("📊 Dashboard Phân tích & Dự đoán Rời bỏ Khách hàng")
st.caption("Olist E-commerce · Dữ liệu giao dịch 12 tháng gần nhất")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Khách hàng nghiên cứu", "92,077")
m2.metric("Tỷ lệ Churn (>90 ngày)", "80.02%", help="73,677 / 92,077 khách hàng")
m3.metric("Tỷ lệ mua lặp lại", "2.98%", help="2,747 / 92,077 khách hàng từng mua ≥ 2 lần")
m4.metric("AOV trung vị", "R$ 107.78", help="Trung bình: R$ 165.94 — lệch phải mạnh")

st.divider()


def render_chart(chart: dict):
    st.subheader(chart["title"])
    img_path = os.path.join(ASSETS_DIR, chart["file"])
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.warning(f"⚠️ Chưa tìm thấy ảnh: `{chart['file']}` trong thư mục assets/")

    axis_bits = []
    if chart.get("x_label"):
        axis_bits.append(f"**Trục X:** {chart['x_label']}")
    if chart.get("y_label"):
        axis_bits.append(f"**Trục Y:** {chart['y_label']}")
    if axis_bits:
        st.caption(" &nbsp;|&nbsp; ".join(axis_bits))

    if chart.get("legend"):
        st.caption(f"🔖 **Chú thích:** {chart['legend']}")

    st.info(f"📌 **Nhận xét:** {chart['insight']}")


def render_chart_group(group_key: str, config: dict):
    group = config[group_key]
    charts = group["charts"]
    for i, chart in enumerate(charts):
        render_chart(chart)
        if i < len(charts) - 1:
            st.markdown("---")


def render_summary_table(rows: list):
    """Bảng tóm tắt hiển thị đầy đủ nội dung (không bị cắt chữ như st.metric
    khi text dài), dùng markdown table — tự thích ứng theme sáng/tối."""
    lines = ["| Yếu tố | Chỉ số chính |", "|---|---|"]
    for label, value in rows:
        lines.append(f"| {label} | {value} |")
    st.markdown("\n".join(lines))


# ---------------------------------------------------------------------------
# TABS CHÍNH
# ---------------------------------------------------------------------------
tab_eda, tab_diag, tab_model = st.tabs(
    ["1. Mô tả Dữ liệu (EDA)", "2. Phân tích Chẩn đoán", "3. Dự đoán Churn & Đề xuất"]
)

# ============================== TAB 1: EDA ==============================
with tab_eda:
    st.markdown(
        "9 biểu đồ mô tả dưới đây được chia theo 4 chủ đề: "
        "doanh thu/ngành hàng, khách hàng/thanh toán, hành vi mua lặp lại/churn, "
        "và trải nghiệm giao hàng."
    )
    sub_tabs = st.tabs([CHARTS_CONFIG[key]["tab_label"] for key in CHARTS_CONFIG])
    for sub_tab, key in zip(sub_tabs, CHARTS_CONFIG):
        with sub_tab:
            render_chart_group(key, config=CHARTS_CONFIG)

# ============================== TAB 2: PHÂN TÍCH CHẨN ĐOÁN ==============================
with tab_diag:
    st.markdown(
        "So sánh nhóm **Active (< 90 ngày)** và **Churn (≥ 90 ngày)** theo **6 yếu tố nghi vấn** "
        "gây rời bỏ khách hàng"
    )

    render_summary_table(
        [
            ("1. Giao hàng trễ", "Churn 6.25% vs Active 3.54% (p < 0.001)"),
            ("2. Tỷ trọng phí ship", "Gần như không đổi: 18.3% vs 19.2% (chênh lệch thực tế nhỏ)"),
            ("3. Số ngày giao trễ (tuyệt đối)", "Không có ý nghĩa thống kê (p = 0.7554 > 0.05)"),
            ("4. Đánh giá xấu (1-2 sao)", "Churn 12.45% vs Active 9.48% (p < 0.001) — tín hiệu mạnh nhất"),
            ("5. Ngành hàng", "Tỷ lệ churn dao động 73.8% – 87.1% tùy ngành (p < 0.001)"),
            ("6. Vùng địa lý (Bang)", "Tỷ lệ churn dao động 77.6% – 82.5% tùy vùng (p < 0.001)"),
        ]
    )

    st.divider()

    diag_tabs = st.tabs([DIAGNOSTIC_CONFIG[key]["tab_label"] for key in DIAGNOSTIC_CONFIG])
    for diag_tab, key in zip(diag_tabs, DIAGNOSTIC_CONFIG):
        with diag_tab:
            render_chart_group(key, config=DIAGNOSTIC_CONFIG)   

# ============================== TAB 3: DỰ ĐOÁN & ĐỀ XUẤT ==============================
with tab_model:
    st.markdown(
        "Phần này trình bày toàn bộ quy trình xây dựng mô hình dự đoán churn: từ chuẩn bị "
        "dữ liệu, huấn luyện mô hình **baseline** (Logistic Regression), so sánh với mô hình "
        "**nâng cao** (XGBoost), đến diễn giải kết quả bằng SHAP — sau đó là công cụ dự đoán "
        "tương tác và mô phỏng ROI, wiring tới `core/model_helper.py`."
    )

    result_tabs = st.tabs([MODEL_CONFIG[key]["tab_label"] for key in MODEL_CONFIG])
    for result_tab, key in zip(result_tabs, MODEL_CONFIG):
        with result_tab:
            render_chart_group(key, config=MODEL_CONFIG)

    st.divider()
    st.subheader("📋 Tổng kết Kết quả Mô hình")
    st.warning(
        "⚠️ **Phát hiện quan trọng:** Mô hình nâng cao (XGBoost) hiện đang cho kết quả **thấp hơn** "
        "mô hình baseline (Logistic Regression) trên cả AUC-ROC (0.5187 so với 0.5346) lẫn AUC-PR "
        "(0.0155 so với 0.0264). Đây là dấu hiệu cho thấy cần cải thiện thêm trước khi triển khai "
        "thực tế — ví dụ: xử lý mất cân bằng lớp (class dương chỉ chiếm 1.48%), tinh chỉnh "
        "hyperparameter kỹ hơn, hoặc bổ sung đặc trưng hành vi mới — thay vì chỉ dựa vào việc đổi "
        "sang thuật toán phức tạp hơn."
    )

    st.divider()
    st.subheader("Công cụ Dự đoán Tương tác")
    st.markdown(
        "Sử dụng `core/data_scaler.py` (chuẩn hóa đặc trưng) và `core/model_helper.py` "
        "(dự đoán xác suất giữ chân, giải thích SHAP, gói can thiệp marketing & mô phỏng ROI)."
    )


    with st.form("prediction_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            order_spent = st.number_input("Tổng chi tiêu đơn hàng (R$)", min_value=0.0, value=150.0, step=10.0)
            max_installments = st.number_input("Số kỳ trả góp tối đa", min_value=1, max_value=24, value=3)
            payment_type = st.selectbox(
                "Phương thức thanh toán", ["credit_card", "boleto", "voucher", "debit_card"]
            )
        with c2:
            delivery_days = st.number_input("Số ngày giao hàng thực tế", min_value=0.0, value=8.0, step=1.0)
            estimated_delivery_days = st.number_input("Số ngày giao hàng ước tính", min_value=0.0, value=15.0, step=1.0)
            review_score = st.slider("Điểm đánh giá (Review score)", 1, 5, 5)
        with c3:
            customer_state = st.selectbox("Bang khách hàng", ["SP", "RJ", "MG", "RS", "PR", "SC", "Khác"])
            product_category = st.text_input("Ngành hàng (product_category_name)", value="cama_mesa_banho")

        submitted = st.form_submit_button("Dự đoán")

    if submitted:
        try:
            from model_helper import OlistCustomerPredictor  # import trong core/

            predictor = OlistCustomerPredictor(model_dir=DEFAULT_MODEL_DIR)
            result = predictor.predict_and_prescribe(
                order_spent=order_spent,
                max_installments=max_installments,
                payment_type=payment_type,
                delivery_days=delivery_days,
                estimated_delivery_days=estimated_delivery_days,
                review_score=review_score,
                customer_state=customer_state,
                product_category=product_category,
            )

            r1, r2 = st.columns([1, 1])
            with r1:
                st.metric("Xác suất giữ chân (P-Retain)", result["prob_retain_pct"])
                st.markdown(f"**Tầng rủi ro:** :orange[{result['risk_tier']}]")
            with r2:
                st.markdown(f"**Nguyên nhân tác động lớn nhất:** {result['top_cause']}")
                st.dataframe(result["pie_chart_data"], hide_index=True, use_container_width=True)

            st.subheader("💡 Đề xuất can thiệp")
            st.markdown(f"**{result['action_title']}**")
            st.write(result["action_desc"])
            st.caption(f"Kênh triển khai: {result['action_channel']}")

        except FileNotFoundError as e:
            st.error(
                "❌ Chưa tìm thấy file mô hình hoặc feature_columns.json. "
                f"Chi tiết lỗi: {e}\n\n"
                f"Đường dẫn hiện đang dùng: `{DEFAULT_MODEL_DIR}`. Vui lòng đặt "
                "`advanced/best_run/best_model.pkl` và `feature_columns.json` đúng vào đó — "
                "hoặc sửa hằng số `DEFAULT_MODEL_DIR` ở đầu file `app.py` nếu cấu trúc thư mục "
                "trên máy bạn khác."
            )
        except ModuleNotFoundError as e:
            st.error(
                f"❌ Thiếu thư viện: {e}. Cài đặt bằng `pip install -r requirements.txt`."
            )
        except Exception as e:  # noqa: BLE001
            st.error(f"❌ Có lỗi xảy ra khi dự đoán: {e}")

    st.divider()
    st.subheader("💰 Mô phỏng ROI Chiến dịch Giữ chân")
    st.caption(
        "Dùng hàm `simulate_roi` trong model_helper.py để ước tính hiệu quả tài chính "
        "của chiến dịch marketing giữ chân trước khi phân bổ ngân sách quý tới."
    )
    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        target_customers = st.number_input("Số khách hàng mục tiêu", min_value=1, value=4124, step=100)
        cost_per_voucher = st.number_input("Chi phí / voucher (R$)", min_value=0.0, value=20.0, step=1.0)
    with rc2:
        expected_uplift_pct = st.number_input("Tỷ lệ giữ chân kỳ vọng (%)", min_value=0.0, max_value=100.0, value=20.0)
        avg_order_value = st.number_input("Giá trị đơn hàng TB (R$)", min_value=0.0, value=160.0, step=10.0)
    with rc3:
        net_margin_pct = st.number_input("Biên lợi nhuận ròng (%)", min_value=0.0, max_value=100.0, value=30.0)
        future_orders = st.number_input("Số đơn tương lai kỳ vọng / khách", min_value=0.0, value=1.5, step=0.1)

    if st.button("📈 Tính ROI"):
        try:
            from model_helper import OlistCustomerPredictor

            roi = OlistCustomerPredictor.simulate_roi(
                target_customers=target_customers,
                cost_per_voucher=cost_per_voucher,
                expected_uplift_pct=expected_uplift_pct,
                avg_order_value=avg_order_value,
                net_margin_pct=net_margin_pct,
                future_orders=future_orders,
            )
            k1, k2, k3 = st.columns(3)
            k1.metric("Tổng chi phí", f"R$ {roi['total_cost']:,.0f}")
            k2.metric("Lợi nhuận ròng", f"R$ {roi['net_profit']:,.0f}")
            k3.metric("ROI", f"{roi['roi_pct']:.1f}%")
            if roi["is_profitable"]:
                st.success("✅ Chiến dịch có lợi nhuận dương (khả thi về mặt tài chính).")
            else:
                st.error("❌ Chiến dịch đang lỗ với các tham số hiện tại — cân nhắc điều chỉnh.")
        except Exception as e:  # noqa: BLE001
            st.error(f"❌ Có lỗi xảy ra khi tính ROI: {e}")

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.divider()
st.caption(
    "Nguồn dữ liệu: Olist E-commerce (Brazil) · Dashboard xây dựng bằng Streamlit · "
)
