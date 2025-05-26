import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Streamlit 페이지 설정
st.set_page_config(page_title="📈 글로벌 시가총액 TOP10 주가 트렌드", layout="wide")
st.title("📈 글로벌 시가총액 TOP10 기업의 최근 1년 주가 트렌드")

# 시가총액 상위 10개 기업 (2025년 기준 예시)
top10_companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",  # 사우디 거래소
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta Platforms": "META",
    "TSMC": "TSM",
    "Tesla": "TSLA"
}

# 날짜 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 데이터 수집
st.info("데이터를 불러오고 있습니다. 잠시만 기다려주세요...")

data = {}
for name, ticker in top10_companies.items():
    try:
        df = yf.download(ticker, start=start_date, end=end_date)
        if not df.empty:
            data[name] = df["Adj Close"]
    except Exception as e:
        st.warning(f"{name} 데이터 로드 실패: {e}")

# 데이터 통합
price_df = pd.DataFrame(data)

# 시각화
fig = go.Figure()
for company in price_df.columns:
    fig.add_trace(go.Scatter(x=price_df.index, y=price_df[company],
                             mode='lines', name=company))

fig.update_layout(
    title="📊 글로벌 시가총액 상위 10개 기업의 최근 1년간 주가 변화",
    xaxis_title="날짜",
    yaxis_title="조정 종가 (USD)",
    height=700,
    legend=dict(orientation="h", y=-0.2),
)

st.plotly_chart(fig, use_container_width=True)
