"""
DASHBOARD PHÂN TÍCH VÀ DỰ ĐOÁN RỜI BỎ KHÁCH HÀNG (CUSTOMER RETENTION INTELLIGENCE)
Sàn Thương mại Điện tử Brazil (Olist E-Commerce)
"""

import os
import sys
import importlib
import streamlit as st
import pandas as pd
import numpy as np

try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

import charts_config
importlib.reload(charts_config)
from charts_config import CHARTS_CONFIG, DIAGNOSTIC_CONFIG, MODEL_CONFIG, PRESCRIPTIVE_CONFIG

# ---------------------------------------------------------------------------
# CẤU HÌNH TRANG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Olist Retention Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# HỆ THỐNG THIẾT KẾ (DESIGN SYSTEM) - HỖ TRỢ DARK & LIGHT MODE
# ---------------------------------------------------------------------------
SCALE_MAP = {"Chuẩn": 1.0, "Lớn": 1.2, "Trình chiếu": 1.4}
_scale = SCALE_MAP.get(st.session_state.get("ui_scale", "Chuẩn"), 1.0)

def _px(v: float) -> str:
    return f"{round(v * _scale)}px"

_ROOT_SIZES = f"""
:root {{
    --fs-body: {_px(16)};
    --fs-small: {_px(14)};
    --fs-label: {_px(15)};
    --fs-input: {_px(15.5)};
    --fs-insight: {_px(16.5)};
    --fs-metric: {_px(28)};
    --fs-h1: {_px(32)};
    --fs-section: {_px(24)};
}}
"""

_STATIC_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap&subset=vietnamese');

.stApp { 
    font-family: 'Inter', system-ui, -apple-system, sans-serif; 
}

/* ẨN HEADER VÀ FOOTER DƯ THỪA */
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeaderActionElements"] { display: none; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; }

/* 1. SỬA LỖI TIÊU ĐỀ CHÍNH (H1) BỊ TỐI MÀU */
[data-testid="stMain"] h1, .main h1 {
    font-size: var(--fs-h1) !important;
    font-weight: 800 !important;
    color: var(--st-color-text, inherit) !important;
    line-height: 1.3 !important;
    margin-bottom: 12px !important;
}

/* 2. SỬA LỖI BANNER CHUỖI GIÁ TRỊ (SUBTITLE) */
.project-subtitle {
    font-size: var(--fs-body);
    font-weight: 600;
    color: #0284c7 !important;
    background: rgba(14, 165, 233, 0.12);
    padding: 12px 18px;
    border-radius: 10px;
    border-left: 5px solid #0284c7;
    margin-bottom: 24px;
    display: inline-block;
    width: 100%;
}

/* 3. SỬA LỖI TÊN SIDEBAR VÀ ĐIỀU HƯỚNG BỊ TỐI */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 {
    color: var(--st-color-text, inherit) !important;
}

.sidebar-header-title {
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 2px;
}
.sidebar-header-sub {
    font-size: 13px;
    opacity: 0.8;
    margin-bottom: 15px;
}

/* NÚT ĐIỀU HƯỚNG MENU */
[data-testid="stSidebar"] button[kind="secondary"] {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(150, 150, 150, 0.2) !important;
    color: var(--st-color-text, inherit) !important;
    font-weight: 500 !important;
    transition: all 0.2s ease;
}
[data-testid="stSidebar"] button[kind="secondary"]:hover {
    border-color: #0284c7 !important;
    color: #0284c7 !important;
}
[data-testid="stSidebar"] button[kind="primary"] {
    background-color: #0284c7 !important;
    border-color: #0284c7 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
}

/* 4. SỬA TIÊU ĐỀ PHÂN HỆ */
.main-section-header {
    font-size: var(--fs-section);
    font-weight: 800;
    color: #0284c7;
    line-height: 1.3;
    margin: 10px 0 16px 0;
    padding-left: 12px;
    border-left: 5px solid #0284c7;
}

