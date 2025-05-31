import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="📈 글로벌 시가총액 Top 10", layout="wide")
st.title("📊 전 세계 시가총액 상위 10개 기업의 3년간 주가 변화")

# 기업명과 티커 매핑
companies = {
    "Microsoft": "MSFT",
    "Nvidia": "NVDA",
    "Apple": "AAPL",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Saudi Aramco": "2222.SR",  # 사우디 거래소
    "Meta Platforms": "META",
    "Tesla": "TSLA",
    "Berkshire Hathaway": "BRK-B",
    "Broadcom": "AVGO"
}

start_date = (datetime.today() - timedelta(days=365 * 3)).strftime('%Y-%m-%d')
end_date = datetime.today().strftime('%Y-%m-%d')

@st.cache_data
def fetch_adj_close(ticker_dict, start, end):
    all_data = {}
    for name, ticker in ticker_dict.items():
        try:
            data = yf.download(ticker, start=start, end=end, interval="1mo", progress=False)
            if 'Adj Close' in data.columns:
                all_data[name] = data['Adj Close']
        except Exception as e:
            st.warning(f"{name} ({ticker}) 데이터 다운로드 실패: {e}")
    df = pd.DataFrame(all_data)
    return df.dropna(how="all")

df = fetch_adj_close(companies, start_date, end_date)

# 그래프 생성
fig = go.Figure()
for company in df.columns:
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[company],
        mode='lines+markers',
        name=company
    ))

fig.update_layout(
    title="💹 시가총액 상위 10개 기업의 주가 변화 (최근 3년)",
    xaxis_title="날짜",
    yaxis_title="주가 (USD)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
