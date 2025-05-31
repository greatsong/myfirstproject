import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="글로벌 시가총액 Top 10 대시보드",
    page_icon="📈",
    layout="wide"
)

# 제목과 설명
st.title("🌍 글로벌 시가총액 Top 10 기업 - 3년간 변화 분석")
st.markdown("""
이 대시보드는 전 세계 시가총액 상위 10개 기업의 지난 3년간 변화를 인터랙티브하게 보여줍니다.
데이터는 Yahoo Finance에서 실시간으로 가져옵니다.
""")

# Top 10 기업 정보 (2025년 5월 기준)
TOP_10_COMPANIES = {
    'Apple': 'AAPL',
    'Nvidia': 'NVDA', 
    'Microsoft': 'MSFT',
    'Alphabet': 'GOOGL',
    'Amazon': 'AMZN',
    'Meta Platforms': 'META',
    'Tesla': 'TSLA',
    'Berkshire Hathaway': 'BRK-A',
    'Taiwan Semiconductor': 'TSM',
    'Broadcom': 'AVGO'
}

@st.cache_data(ttl=3600)  # 1시간 캐시
def get_stock_data(symbol, period="3y"):
    """주식 데이터를 가져오는 함수"""
    try:
        stock = yf.Ticker(symbol)
        hist = stock.get_history(period=period)
        info = stock.get_info()
        
        # 시가총액 계산 (주가 * 발행주식수)
        shares_outstanding = info.get('sharesOutstanding', info.get('impliedSharesOutstanding', 1))
        hist['Market_Cap'] = hist['Close'] * shares_outstanding / 1e12  # 조 달러 단위
        
        return hist, info
    except Exception as e:
        st.error(f"{symbol} 데이터를 가져오는 중 오류 발생: {e}")
        return None, None

@st.cache_data(ttl=3600)
def load_all_data():
    """모든 기업의 데이터를 로드"""
    all_data = {}
    company_info = {}
    
    progress_bar = st.progress(0)
    progress_text = st.empty()
    
    total_companies = len(TOP_10_COMPANIES)
    
    for i, (company, symbol) in enumerate(TOP_10_COMPANIES.items()):
        progress_text.text(f"데이터 로딩 중: {company} ({symbol})")
        progress_bar.progress((i + 1) / total_companies)
        
        hist, info = get_stock_data(symbol)
        if hist is not None:
            all_data[company] = hist
            company_info[company] = info
    
    progress_bar.empty()
    progress_text.empty()
    
    return all_data, company_info

# 데이터 로딩
with st.spinner("데이터를 불러오는 중..."):
    stock_data, company_info = load_all_data()

if not stock_data:
    st.error("데이터를 불러올 수 없습니다. 나중에 다시 시도해주세요.")
    st.stop()

# 사이드바 설정
st.sidebar.header("📊 차트 설정")

# 기업 선택 (멀티셀렉트)
selected_companies = st.sidebar.multiselect(
    "표시할 기업 선택:",
    options=list(TOP_10_COMPANIES.keys()),
    default=list(TOP_10_COMPANIES.keys())[:5]  # 기본적으로 상위 5개 선택
)

# 기간 선택
period_options = {
    "최근 1년": "1y",
    "최근 2년": "2y", 
    "최근 3년": "3y"
}
selected_period = st.sidebar.selectbox(
    "기간 선택:",
    options=list(period_options.keys()),
    index=2  # 기본값: 3년
)

# 차트 타입 선택
chart_type = st.sidebar.radio(
    "차트 타입:",
    ["라인 차트", "영역 차트", "로그 스케일"]
)

# 메인 차트
st.subheader("📈 시가총액 변화 추이")

if selected_companies:
    # 선택된 기업들의 데이터 준비
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set3
    
    for i, company in enumerate(selected_companies):
        if company in stock_data:
            data = stock_data[company]
            
            # 선택된 기간에 따라 데이터 필터링
            if selected_period != "최근 3년":
                end_date = datetime.now()
                if selected_period == "최근 1년":
                    start_date = end_date - timedelta(days=365)
                else:  # 2년
                    start_date = end_date - timedelta(days=730)
                data = data[data.index >= start_date]
            
            color = colors[i % len(colors)]
            
            if chart_type == "영역 차트":
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['Market_Cap'],
                    mode='lines',
                    name=company,
                    line=dict(color=color),
                    fill='tonexty' if i > 0 else 'tozeroy',
                    fillcolor=color.replace('rgb', 'rgba').replace(')', ', 0.3)')
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=data['Market_Cap'],
                    mode='lines+markers',
                    name=company,
                    line=dict(color=color, width=3),
                    marker=dict(size=6),
                    hovertemplate='<b>%{fullData.name}</b><br>' +
                                  '날짜: %{x}<br>' +
                                  '시가총액: $%{y:.2f}T<br>' +
                                  '<extra></extra>'
                ))
    
    # 차트 레이아웃 설정
    fig.update_layout(
        title=f"시가총액 변화 ({period_options[selected_period]})",
        xaxis_title="날짜",
        yaxis_title="시가총액 (조 달러)",
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=600,
        template="plotly_white"
    )
    
    # 로그 스케일 적용
    if chart_type == "로그 스케일":
        fig.update_yaxis(type="log")
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("하나 이상의 기업을 선택해주세요.")

