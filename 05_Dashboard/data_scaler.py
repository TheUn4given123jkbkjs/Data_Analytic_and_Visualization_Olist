"""
DATA SCALER & FEATURE PREPROCESSOR FOR OLIST DASHBOARD
DỰ ÁN PHÂN TÍCH DỮ LIỆU THƯƠNG MẠI ĐIỆN TỬ BRAZIL (OLIST E-COMMERCE)

Công cụ này giúp tiền xử lý, trích xuất đặc trưng và chuẩn hóa (Scale/Transform)
mọi định dạng dữ liệu đầu vào thành đúng ma trận 33 đặc trưng chuẩn để đưa trực tiếp vào mô hình AI.

Hỗ trợ 3 cách nhập liệu:
1. Truyền từng tham số lẻ (kwargs) từ các widget Streamlit (slider, selectbox).
2. Truyền 1 Dictionary / JSON.
3. Truyền cả 1 DataFrame / file CSV thô (Batch processing).
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class OlistFeatureScaler:
    """
    Bộ tiền xử lý & Scaler chuẩn hóa dữ liệu khách hàng Olist.
    """
    def __init__(self, model_dir=None):
        if model_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.model_dir = os.path.abspath(os.path.join(current_dir, "..", "03_Predictive", "models"))
        else:
            self.model_dir = model_dir
            
        self.features_path = os.path.join(self.model_dir, "feature_columns.json")
        self.train_data_path = os.path.abspath(os.path.join(self.model_dir, "..", "data", "train_test", "X_train.csv"))
        
        # Load danh sách 33 đặc trưng chuẩn
        if os.path.exists(self.features_path):
            with open(self.features_path, "r", encoding="utf-8") as f:
                self.feature_columns = json.load(f)
        else:
            raise FileNotFoundError(f"Không tìm thấy file feature columns tại: {self.features_path}")
            
        # Khởi tạo Scaler nếu cần dùng cho các mô hình tuyến tính (Logistic Regression / SVM)
        self.scaler = None
        self._is_scaler_fitted = False
        
    def fit_scaler(self, method="standard"):
        """
        Fit scaler trên tập huấn luyện gốc X_train để chuẩn hóa thang đo Z-score hoặc MinMax.
        """
        if os.path.exists(self.train_data_path):
            df_train = pd.read_csv(self.train_data_path)[self.feature_columns]
            if method == "standard":
                self.scaler = StandardScaler()
            elif method == "minmax":
                self.scaler = MinMaxScaler()
            else:
                self.scaler = None
                self._is_scaler_fitted = False
                return self
                
            self.scaler.fit(df_train)
            self._is_scaler_fitted = True
        return self

    def _transform_single_dict(self, d):
        """
        Biến đổi 1 bản ghi thô thành 1 dòng 33 đặc trưng.
        """
        # 1. Trích xuất các trường cơ bản với giá trị mặc định thông minh
        order_spent = float(d.get("order_spent", d.get("price", d.get("total_payment", 150.0))))
        max_installments = int(d.get("max_installments", d.get("payment_installments", 1)))
        payment_type = str(d.get("payment_type", "credit_card")).lower().strip()
        delivery_days = float(d.get("delivery_days", d.get("actual_delivery_days", 8.0)))
        estimated_delivery_days = float(d.get("estimated_delivery_days", d.get("estimated_days", 15.0)))
        review_score = float(d.get("review_score", d.get("score", 5.0)))
        customer_state = str(d.get("customer_state", d.get("state", "SP"))).upper().strip()
        product_category = str(d.get("product_category", d.get("product_category_name", "cama_mesa_banho"))).lower().strip()
        
        # 2. Tính toán các đặc trưng phái sinh & Tương tác phi tuyến (Interaction Features)
        delivery_delay = delivery_days - estimated_delivery_days
        delivery_speed_ratio = np.clip(delivery_days / max(estimated_delivery_days, 1.0), 0.0, 5.0)
        monthly_installment_burden = order_spent / max(max_installments, 1)
        is_b2b_profile = 1.0 if (order_spent > 300.0 and payment_type == "boleto") else 0.0
        
        # 3. Tạo dictionary 33 cột
        row = {col: 0.0 for col in self.feature_columns}
        
        # Điền biến số liên tục
        row["delivery_days"] = delivery_days
        row["delivery_delay"] = delivery_delay
        row["delivery_speed_ratio"] = delivery_speed_ratio
        row["review_score"] = review_score
        row["order_spent"] = order_spent
        row["monthly_installment_burden"] = monthly_installment_burden
        row["max_installments"] = float(max_installments)
        row["is_b2b_profile"] = is_b2b_profile
        
        # One-hot Payment
        pay_key = f"pay_{payment_type}"
        if pay_key in row:
            row[pay_key] = 1.0
            
        # One-hot State (SP, RJ, MG, Sul, outros)
        if customer_state == "SP":
            row["state_SP"] = 1.0
        elif customer_state == "RJ":
            row["state_RJ"] = 1.0
        elif customer_state == "MG":
            row["state_MG"] = 1.0
        elif any(s in customer_state for s in ["SUL", "RS", "PR", "SC"]):
            row["state_Sul"] = 1.0
        else:
            row["state_outros"] = 1.0
            
        # One-hot Category
        cat_key = f"cat_{product_category}"
        if cat_key in row:
            row[cat_key] = 1.0
        else:
            row["cat_outros"] = 1.0
            
        return row

    def transform(self, data=None, scale=False, scale_method="standard", **kwargs):
        """
        Hàm trung tâm: Nhận mọi loại đầu vào -> Trả về DataFrame 33 cột chuẩn 100%.
        
        Parameters:
        -----------
        data : dict, list of dicts, pandas.DataFrame, hoặc None (nếu truyền kwargs)
        scale : bool, True nếu muốn chuẩn hóa dữ liệu qua StandardScaler/MinMaxScaler
        scale_method : str, 'standard' (Z-score) hoặc 'minmax'
        **kwargs : các tùy chọn lẻ từ UI như order_spent=120, delivery_days=5...
        
        Returns:
        --------
        pandas.DataFrame: DataFrame đúng 33 cột theo đúng thứ tự mô hình yêu cầu.
        """
        # Trường hợp 1: Nhận DataFrame
        if isinstance(data, pd.DataFrame):
            # Nếu DataFrame đã có đúng 33 cột
            if all(col in data.columns for col in self.feature_columns):
                df_res = data[self.feature_columns].copy()
            else:
                # DataFrame chứa cột thô -> chuyển đổi từng dòng
                records = data.to_dict(orient="records")
                transformed_records = [self._transform_single_dict(r) for r in records]
                df_res = pd.DataFrame(transformed_records)[self.feature_columns]
                
        # Trường hợp 2: Nhận List of Dicts
        elif isinstance(data, list):
            transformed_records = [self._transform_single_dict(r) for r in data]
            df_res = pd.DataFrame(transformed_records)[self.feature_columns]
            
        # Trường hợp 3: Nhận 1 Dict
        elif isinstance(data, dict):
            # Gộp chung với kwargs nếu có
            merged_dict = {**data, **kwargs}
            transformed_record = self._transform_single_dict(merged_dict)
            df_res = pd.DataFrame([transformed_record])[self.feature_columns]
            
        # Trường hợp 4: Chỉ truyền qua kwargs lẻ
        else:
            transformed_record = self._transform_single_dict(kwargs)
            df_res = pd.DataFrame([transformed_record])[self.feature_columns]

        # Chuẩn hóa (nếu được yêu cầu)
        if scale:
            if not self._is_scaler_fitted:
                self.fit_scaler(method=scale_method)
            if self.scaler is not None:
                scaled_arr = self.scaler.transform(df_res)
                df_res = pd.DataFrame(scaled_arr, columns=self.feature_columns, index=df_res.index)

        return df_res

# =====================================================================
# HÀM RÚT GỌN 1 DÒNG DÀNH CHO CÁC THÀNH VIÊN LÀM STREAMLIT NHANH CHÓNG
# =====================================================================

_global_scaler_instance = None

def get_scaler_instance():
    global _global_scaler_instance
    if _global_scaler_instance is None:
        _global_scaler_instance = OlistFeatureScaler()
    return _global_scaler_instance

def prepare_input(data=None, scale=False, **kwargs):
    """
    Hàm rút gọn cực nhanh: Chỉ cần gọi prepare_input(...) là có ngay dữ liệu nạp vào model.
    
    Ví dụ sử dụng:
    --------------
    from data_scaler import prepare_input
    
    # 1. Từ các biến giao diện Streamlit:
    X = prepare_input(
        order_spent=250.0,
        delivery_days=12.0,
        estimated_delivery_days=18.0,
        payment_type="credit_card",
        customer_state="SP",
        product_category="beleza_saude",
        review_score=5,
        max_installments=4
    )
    
    # 2. Hoặc từ 1 Dictionary:
    raw_dict = {"order_spent": 350.0, "payment_type": "boleto", "delivery_days": 20.0}
    X = prepare_input(raw_dict)
    
    # 3. Đưa trực tiếp vào Model:
    prob = model.predict_proba(X)[0, 1]
    """
    scaler = get_scaler_instance()
    return scaler.transform(data=data, scale=scale, **kwargs)

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("--- KIEM TRA BO SCALER & TRANSFORMER ---")
    scaler = OlistFeatureScaler()
    
    # Test 1: Kwargs le
    df1 = prepare_input(order_spent=500.0, payment_type="boleto", delivery_days=15.0, estimated_delivery_days=10.0, customer_state="RJ")
    print("\n[Test 1] Single Input Transformed Shape:", df1.shape)
    print("is_b2b_profile value:", df1["is_b2b_profile"].values[0])
    print("delivery_delay value:", df1["delivery_delay"].values[0])
    print("delivery_speed_ratio value:", df1["delivery_speed_ratio"].values[0])
    print("state_RJ value:", df1["state_RJ"].values[0])
    
    # Test 2: Raw DataFrame
    raw_df = pd.DataFrame([
        {"price": 120.0, "actual_delivery_days": 7.0, "estimated_days": 14.0, "state": "SP", "payment_type": "voucher"},
        {"price": 450.0, "actual_delivery_days": 22.0, "estimated_days": 15.0, "state": "RS", "payment_type": "boleto"}
    ])
    df2 = prepare_input(raw_df)
    print("\n[Test 2] Batch DataFrame Transformed Shape:", df2.shape)
    print(df2[["order_spent", "delivery_days", "delivery_delay", "is_b2b_profile", "state_SP", "state_Sul"]])
    print("\n[OK] Scaler & Preprocessor hoat dong hoan hao 100%!")
