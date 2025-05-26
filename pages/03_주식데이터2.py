import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import folium
from streamlit_folium import st_folium
import pandas as pd
import random

# --- 한글 폰트 설정 ---
# 시스템 환경에 따라 경로 조정 (Streamlit Cloud 또는 리눅스 서버 기준 예시)
font_path = os.path.join("fonts", "Malgun Gothic")
if os.path.exists(font_path):
    fontprop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = fontprop.get_name()
else:
    st.warning("한글 폰트 파일이 존재하지 않습니다. 경로를 확인해주세요.")

# --- 페이지 설정 ---
st.set_page_config(
    page_title="나만의 K-기업 투자 지도",
    page_icon="🇰🇷",
    layout="wide"
)

# --- 데이터 ---
COMPANIES = {
    "삼성전자": {"ticker": "005930.KS", "lat": 37.2390, "lon": 127.0708, "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Samsung_Logo.svg/2560px-Samsung_Logo.svg.png"},
    "SK하이닉스": {"ticker": "000660.KS", "lat": 37.2780, "lon": 127.1460, "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/SK_Hynix_logo.svg/1200px-SK_Hynix_logo.svg.png"},
    "LG에너지솔루션": {"ticker": "373220.KS", "lat": 37.5267, "lon": 126.9290, "logo": "https://www.lgensol.com/assets/images/common/logo_header.svg"},
    "현대자동차": {"ticker": "005380.KS", "lat": 37.5282, "lon": 127.0262, "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Hyundai_Motor_Company_logo.svg/1920px-Hyundai_Motor_Company_logo.svg.png"},
    "NAVER": {"ticker": "035420.KS", "lat": 37.3948, "lon": 127.1112, "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Naver_Logotype.svg/1200px-Naver_Logotype.svg.png"},
    "카카오": {"ticker": "035720.KS", "lat": 33.4996, "lon": 126.5312, "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/KakaoTalk_logo.svg/1024px-KakaoTalk_logo.svg.png"}
}

INVESTMENT_OPINIONS = [
    "🚀 지금이 매수 타이밍! 우주로 가즈아!",
    "🤔 신중한 접근이 필요해 보입니다. 시장 상황을 더 지켜보세요.",
    "📈 장기적으로 성장 가능성이 높아 보입니다. 분할 매수를 고려해보세요!",
    "📉 단기 변동성에 주의하세요. 하지만 기업 가치는 튼튼합니다!",
    "💡 새로운 기술/서비스에 주목! 미래가 기대됩니다.",
    "🧐 경쟁이 치열한 분야입니다. 차별점을 확인하세요."
]

# --- 함수 정의 ---
@st.cache_data(ttl=3600)
def get_stock_data(ticker_symbol, period="1y"):
    try:
        stock = yf.Ticker(ticker_symbol)
        data = stock.history(period=period)
        data.index = data.index.strftime('%Y-%m-%d')
        return data
    except Exception as e:
        st.error(f"{ticker_symbol} 주식 데이터를 가져오는 중 오류 발생: {e}")
        return pd.DataFrame()

def plot_stock_chart(data, company_name):
    if data.empty or 'Close' not in data.columns:
        st.warning(f"{company_name}의 주가 데이터를 표시할 수 없습니다.")
        return None

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data.index, data['Close'], label=f'{company_name} 종가', color='dodgerblue', linewidth=2)
    ax.set_title(f'{company_name} 최근 1년 주가 추이', fontsize=18)
    ax.set_xlabel('날짜', fontsize=12)
    ax.set_ylabel('주가 (KRW)', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    if len(data.index) > 50:
        ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    plt.tight_layout()
    return fig

# --- 앱 UI 구성 ---
st.title("📈 나만의 K-기업 투자 지도 🗺️")
st.markdown("관심 있는 한국 기업의 주가와 본사 위치를 한눈에 살펴보세요!")

# --- 사이드바 ---
st.sidebar.header("🏢 기업 선택")
selected_company_name = st.sidebar.selectbox(
    "분석할 기업을 선택하세요:",
    list(COMPANIES.keys())
)

selected_company_info = COMPANIES[selected_company_name]
ticker = selected_company_info["ticker"]

# --- 메인 화면 ---
st.header(f"{selected_company_name} ({ticker})")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 주가 정보 (최근 1년)")
    stock_data = get_stock_data(ticker)

    if not stock_data.empty:
        chart_fig = plot_stock_chart(stock_data, selected_company_name)
        if chart_fig:
            st.pyplot(chart_fig)

        st.markdown("---")
        latest_price = stock_data['Close'].iloc[-1]
        highest_price_1y = stock_data['High'].max()
        lowest_price_1y = stock_data['Low'].min()
        st.markdown(f"""
        - **최근 종가:** `{latest_price:,.0f} KRW`
        - **지난 1년 최고가:** `{highest_price_1y:,.0f} KRW`
        - **지난 1년 최저가:** `{lowest_price_1y:,.0f} KRW`
        """)
    else:
        st.warning(f"{selected_company_name}의 주가 데이터를 가져올 수 없습니다.")

with col2:
    st.subheader("📍 본사 위치")
    map_center_lat = selected_company_info["lat"]
    map_center_lon = selected_company_info["lon"]

    m = folium.Map(location=[map_center_lat, map_center_lon], zoom_start=7)

    for name, info in COMPANIES.items():
        popup_html = f"""
        <b>{name}</b> ({info['ticker']})<br>
        <img src='{info.get('logo', '')}' alt='logo' width='50' onerror="this.style.display='none'"><br>
        <a href='https://finance.yahoo.com/quote/{info['ticker']}' target='_blank'>Yahoo Finance에서 보기</a>
        """
        if name == selected_company_name:
            folium.Marker(
                [info["lat"], info["lon"]],
                popup=folium.Popup(popup_html, max_width=200),
                tooltip=f"{name} (선택됨)",
                icon=folium.Icon(color="red", icon="star")
            ).add_to(m)
        else:
            folium.Marker(
                [info["lat"], info["lon"]],
                popup=folium.Popup(popup_html, max_width=200),
                tooltip=name,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

    st_folium(m, width=700, height=400)

    st.markdown("---")
    st.subheader("🤖 AI의 재미로 보는 투자 의견")
    opinion = random.choice(INVESTMENT_OPINIONS)
    st.info(opinion)
    st.caption("주의: 이 의견은 실제 투자 조언이 아니며, 재미를 위해 제공됩니다.")

# --- 추가 정보 ---
st.markdown("---")
st.subheader("ℹ️ 정보")
st.markdown("""
- 이 앱은 `Streamlit`, `yfinance`, `Matplotlib`, `Folium` 등을 사용하여 제작되었습니다.
- 주가 데이터는 Yahoo Finance에서 제공되며, 실시간이 아닐 수 있습니다.
- 본사 위치 및 로고는 예시이며, 실제와 다를 수 있습니다.
- 모든 투자 결정은 개인의 판단과 책임 하에 이루어져야 합니다.
""")
