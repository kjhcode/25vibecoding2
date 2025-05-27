import pandas as pd
import plotly.express as px

# CSV 파일 로드 (encoding 문제 주의)
df = pd.read_csv('한국언론진흥재단_10대미디어이용통계_SNS 서비스별 이용률_20221231.csv', encoding='cp949')

# 데이터 변환: 학년별 이용현황을 세로로 피벗
df_melted = df.melt(id_vars='SNS 종류', 
                    value_vars=['초등학생 이용현황', '중학생 이용현황', '고등학생 이용현황'], 
                    var_name='학년', 
                    value_name='이용률')

# 그룹 막대그래프 생성
fig = px.bar(df_melted, 
             x='SNS 종류', 
             y='이용률', 
             color='학년', 
             barmode='group',
             title='SNS 서비스별 학년별 이용률 비교')

fig.show()
