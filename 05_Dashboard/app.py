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
    /* =======================================================================
       GLOBAL LARGE TYPOGRAPHY SYSTEM ACROSS ALL 5 TABS (MINIMUM >= 22px - 26px)
       ======================================================================= */
    html, body {
        font-size: 22px;
    }
    
    .stMarkdown p, .stMarkdown li, [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li {
        font-size: 24px !important;
        line-height: 1.65 !important;
        color: #1e293b;
    }
    
    /* Captions & Ghi chú dưới biểu đồ */
    .stCaption, [data-testid="stCaptionContainer"] p, [data-testid="stCaptionContainer"] span, [data-testid="stCaptionContainer"] * {
        font-size: 22px !important;
        color: #475569 !important;
        line-height: 1.5 !important;
    }

    /* =======================================================================
       TIÊU ĐỀ SECTION CHÍNH (50PX VỪA VẶN, NỔI BẬT)
       ======================================================================= */
    .main-section-header,
    h1.main-section-header,
    h2.main-section-header,
    div.main-section-header,
    p.main-section-header,
    [data-testid="stMarkdownContainer"] .main-section-header,
    [data-testid="stMarkdownContainer"] h1.main-section-header,
    [data-testid="stMarkdownContainer"] h2.main-section-header,
    [data-testid="stMarkdownContainer"] div.main-section-header,
    [data-testid="stMarkdownContainer"] p.main-section-header {
        font-size: 50px !important;
        font-weight: 900 !important;
        color: #0f4c81 !important;
        margin-top: 20px !important;
        margin-bottom: 14px !important;
        line-height: 1.2 !important;
        display: block !important;
    }

    /* Tiêu đề phân mục lớn */
    h1, [data-testid="stMarkdownContainer"] h1 {
        font-size: 44px !important;
        font-weight: 900 !important;
        color: #0f172a !important;
        line-height: 1.3 !important;
    }
    h2, [data-testid="stMarkdownContainer"] h2, .main h2 {
        font-size: 36px !important;
        font-weight: 800 !important;
        color: #0f4c81 !important;
        margin-top: 20px !important;
        margin-bottom: 14px !important;
        line-height: 1.25 !important;
    }
    h3, [data-testid="stMarkdownContainer"] h3 {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #1e293b !important;
    }
    h4, [data-testid="stMarkdownContainer"] h4 {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #334155 !important;
    }
    h5, [data-testid="stMarkdownContainer"] h5 {
        font-size: 24px !important;
        font-weight: 700 !important;
    }

    /* Khung nhận xét kéo trượt (Sliding Insight Cards) ở cả 4 phân hệ */
    .insight-card {
        background-color: #f8fafc;
        border-left: 8px solid #1f77b4;
        padding: 24px 28px;
        border-radius: 12px;
        margin-bottom: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .insight-card h4, .insight-card h4 * {
        margin-top: 0;
        color: #0f4c81 !important;
        font-weight: 800 !important;
        font-size: 28px !important;
        margin-bottom: 14px !important;
    }
    .insight-card p, .insight-card span, .insight-card div, .insight-text {
        font-size: 26px !important;
        line-height: 1.6 !important;
        color: #1e293b !important;
    }
    
    /* =======================================================================
       DEMO RESULTS & PRESCRIPTION ACTION BOX TYPOGRAPHY (26px - 28px)
       ======================================================================= */
    .demo-large-text,
    .demo-large-text *,
    .demo-large-text p,
    .demo-large-text span,
    .demo-large-text strong,
    .demo-large-text div,
    .demo-action-box,
    .demo-action-box *,
    .demo-action-box p,
    .demo-action-box span,
    .demo-action-box strong,
    .demo-action-box div {
        font-size: 26px !important;
        line-height: 1.55 !important;
    }

    .demo-action-box {
        background-color: #f8fafc;
        border-left: 8px solid #10b981;
        border-radius: 12px;
        padding: 24px 28px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-top: 12px;
    }
    .demo-action-box h3,
    .demo-action-box h3 * {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #047857 !important;
        margin-top: 0;
        margin-bottom: 16px;
        line-height: 1.35 !important;
    }
    
    /* Nâng cỡ chữ các nhãn (labels) và input trong Form & Điều khiển */
    [data-testid="stForm"] label p, 
    [data-testid="stForm"] label span, 
    [data-testid="stForm"] label div,
    .stSelectbox label p,
    .stSelectbox label span,
    .stSlider label p,
    .stSlider label span,
    .stNumberInput label p,
    .stNumberInput label span {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        margin-bottom: 8px !important;
    }
    
    /* Cỡ chữ nội dung đang chọn trong input, number, selectbox */
    [data-testid="stForm"] input, 
    [data-testid="stForm"] div[data-baseweb="select"] *,
    .stSelectbox div[data-baseweb="select"] *,
    .stNumberInput input,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        font-size: 26px !important;
        font-weight: 600 !important;
        color: #0f172a !important;
    }
    
    /* Cỡ chữ toàn bộ danh sách tùy chọn khi mở sổ xuống (Dropdown Menu Listbox Items) */
    div[data-baseweb="popover"] *,
    ul[role="listbox"] li,
    ul[role="listbox"] li div,
    ul[role="listbox"] li span,
    li[role="option"] * {
        font-size: 24px !important;
        font-weight: 600 !important;
        line-height: 1.45 !important;
        padding-top: 6px !important;
        padding-bottom: 6px !important;
    }
    .stSlider div[data-testid="stThumbValue"],
    .stSlider div[data-testid="stTickBarMin"],
    .stSlider div[data-testid="stTickBarMax"] {
        font-size: 24px !important;
        font-weight: 700 !important;
    }
    
    /* Nút bấm AI thông minh (Xanh biển tươi sáng, dịu mắt) */
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #0284c7 0%, #0ea5e9 50%, #38bdf8 100%) !important;
        color: #ffffff !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        letter-spacing: 1px;
        padding: 20px 36px !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 14px !important;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.35) !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-top: 24px !important;
        margin-bottom: 12px !important;
        text-transform: uppercase;
        cursor: pointer;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #0369a1 0%, #0284c7 50%, #0ea5e9 100%) !important;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.5) !important;
        transform: translateY(-3px) scale(1.015) !important;
    }
    
    /* Metrics Top Cards */
    [data-testid="stMetricLabel"] * {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #334155 !important;
    }
    [data-testid="stMetricValue"] * {
        font-size: 34px !important;
        font-weight: 800 !important;
    }
    .metric-sub {
        font-size: 20px !important;
        color: #6c757d;
        margin-top: -8px;
    }
    .badge-tier {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 20px !important;
    }
    
    /* =======================================================================
       DANH MỤC SUBTABS (TABS CON) Ở TẤT CẢ CÁC PHÂN HỆ (DẠNG THẺ LỚN 26px)
       ======================================================================= */
    [data-testid="stTabs"] {
        width: 100%;
        margin-top: 14px;
        margin-bottom: 24px;
    }
    
    div[data-baseweb="tab-list"],
    [data-testid="stTabs"] [role="tablist"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        overflow-y: hidden !important;
        white-space: nowrap !important;
        scrollbar-width: thin !important;
        scrollbar-color: #0284c7 #e0f2fe !important;
        padding-bottom: 12px !important;
        margin-bottom: 20px !important;
        gap: 12px !important;
        scroll-behavior: smooth !important;
        -webkit-overflow-scrolling: touch !important;
        border-bottom: 3px solid #bae6fd !important;
    }
    div[data-baseweb="tab-list"]::-webkit-scrollbar,
    [data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar {
        height: 10px !important;
    }
    div[data-baseweb="tab-list"]::-webkit-scrollbar-track,
    [data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar-track {
        background: #f0f9ff !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="tab-list"]::-webkit-scrollbar-thumb,
    [data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar-thumb {
        background: #38bdf8 !important;
        border-radius: 6px !important;
    }
    
    /* Thiết kế từng nút Subtab dạng thẻ Card lớn, rõ ràng */
    div[data-baseweb="tab-list"] button,
    button[data-baseweb="tab"],
    button[role="tab"],
    [data-testid="stTabs"] button {
        flex-shrink: 0 !important;
        white-space: nowrap !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 16px 28px !important;
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-bottom: none !important;
        margin-right: 8px !important;
        height: auto !important;
        min-height: 58px !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    div[data-baseweb="tab-list"] button *,
    div[data-baseweb="tab-list"] p,
    div[data-baseweb="tab-list"] span,
    div[data-baseweb="tab-list"] div,
    button[data-baseweb="tab"] *,
    button[role="tab"] *,
    button[role="tab"] p,
    button[role="tab"] span,
    [data-testid="stTabs"] button *,
    [data-testid="stTabs"] button p,
    [data-testid="stTabs"] button span,
    [data-testid="stTabs"] p,
    [data-testid="stTabs"] span {
        font-size: 26px !important;
        font-weight: 800 !important;
        line-height: 1.4 !important;
        color: #334155 !important;
    }
    
    div[data-baseweb="tab-list"] button:hover,
    button[role="tab"]:hover,
    [data-testid="stTabs"] button:hover {
        background-color: #f0f9ff !important;
        border-color: #7dd3fc !important;
    }
    div[data-baseweb="tab-list"] button:hover *,
    button[role="tab"]:hover *,
    [data-testid="stTabs"] button:hover * {
        color: #0284c7 !important;
    }
    
    /* Tab đang chọn (Active Subtab) */
    div[data-baseweb="tab-list"] button[aria-selected="true"],
    button[role="tab"][aria-selected="true"],
    [data-testid="stTabs"] button[aria-selected="true"] {
        background-color: #eff6ff !important;
        border-top: 5px solid #0284c7 !important;
        border-left: 1px solid #93c5fd !important;
        border-right: 1px solid #93c5fd !important;
        box-shadow: 0 -2px 10px rgba(2, 132, 199, 0.12) !important;
    }
    div[data-baseweb="tab-list"] button[aria-selected="true"] *,
    button[role="tab"][aria-selected="true"] *,
    [data-testid="stTabs"] button[aria-selected="true"] * {
        color: #0284c7 !important;
        font-weight: 900 !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #0284c7 !important;
        height: 4px !important;
    }
    
    /* Sidebar Navigation Bars (22px - 24px, Tone Xanh Biển Nhạt Dịu Mắt) */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div > div > .stButton > button {
        width: 100% !important;
        text-align: left !important;
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        padding: 18px 22px !important;
        margin-bottom: 12px !important;
        border-radius: 12px !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
    }
    /* Inactive Navigation Bar */
    [data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background-color: #f8fafc !important;
        color: #334155 !important;
        border: 1px solid #e2e8f0 !important;
        border-left: 6px solid #cbd5e1 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }
    /* Inactive Navigation Bar Hover Effect (Xanh biển nhạt tươi sáng) */
    [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
        background-color: #f0f9ff !important;
        color: #0284c7 !important;
        border-color: #bae6fd !important;
        border-left: 6px solid #38bdf8 !important;
        transform: translateX(6px) !important;
        box-shadow: 0 4px 14px rgba(14, 165, 233, 0.15) !important;
    }
    /* Active Navigation Bar (Currently Selected Tab - Xanh Biển Tươi) */
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #0ea5e9 100%) !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-left: 6px solid #7dd3fc !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25) !important;
        font-weight: 800 !important;
        font-size: 22px !important;
    }
    /* Active Navigation Bar Hover */
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0369a1 0%, #0284c7 100%) !important;
        transform: translateX(6px) !important;
        box-shadow: 0 6px 18px rgba(2, 132, 199, 0.35) !important;
    }
    
    /* Expanders & Markdown Tables */
    [data-testid="stExpander"] summary, [data-testid="stExpander"] summary * {
        font-size: 24px !important;
        font-weight: 700 !important;
        padding: 12px 0 !important;
    }
    
    /* Nút bấm tương tác chung (Mũi tên kéo nhận xét, điều khiển) */
    .stButton > button {
        font-size: 24px !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
    }
    table, table th, table td, .stMarkdown table, .stMarkdown table * {
        font-size: 22px !important;
        line-height: 1.55 !important;
    }
    table th {
        background-color: #f1f5f9 !important;
        font-weight: 800 !important;
        padding: 14px 18px !important;
    }
    table td {
        padding: 12px 18px !important;
    }
    
    /* Alert / Info Boxes */
    [data-testid="stAlert"] * {
        font-size: 24px !important;
        line-height: 1.6 !important;
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
    st.title("Olist Retention AI")
    st.caption("Hệ thống Dự báo & Tối ưu hóa Giữ chân Khách hàng")
    st.divider()
    
    st.markdown("### ĐIỀU HƯỚNG CHƯƠNG TRÌNH")
    for item in NAV_ITEMS:
        is_active = (st.session_state.nav_choice == item)
        btn_type = "primary" if is_active else "secondary"
        if st.button(item, key=f"nav_btn_{item}", type=btn_type, use_container_width=True):
            if st.session_state.nav_choice != item:
                st.session_state.nav_choice = item
                st.rerun()
                
    st.divider()
    st.caption("Đồ án Phân tích và Trực quan hóa Dữ liệu · TDTU")

nav_choice = st.session_state.nav_choice

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
# 1. PHÂN HỆ: DEMO (DỰ BÁO & CHỈ ĐỊNH)
# ===========================================================================
if nav_choice == "Demo":
    st.markdown("<div class='main-section-header' style='font-size: 50px !important; font-weight: 900 !important; color: #0f4c81 !important; margin-top: 20px !important; margin-bottom: 14px !important; line-height: 1.2 !important;'>Dự Đoán Thời Gian Thực và Chỉ Định Hành Động</div>", unsafe_allow_html=True)
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

    # Bố cục 2 Cột Song Song: Kết Quả Dự Đoán Bên Trái (58%) | Bảng Chọn Chỉ Số Bên Phải (42%)
    col_results, col_controls = st.columns([0.58, 0.42], gap="large")

    with col_controls:
        st.markdown("### THIẾT LẬP THÔNG SỐ ĐƠN HÀNG")
        selected_preset_key = st.selectbox(
            "Chọn Nhanh Mẫu Khách Hàng Điển Hình:",
            list(PRESET_OPTIONS.keys()),
            index=0,
            help="Chọn một kịch bản điển hình để tự động điền các thông số tương ứng vào form bên dưới"
        )
        
        preset_val = PRESET_OPTIONS[selected_preset_key]
        if preset_val == "RANDOM":
            rng = np.random.RandomState(st.session_state.random_profile_counter)
            r_spent = float(rng.choice([29.0, 48.0, 75.0, 110.0, 165.0, 245.0, 380.0, 520.0, 780.0]))
            r_pay = str(rng.choice(["credit_card", "credit_card", "credit_card", "boleto", "voucher", "debit_card"]))
            r_inst = int(rng.choice([1, 2, 3, 4, 6, 8, 10, 12])) if r_pay == "credit_card" else 1
            r_est = float(rng.randint(8, 28))
            r_bias = int(rng.choice([-10, -6, -3, 0, 2, 8, 14]))
            r_deliv = float(max(1.0, r_est + r_bias))
            r_score = int(rng.choice([1, 2, 3, 4, 5, 5, 5]))
            r_state = str(rng.choice(list(STATES_DICT.keys())))
            r_cat = str(rng.choice(list(CATEGORIES_DICT.keys())))
            
            preset_chosen = {
                "order_spent": r_spent,
                "max_installments": r_inst,
                "payment_type": r_pay,
                "delivery_days": r_deliv,
                "estimated_delivery_days": r_est,
                "review_score": r_score,
                "customer_state": r_state,
                "product_category": r_cat
            }
            if st.button("Sinh Mẫu Ngẫu Nhiên Khác (Re-roll Random)", use_container_width=True):
                st.session_state.random_profile_counter += 1
                st.rerun()
        else:
            preset_chosen = preset_val

        # Form nhập liệu dạng 1 cột dọc bên phải
        with st.form("hero_prediction_form"):
            submitted = st.form_submit_button("CHẠY DỰ BÁO AI VÀ GÁN CHÍNH SÁCH CAN THIỆP", use_container_width=True)
            
            st.markdown("#### Thông số Đơn hàng Đầu tiên ($T_0$)")
            
            # Mặc định lấy từ preset hoặc giá trị chuẩn
            def_spent = preset_chosen["order_spent"] if preset_chosen else 150.0
            def_inst = preset_chosen["max_installments"] if preset_chosen else 3
            def_pay = preset_chosen["payment_type"] if preset_chosen else "credit_card"
            def_deliv = preset_chosen["delivery_days"] if preset_chosen else 8.0
            def_est = preset_chosen["estimated_delivery_days"] if preset_chosen else 15.0
            def_score = preset_chosen["review_score"] if preset_chosen else 5
            def_state = preset_chosen["customer_state"] if preset_chosen else "SP"
            def_cat = preset_chosen["product_category"] if preset_chosen else "cama_mesa_banho"
            
            form_key_suffix = f"{selected_preset_key}_{st.session_state.random_profile_counter}"
            
            in_spent = st.number_input("Tổng giá trị đơn hàng (R$)", min_value=1.0, value=float(def_spent), step=10.0, key=f"spent_{form_key_suffix}")
            in_installments = st.number_input("Số kỳ trả góp", min_value=1, max_value=24, value=int(def_inst), key=f"inst_{form_key_suffix}")
            
            pay_keys = list(PAYMENTS_DICT.keys())
            pay_idx = pay_keys.index(def_pay) if def_pay in pay_keys else 0
            in_pay_type = st.selectbox(
                "Phương thức thanh toán", pay_keys,
                index=pay_idx,
                format_func=lambda k: PAYMENTS_DICT.get(k, k),
                key=f"pay_{form_key_suffix}"
            )
            
            in_delivery = st.number_input("Số ngày giao hàng thực tế", min_value=1.0, value=float(def_deliv), step=1.0, key=f"deliv_{form_key_suffix}")
            in_est_delivery = st.number_input("Số ngày giao hàng dự kiến (SLA)", min_value=1.0, value=float(def_est), step=1.0, key=f"est_{form_key_suffix}")
            in_review = st.slider("Điểm đánh giá (Review score)", 1, 5, int(def_score), key=f"rev_{form_key_suffix}")
            
            state_keys = list(STATES_DICT.keys())
            state_idx = state_keys.index(def_state) if def_state in state_keys else 0
            in_state = st.selectbox(
                "Bang khách hàng (State / Região)", state_keys,
                index=state_idx,
                format_func=lambda k: STATES_DICT.get(k, k),
                key=f"state_{form_key_suffix}"
            )
            
            cat_keys = list(CATEGORIES_DICT.keys())
            cat_idx = cat_keys.index(def_cat) if def_cat in cat_keys else 0
            in_category = st.selectbox(
                "Ngành hàng sản phẩm (Category)", cat_keys,
                index=cat_idx,
                format_func=lambda k: CATEGORIES_DICT.get(k, k),
                key=f"cat_{form_key_suffix}"
            )

    with col_results:
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
            
            st.markdown("### KẾT QUẢ DỰ BÁO AI VÀ GIẢI THÍCH TREESHAP")
            
            # 4 Thẻ Chỉ số Kết quả dạng lưới 2x2
            m_top1, m_top2 = st.columns(2)
            m_top1.metric("Xác suất Giữ chân P(Retain)", res["prob_retain_pct"])
            m_top2.metric("Tỷ lệ Rời bỏ P(Churn)", res["prob_churn_pct"])
            
            m_bot1, m_bot2 = st.columns(2)
            m_bot1.metric("Phân tầng Rủi ro", res["risk_tier"].split(":")[0], help=res["risk_tier"])
            m_bot2.metric("Luồng Thực thi", res["assigned_engine"].split("(")[0], help=res["assigned_engine"])
            
            st.divider()
            
            # Phần bóc tách TreeSHAP và Gói can thiệp
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
                        "Logistics & Vận chuyển": "#0284c7",
                        "Trải nghiệm Đánh giá": "#f59e0b",
                        "Tài chính & Trả góp": "#10b981",
                        "Ngành hàng & Vùng miền": "#dc2626"
                    }
                )
                fig_donut.update_traces(textposition='inside', textinfo='percent+label', textfont_size=16)
                fig_donut.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320, showlegend=False)
                st.plotly_chart(fig_donut, use_container_width=True)
            else:
                st.dataframe(df_pie, hide_index=True, use_container_width=True)
            
            st.markdown(f"""
            <div class="demo-large-text" style="background:#f8fafc; padding:18px 22px; border-radius:10px; border-left:8px solid #dc2626; box-shadow:0 2px 8px rgba(0,0,0,0.06); margin-top:12px; margin-bottom:18px;">
                <strong style="font-size:26px !important;">Yếu tố tác động lớn nhất:</strong><br>
                <span style="color:#dc2626; font-weight:800; font-size:26px !important;">{res['top_cause']}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<h4 style='font-size:28px !important; font-weight:800; color:#0f4c81; margin-top:16px; margin-bottom:10px;'>Gói Chính Sách Can Thiệp Chỉ Định</h4>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="demo-action-box">
                <h3 style="font-size:28px !important; color:#047857; font-weight:800;">{res['action_title']}</h3>
                <div class="demo-large-text">
                    <p style="margin-bottom: 16px; font-size:26px !important;">
                        <strong style="color:#0f172a; font-size:26px !important;">Nội dung thực thi:</strong><br>
                        <span style="font-size:26px !important;">{res['action_desc']}</span>
                    </p>
                    <p style="margin-bottom: 16px; color:#0369a1; background:#e0f2fe; padding:14px 18px; border-radius:8px; font-size:26px !important;">
                        <strong style="font-size:26px !important;">Kênh triển khai tiếp thị:</strong><br>
                        <span style="font-size:26px !important;">{res['action_channel']}</span>
                    </p>
                    <p style="margin-bottom: 0px; color:#334155; font-size:26px !important;">
                        <strong style="font-size:26px !important;">Phân luồng Hệ thống:</strong><br>
                        <span style="font-size:26px !important; font-weight:bold; color:#0f172a; background:#e2e8f0; padding:6px 14px; border-radius:6px; display:inline-block; margin-top:6px;">
                            {res['assigned_engine']}
                        </span>
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Có lỗi khi thực thi dự báo: {e}")

# ===========================================================================
# 2. PHÂN HỆ: 01. DESCRIPTIVE
# ===========================================================================
elif nav_choice == "01. Descriptive":
    st.markdown("<div class='main-section-header' style='font-size: 50px !important; font-weight: 900 !important; color: #0f4c81 !important; margin-top: 20px !important; margin-bottom: 14px !important; line-height: 1.2 !important;'>01. Phân Tích Mô Tả (Descriptive Analytics)</div>", unsafe_allow_html=True)
    st.markdown(
        "Tổng hợp đặc trưng phân phối của **92,077 khách hàng** giao dịch thành công. "
        "Bố cục so le 2 cột nhấn mạnh trực tiếp vào bài học nghiệp vụ rút ra."
    )
    eda_tabs = st.tabs([CHARTS_CONFIG[k]["tab_label"] for k in CHARTS_CONFIG])
    for s_tab, k in zip(eda_tabs, CHARTS_CONFIG):
        with s_tab:
            render_chart_group_alternating(k, config=CHARTS_CONFIG)

# ===========================================================================
# 3. PHÂN HỆ: 02. DIAGNOSTIC
# ===========================================================================
elif nav_choice == "02. Diagnostic":
    st.markdown("<div class='main-section-header' style='font-size: 50px !important; font-weight: 900 !important; color: #0f4c81 !important; margin-top: 20px !important; margin-bottom: 14px !important; line-height: 1.2 !important;'>02. Phân Tích Chẩn Đoán (Diagnostic Hypotheses)</div>", unsafe_allow_html=True)
    st.markdown(
        "Kiểm định thống kê chuyên sâu ($p$-value, Chi-Square, Mann-Whitney U) trên **6 yếu tố nghi vấn** "
        "gây rời bỏ khách hàng giữa nhóm Active (< 90 ngày) và nhóm Churn (≥ 90 ngày)."
    )
    
    # Bảng tóm tắt kết quả kiểm định (Kéo mở rộng từ bên dưới)
    with st.expander("BẢNG TỔNG HỢP KẾT QUẢ KIỂM ĐỊNH 6 GIẢ THUYẾT", expanded=False):
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
# 4. PHÂN HỆ: 03. PREDICTIVE
# ===========================================================================
elif nav_choice == "03. Predictive":
    st.markdown("<div class='main-section-header' style='font-size: 50px !important; font-weight: 900 !important; color: #0f4c81 !important; margin-top: 20px !important; margin-bottom: 14px !important; line-height: 1.2 !important;'>03. Đánh Giá Mô Hình Dự Báo (Predictive Modeling)</div>", unsafe_allow_html=True)
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
# 5. PHÂN HỆ: 04. PRESCRIPTIVE
# ===========================================================================
elif nav_choice == "04. Prescriptive":
    st.markdown("<div class='main-section-header' style='font-size: 50px !important; font-weight: 900 !important; color: #0f4c81 !important; margin-top: 20px !important; margin-bottom: 14px !important; line-height: 1.2 !important;'>04. Chiến Lược Chỉ Định và Tối Ưu Hóa Ngân Sách (Prescriptive Analytics)</div>", unsafe_allow_html=True)
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
        
        with st.expander("1. TỔNG QUAN PHÂN ĐỊNH CHIẾN LƯỢC (PHÂN LUỒNG 2 TẦNG)", expanded=False):
            st.markdown(r"""
            | Phân Luồng | Quy mô Khách | Vốn Cấp Trước | Doanh Số Kỳ Vọng | Lợi Nhuận Ròng | Tỷ suất ROI | Cơ Chế Thực Thi Quản Trị |
            | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
            | **Tier 2A (VIP - Cấp vốn)** | **600** ($4.44\%$) | **3,803.95 R$** | **14,729.80 R$** | **10,925.85 R$** | **287.22%** | Cấp vốn trực tiếp - Thu hồi vốn trong 14 ngày |
            | **Tier 2B (Nền tảng - Tự tài trợ)** | **12,925** ($95.56\%$) | **0.00 R$** | **129,300.00 R$** | **28,446.00 R$** | $\infty$ | Tự tài trợ (Locked Cashback 14 ngày + Min-Cart $\ge$ 150%) |
            | **TỔNG CỘNG HỢP NHẤT** | **13,525** ($100\%$) | **3,803.95 R$** | **144,029.80 R$** | **39,371.85 R$** | **10.3× Vốn** | **Lợi nhuận ròng gấp 10.3 lần vốn đầu tư ban đầu** |
            """)
        
        with st.expander("2. MA TRẬN CAN THIỆP 4 CỤM ĐIỂM NGHẼN & CHUẨN ĐỐI SÁNH", expanded=False):
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
