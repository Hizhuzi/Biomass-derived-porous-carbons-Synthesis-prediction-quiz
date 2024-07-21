import streamlit as st  
import pandas as pd  
import io  

# 预先加载数据  
@st.cache_data  
def load_data():  
    # 替换为您的实际数据文件路径  
    df = pd.read_excel("your_data.xlsx")  
    return df.iloc[:, [8, 9]].sample(n=50, random_state=42).reset_index(drop=True)  

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
mass_ratio = st.slider('活化剂与原料的质量比', 0.25, 8.00, 0.5, step=0.25)  
temperature = st.slider('温度 (°C)', 300, 1000, 500, step=1)  
time = st.slider('时间 (小时)', 1.0, 8.0, 4.0, step=0.1)  # 修改了这里  
heating_rate = st.slider('升温速率 (°C/min)', 1, 40, 20, step=1)  
activator = st.selectbox('活化剂', ['Air', 'CO₂', 'Steam', 'KOH', 'NaOH', 'K₂CO₃', 'ZnCl₂', 'NaNH₂', 'K₂SiO₃', 'H₃PO₄', 'H₂SO₄', 'HNO₃', 'HCl', 'No Activator'])  
certainty = st.slider('确定程度', 1, 5, 3, step=1)  

def save_data():  
    result_df = pd.DataFrame(st.session_state.data)  
    result_df.to_csv('human_expert_predictions.csv', index=False)  
    st.success('预测结果已保存')  

def submit_data():  
    st.session_state.data.append({  
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