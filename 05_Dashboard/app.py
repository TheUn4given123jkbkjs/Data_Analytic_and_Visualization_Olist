"""
DASHBOARD PHÂN TÍCH VÀ DỰ ĐOÁN RỜI BỎ KHÁCH HÀNG (CUSTOMER RETENTION INTELLIGENCE)
Sàn Thương mại Điện tử Brazil (Olist E-Commerce)

Cấu trúc 5 Tab Chuyên sâu:
  Tab 1 (Nhân vật chính): DEMO TRỰC TIẾP: DỰ BÁO VÀ CHỈ ĐỊNH HÀNH ĐỘNG
  Tab 2: 01. Phân tích Mô tả (Descriptive Analytics & EDA)
  Tab 3: 02. Phân tích Chẩn đoán (Diagnostic Hypotheses & 6 Yếu tố Churn)
  Tab 4: 03. Đánh giá Mô hình Dự báo (Predictive Modeling: Baseline vs XGBoost Giai đoạn 2)
  Tab 5: 04. Chiến lược Chỉ định & Tối ưu hóa Ngân sách (Prescriptive Strategy & Knapsack ILP)

Chạy Dashboard: streamlit run 05_Dashboard/app.py
"""

import os
import sys
import textwrap
import streamlit as st
import pandas as pd
import numpy as np

try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

import importlib
import charts_config
importlib.reload(charts_config)
from charts_config import CHARTS_CONFIG, DIAGNOSTIC_CONFIG, MODEL_CONFIG, PRESCRIPTIVE_CONFIG