/* KHUNG NHẬN XÉT INSIGHT */
.insight-card {
    background: rgba(14, 165, 233, 0.05);
    border: 1px solid rgba(14, 165, 233, 0.2);
    border-left: 5px solid #0284c7;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 16px 0;
}
.insight-card .insight-label {
    font-size: var(--fs-small);
    font-weight: 800;
    color: #0284c7;
    margin-bottom: 6px;
}
.insight-card .insight-text {
    font-size: var(--fs-body) !important;
    line-height: 1.6 !important;
    margin: 0;
}
"""

st.markdown(f"<style>{_STATIC_CSS}{_ROOT_SIZES}</style>", unsafe_allow_html=True)

def section_header(title: str):
    st.markdown(f"<div class='main-section-header'>{title}</div>", unsafe_allow_html=True)

def _pct_to_float(value):
    try:
        return max(0.0, min(1.0, float(str(value).replace("%", "").replace(",", ".").strip()) / 100.0))
    except (TypeError, ValueError):
        return None

# ---------------------------------------------------------------------------
# XỬ LÝ ĐƯỜNG DẪN THƯ MỤC DỰ ÁN VÀ QUAN LÝ ASSETS
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

CORE_DIR = os.path.join(BASE_DIR, "core")
sys.path.insert(0, CORE_DIR)
sys.path.insert(0, BASE_DIR)

SEARCH_ASSET_DIRS = [
    BASE_DIR,
    os.path.join(BASE_DIR, "assets"),
    os.path.join(PROJECT_ROOT, "01_Descriptive"),
    os.path.join(PROJECT_ROOT, "01_Descriptive", "assets"),
    os.path.join(PROJECT_ROOT, "02_Diagnostic"),
    os.path.join(PROJECT_ROOT, "02_Diagnostic", "assets"),
    os.path.join(PROJECT_ROOT, "03_Predictive"),
    os.path.join(PROJECT_ROOT, "03_Predictive", "assets"),
    os.path.join(PROJECT_ROOT, "04_Prescriptive"),
    os.path.join(PROJECT_ROOT, "04_Prescriptive", "assets"),
]

FALLBACK_FILENAMES = {
    "pareto_categories_modelstage.png": "pareto_categories.png"
}

def find_image_path(filename: str):
    for d in SEARCH_ASSET_DIRS:
        p = os.path.join(d, filename)
        if os.path.exists(p):
            return p
            
    if filename in FALLBACK_FILENAMES:
        fb_name = FALLBACK_FILENAMES[filename]
        for d in SEARCH_ASSET_DIRS:
            p = os.path.join(d, fb_name)
            if os.path.exists(p):
                return p
    return None

DEFAULT_MODEL_DIR = os.path.join(PROJECT_ROOT, "03_Predictive", "models")

@st.cache_resource(show_spinner="Đang tải mô hình AI...")
def load_predictor(model_dir: str):
    from model_helper import OlistCustomerPredictor
    return OlistCustomerPredictor(model_dir=model_dir)

# ---------------------------------------------------------------------------
# HÀM HIỂN THỊ BIỂU ĐỒ & NHẬN XÉT
# ---------------------------------------------------------------------------
def render_chart_sliding(chart: dict, index: int, uid_prefix: str = "c"):
    st.subheader(chart['title'])
    img_path = find_image_path(chart["file"])
    
    if img_path and os.path.exists(img_path):
        img_scale = chart.get("img_scale", 1.0)
        if img_scale < 1.0:
            pad = (1.0 - img_scale) / 2.0
            _, c_img, _ = st.columns([pad, img_scale, pad])
            with c_img:
                st.image(img_path, use_container_width=True)
        else:
            st.image(img_path, use_container_width=True)
    else:
        st.error(f"⚠️ Không tìm thấy sơ đồ: `{chart['file']}`.")

    caption_parts = []
    if chart.get("x_label"):
        caption_parts.append(f"**Trục X:** {chart['x_label']}")
    if chart.get("y_label"):
        caption_parts.append(f"**Trục Y:** {chart['y_label']}")
    if chart.get("legend"):
        caption_parts.append(f"**Chú thích:** {chart['legend']}")
    
    if caption_parts:
        st.caption(" &nbsp;|&nbsp; ".join(caption_parts))

    if chart.get("insight"):
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-label">NHẬN XÉT CHIẾN LƯỢC & BÀI HỌC NGHIỆP VỤ</div>
            <div class="insight-text">{chart['insight']}</div>
        </div>
        """, unsafe_allow_html=True)

