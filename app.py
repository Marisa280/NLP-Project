import streamlit as st
import pandas as pd

# ฟังก์ชันโหลดข้อมูลจาก URL
def load_data():
    url = "https://raw.githubusercontent.com/username/repository/branch/data_clean.csv"  # เปลี่ยนเป็น URL จริงของไฟล์
    data = pd.read_csv(url)
    return data

def filter_data(data, keyword, price_type):
    # กรองเมนูที่เกี่ยวข้องกับ keyword
    filtered_data = data[data['menu'].str.contains(keyword, case=False, na=False)]
    
    # แปลง price_level เป็นตัวเลข
    price_map = {
        "ต่ำกว่า 100": 1,
        "100-250": 2,
        "251-500": 3,
        "501-1,000": 4,
        "มากกว่า 1,000": 5
    }
    selected_price = price_map.get(price_type, None)
    
    # กรองตามระดับราคา
    if selected_price is not None:
        filtered_data = filtered_data[filtered_data["price_level"] == selected_price]

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
            background-color: #ff5722;
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
    
    price_type = st.selectbox("💵 เลือกราคาโดยประมาณ", ["ต่ำกว่า 100", "100-250", "251-500", "501-1,000", "มากกว่า 1,000"])

    if st.button("ค้นหาเมนู"):
        if keyword:
            results = filter_data(data, keyword, price_type)
            if not results.empty:
                st.success(f"🔍 พบ {len(results)} ร้านที่ตรงกับเงื่อนไขของคุณ")
                for _, row in results.iterrows():
                    st.markdown(f"""
                    **📌 ชื่อร้าน:** {row["Name"]}  
                    **💵 ราคาโดยประมาณ:** {row["price_level"]}  
                    **🍽 หมวดหมู่:** {row["category"]}  
                    🔗 [ดูรายละเอียดร้าน]({row["url"]})  
                    --- 
                    """)
            else:
                st.warning("❌ ไม่พบร้านอาหารที่ตรงกับเงื่อนไขของคุณ")
        else:
            st.warning("⚠️ กรุณาใส่เมนูอาหารที่ต้องการค้นหา")

if __name__ == "__main__":   
    main()