# 현재 시가총액 순위
st.subheader("🏆 현재 시가총액 순위")

# 현재 시가총액 데이터 생성
current_market_caps = []
for company, symbol in TOP_10_COMPANIES.items():
    if company in stock_data and company in company_info:
        try:
            latest_price = stock_data[company]['Close'].iloc[-1]
            shares = company_info[company].get('sharesOutstanding', 
                    company_info[company].get('impliedSharesOutstanding', 1))
            market_cap = (latest_price * shares) / 1e12
            current_market_caps.append({
                'Company': company,
                'Symbol': symbol,
                'Market Cap (T$)': market_cap,
                'Latest Price ($)': latest_price
            })
        except:
            continue

if current_market_caps:
    df_current = pd.DataFrame(current_market_caps)
    df_current = df_current.sort_values('Market Cap (T$)', ascending=False).reset_index(drop=True)
    df_current.index += 1
    
    # 순위 차트
    fig_ranking = px.bar(
        df_current.head(10), 
        x='Market Cap (T$)', 
        y='Company',
        orientation='h',
        title="현재 시가총액 Top 10",
        color='Market Cap (T$)',
        color_continuous_scale='viridis'
    )
    fig_ranking.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_ranking, use_container_width=True)
    
    # 테이블로도 표시
    st.dataframe(
        df_current.head(10).style.format({
            'Market Cap (T$)': '{:.2f}',
            'Latest Price ($)': '{:.2f}'
        }),
        use_container_width=True
    )

# 성장률 분석
st.subheader("📊 성장률 분석")

col1, col2 = st.columns(2)

with col1:
    st.write("**1년 수익률 Top 5**")
    returns_1y = []
    for company in TOP_10_COMPANIES.keys():
        if company in stock_data:
            data = stock_data[company]
            if len(data) >= 252:  # 1년 데이터
                return_1y = ((data['Close'].iloc[-1] / data['Close'].iloc[-252]) - 1) * 100
                returns_1y.append({'Company': company, 'Return (%)': return_1y})
    
    if returns_1y:
        df_returns_1y = pd.DataFrame(returns_1y).sort_values('Return (%)', ascending=False)
        st.dataframe(
            df_returns_1y.head(5).style.format({'Return (%)': '{:.1f}%'}),
            hide_index=True
        )

with col2:
    st.write("**3년 수익률 Top 5**")
    returns_3y = []
    for company in TOP_10_COMPANIES.keys():
        if company in stock_data:
            data = stock_data[company]
            if len(data) >= 756:  # 3년 데이터
                return_3y = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
                returns_3y.append({'Company': company, 'Return (%)': return_3y})
    
    if returns_3y:
        df_returns_3y = pd.DataFrame(returns_3y).sort_values('Return (%)', ascending=False)
        st.dataframe(
            df_returns_3y.head(5).style.format({'Return (%)': '{:.1f}%'}),
            hide_index=True
        )

# 변동성 분석
st.subheader("📈 변동성 분석")

volatility_data = []
for company in selected_companies:
    if company in stock_data:
        data = stock_data[company]
        daily_returns = data['Close'].pct_change().dropna()
        volatility = daily_returns.std() * np.sqrt(252) * 100  # 연간 변동성
        volatility_data.append({'Company': company, 'Annual Volatility (%)': volatility})

if volatility_data:
    df_volatility = pd.DataFrame(volatility_data).sort_values('Annual Volatility (%)')
    
    fig_vol = px.bar(
        df_volatility,
        x='Company',
        y='Annual Volatility (%)',
        title="연간 변동성 비교",
        color='Annual Volatility (%)',
        color_continuous_scale='reds'
    )
    fig_vol.update_layout(height=400)
    st.plotly_chart(fig_vol, use_container_width=True)

# 푸터
st.markdown("---")
st.markdown("""
**데이터 출처:** Yahoo Finance  
**업데이트:** 실시간 (1시간 캐시)  
**면책조항:** 이 데이터는 투자 조언이 아닙니다. 투자 결정은 전문가와 상담 후 신중히 하시기 바랍니다.
""")