def render_chart_group_sliding(group_key: str, config: dict):
    group = config[group_key]
    charts = group["charts"]
    for i, chart in enumerate(charts):
        render_chart_sliding(chart, index=i, uid_prefix=group_key)
        if i < len(charts) - 1:
            st.divider()

render_chart_alternating = render_chart_sliding
render_chart_group_alternating = render_chart_group_sliding

# ---------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------------------------
NAV_ITEMS = [
    "Demo",
    "01. Descriptive",
    "02. Diagnostic",
    "03. Predictive",
    "04. Prescriptive"
]

if "nav_choice" not in st.session_state or st.session_state.nav_choice not in NAV_ITEMS:
    st.session_state.nav_choice = NAV_ITEMS[0]

with st.sidebar:
    st.markdown('<div class="sidebar-header-title">Olist Retention AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-header-sub">Hệ thống Dự báo & Tối ưu hóa Giữ chân Khách hàng</div>', unsafe_allow_html=True)
    st.divider()
    
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    for item in NAV_ITEMS:
        is_active = (st.session_state.nav_choice == item)
        btn_type = "primary" if is_active else "secondary"
        if st.button(item, key=f"nav_btn_{item}", type=btn_type, use_container_width=True):
            if st.session_state.nav_choice != item:
                st.session_state.nav_choice = item
                st.rerun()
                
    st.divider()
    st.markdown("<b>HIỂN THỊ</b>", unsafe_allow_html=True)
    st.radio(
        "Cỡ chữ",
        list(SCALE_MAP.keys()),
        key="ui_scale",
        horizontal=True,
    )

nav_choice = st.session_state.nav_choice

# ---------------------------------------------------------------------------
# HEADER CHÍNH DỰ ÁN
# ---------------------------------------------------------------------------
st.title("Hệ Thống Dự Báo và Tối Ưu Hóa Giữ Chân Khách Hàng Olist")

