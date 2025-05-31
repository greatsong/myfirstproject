import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="📈 글로벌 시가총액 Top 10", layout="wide")
st.title("📊 전 세계 시가총액 상위 10개 기업의 3년간 변화")

# 기업 티커
companies = {
    "Microsoft": "MSFT",
    "Nvidia": "NVDA",
    "Apple": "AAPL",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Saudi Aramco": "2222.SR",
    "Meta Platforms": "META",
    "Tesla": "TSLA",
    "Berkshire Hathaway": "BRK-B",
    "Broadcom": "AVGO"
}

# 데이터 불러오기
start_date = (datetime.today() - timedelta(days=365*3)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

@st.cache_data
def fetch_data(tickers, start, end):
    df = yf.download(tickers, start=start, end=end, interval='1mo', progress=False)["Adj Close"]
    df = df.dropna(how="all")  # 결측치 제거
    return df

tickers = list(companies.values())
price_df = fetch_data(tickers, start_date, end_date)

# 컬럼명 변환
price_df.columns = [name for name in companies.keys()]

# 그래프 생성
fig = go.Figure()

for company in price_df.columns:
    fig.add_trace(go.Scatter(
        x=price_df.index,
        y=price_df[company],
        mode='lines+markers',
        name=company
    ))

fig.update_layout(
    title="📈 기업별 시가총액 변화 (주가 기준, 월간)",
    xaxis_title="날짜",
    yaxis_title="조정 종가 (USD)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

