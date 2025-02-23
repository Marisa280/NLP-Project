import streamlit as st
import pandas as pd
import random

# ฟังก์ชันโหลดข้อมูลจาก URL
def load_data():
    url = "https://raw.githubusercontent.com/Marisa280/NLP-Project-reccomend-food/refs/heads/main/data_clean.csv"  # ใช้ URL สำหรับ raw GitHub file
    data = pd.read_csv(url)
    return data

def filter_data(data, keyword, price_type):
    # กรองเมนูที่เกี่ยวข้องกับ keyword
    filtered_data = data[data['name'].str.contains(keyword, case=False, na=False)]
    
    # กรองตามระดับราคา
    if price_type:
        filtered_data = filtered_data[filtered_data["price_level"].str.contains(price_type, case=False, na=False)]

    return filtered_data

def main():
    st.set_page_config(page_title="ค้นหาร้านอาหารด้วยเมนูที่ชอบ", page_icon="🥙")

    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
        * {
            font-family: 'Kanit', sans-serif;
        }
        .stTextInput, .stNumberInput, .stButton > button {
            border-radius: 10px;
            font-size: 18px;
        }
        .stButton > button {
            background-color: #ff7043;
            color: white;
            border: none;
        }
        .stButton > button:hover {
            background-color: #f8f8f8;
        }
        h1 {
            font-family: 'Kanit', sans-serif !important;   
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🥞 ค้นหาร้านอาหารด้วยเมนู")

    data = load_data()  # โหลดข้อมูลจาก URL

    keyword = st.text_input("🔍 ใส่เมนูอาหารที่คุณชอบได้ที่ด้านล่าง")
    
    price_type = st.selectbox("💵 เลือกราคาโดยประมาณ", ["ต่ำกว่า 100", "100-250 บาท", "251-500 บาท", "501-1,000 บาท", "มากกว่า 1,000"])
    
    num_results = st.slider("จำนวนร้านที่ต้องการแสดง", 1, 20, 5)  # ให้ผู้ใช้เลือกจำนวนร้านที่ต้องการแสดง

    if st.button("ค้นหาเมนู"):
        if keyword:
            results = filter_data(data, keyword, price_type)
            if not results.empty:
                st.success(f"🔍 พบ {len(results)} ร้านที่ตรงกับเงื่อนไขของคุณ")
                
                # สุ่มลำดับผลลัพธ์
                results = results.sample(frac=1).reset_index(drop=True)
                
                # เลือกเฉพาะจำนวนร้านที่ผู้ใช้เลือก
                results_to_show = results.head(num_results)
                
                # แสดงผลลัพธ์
                for _, row in results_to_show.iterrows():
                    st.markdown(f"""
                    <div style="border: 2px solid #ff7043; padding: 15px; border-radius: 10px; margin-bottom: 10px; background-color: #6495ED;">
                        <strong>📌 ชื่อร้าน:</strong> {row["name"]}  
                        <br>
                        <strong>💵 ราคาโดยประมาณ:</strong> {row["price_level"]}  
                        <br>
                        <strong>🍽 หมวดหมู่:</strong> {row["category"]}  
                        <br>
                        <strong>🔗 [ดูรายละเอียดร้าน]({row["url"]})</strong>  
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("❌ ไม่พบร้านอาหารที่ตรงกับเงื่อนไขของคุณ")
        else:
            st.warning("⚠️ กรุณาใส่เมนูอาหารที่ต้องการค้นหา")

if __name__ == "__main__":   
    main()