st.markdown(
    '<div class="project-subtitle">Chuỗi giá trị: Descriptive (01) → Diagnostic (02) → Predictive (03) → Prescriptive (04)</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Quần thể Nghiên cứu", "92,077", help="Khách hàng phát sinh đơn hàng delivered")
k2.metric("Tỷ lệ Rời bỏ (Churn >90d)", "80.02%", help="73,678 / 92,077 khách hàng rời bỏ sàn")
k3.metric("Tỷ lệ Mua lặp lại (F ≥ 2)", "2.98%", help="2,744 / 92,077 khách hàng mua từ 2 lần trở lên")
k4.metric("AOV Trung vị / Trung bình", "R$ 107.78", help="Trung bình: R$ 165.94 (Lệch phải mạnh)")

st.divider()

CATEGORIES_DICT = {
    "cama_mesa_banho": "Phòng ngủ & Phòng tắm (cama_mesa_banho)",
    "beleza_saude": "Sức khỏe & Sắc đẹp (beleza_saude)",
    "esporte_lazer": "Thể thao & Dã ngoại (esporte_lazer)",
    "moveis_decoracao": "Nội thất & Trang trí (moveis_decoracao)",
    "informatica_acessorios": "Máy tính & Phụ kiện công nghệ (informatica_acessorios)",
    "utilidades_domesticas": "Đồ gia dụng & Tiện ích (utilidades_domesticas)",
    "relogios_presentes": "Đồng hồ & Quà tặng (relogios_presentes)",
    "telefonia": "Điện thoại & Viễn thông (telefonia)",
    "ferramentas_jardim": "Dụng cụ & Làm vườn (ferramentas_jardim)",
    "automotivo": "Phụ tùng Ô tô & Xe máy (automotivo)",
    "brinquedos": "Đồ chơi trẻ em (brinquedos)",
    "cool_stuff": "Đồ sáng tạo & Công nghệ độc lạ (cool_stuff)",
    "perfumaria": "Nước hoa & Mỹ phẩm (perfumaria)",
    "bebes": "Mẹ & Bé (bebes)",
    "eletronicos": "Thiết bị điện tử (eletronicos)",
    "outros": "Danh mục khác (outros - 59 ngành hàng đuôi dài)"
}

STATES_DICT = {
    "SP": "SP - São Paulo (Đông Nam)",
    "RJ": "RJ - Rio de Janeiro (Đông Nam)",
    "MG": "MG - Minas Gerais (Đông Nam)",
    "RS": "RS - Rio Grande do Sul (Vùng Sul)",
    "PR": "PR - Paraná (Vùng Sul)",
    "SC": "SC - Santa Catarina (Vùng Sul)",
    "BA": "BA - Bahia (Đông Bắc)",
    "DF": "DF - Distrito Federal (Thủ đô Brasília)",
    "GO": "GO - Goiás (Trung Tây)",
    "ES": "ES - Espírito Santo (Đông Nam)",
    "PE": "PE - Pernambuco (Đông Bắc)",
    "CE": "CE - Ceará (Đông Bắc)",
    "outros": "outros - Các bang khác (Outros Estados)"
}

PAYMENTS_DICT = {
    "credit_card": "Thẻ tín dụng (Cartão de Crédito)",
    "boleto": "Phiếu thu ngân hàng (Boleto Bancário)",
    "voucher": "Phiếu ưu đãi (Voucher)",
    "debit_card": "Thẻ ghi nợ (Cartão de Débito)"
}

# ===========================================================================
# 1. PHÂN HỆ: DEMO (DỰ BÁO & CHỈ ĐỊNH)
# ===========================================================================
if nav_choice == "Demo":
    section_header("Dự Đoán Thời Gian Thực và Chỉ Định Hành Động")
    st.markdown(
        "Nhập thông tin đơn hàng đầu tiên ($T_0$) của khách hàng để Mô hình AI dự báo xác suất quay lại, "
        "tự động bóc tách **4 nhóm nguyên nhân TreeSHAP** và gán **Gói chính sách Marketing tối ưu**."
    )
    
    PRESET_OPTIONS = {
        "Tuỳ chỉnh thông số tự do (Custom Input)": None,
        "Mẫu 1: Khách Trả góp Đơn lớn (Cụm 0 - Áp lực tài chính)": {
            "order_spent": 380.0, "max_installments": 10, "payment_type": "credit_card",
            "delivery_days": 7.0, "estimated_delivery_days": 18.0, "review_score": 5,
            "customer_state": "SP", "product_category": "relogios_presentes"
        },
        "Mẫu 2: Khách Đánh giá 1 Sao (Cụm 1 - Khủng hoảng CSKH)": {
            "order_spent": 95.0, "max_installments": 2, "payment_type": "credit_card",
            "delivery_days": 12.0, "estimated_delivery_days": 15.0, "review_score": 1,
            "customer_state": "RJ", "product_category": "beleza_saude"
        },
        "Mẫu 3: Khách Giao hàng Trễ hạn (Cụm 2 - Hụt cam kết SLA)": {
            "order_spent": 140.0, "max_installments": 3, "payment_type": "credit_card",
            "delivery_days": 28.0, "estimated_delivery_days": 12.0, "review_score": 2,
            "customer_state": "BA", "product_category": "cama_mesa_banho"
        },
        "Mẫu 4: Khách hàng Vãng lai Đơn nhỏ (Tier 1 - Churn tự nhiên)": {
            "order_spent": 35.0, "max_installments": 1, "payment_type": "boleto",
            "delivery_days": 6.0, "estimated_delivery_days": 14.0, "review_score": 5,
            "customer_state": "SP", "product_category": "telefonia"
        },
        "Mẫu 5: Khách Trung thành Tự nhiên (Tier 3 - Organic Safe)": {
            "order_spent": 150.0, "max_installments": 10, "payment_type": "credit_card",
            "delivery_days": 2.0, "estimated_delivery_days": 20.0, "review_score": 5,
            "customer_state": "SP", "product_category": "perfumaria"
        },
        "Mẫu ngẫu nhiên (Random Profile)": "RANDOM"
    }
    
    if "random_profile_counter" not in st.session_state:
        st.session_state.random_profile_counter = 101

    col_results, col_controls = st.columns([0.58, 0.42], gap="large")

    with col_controls:
        st.markdown("### THIẾT LẬP THÔNG SỐ ĐƠN HÀNG")
        selected_preset_key = st.selectbox(
            "Chọn Nhanh Mẫu Khách Hàng Điển Hình:",
            list(PRESET_OPTIONS.keys()),
            index=0
        )
        
        preset_val = PRESET_OPTIONS[selected_preset_key]
        if preset_val == "RANDOM":
            rng = np.random.RandomState(st.session_state.random_profile_counter)
            preset_chosen = {
                "order_spent": float(rng.choice([29.0, 48.0, 75.0, 110.0, 165.0, 245.0, 380.0])),
                "max_installments": int(rng.choice([1, 2, 3, 4, 6, 8, 10, 12])),
                "payment_type": str(rng.choice(["credit_card", "boleto", "voucher", "debit_card"])),
                "delivery_days": float(rng.randint(2, 25)),
                "estimated_delivery_days": float(rng.randint(8, 28)),
                "review_score": int(rng.choice([1, 2, 3, 4, 5])),
                "customer_state": str(rng.choice(list(STATES_DICT.keys()))),
                "product_category": str(rng.choice(list(CATEGORIES_DICT.keys())))
            }
            if st.button("Sinh Mẫu Ngẫu Nhiên Khác (Re-roll)", use_container_width=True):
                st.session_state.random_profile_counter += 1
                st.rerun()
        else:
            preset_chosen = preset_val

        with st.form("hero_prediction_form"):
            st.markdown("#### Thông số Đơn hàng Đầu tiên ($T_0$)")

            def_spent = preset_chosen["order_spent"] if preset_chosen else 150.0
            def_inst = preset_chosen["max_installments"] if preset_chosen else 3
            def_pay = preset_chosen["payment_type"] if preset_chosen else "credit_card"
            def_deliv = preset_chosen["delivery_days"] if preset_chosen else 8.0
            def_est = preset_chosen["estimated_delivery_days"] if preset_chosen else 15.0
            def_score = preset_chosen["review_score"] if preset_chosen else 5
            def_state = preset_chosen["customer_state"] if preset_chosen else "SP"
            def_cat = preset_chosen["product_category"] if preset_chosen else "cama_mesa_banho"

            form_key_suffix = f"{selected_preset_key}_{st.session_state.random_profile_counter}"

            st.markdown("<b>Giá trị & thanh toán</b>", unsafe_allow_html=True)
            f_a, f_b = st.columns(2)
            with f_a:
                in_spent = st.number_input("Tổng giá trị đơn hàng (R$)", min_value=1.0, value=float(def_spent), step=10.0, key=f"spent_{form_key_suffix}")
            with f_b:
                in_installments = st.number_input("Số kỳ trả góp", min_value=1, max_value=24, value=int(def_inst), key=f"inst_{form_key_suffix}")

            pay_keys = list(PAYMENTS_DICT.keys())
            pay_idx = pay_keys.index(def_pay) if def_pay in pay_keys else 0
            in_pay_type = st.selectbox("Phương thức thanh toán", pay_keys, index=pay_idx, format_func=lambda k: PAYMENTS_DICT.get(k, k), key=f"pay_{form_key_suffix}")

            st.markdown("<b>Vận chuyển & trải nghiệm</b>", unsafe_allow_html=True)
            f_c, f_d = st.columns(2)
            with f_c:
                in_delivery = st.number_input("Số ngày giao thực tế", min_value=1.0, value=float(def_deliv), step=1.0, key=f"deliv_{form_key_suffix}")
            with f_d:
                in_est_delivery = st.number_input("Số ngày giao dự kiến (SLA)", min_value=1.0, value=float(def_est), step=1.0, key=f"est_{form_key_suffix}")
            in_review = st.slider("Điểm đánh giá (Review score)", 1, 5, int(def_score), key=f"rev_{form_key_suffix}")

            st.markdown("<b>Khách hàng & sản phẩm</b>", unsafe_allow_html=True)
            state_keys = list(STATES_DICT.keys())
            state_idx = state_keys.index(def_state) if def_state in state_keys else 0
            in_state = st.selectbox("Bang khách hàng", state_keys, index=state_idx, format_func=lambda k: STATES_DICT.get(k, k), key=f"state_{form_key_suffix}")

            cat_keys = list(CATEGORIES_DICT.keys())
            cat_idx = cat_keys.index(def_cat) if def_cat in cat_keys else 0
            in_category = st.selectbox("Ngành hàng sản phẩm", cat_keys, index=cat_idx, format_func=lambda k: CATEGORIES_DICT.get(k, k), key=f"cat_{form_key_suffix}")

            submitted = st.form_submit_button("CHẠY DỰ BÁO AI VÀ GÁN CHÍNH SÁCH CAN THIỆP", type="primary", use_container_width=True)

    with col_results:
        try:
            predictor = load_predictor(DEFAULT_MODEL_DIR)
            res = predictor.predict_and_prescribe(
                order_spent=in_spent, max_installments=in_installments, payment_type=in_pay_type,
                delivery_days=in_delivery, estimated_delivery_days=in_est_delivery, review_score=in_review,
                customer_state=in_state, product_category=in_category
            )

            st.markdown("### KẾT QUẢ DỰ BÁO AI VÀ GIẢI THÍCH TREESHAP")
            m_top1, m_top2 = st.columns(2)
            m_top1.metric("Xác suất Giữ chân P(Retain)", res["prob_retain_pct"])
            m_top2.metric("Tỷ lệ Rời bỏ P(Churn)", res["prob_churn_pct"])

            m_bot1, m_bot2 = st.columns(2)
            m_bot1.metric("Phân tầng Rủi ro", res["risk_tier"].split(":")[0], help=res["risk_tier"])
            m_bot2.metric("Luồng Thực thi", res["assigned_engine"].split("(")[0], help=res["assigned_engine"])

            _p_churn = _pct_to_float(res["prob_churn_pct"])
            if _p_churn is not None:
                st.progress(_p_churn, text=f"Mức nguy cơ rời bỏ: {res['prob_churn_pct']}")

            st.divider()

            st.markdown("#### Bóc Tách 4 Nhóm Động Lực (TreeSHAP XAI)")
            df_pie = res["pie_chart_data"]

            if HAS_PLOTLY:
                fig_donut = px.pie(
                    df_pie, names="Nhóm Nguyên Nhân", values="Tỷ trọng (%)", hole=0.55,
                    color="Nhóm Nguyên Nhân",
                    color_discrete_map={
                        "Logistics & Vận chuyển": "#0284c7",
                        "Trải nghiệm Đánh giá": "#f59e0b",
                        "Tài chính & Trả góp": "#10b981",
                        "Ngành hàng & Vùng miền": "#dc2626"
                    }
                )
                fig_donut.update_traces(textposition='inside', textinfo='percent+label', textfont_size=15)
                fig_donut.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320, showlegend=False)
                st.plotly_chart(fig_donut, use_container_width=True)
            else:
                st.dataframe(df_pie, hide_index=True, use_container_width=True)

            st.info(f"**Yếu tố tác động lớn nhất:** {res['top_cause']}")

            st.markdown("#### Gói Chính Sách Can Thiệp Chỉ Định")
            st.success(f"**{res['action_title']}**\n\n"
                       f"- **Nội dung thực thi:** {res['action_desc']}\n"
                       f"- **Kênh triển khai:** {res['action_channel']}\n"
                       f"- **Phân luồng:** {res['assigned_engine']}")

        except Exception as e:
            st.error(f"Có lỗi khi thực thi dự báo: {e}")

