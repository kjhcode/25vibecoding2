import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="📈 글로벌 시가총액 TOP10 주가 트렌드", layout="wide")
st.title("📈 글로벌 시가총액 TOP10 기업의 최근 1년 주가 트렌드")

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

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

st.info("📡 주가 데이터를 로딩 중입니다...")

data = {}
error_list = []

for name, ticker in top10_companies.items():
    try:
        df = yf.download(ticker, start=start_date, end=end_date)
        if df.empty:
            error_list.append(f"{name} 데이터가 비어 있음")
            continue
        # 컬럼 확인: 'Adj Close' 없으면 'Close' 사용
        if "Adj Close" in df.columns:
            series = df["Adj Close"]
        elif "Close" in df.columns:
            series = df["Close"]
        else:
            error_list.append(f"{name}: 'Adj Close' 또는 'Close' 컬럼 없음")
            continue
        data[name] = series
    except Exception as e:
        error_list.append(f"{name} 데이터 로드 실패: {e}")

# 시각화
if data:
    price_df = pd.DataFrame(data)
    fig = go.Figure()
    for company in price_df.columns:
        fig.add_trace(go.Scatter(x=price_df.index, y=price_df[company],
                                 mode='lines', name=company))

    fig.update_layout(
        title="📊 글로벌 시가총액 상위 10개 기업의 최근 1년간 주가 변화",
        xaxis_title="날짜",
        yaxis_title="주가 (USD)",
        height=700,
        legend=dict(orientation="h", y=-0.2),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("❌ 유효한 데이터를 불러오지 못했습니다. 인터넷 연결 또는 API 문제일 수 있습니다.")

# 오류 메시지 표시
if error_list:
    st.subheader("⚠️ 데이터 로드 오류")
    for err in error_list:
        st.error(err)
