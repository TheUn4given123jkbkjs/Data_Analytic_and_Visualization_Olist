"""
MODEL HELPER & FEATURE TRANSFORMER MODULE FOR STREAMLIT DASHBOARD
DỰ ÁN PHÂN TÍCH DỮ LIỆU THƯƠNG MẠI ĐIỆN TỬ BRAZIL (OLIST E-COMMERCE)

Module này cung cấp toàn bộ công cụ đóng gói:
1. Tự động tiền xử lý dữ liệu nhập từ UI -> Ma trận 33 đặc trưng chuẩn.
2. Dự báo xác suất giữ chân P(Retain) & Gán Tầng Rủi ro (Risk Tiers).
3. Bóc tách TreeSHAP và tính tỷ trọng % cho Biểu đồ Tròn (Pie Chart).
4. Đề xuất gói can thiệp Marketing và Giả lập Tài chính ROI.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
import shap

class OlistCustomerPredictor:
    """
    Class quản lý toàn bộ quy trình Load Model, Transform Dữ liệu và Dự báo Phân tích Chỉ định.
    """
    def __init__(self, model_dir=None):
        if model_dir is None:
            # Đường dẫn tương đối chuẩn từ fix/05_Dashboard sang fix/03_Predictive/models
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.model_dir = os.path.abspath(os.path.join(current_dir, "..", "03_Predictive", "models"))
        else:
            self.model_dir = model_dir
            
        self.model_path = os.path.join(self.model_dir, "advanced", "best_run", "best_model.pkl")
        self.features_path = os.path.join(self.model_dir, "feature_columns.json")
        
        # Load model & feature list
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Không tìm thấy file model tại: {self.model_path}")
        if not os.path.exists(self.features_path):
            raise FileNotFoundError(f"Không tìm thấy file feature columns tại: {self.features_path}")
            
        self.model = joblib.load(self.model_path)
        with open(self.features_path, "r", encoding="utf-8") as f:
            self.feature_columns = json.load(f)
            
        # Khởi tạo TreeExplainer cho XAI
        self.explainer = shap.TreeExplainer(self.model)

        from data_scaler import OlistFeatureScaler, prepare_input
        self.scaler = OlistFeatureScaler(model_dir=self.model_dir)

    def transform_input(self, order_spent=150.0, max_installments=3, payment_type="credit_card",
                        delivery_days=8.0, estimated_delivery_days=15.0, review_score=5.0,
                        customer_state="SP", product_category="cama_mesa_banho"):
        """
        Nhận dữ liệu thô từ Streamlit UI -> Chuyển thành DataFrame 33 cột chuẩn 100%.
        """
        return self.scaler.transform(
            order_spent=order_spent,
            max_installments=max_installments,
            payment_type=payment_type,
            delivery_days=delivery_days,
            estimated_delivery_days=estimated_delivery_days,
            review_score=review_score,
            customer_state=customer_state,
            product_category=product_category
        )

    def predict_and_prescribe(self, **kwargs):
        """
        Dự báo toàn diện: Xác suất Retain, Tầng Rủi ro, Tỷ trọng Pie Chart SHAP và Gói Can thiệp.
        """
        # 1. Transform dữ liệu
        X_sample = self.transform_input(**kwargs)
        
        # 2. Dự báo xác suất
        prob_retain = float(self.model.predict_proba(X_sample)[0, 1])
        
        # 3. Phân tầng rủi ro
        if prob_retain < 0.189:
            tier_label = "Tier 1: Irretrievable / Dead Loss (Khách vãng lai)"
            tier_color = "#e63946" # Đỏ
            can_intervene = False
        elif prob_retain <= 0.450:
            tier_label = "Tier 2: Savable Customers (Tệp Mục Tiêu Cần Cứu Vãn)"
            tier_color = "#f4a261" # Cam
            can_intervene = True
        else:
            tier_label = "Tier 3: Organic Safe (Khách Trung Thành Tự Nhiên)"
            tier_color = "#2a9d8f" # Xanh lá
            can_intervene = False
            
        # 4. Tính toán TreeSHAP & Phân bổ Tỷ trọng % Nguyên nhân Rời bỏ (Churn Frictions)
        shap_vals = self.explainer(X_sample)
        shap_dict = dict(zip(X_sample.columns, shap_vals.values[0]))
        
        # 4.1. Logistics Friction: SHAP vận chuyển + độ trễ giao hàng thực tế
        deliv_shap = sum(abs(shap_dict[c]) for c in ["delivery_days", "delivery_delay", "delivery_speed_ratio"] if c in shap_dict)
        delivery_days = float(kwargs.get("delivery_days", 8.0))
        est_days = float(kwargs.get("estimated_delivery_days", 15.0))
        delay_days = delivery_days - est_days
        logistics_friction = deliv_shap + (max(0.0, delay_days) * 0.25) + (max(0.0, delivery_days - 14.0) * 0.08)
        
        # 4.2. Review & Service Friction: SHAP review + hình phạt khi chấm điểm thấp (1-3 sao)
        review_score = float(kwargs.get("review_score", 5.0))
        review_shap = abs(shap_dict.get("review_score", 0.0))
        review_friction = review_shap + (max(0.0, 5.0 - review_score) * 0.60)
        
        # 4.3. Financial Friction: SHAP tài chính + áp lực trả góp / giỏ hàng lớn
        order_spent = float(kwargs.get("order_spent", 150.0))
        installments = float(kwargs.get("max_installments", 1))
        fin_shap = sum(abs(shap_dict[c]) for c in ["order_spent", "monthly_installment_burden", "max_installments", "is_b2b_profile"] if c in shap_dict)
        active_pay = f"pay_{kwargs.get('payment_type', 'credit_card')}"
        pay_shap = abs(shap_dict.get(active_pay, 0.05))
        fin_friction = fin_shap + pay_shap + (max(0.0, order_spent - 140.0) * 0.005) + (max(0.0, installments - 3.0) * 0.15)
        
        # 4.4. Category & Geography Friction: Chỉ tính cột One-Hot thực tế đang kích hoạt
        active_cat = f"cat_{kwargs.get('product_category', 'cama_mesa_banho')}"
        active_state = f"state_{kwargs.get('customer_state', 'SP')}"
        cat_shap = abs(shap_dict.get(active_cat, shap_dict.get("cat_outros", 0.05)))
        state_shap = abs(shap_dict.get(active_state, shap_dict.get("state_outros", 0.05)))
        cat_geo_friction = cat_shap + state_shap + 0.15
        
        group_impacts = {
            "Logistics & Vận chuyển": max(0.01, logistics_friction),
            "Trải nghiệm Đánh giá": max(0.01, review_friction),
            "Tài chính & Trả góp": max(0.01, fin_friction),
            "Ngành hàng & Vùng miền": max(0.01, cat_geo_friction)
        }
        
        total_impact = max(sum(group_impacts.values()), 1e-6)
        df_pie = pd.DataFrame({
            "Nhóm Nguyên Nhân": list(group_impacts.keys()),
            "Mức độ Tác động": list(group_impacts.values()),
            "Tỷ trọng (%)": [v / total_impact * 100 for v in group_impacts.values()]
        }).sort_values(by="Tỷ trọng (%)", ascending=False)
        
        top_cause = df_pie.iloc[0]["Nhóm Nguyên Nhân"]
        
        # 5. Xác định Gói Can thiệp Marketing theo 4 Cụm & Phân luồng 2 Tầng
        if not can_intervene:
            if prob_retain < 0.189:
                action_title = "KHÔNG CHI TIỀN MARKETING (TIER 1)"
                action_desc = "Khách hàng vãng lai có nhu cầu phát sinh 1 lần duy nhất. Chi voucher vào nhóm này sẽ gây lãng phí 100% ngân sách (Deadweight Loss)."
                action_channel = "Không phân bổ ngân sách"
                assigned_engine = "Không can thiệp"
            else:
                action_title = "KHÔNG CẦN PHÁT VOUCHER (TIER 3)"
                action_desc = "Khách hàng có xu hướng tự nhiên quay lại mua hàng. Tặng voucher trực tiếp sẽ làm suy giảm biên lợi nhuận của doanh nghiệp."
                action_channel = "Duy trì dịch vụ CSKH tự nhiên"
                assigned_engine = "Chăm sóc hữu cơ"
        else:
            if "Logistics" in top_cause:
                action_title = "GÓI BẢO HIỂM SLA VẬN CHUYỂN (EXPERIENCE RECOVERY - CỤM 2)"
                action_desc = "Gửi SMS xin lỗi từ Ban Giám Đốc + Tặng mã Hoàn 100% Cước Phí Giao Hàng (Free Ship 16,49 R$) cho đơn tiếp theo."
                action_channel = "SMS & CRM Tự động (Tham chiếu Amazon Prime & JD.com)"
                assigned_engine = "Nhánh Tier 2A (Cấp vốn tức thì - Hoàn vốn sau 14 ngày)"
            elif "Tài chính" in top_cause or order_spent > 140:
                action_title = "GÓI TÀI TRỢ TRẢ GÓP 0% LÃI SUẤT (FINANCIAL RELIEF - CỤM 0)"
                action_desc = "Sàn chi trả 6% phí chuyển đổi ngân hàng, kích hoạt cổng Trả góp 0% từ 6 - 12 kỳ trực tiếp tại checkout."
                action_channel = "Cổng Thanh toán Checkout & App Banner (Tham chiếu Mercado Libre Brazil)"
                assigned_engine = "Nhánh Tier 2A (Cấp vốn tức thì - Hoàn vốn sau 14 ngày)"
            elif "Trải nghiệm" in top_cause or review_score <= 3.0:
                action_title = "GÓI CHĂM SÓC KHÁCH HÀNG VIP 1-1 (SERVICE RESOLUTION - CỤM 1)"
                action_desc = "Đội CSKH VIP gọi điện hỗ trợ đổi trả trong 24h + Tặng voucher đền bù thiện chí 12% giá trị đơn hàng (~12,01 R$)."
                action_channel = "Tổng đài CSKH VIP 1-1 & Nạp ví tự động (Tham chiếu Amazon CSKH)"
                assigned_engine = "Nhánh Tier 2A (Cấp vốn tức thì - Hoàn vốn sau 14 ngày)"
            else:
                action_title = "GÓI TỰ TÀI TRỢ NUÔI DƯỠNG 4 BƯỚC (CATEGORY RE-ENGAGEMENT - CỤM 3)"
                action_desc = "Ví hoàn tiền tạm khóa (14 ngày) + Khóa ngưỡng giỏ hàng tối thiểu (Min-Cart >= 150%) + Nhắc mua lại chu kỳ 30 ngày + Thăng hạng hội viên."
                action_channel = "Push Notification, In-App Widget & Loyalty Passport (Tham chiếu Shopee & Taobao)"
                assigned_engine = "Nhánh Tier 2B (Tự tài trợ - Bảo toàn lãi ròng 22% trên đơn mới)"

        return {
            "transformed_features": X_sample,
            "prob_retain": prob_retain,
            "prob_retain_pct": f"{prob_retain:.2%}",
            "prob_churn_pct": f"{(1.0 - prob_retain):.2%}",
            "risk_tier": tier_label,
            "tier_color": tier_color,
            "can_intervene": can_intervene,
            "pie_chart_data": df_pie,
            "top_cause": top_cause,
            "action_title": action_title,
            "action_desc": action_desc,
            "action_channel": action_channel,
            "assigned_engine": assigned_engine
        }

    @staticmethod
    def simulate_roi(target_customers=600, cost_per_voucher=6.34, expected_uplift_pct=25.0,
                      avg_order_value=140.0, net_margin_pct=30.0, future_orders=1.5):
        """
        Hàm mô phỏng tài chính & ROI cho Dashboard Simulator.
        """
        uplift_rate = float(expected_uplift_pct) / 100.0
        margin_rate = float(net_margin_pct) / 100.0
        
        total_cost = float(target_customers) * float(cost_per_voucher)
        retained_customers = float(target_customers) * uplift_rate
        clv_per_cust = float(avg_order_value) * margin_rate * float(future_orders)
        total_retained_profit = retained_customers * clv_per_cust
        net_profit = total_retained_profit - total_cost
        roi = (net_profit / max(total_cost, 1.0)) * 100.0
        
        return {
            "total_cost": total_cost,
            "retained_customers": retained_customers,
            "total_retained_profit": total_retained_profit,
            "net_profit": net_profit,
            "roi_pct": roi,
            "is_profitable": net_profit > 0
        }