# ===========================================================================
# 2. PHÂN HỆ: 01. DESCRIPTIVE
# ===========================================================================
elif nav_choice == "01. Descriptive":
    section_header("01. Phân Tích Mô Tả (Descriptive Analytics)")
    st.markdown("Tổng hợp đặc trưng phân phối của **92,077 khách hàng** giao dịch thành công.")
    eda_tabs = st.tabs([CHARTS_CONFIG[k]["tab_label"] for k in CHARTS_CONFIG])
    for s_tab, k in zip(eda_tabs, CHARTS_CONFIG):
        with s_tab:
            render_chart_group_alternating(k, config=CHARTS_CONFIG)

# ===========================================================================
# 3. PHÂN HỆ: 02. DIAGNOSTIC
# ===========================================================================
elif nav_choice == "02. Diagnostic":
    section_header("02. Phân Tích Chẩn Đoán (Diagnostic Hypotheses)")
    st.markdown("Kiểm định thống kê chuyên sâu ($p$-value, Chi-Square, Mann-Whitney U) trên **5 yếu tố nghi vấn**.")
    
    with st.expander("BẢNG TỔNG HỢP KẾT QUẢ KIỂM ĐỊNH 5 GIẢ THUYẾT", expanded=False):
        st.markdown(r"""
        | STT | Giả thuyết Nghi vấn | Kết quả Thống kê | Mức Ý nghĩa ($p$-value) | Kết luận Nghiệp vụ |
        | :---: | :--- | :--- | :---: | :--- |
        | **2** | Tỷ trọng phí vận chuyển | Churn $18.3\%$ vs Active $19.2\%$ | $p > 0.05$ | **Bác bỏ**: Phí ship không tạo ra sự phân hóa lớn |
        | **3** | Số ngày giao trễ tuyệt đối | Chênh lệch trung bình không đáng kể | $p = 0.7554$ | **Bác bỏ**: Bị trễ quan trọng hơn trễ bao nhiêu ngày |
        | **4** | Đánh giá xấu (1-2 sao) | Churn $12.45\%$ vs Active $9.48\%$ | $p < 0.001$ | **Chấp nhận**: Tín hiệu cảnh báo churn mạnh nhất |
        | **5** | Ngành hàng sản phẩm | Churn dao động từ $73.8\% \to 87.1\%$ | $p < 0.001$ | **Chấp nhận**: Ngành hàng lâu bền có churn cao tự nhiên |
        | **6** | Vùng địa lý & KT-XH | Đông Nam churn thấp hơn Ngoại vi | $p < 0.001$ | **Chấp nhận**: Hạ tầng logistics chi phối tỷ lệ churn |
        """)
    st.divider()
    
    diag_tabs = st.tabs([DIAGNOSTIC_CONFIG[k]["tab_label"] for k in DIAGNOSTIC_CONFIG])
    for d_tab, k in zip(diag_tabs, DIAGNOSTIC_CONFIG):
        with d_tab:
            render_chart_group_alternating(k, config=DIAGNOSTIC_CONFIG)

