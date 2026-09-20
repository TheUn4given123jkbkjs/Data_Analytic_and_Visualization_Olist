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
            
        # 4. Tính toán SHAP Values & Tỷ trọng % Biểu đồ Tròn
        shap_vals = self.explainer(X_sample)
        
        group_impacts = {
            "Logistics & Vận chuyển": float(sum(abs(v) for f, v in zip(X_sample.columns, shap_vals.values[0]) if "delivery" in f)),
            "Trải nghiệm Đánh giá": float(sum(abs(v) for f, v in zip(X_sample.columns, shap_vals.values[0]) if "review" in f)),
            "Tài chính & Trả góp": float(sum(abs(v) for f, v in zip(X_sample.columns, shap_vals.values[0]) if any(k in f for k in ["spent", "installment", "pay", "b2b"]))),
            "Ngành hàng & Vùng miền": float(sum(abs(v) for f, v in zip(X_sample.columns, shap_vals.values[0]) if any(k in f for k in ["cat_", "state_"])))
        }
        
        total_impact = max(sum(group_impacts.values()), 1e-6)
        df_pie = pd.DataFrame({
            "Nhóm Nguyên Nhân": list(group_impacts.keys()),
            "Mức độ Tác động": list(group_impacts.values()),
            "Tỷ trọng (%)": [v / total_impact * 100 for v in group_impacts.values()]
        }).sort_values(by="Tỷ trọng (%)", ascending=False)
        
        top_cause = df_pie.iloc[0]["Nhóm Nguyên Nhân"]
        
        # 5. Xác định Gói Can thiệp Marketing
        review_score = float(kwargs.get("review_score", 5.0))
        order_spent = float(kwargs.get("order_spent", 150.0))
        
        if not can_intervene:
            if prob_retain < 0.189:
                action_title = "KHÔNG CHI TIỀN MARKETING"
                action_desc = "Khách hàng vãng lai có nhu cầu phát sinh 1 lần duy nhất. Chi voucher vào nhóm này sẽ gây lãng phí 100% ngân sách (Deadweight Loss)."
                action_channel = "Không phân bổ ngân sách"
            else:
                action_title = "KHÔNG CẦN PHÁT VOUCHER"
                action_desc = "Khách hàng có xu hướng tự nhiên quay lại mua hàng. Tặng voucher sẽ làm giảm biên lợi nhuận của doanh nghiệp."
                action_channel = "Duy trì dịch vụ CSKH tự nhiên"
        else:
            if "Logistics" in top_cause or review_score <= 3.0:
                action_title = "GÓI BỒI THƯỜNG TRẢI NGHIỆM (EXPERIENCE RECOVERY)"
                action_desc = "Tự động gửi Email/SMS xin lỗi về sự chậm trễ vận chuyển + Tặng Voucher Giảm 15% (hoặc Free Ship) cho đơn hàng tiếp theo có hạn dùng 30 ngày."
                action_channel = "Push Notification & Email Automation (Chi phí: ~25 BRL/khách)"
            elif "Tài chính" in top_cause or order_spent > 300:
                action_title = "GÓI KÍCH CẦU THANH KHOẢN (FINANCIAL RELIEF)"
                action_desc = "Gửi thông báo ưu đãi Gói Trả góp 0% Lãi suất lên đến 10-12 kỳ cho lần mua tới + Đề xuất các sản phẩm combo giảm áp lực giỏ hàng."
                action_channel = "Re-targeting Facebook/Google Ads & App Banner (Chi phí: ~15 BRL/lead)"
            else:
                action_title = "GÓI TÁI TƯƠNG TÁC NGÀNH HÀNG (CATEGORY RE-ENGAGEMENT)"
                action_desc = "Gợi ý sản phẩm bổ trợ hoặc hàng tiêu hao định kỳ cùng ngành hàng + Tặng Voucher 10% cho đơn hàng đạt giá trị tối thiểu 100 BRL."
                action_channel = "Personalized Recommendation Widget trên App (Chi phí: ~10 BRL/khách)"

        return {
            "transformed_features": X_sample,
            "prob_retain": prob_retain,
            "prob_retain_pct": f"{prob_retain:.2%}",
            "risk_tier": tier_label,
            "tier_color": tier_color,
            "can_intervene": can_intervene,
            "pie_chart_data": df_pie,
            "top_cause": top_cause,
            "action_title": action_title,
            "action_desc": action_desc,
            "action_channel": action_channel
        }

    @staticmethod
    def simulate_roi(target_customers=4124, cost_per_voucher=20.0, expected_uplift_pct=20.0,
                      avg_order_value=160.0, net_margin_pct=30.0, future_orders=1.5):
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
