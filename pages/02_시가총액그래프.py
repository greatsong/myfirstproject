import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="📈 글로벌 시가총액 Top 10", layout="wide")
st.title("📊 전 세계 시가총액 상위 10개 기업의 3년간 주가 변화")

# 티커 정보
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

start_date = (datetime.today() - timedelta(days=365*3)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

@st.cache_data
def fetch_price_data(tickers, start, end):
    data = yf.download(tickers, start=start, end=end, interval='1mo', progress=False)
    adj_close = data['Adj Close']  # 다중 컬럼에서 'Adj Close'만 선택
    adj_close = adj_close.dropna(how="all")
    return adj_close

tickers = list(companies.values())
df = fetch_price_data(tickers, start_date, end_date)

# 컬럼명을 기업 이름으로 변환
df.columns = [k for k, v in companies.items() if v in df.columns or v in tickers]

# 그래프 그리기
fig = go.Figure()

for ticker, company in zip(tickers, companies.keys()):
    if ticker in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[ticker],
            mode='lines+markers',
            name=company
        ))

fig.update_layout(
    title="💹 시가총액 상위 10개 기업 주가 변화 (월간 기준)",
    xaxis_title="날짜",
    yaxis_title="주가 (USD)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