# ===========================================================================
# 4. PHÂN HỆ: 03. PREDICTIVE
# ===========================================================================
elif nav_choice == "03. Predictive":
    section_header("03. Đánh Giá Mô Hình Dự Báo (Predictive Modeling)")
    st.markdown("Đối sáng hiệu năng kỹ thuật giữa **Baseline (Logistic Regression)** và **Advanced (XGBoost Giai đoạn 2)**.")
    
    st.info("**Điểm Đột Phá Giai Đoạn 2:** XGBoost nâng Recall lên **57.36% (đỉnh 77.36%)**, khoanh vùng chính xác **22.97% tệp khách hàng** cần cứu vãn.")
    st.divider()
    
    model_tabs = st.tabs([MODEL_CONFIG[k]["tab_label"] for k in MODEL_CONFIG])
    for m_tab, k in zip(model_tabs, MODEL_CONFIG):
        with m_tab:
            render_chart_group_alternating(k, config=MODEL_CONFIG)

# ===========================================================================
# 5. PHÂN HỆ: 04. PRESCRIPTIVE
# ===========================================================================
elif nav_choice == "04. Prescriptive":
    section_header("04. Chiến Lược Chỉ Định và Tối Ưu Hóa Ngân Sách (Prescriptive Analytics)")
    st.markdown("Tối ưu hóa ngân sách qua **Thuật toán Knapsack ILP** và **Cơ chế Phân luồng Kép (Dual-Engine)**.")
    
    p_tab1, p_tab2, p_tab3, p_tab4 = st.tabs([
        "1. Phân Cụm Điểm Nghẽn (K-Means)",
        "2. Tối Ưu Knapsack & Phân Bổ Vốn",
        "3. Điểm Hòa Vốn & Kiểm Định Kịch Bản",
        "4. Tổng Kết Chiến Lược & Bộ Giả Lập Tài Chính Kép"
    ])
    
    with p_tab1:
        st.markdown("### Bước 1 & 2: Khảo Sát Điểm Nghẽn và Phân Cụm K-Means ($k=4$)")
        render_chart_group_alternating("clustering", config=PRESCRIPTIVE_CONFIG)
        
    with p_tab2:
        st.markdown("### Bước 5: Tối Ưu Hóa Ngân Sách Knapsack Tuyến Tính Nguyên (ILP)")
        render_chart_group_alternating("knapsack_budget", config=PRESCRIPTIVE_CONFIG)
        
    with p_tab3:
        st.markdown("### Bước 6: Ma Trận Hòa Vốn và Kiểm Định Stress-Test 3 Kịch Bản")
        render_chart_group_alternating("risk_scenarios", config=PRESCRIPTIVE_CONFIG)
        
    with p_tab4:
        st.markdown("### Bộ Giả Lập Tài Chính Kép Tương Tác (Dual-Engine ROI Simulator)")
        
        sim_col1, sim_col2 = st.columns(2, gap="large")
        with sim_col1:
            with st.container(border=True):
                st.markdown("##### Luồng Tier 2A: Khách Hàng VIP (Cấp Vốn)")
                s_target = st.slider("Quy mô tệp VIP Tier 2A", 100, 1500, 600, step=50)
                s_cost = st.number_input("Chi phí voucher TB (R$/khách)", min_value=1.0, value=6.34, step=0.5)
                s_uplift = st.slider("Tỷ lệ giữ chân kỳ vọng Tier 2A (%)", 5.0, 50.0, 25.0, step=1.0)
                s_aov = st.number_input("AOV trung bình (R$)", min_value=50.0, value=140.0, step=10.0)
                s_margin = st.slider("Biên lợi nhuận ròng sàn (%)", 10.0, 50.0, 30.0, step=5.0)

        with sim_col2:
            with st.container(border=True):
                st.markdown("##### Luồng Tier 2B: Khách Nền Tảng (Tự Tài Trợ)")
                s_b_target = st.number_input("Quy mô tệp Nền tảng Tier 2B", min_value=1000, value=12925, step=500)
                s_b_conv = st.slider("Tỷ lệ kích hoạt mua lại Tier 2B (%)", 1.0, 15.0, 5.0, step=0.5)
                s_b_min_cart = st.number_input("Giá trị giỏ hàng tối thiểu Min-Cart (R$)", min_value=100.0, value=210.0, step=10.0)
                s_b_margin = st.slider("Biên lợi nhuận sau giảm giá Tier 2B (%)", 10.0, 40.0, 22.0, step=2.0)

        cost_2a = s_target * s_cost
        rev_2a = s_target * (s_uplift / 100.0) * s_aov * 1.5
        profit_2a = (rev_2a * (s_margin / 100.0)) - cost_2a
        roi_2a = (profit_2a / max(cost_2a, 1.0)) * 100.0

        rev_2b = s_b_target * (s_b_conv / 100.0) * s_b_min_cart
        profit_2b = rev_2b * (s_b_margin / 100.0)

        total_budget = cost_2a
        total_rev = rev_2a + rev_2b
        total_profit = profit_2a + profit_2b
        multiple = total_profit / max(total_budget, 1.0)

        st.markdown("---")
        st.markdown("##### BẢNG KẾT QUẢ MÔ PHỎNG TÀI CHÍNH HỢP NHẤT")
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Tổng Vốn Cấp Trước", f"R$ {total_budget:,.2f}")
        r2.metric("Tổng Doanh Số Kỳ Vọng", f"R$ {total_rev:,.2f}")
        r3.metric("Tổng Lợi Nhuận Ròng", f"R$ {total_profit:,.2f}")
        r4.metric("Hệ Số Sinh Lời Vốn", f"{multiple:.1f}× Vốn", delta=f"ROI Tier 2A: {roi_2a:.1f}%")

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.divider()
st.caption("Olist E-Commerce Retention Intelligence Platform")