# ---------------------------------------------------------------------------
# CẤU HÌNH TRANG & CSS TÙY BIẾN
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Olist Retention Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Custom CSS cho khung nhận xét (Insight Cards) và Badges
st.markdown("""
<style>
    .insight-card {
        background-color: #f8f9fa;
        border-left: 5px solid #1f77b4;
        padding: 16px 20px;
        border-radius: 6px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .insight-card h4 {
        margin-top: 0;
        color: #0f4c81;
        font-weight: 700;
        font-size: 1.35rem;
    }
    .insight-text {
        font-size: 30px !important;
        line-height: 1.55;
        color: #1e293b;
    }
    .metric-sub {
        font-size: 0.85rem;
        color: #6c757d;
        margin-top: -8px;
    }
    .badge-tier {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    /* Tùy biến thanh trượt cuộn ngang (Horizontal Scroll Slider) cho tất cả các Subtabs */
    [data-testid="stTabs"] {
        width: 100%;
        margin-top: 8px;
        margin-bottom: 16px;
    }
    div[data-baseweb="tab-list"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        overflow-y: hidden !important;
        white-space: nowrap !important;
        scrollbar-width: thin !important;
        scrollbar-color: #1f77b4 #e9ecef !important;
        padding-bottom: 8px !important;
        margin-bottom: 12px !important;
        gap: 8px !important;
        scroll-behavior: smooth !important;
        -webkit-overflow-scrolling: touch !important;
        border-bottom: 1px solid #dee2e6;
    }
    div[data-baseweb="tab-list"]::-webkit-scrollbar {
        height: 6px !important;
    }
    div[data-baseweb="tab-list"]::-webkit-scrollbar-track {
        background: #e9ecef !important;
        border-radius: 4px !important;
    }
    div[data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
        background: #1f77b4 !important;
        border-radius: 4px !important;
    }
    div[data-baseweb="tab-list"]::-webkit-scrollbar-thumb:hover {
        background: #0f4c81 !important;
    }
    div[data-baseweb="tab-list"] button {
        flex-shrink: 0 !important;
        white-space: nowrap !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        transition: all 0.2s ease-in-out !important;
    }
    div[data-baseweb="tab-list"] button:hover {
        background-color: #f1f3f5 !important;
        color: #0f4c81 !important;
    }

    /* =======================================================================
       CARD BIỂU ĐỒ VÀ KHUNG NHẬN XÉT TRƯỢT 4 HƯỚNG TƯƠNG TÁC
       ======================================================================= */
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(24px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-24px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pushLeft {
        from { transform: translateX(12px); }
        to { transform: translateX(0); }
    }
    @keyframes pushRight {
        from { transform: translateX(-12px); }
        to { transform: translateX(0); }
    }
    @keyframes pushUp {
        from { transform: translateY(12px); }
        to { transform: translateY(0); }
    }
    @keyframes pushDown {
        from { transform: translateY(-12px); }
        to { transform: translateY(0); }
    }
    .anim-slide-in-right { animation: slideInRight 0.35s cubic-bezier(0.25, 1, 0.5, 1); }
    .anim-slide-in-left { animation: slideInLeft 0.35s cubic-bezier(0.25, 1, 0.5, 1); }
    .anim-slide-in-up { animation: slideInUp 0.35s cubic-bezier(0.25, 1, 0.5, 1); }
    .anim-slide-in-down { animation: slideInDown 0.35s cubic-bezier(0.25, 1, 0.5, 1); }
    .anim-push-left { animation: pushLeft 0.35s cubic-bezier(0.25, 1, 0.5, 1); }
    .anim-push-right { animation: pushRight 0.35s cubic-bezier(0.25, 1, 0.5, 1); }
    .anim-push-up { animation: pushUp 0.35s cubic-bezier(0.25, 1, 0.5, 1); }
    .anim-push-down { animation: pushDown 0.35s cubic-bezier(0.25, 1, 0.5, 1); }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CORE_DIR = os.path.join(BASE_DIR, "core")
sys.path.insert(0, CORE_DIR)
sys.path.insert(0, BASE_DIR)

# Danh sách các thư mục chứa ảnh assets của từng Module
SEARCH_ASSET_DIRS = [
    os.path.join(BASE_DIR, "assets"),
    os.path.join(PROJECT_ROOT, "01_Descriptive", "assets"),
    os.path.join(PROJECT_ROOT, "02_Diagnostic", "assets"),
    os.path.join(PROJECT_ROOT, "03_Predictive", "assets"),
    os.path.join(PROJECT_ROOT, "04_Prescriptive", "figures"),
    os.path.join(PROJECT_ROOT, "04_Prescriptive", "assets"),
    os.path.join(PROJECT_ROOT, "01_Descriptive"),
    os.path.join(PROJECT_ROOT, "02_Diagnostic"),
    os.path.join(PROJECT_ROOT, "03_Predictive"),
    os.path.join(PROJECT_ROOT, "04_Prescriptive"),
]

FALLBACK_FILENAMES = {
    "pareto_categories_modelstage.png": "pareto_categories.png"
}

def find_image_path(filename: str):
    """Tìm đường dẫn tuyệt đối của file ảnh trong toàn bộ các thư mục assets."""
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

# ---------------------------------------------------------------------------
# HÀM HIỂN THỊ BIỂU ĐỒ VÀ 3 THANH MŨI TÊN KÉO NHẬN XÉT VIỀN QUANH ẢNH
# ---------------------------------------------------------------------------
def render_chart_sliding(chart: dict, index: int, uid_prefix: str = "c"):
    """
    Hiển thị biểu đồ theo đúng bản vẽ thiết kế:
    - 3 thanh mũi tên mờ được gắn trực tiếp ở 3 viền xung quanh ảnh (Trái, Phải, Dưới).
    - Hỗ trợ cấu hình riêng (allowed_directions) cho từng subtab EDA.
    - Cỡ chữ nhận xét 20px dễ đọc.
    """
    st.subheader(chart['title'])
    img_path = find_image_path(chart["file"])
    
    uid = f"{uid_prefix}_{index}_{abs(hash(chart['file'])) % 100000}"
    state_key = f"drawer_state_{uid}"
    
    allowed_dirs = chart.get("allowed_directions", ["right", "left", "bottom"])
    img_scale = chart.get("img_scale", 1.0)
    
    if state_key not in st.session_state:
        if len(allowed_dirs) == 1:
            st.session_state[state_key] = allowed_dirs[0]
        else:
            st.session_state[state_key] = ["right", "left", "bottom"][index % 3]
            
    current_state = st.session_state[state_key]
    if current_state not in allowed_dirs and current_state != "closed":
        current_state = allowed_dirs[0]
    
    def render_caption_fixed():
        caption_parts = []
        if chart.get("x_label"):
            caption_parts.append(f"**Trục X:** {chart['x_label']}")
        if chart.get("y_label"):
            caption_parts.append(f"**Trục Y:** {chart['y_label']}")
        if chart.get("legend"):
            caption_parts.append(f"**Chú thích:** {chart['legend']}")
        
        if caption_parts:
            st.caption(" &nbsp;|&nbsp; ".join(caption_parts))

    def render_raw_image():
        if img_path and os.path.exists(img_path):
            if img_scale < 1.0:
                pad = (1.0 - img_scale) / 2.0
                c_p1, c_img_sub, c_p2 = st.columns([pad, img_scale, pad])
                with c_img_sub:
                    st.image(img_path, use_container_width=True)
            else:
                st.image(img_path, use_container_width=True)
        else:
            st.warning(f"Chưa tìm thấy file ảnh: `{chart['file']}`")

    def render_framed_image():
        """Vẽ khối ảnh với các thanh mũi tên viền tương ứng (chỉ hiển thị ký hiệu mũi tên)."""
        # Trường hợp chỉ cho phép kéo từ dưới
        if allowed_dirs == ["bottom"]:
            render_raw_image()
            if current_state == "bottom":
                if st.button("⇧", key=f"btn_close_b_{uid}", help="Thu gọn nhận xét vào sau ảnh", use_container_width=True):
                    st.session_state[state_key] = "closed"
                    st.rerun()
            else:
                if st.button("⇩", key=f"btn_open_b_{uid}", help="Kéo mở nhận xét phía dưới (100% chiều ngang)", use_container_width=True):
                    st.session_state[state_key] = "bottom"
                    st.rerun()
            render_caption_fixed()
            return

        # Trường hợp chỉ cho phép kéo bên phải
        if allowed_dirs == ["right"]:
            c_center_img, c_right_strip = st.columns([0.94, 0.06])
            with c_center_img:
                render_raw_image()
                render_caption_fixed()
            with c_right_strip:
                if current_state == "right":
                    if st.button("⇦", key=f"btn_close_r_{uid}", help="Thu gọn nhận xét vào sau ảnh", use_container_width=True):
                        st.session_state[state_key] = "closed"
                        st.rerun()
                else:
                    if st.button("⇨", key=f"btn_open_r_{uid}", help="Kéo nhận xét sang bên Phải (70:30)", use_container_width=True):
                        st.session_state[state_key] = "right"
                        st.rerun()
            return

        # Trường hợp chỉ cho phép kéo bên trái
        if allowed_dirs == ["left"]:
            c_left_strip, c_center_img = st.columns([0.06, 0.94])
            with c_left_strip:
                if current_state == "left":
                    if st.button("⇨", key=f"btn_close_l_{uid}", help="Thu gọn nhận xét vào sau ảnh", use_container_width=True):
                        st.session_state[state_key] = "closed"
                        st.rerun()
                else:
                    if st.button("⇦", key=f"btn_open_l_{uid}", help="Kéo nhận xét sang bên Trái (30:70)", use_container_width=True):
                        st.session_state[state_key] = "left"
                        st.rerun()
            with c_center_img:
                render_raw_image()
                render_caption_fixed()
            return

        # Trường hợp đầy đủ 3 hướng (Trái, Phải, Dưới)
        c_left_strip, c_center_img, c_right_strip = st.columns([0.06, 0.88, 0.06])
        with c_left_strip:
            if current_state == "left":
                if st.button("⇨", key=f"btn_close_l_{uid}", help="Thu gọn nhận xét vào sau ảnh", use_container_width=True):
                    st.session_state[state_key] = "closed"
                    st.rerun()
            else:
                if st.button("⇦", key=f"btn_open_l_{uid}", help="Kéo nhận xét sang bên Trái (30:70)", use_container_width=True):
                    st.session_state[state_key] = "left"
                    st.rerun()
                    
        with c_center_img:
            render_raw_image()
            if current_state == "bottom":
                if st.button("⇧", key=f"btn_close_b_{uid}", help="Thu gọn nhận xét vào sau ảnh", use_container_width=True):
                    st.session_state[state_key] = "closed"
                    st.rerun()
            else:
                if st.button("⇩", key=f"btn_open_b_{uid}", help="Kéo mở nhận xét phía dưới (100% chiều ngang)", use_container_width=True):
                    st.session_state[state_key] = "bottom"
                    st.rerun()
            render_caption_fixed()

        with c_right_strip:
            if current_state == "right":
                if st.button("⇦", key=f"btn_close_r_{uid}", help="Thu gọn nhận xét vào sau ảnh", use_container_width=True):
                    st.session_state[state_key] = "closed"
                    st.rerun()
            else:
                if st.button("⇨", key=f"btn_open_r_{uid}", help="Kéo nhận xét sang bên Phải (70:30)", use_container_width=True):
                    st.session_state[state_key] = "right"
                    st.rerun()

    def render_insight_card(anim_class: str = "anim-slide-in-right"):
        st.markdown(f"""
        <div class="insight-card {anim_class}">
            <h4>NHẬN XÉT</h4>
            <p class="insight-text">{chart['insight']}</p>
        </div>
        """, unsafe_allow_html=True)

    # 1. Trạng thái: Kéo sang Phải (Ảnh 70% | Nhận xét 30%)
    if current_state == "right":
        col_img, col_ins = st.columns([7, 3])
        with col_img:
            render_framed_image()
        with col_ins:
            render_insight_card("anim-slide-in-right")
            
    # 2. Trạng thái: Kéo sang Trái (Nhận xét 30% | Ảnh 70%)
    elif current_state == "left":
        col_ins, col_img = st.columns([3, 7])
        with col_ins:
            render_insight_card("anim-slide-in-left")
        with col_img:
            render_framed_image()
            
    # 3. Trạng thái: Kéo xuống Dưới (100% chiều ngang)
    elif current_state == "bottom":
        render_framed_image()
        render_insight_card("anim-slide-in-up")
        
    # 4. Trạng thái: Thu gọn (Giấu sau ảnh)
    elif current_state == "closed":
        render_framed_image()




def render_chart_group_sliding(group_key: str, config: dict):
    group = config[group_key]
    charts = group["charts"]
    for i, chart in enumerate(charts):
        render_chart_sliding(chart, index=i, uid_prefix=group_key)
        if i < len(charts) - 1:
            st.divider()

# Alias hỗ trợ tương thích
render_chart_alternating = render_chart_sliding
render_chart_group_alternating = render_chart_group_sliding



# ---------------------------------------------------------------------------
# SIDEBAR ĐIỀU HƯỚNG MỤC PHÂN TÍCH
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("Olist Retention AI")
    st.caption("Hệ thống Dự báo & Tối ưu hóa Giữ chân Khách hàng")
    st.divider()
    
    st.markdown("### ĐIỀU HƯỚNG CHƯƠNG TRÌNH")
    nav_choice = st.radio(
        "Lựa chọn phân hệ phân tích:",
        [
            "DEMO TRỰC TIẾP: DỰ BÁO & CHỈ ĐỊNH",
            "01. Phân tích Mô tả (EDA)",
            "02. Phân tích Chẩn đoán (Diagnostic)",
            "03. Đánh giá Mô hình Dự báo (Predictive)",
            "04. Chiến lược Tối ưu hóa (Prescriptive)"
        ],
        index=0,
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("Đồ án Phân tích và Trực quan hóa Dữ liệu · TDTU")

# ---------------------------------------------------------------------------
# HEADER CHỈ SỐ TOÀN DIỆN
# ---------------------------------------------------------------------------
st.title("Hệ Thống Dự Báo và Tối Ưu Hóa Giữ Chân Khách Hàng Olist")
st.caption("Chuỗi giá trị: Descriptive (01) → Diagnostic (02) → Predictive (03) → Prescriptive (04)")

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
# 1. PHÂN HỆ: DEMO TRỰC TIẾP (NHÂN VẬT CHÍNH)
# ===========================================================================
if nav_choice == "DEMO TRỰC TIẾP: DỰ BÁO & CHỈ ĐỊNH":
    st.markdown("## Dự Đoán Thời Gian Thực và Chỉ Định Hành Động")
    st.markdown(
        "Nhập thông tin đơn hàng đầu tiên ($T_0$) của khách hàng để Mô hình AI dự báo xác suất quay lại, "
        "tự động bóc tách **4 nhóm nguyên nhân TreeSHAP** và gán **Gói chính sách Marketing tối ưu**."
    )
    
    st.markdown("### Chọn Nhanh Mẫu Khách Hàng Điển Hình")
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    
    preset_chosen = None
    with p_col1:
        if st.button("Khách Trả góp Đơn lớn (Cụm 0)", use_container_width=True):
            preset_chosen = {
                "order_spent": 380.0, "max_installments": 10, "payment_type": "credit_card",
                "delivery_days": 7.0, "estimated_delivery_days": 18.0, "review_score": 5,
                "customer_state": "SP", "product_category": "relogios_presentes"
            }
    with p_col2:
        if st.button("Khách Đánh giá 1 Sao (Cụm 1)", use_container_width=True):
            preset_chosen = {
                "order_spent": 95.0, "max_installments": 2, "payment_type": "credit_card",
                "delivery_days": 12.0, "estimated_delivery_days": 15.0, "review_score": 1,
                "customer_state": "RJ", "product_category": "beleza_saude"
            }
    with p_col3:
        if st.button("Khách Giao hàng Trễ hạn (Cụm 2)", use_container_width=True):
            preset_chosen = {
                "order_spent": 140.0, "max_installments": 3, "payment_type": "credit_card",
                "delivery_days": 28.0, "estimated_delivery_days": 12.0, "review_score": 2,
                "customer_state": "BA", "product_category": "cama_mesa_banho"
            }
    with p_col4:
        if st.button("Khách hàng Vãng lai (Tier 1)", use_container_width=True):
            preset_chosen = {
                "order_spent": 35.0, "max_installments": 1, "payment_type": "boleto",
                "delivery_days": 6.0, "estimated_delivery_days": 14.0, "review_score": 5,
                "customer_state": "SP", "product_category": "telefonia"
            }

    # Form nhập liệu
    with st.form("hero_prediction_form"):
        st.markdown("#### Thông số Đơn hàng Đầu tiên ($T_0$)")
        f_c1, f_c2, f_c3 = st.columns(3)
        
        # Mặc định lấy từ preset hoặc giá trị chuẩn
        def_spent = preset_chosen["order_spent"] if preset_chosen else 150.0
        def_inst = preset_chosen["max_installments"] if preset_chosen else 3
        def_pay = preset_chosen["payment_type"] if preset_chosen else "credit_card"
        def_deliv = preset_chosen["delivery_days"] if preset_chosen else 8.0
        def_est = preset_chosen["estimated_delivery_days"] if preset_chosen else 15.0
        def_score = preset_chosen["review_score"] if preset_chosen else 5
        def_state = preset_chosen["customer_state"] if preset_chosen else "SP"
        def_cat = preset_chosen["product_category"] if preset_chosen else "cama_mesa_banho"
        
        with f_c1:
            in_spent = st.number_input("Tổng giá trị đơn hàng (R$)", min_value=1.0, value=float(def_spent), step=10.0)
            in_installments = st.number_input("Số kỳ trả góp", min_value=1, max_value=24, value=int(def_inst))
            pay_keys = list(PAYMENTS_DICT.keys())
            pay_idx = pay_keys.index(def_pay) if def_pay in pay_keys else 0
            in_pay_type = st.selectbox(
                "Phương thức thanh toán", pay_keys,
                index=pay_idx,
                format_func=lambda k: PAYMENTS_DICT.get(k, k)
            )
        with f_c2:
            in_delivery = st.number_input("Số ngày giao hàng thực tế", min_value=1.0, value=float(def_deliv), step=1.0)
            in_est_delivery = st.number_input("Số ngày giao hàng dự kiến (SLA)", min_value=1.0, value=float(def_est), step=1.0)
            in_review = st.slider("Điểm đánh giá (Review score)", 1, 5, int(def_score))
        with f_c3:
            state_keys = list(STATES_DICT.keys())
            state_idx = state_keys.index(def_state) if def_state in state_keys else 0
            in_state = st.selectbox(
                "Bang khách hàng (State / Região)", state_keys,
                index=state_idx,
                format_func=lambda k: STATES_DICT.get(k, k)
            )
            cat_keys = list(CATEGORIES_DICT.keys())
            cat_idx = cat_keys.index(def_cat) if def_cat in cat_keys else 0
            in_category = st.selectbox(
                "Ngành hàng sản phẩm (Category)", cat_keys,
                index=cat_idx,
                format_func=lambda k: CATEGORIES_DICT.get(k, k)
            )
            
        submitted = st.form_submit_button("CHẠY DỰ BÁO VÀ GÁN CHÍNH SÁCH CAN THIỆP", use_container_width=True)

    if submitted or preset_chosen is not None:
        try:
            from model_helper import OlistCustomerPredictor
            predictor = OlistCustomerPredictor(model_dir=DEFAULT_MODEL_DIR)
            
            res = predictor.predict_and_prescribe(
                order_spent=in_spent,
                max_installments=in_installments,
                payment_type=in_pay_type,
                delivery_days=in_delivery,
                estimated_delivery_days=in_est_delivery,
                review_score=in_review,
                customer_state=in_state,
                product_category=in_category
            )
            
            st.divider()
            st.markdown("### KẾT QUẢ DỰ BÁO AI VÀ GIẢI THÍCH TREESHAP")
            
            # 4 Thẻ Chỉ số Kết quả
            m_res1, m_res2, m_res3, m_res4 = st.columns(4)
            m_res1.metric("Xác suất Giữ chân P(Retain)", res["prob_retain_pct"])
            m_res2.metric("Tỷ lệ Rời bỏ P(Churn)", res["prob_churn_pct"])
            m_res3.metric("Phân tầng Rủi ro", res["risk_tier"].split(":")[0], help=res["risk_tier"])
            m_res4.metric("Luồng Thực thi", res["assigned_engine"].split("(")[0], help=res["assigned_engine"])
            
            st.markdown("---")
            
            # 2 Cột: Donut Chart SHAP (Trái) | Gói Hành động (Phải)
            res_left, res_right = st.columns([1, 1])
            
            with res_left:
                st.markdown("#### Bóc Tách 4 Nhóm Động Lực (TreeSHAP XAI)")
                df_pie = res["pie_chart_data"]
                
                if HAS_PLOTLY:
                    fig_donut = px.pie(
                        df_pie,
                        names="Nhóm Nguyên Nhân",
                        values="Tỷ trọng (%)",
                        hole=0.55,
                        color="Nhóm Nguyên Nhân",
                        color_discrete_map={
                            "Logistics & Vận chuyển": "#e63946",
                            "Trải nghiệm Đánh giá": "#f4a261",
                            "Tài chính & Trả góp": "#2a9d8f",
                            "Ngành hàng & Vùng miền": "#457b9d"
                        }
                    )
                    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
                    fig_donut.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320, showlegend=False)
                    st.plotly_chart(fig_donut, use_container_width=True)
                else:
                    st.dataframe(df_pie, hide_index=True, use_container_width=True)
                st.caption(f"**Yếu tố tác động lớn nhất:** {res['top_cause']}")

            with res_right:
                st.markdown("#### Gói Chính Sách Can Thiệp Chỉ Định")
                st.success(f"### {res['action_title']}")
                st.markdown(f"**Nội dung thực thi:**\n{res['action_desc']}")
                st.info(f"**Kênh tiếp thị và Đối chuẩn:** {res['action_channel']}")
                st.markdown(f"**Phân luồng Hệ thống:** `{res['assigned_engine']}`")
                
        except Exception as e:
            st.error(f"Có lỗi khi thực thi dự báo: {e}")

# ===========================================================================
# 2. PHÂN HỆ: 01. PHÂN TÍCH MÔ TẢ (EDA)
# ===========================================================================
elif nav_choice == "01. Phân tích Mô tả (EDA)":
    st.markdown("## 01. Phân Tích Mô Tả (Descriptive Analytics)")
    st.markdown(
        "Tổng hợp đặc trưng phân phối của **92,077 khách hàng** giao dịch thành công. "
        "Bố cục so le 2 cột nhấn mạnh trực tiếp vào bài học nghiệp vụ rút ra."
    )
    eda_tabs = st.tabs([CHARTS_CONFIG[k]["tab_label"] for k in CHARTS_CONFIG])
    for s_tab, k in zip(eda_tabs, CHARTS_CONFIG):
        with s_tab:
            render_chart_group_alternating(k, config=CHARTS_CONFIG)

# ===========================================================================
# 3. PHÂN HỆ: 02. PHÂN TÍCH CHẨN ĐOÁN (DIAGNOSTIC)
# ===========================================================================
elif nav_choice == "02. Phân tích Chẩn đoán (Diagnostic)":
    st.markdown("## 02. Phân Tích Chẩn Đoán (Diagnostic Hypotheses)")
    st.markdown(
        "Kiểm định thống kê chuyên sâu ($p$-value, Chi-Square, Mann-Whitney U) trên **6 yếu tố nghi vấn** "
        "gây rời bỏ khách hàng giữa nhóm Active (< 90 ngày) và nhóm Churn (≥ 90 ngày)."
    )
    
    # Bảng tóm tắt kết quả kiểm định (Kéo mở rộng từ bên dưới)
    with st.expander("⇩ BẢNG TỔNG HỢP KẾT QUẢ KIỂM ĐỊNH 6 GIẢ THUYẾT ⇩", expanded=False):
        st.markdown(r"""
        | STT | Giả thuyết Nghi vấn | Kết quả Thống kê | Mức Ý nghĩa ($p$-value) | Kết luận Nghiệp vụ |
        | :---: | :--- | :--- | :---: | :--- |
        | **1** | Giao hàng trễ hạn | Churn $6.25\%$ vs Active $3.54\%$ | $p < 0.001$ | **Chấp nhận**: Giao trễ làm tăng vọt nguy cơ rời bỏ |
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
# 4. PHÂN HỆ: 03. ĐÁNH GIÁ MÔ HÌNH DỰ BÁO (PREDICTIVE EVALUATION)
# ===========================================================================
elif nav_choice == "03. Đánh giá Mô hình Dự báo (Predictive)":
    st.markdown("## 03. Đánh Giá Mô Hình Dự Báo (Predictive Modeling)")
    st.markdown(
        "Tập trung đánh giá so sánh hiệu năng kỹ thuật giữa **Baseline (Logistic Regression)** và **Advanced (XGBoost Giai đoạn 2)**. "
        "Thiết kế 100% Zero-Leakage với Temporal Split và vùng đệm 78 ngày."
    )
    
    st.info(
        "**Điểm Đột Phá Giai Đoạn 2:** Nhờ bổ sung 3 biến tương tác phi tuyến "
        "(`delivery_speed_ratio`, `monthly_installment_burden`, `is_b2b_profile`), XGBoost nâng Recall từ **28.30% lên 57.36% (đỉnh 77.36%)**, "
        "đồng thời khoanh vùng chính xác **22.97% tệp khách hàng** cần cứu vãn, giúp tiết kiệm gần **77% ngân sách marketing**."
    )
    st.divider()
    
    model_tabs = st.tabs([MODEL_CONFIG[k]["tab_label"] for k in MODEL_CONFIG])
    for m_tab, k in zip(model_tabs, MODEL_CONFIG):
        with m_tab:
            render_chart_group_alternating(k, config=MODEL_CONFIG)

# ===========================================================================
# 5. PHÂN HỆ: 04. CHIẾN LƯỢC TỐI ƯU HÓA (PRESCRIPTIVE STRATEGY)
# ===========================================================================
elif nav_choice == "04. Chiến lược Tối ưu hóa (Prescriptive)":
    st.markdown("## 04. Chiến Lược Chỉ Định và Tối Ưu Hóa Ngân Sách (Prescriptive Analytics)")
    st.markdown(
        "Chuyển hóa dự báo AI thành hành động kinh doanh thực tế thông qua **Thuật toán Knapsack ILP** và **Cơ chế Phân luồng Kép (Dual-Engine)**. "
        "Bao gồm đầy đủ 6 bước phương pháp luận từ Báo cáo Phân tích Chỉ định."
    )
    
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
        st.markdown("### Bước 6.2 & 6.3: Tổng Kết Hành Động Doanh Nghiệp và Bộ Giả Lập Tài Chính Kép")
        
        st.markdown("#### 1. Tổng Quan Phân Định Chiến Lược (Phân luồng 2 Tầng)")
        st.markdown(r"""
        | Phân Luồng | Quy mô Khách | Vốn Cấp Trước | Doanh Số Kỳ Vọng | Lợi Nhuận Ròng | Tỷ suất ROI | Cơ Chế Thực Thi Quản Trị |
        | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
        | **Tier 2A (VIP - Cấp vốn)** | **600** ($4.44\%$) | **3,803.95 R$** | **14,729.80 R$** | **10,925.85 R$** | **287.22%** | Cấp vốn trực tiếp - Thu hồi vốn trong 14 ngày |
        | **Tier 2B (Nền tảng - Tự tài trợ)** | **12,925** ($95.56\%$) | **0.00 R$** | **129,300.00 R$** | **28,446.00 R$** | $\infty$ | Tự tài trợ (Locked Cashback 14 ngày + Min-Cart $\ge$ 150%) |
        | **TỔNG CỘNG HỢP NHẤT** | **13,525** ($100\%$) | **3,803.95 R$** | **144,029.80 R$** | **39,371.85 R$** | **10.3× Vốn** | **Lợi nhuận ròng gấp 10.3 lần vốn đầu tư ban đầu** |
        """)
        
        st.markdown("#### 2. Ma Trận Can Thiệp 4 Cụm Điểm Nghẽn & Chuẩn Đối Sánh")
        st.markdown(r"""
        | Cụm Điểm Nghẽn | Vấn Đề Cốt Lõi | Luồng Tier 2A (VIP - Cấp Vốn) | Luồng Tier 2B (Nền Tảng - Tự Tài Trợ) | Nền Tảng Đối Chuẩn |
        | :--- | :--- | :--- | :--- | :--- |
        | **Cụm 0: Áp Lực Tài Chính** (2.319 khách) | Đơn to (AOV 140 R$), trả góp dài | Tài trợ Trả góp 0% (Chi phí 6% AOV ~ 8.46 R$/khách) | Ví hoàn tiền tạm khóa (Locked Cashback 14 ngày) + Min-Cart $\ge$ 150% đơn cũ | Mercado Libre Brazil (Mercado Pago 0% Installment) |
        | **Cụm 1: Đánh Giá Kém** (2.086 khách) | Review 2/5 sao, khiếu nại CSKH | Đội CSKH VIP gọi điện trong 24h + Voucher đền bù 12% AOV (~12.01 R$) | Thông báo xin lỗi từ Ban Giám đốc + Mã hoàn tiền 5% đơn kế tiếp | Amazon CSKH & Chính sách Đổi trả A-to-z Guarantee |
        | **Cụm 2: Khủng Hoảng Giao Hàng** (442 khách) | Giao trễ 5.4 ngày, hụt SLA | Hoàn 100% cước phí giao hàng (Free Ship SLA 16.49 R$/khách) | Mã hỗ trợ 50% cước phí vận chuyển cho đơn hàng tiếp theo | Amazon Prime SLA & JD.com (Logistics On-time Guarantee) |
        | **Cụm 3: Rời Bỏ Ngành Hàng** (8.678 khách) | Đơn nhỏ (AOV 78 R$), mua 1 lần | Tự tài trợ $0$ R$ (Gộp chung luồng tự động) | Vòng lặp mua lại 1-Click Refill (30 ngày) + Hộ chiếu Hội viên Loyalty Passport | Shopee (Vòng quay xu/Deal chớp nhoáng) & Taobao Pass |
        """)
        
        st.divider()
        st.markdown("#### 3. Bộ Giả Lập Tài Chính Kép Tương Tác (Dual-Engine ROI Simulator)")
        
        sim_col1, sim_col2 = st.columns(2)
        with sim_col1:
            st.markdown("##### Luồng Tier 2A: Khách Hàng VIP (Cấp Vốn)")
            s_target = st.slider("Quy mô tệp VIP Tier 2A", 100, 1500, 600, step=50)
            s_cost = st.number_input("Chi phí voucher TB (R$/khách)", min_value=1.0, value=6.34, step=0.5)
            s_uplift = st.slider("Tỷ lệ giữ chân kỳ vọng Tier 2A (%)", 5.0, 50.0, 25.0, step=1.0)
            s_aov = st.number_input("AOV trung bình (R$)", min_value=50.0, value=140.0, step=10.0)
            s_margin = st.slider("Biên lợi nhuận ròng sàn (%)", 10.0, 50.0, 30.0, step=5.0)
            
        with sim_col2:
            st.markdown("##### Luồng Tier 2B: Khách Nền Tảng (Tự Tài Trợ)")
            s_b_target = st.number_input("Quy mô tệp Nền tảng Tier 2B", min_value=1000, value=12925, step=500)
            s_b_conv = st.slider("Tỷ lệ kích hoạt mua lại Tier 2B (%)", 1.0, 15.0, 5.0, step=0.5)
            s_b_min_cart = st.number_input("Giá trị giỏ hàng tối thiểu Min-Cart (R$)", min_value=100.0, value=210.0, step=10.0)
            s_b_margin = st.slider("Biên lợi nhuận sau giảm giá Tier 2B (%)", 10.0, 40.0, 22.0, step=2.0)

        # Tính toán hợp nhất
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
        r4.metric("Hệ Số Sinh Lời Vốn", f"{multiple:.1f}× Vốn", help=f"ROI Tier 2A: {roi_2a:.1f}%")

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
st.divider()
st.caption("Olist E-Commerce Retention Intelligence Platform · Xây dựng bằng Streamlit & Python")
