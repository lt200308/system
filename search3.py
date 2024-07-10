import streamlit as st
import pandas as pd
import os

# 读取Excel文件
rare_diseases_df = pd.read_excel('试验.xlsx')
chinese_medicine_df = pd.read_excel('试验2.xlsx')

# 假设图片文件名与罕见病中文名称相同
IMAGE_FOLDER = ''

def main():
    st.title('古道知识发现系统：罕见病知识发现')
    
    disease_name = st.text_input('输入罕见病中文名称')
    
    if disease_name:
        disease_info = rare_diseases_df[rare_diseases_df['中文名称'] == disease_name]
        
        if disease_info.empty:
            st.write("未找到相关信息")
        else:
            # 获取罕见病的同义词词群可视化图像
            image_path = os.path.join(IMAGE_FOLDER, f"{disease_name}.png")
            if not os.path.exists(image_path):
                st.write(f"文件 {image_path} 不存在")
            else:
                try:
                    st.image(image_path, caption=f"{disease_name} 的同义词词群可视化图像", use_column_width=True)
                except Exception as e:
                    st.write(f"打开文件 {image_path} 时发生错误: {e}")
            
            # 获取罕见病的相关信息
            english_name = disease_info.iloc[0]['英文名称']
            symptoms = disease_info.iloc[0]['病症']
            synonyms = disease_info[['同义词1', '同义词2']].values.flatten().tolist()
            
            # 确保同义词列表中的所有元素都是字符串类型
            synonyms = [str(synonym) for synonym in synonyms]
            
            st.write(f"英文名称: {english_name}")
            st.write(f"病症: {symptoms}")
            st.write(f"同义词: {', '.join(synonyms)}")
            
            # 添加按钮跳转到中医疾病介绍界面
            if st.button('查看中医疾病介绍'):
                # 根据“同义词1”列的内容查找“试验2”表格中的信息
                synonym1 = disease_info.iloc[0]['同义词1']
                chinese_medicine_info = chinese_medicine_df[chinese_medicine_df['疾病名称'] == synonym1]
                
                if not chinese_medicine_info.empty:
                    chinese_medicine_text = chinese_medicine_info.iloc[0]['原文复现']
                    st.subheader('中医疾病介绍')
                    st.write(chinese_medicine_text)
                else:
                    st.write("未找到相关中医疾病信息")

if __name__ == '__main__':
    main()