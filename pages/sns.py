import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv("한국언론진흥재단_10대미디어이용통계_SNS 서비스별 이용률_20221231.csv")

# 1. 요일별 SNS 사용 시간 평균
df_day = df.groupby("요일")["사용시간(분)"].mean().reset_index()
fig1 = px.bar(df_day, x="요일", y="사용시간(분)", title="요일별 SNS 평균 사용 시간", color="사용시간(분)")
fig1.show()

# 2. SNS 종류별 감정 점수 boxplot
fig2 = px.box(df, x="SNS종류", y="감정점수(1~10)", title="SNS 종류별 감정 점수 분포", color="SNS종류")
fig2.show()

# 3. 히트맵: 요일 & SNS종류별 평균 감정 점수
pivot_table = df.pivot_table(index="요일", columns="SNS종류", values="감정점수(1~10)", aggfunc="mean")
fig3 = px.imshow(pivot_table, title="요일 & SNS 종류별 감정 점수 히트맵", text_auto=True)
fig3.show()

# 4. 사용 시간에 따른 감정점수 산점도
fig4 = px.scatter(df, x="사용시간(분)", y="감정점수(1~10)", color="SNS종류",
                  title="SNS 사용시간과 감정 점수의 상관관계", trendline="ols")
fig4.show()
