import streamlit as st  
import pandas as pd  
import requests  
from io import BytesIO  
from datetime import datetime  

# GitHub raw content URL for your Excel file  
GITHUB_EXCEL_URL = "https://raw.githubusercontent.com/Hizhuzi/Biomass-derived-porous-carbons-Synthesis-prediction-quiz/main/your_data.xlsx"  

@st.cache_data  
def load_data():  
    response = requests.get(GITHUB_EXCEL_URL)  
    content = BytesIO(response.content)  
    df = pd.read_excel(content)  
    return df.iloc[:, [8, 9]].sample(n=50, random_state=42).reset_index(drop=True)  

# 加载数据  
selected_data = load_data()  

# 初始化 session_state  
if 'current_index' not in st.session_state:  
    st.session_state.current_index = 0  
if 'data' not in st.session_state:  
    st.session_state.data = []  

def display_question(index):  
    st.markdown(f"### 多孔碳结构信息 (问题 {index + 1}/50)")  
    st.write(f"介孔比表面积: {selected_data.iloc[index, 0]} m²/g")  
    st.write(f"微孔比表面积: {selected_data.iloc[index, 1]} cm²/g")  

# 显示当前问题  
display_question(st.session_state.current_index)  

# 定义问卷内容  
st.markdown("### 请填写以下信息：")  
mass_ratio = st.slider('活化剂与原料的质量比', 0.25, 8.00, 0.25)  
temperature = st.slider('温度 (°C)', 300, 1000, 1)  
time = st.slider('时间 (小时)', 1, 8, 1)  
heating_rate = st.slider('升温速率 (°C/min)', 1, 40, 1)  
activator = st.selectbox('活化剂', ['Air', 'CO₂', 'Steam', 'KOH', 'NaOH', 'K₂CO₃', 'ZnCl₂', 'NaNH₂', 'K₂SiO₃', 'H₃PO₄', 'H₂SO₄', 'HNO₃', 'HCl', 'No Activator'])  
certainty = st.slider('确定程度', 1, 5, 1)  

def save_data():  
    result_df = pd.DataFrame(st.session_state.data)  
    buffer = BytesIO()  
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:  
        result_df.to_excel(writer, index=False)  
    st.download_button(  
        label="下载预测结果",  
        data=buffer.getvalue(),  
        file_name=f"human_expert_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",  
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  
    )  

def submit_data():  
    st.session_state.data.append({  
        '问题序号': st.session_state.current_index + 1,  
        '活化剂用量': mass_ratio,  
        '温度': temperature,  
        '时间': time,  
        '升温速率': heating_rate,  
        '活化剂': activator,  
        '确定程度': certainty,  
        '真实SSA': selected_data.iloc[st.session_state.current_index, 0],  
        '真实总孔容': selected_data.iloc[st.session_state.current_index, 1]  
    })  
    st.success('数据已提交！')  
    
    st.session_state.current_index += 1  
    if st.session_state.current_index < len(selected_data):  
        st.experimental_rerun()  
    else:  
        st.success('所有问题已回答完毕！')  
        save_data()  

st.button("提交", on_click=submit_data)  

# 显示进度  
st.progress(st.session_state.current_index / len(selected_data))