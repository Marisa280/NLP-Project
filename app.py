import streamlit as st
import pandas as pd

# โหลดข้อมูลจากไฟล์ CSV
@st.cache_data
def load_data():
    data = pd.read_csv(r"C:\Users\Windows\Desktop\65160280\year_3\semester2\nlp\reccommend_menu\data_clean.csv")  # เปลี่ยนเป็นชื่อไฟล์ CSV ของคุณ
    print(data.columns)  # ตรวจสอบคอลัมน์ใน DataFrame
    # แปลง price_level ให้เป็นตัวเลขโดยการลบคำว่า "บาท"
    data['price_level'] = data['price_level'].str.replace(' บาท', '').map({
        "ต่ำกว่า 100": 1,
        "100-250": 2,
        "251-500": 3,
        "501-1,000": 4,
        "มากกว่า 1,000": 5
    })
    return data

def filter_data(data, keyword, price_type):
    # ใช้คอลัมน์ 'name' แทน 'menu' ในการกรอง
    filtered_data = data[data['name'].str.contains(keyword, case=False, na=False)]
    
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
            font-size: 16px;
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
        .stMarkdown, .stText {
            font-size: 14px;
        }
        .stSelectbox, .stTextInput {
            font-size: 16px;
        }
        .result-card {
            background-color: #ffecb3;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .result-card h3 {
            font-size: 18px;
            color: #ff5722;
        }
        .result-card p {
            font-size: 14px;
            color: #5a5a5a;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🥞 ค้นหาร้านอาหารด้วยเมนู")

    data = load_data()

    keyword = st.text_input("🔍 ใส่เมนูอาหารที่คุณชอบได้ที่ด้านล่าง")
    
    price_type = st.selectbox("💵 เลือกราคาโดยประมาณ", ["ต่ำกว่า 100", "100-250", "251-500", "501-1,000", "มากกว่า 1,000"])

    # เพิ่มตัวเลือกจำนวนร้านที่ต้องการแสดง
    num_results = st.selectbox("🔢 จำนวนร้านที่ต้องการแสดง", [5, 10, 15, 20])

    if st.button("ค้นหาเมนู"):
        if keyword:
            results = filter_data(data, keyword, price_type)
            if not results.empty:
                # จำกัดผลลัพธ์ให้แสดงตามจำนวนที่ผู้ใช้เลือก
                results = results.head(num_results)
                st.success(f"🔍 พบ {len(results)} ร้านที่ตรงกับเงื่อนไขของคุณ")
                for _, row in results.iterrows():
                    st.markdown(f"""
                    <div class="result-card">
                        <h3>📌 ชื่อร้าน: {row["name"]}</h3>
                        <p><strong>💵 ราคาโดยประมาณ:</strong> {row["price_level"]} บาท</p>
                        <p><strong>🍽 หมวดหมู่:</strong> {row["category"]}</p>
                        <p><strong>🔗 ดูรายละเอียดร้าน:</strong> <a href="{row["url"]}" target="_blank">คลิกที่นี่</a></p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("❌ ไม่พบร้านอาหารที่ตรงกับเงื่อนไขของคุณ")
        else:
            st.warning("⚠️ กรุณาใส่เมนูอาหารที่ต้องการค้นหา")

if __name__ == "__main__":   
    main()
