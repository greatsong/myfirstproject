import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 현재 (2025년 5월 기준) 시가총액 Top 10 기업 목록 (Forbes India 2025년 5월 21일 자료 기반)
# 실제 애플리케이션에서는 이 목록을 API 등을 통해 동적으로 가져오는 것이 이상적입니다.
TOP_COMPANIES = [
    "Microsoft", "Nvidia", "Apple", "Amazon", "Alphabet",
    "Saudi Aramco", "Meta Platforms", "Tesla", "Berkshire Hathaway", "Broadcom"
]

@st.cache_data
def load_data():
    """
    지난 3년간의 시가총액 데이터를 생성합니다.
    실제 환경에서는 금융 데이터 API (예: yfinance, Alpha Vantage 등) 또는
    정기적으로 업데이트되는 데이터베이스에서 데이터를 가져와야 합니다.
    여기서는 Wikipedia의 분기별 데이터 형식을 참고하여 임의의 데이터를 생성합니다.
    """
    dates = pd.to_datetime([
        "2022-03-31", "2022-06-30", "2022-09-30", "2022-12-31",
        "2023-03-31", "2023-06-30", "2023-09-30", "2023-12-31",
        "2024-03-31", "2024-06-30", "2024-09-30", "2024-12-31",
        "2025-03-31" # 현재 시점까지의 데이터라고 가정
    ])
    n_dates = len(dates)
    data = []

    # 각 회사에 대해 임의의 시가총액 데이터 생성 (단위: 조 달러)
    # 실제 데이터와는 차이가 있을 수 있습니다. 데모 목적의 데이터입니다.
    base_market_caps = {
        "Microsoft": 2.0, "Nvidia": 0.7, "Apple": 2.5, "Amazon": 1.5, "Alphabet": 1.8,
        "Saudi Aramco": 2.2, "Meta Platforms": 0.6, "Tesla": 0.8, "Berkshire Hathaway": 0.7, "Broadcom": 0.5
    }

    for company in TOP_COMPANIES:
        # 시간에 따라 변동하는 시가총액 데이터 생성
        # 시작 시가총액을 기준으로 랜덤하게 변동 (추세 반영 가능)
        current_cap = base_market_caps.get(company, 1.0) # 기본값 1조 달러
        market_caps = [current_cap]
        for _ in range(1, n_dates):
            change_factor = np.random.uniform(0.9, 1.15) # -10% ~ +15% 변동
            current_cap *= change_factor
            market_caps.append(round(current_cap, 2))

        for i in range(n_dates):
            data.append({
                "Date": dates[i],
                "Company": company,
                "Market Cap (Trillion USD)": market_caps[i]
            })

    df = pd.DataFrame(data)
    return df

# --- Streamlit 앱 구성 ---
st.set_page_config(layout="wide")
st.title("🌍 전 세계 시가총액 Top 10 기업 변화 (지난 3년)")
st.markdown("""
이 애플리케이션은 지난 3년간 시가총액 기준 상위 10개 기업의 변화 추세를 보여줍니다.
데이터는 데모 목적으로 생성된 임의의 값이며, 실제 시장 상황과 다를 수 있습니다.
""")

# 데이터 로드
df_market_cap = load_data()

# 사용자가 선택할 기업 목록 (기본적으로 전체 선택)
selected_companies = st.multiselect(
    "표시할 기업을 선택하세요:",
    options=TOP_COMPANIES,
    default=TOP_COMPANIES
)

if not selected_companies:
    st.warning("하나 이상의 기업을 선택해주세요.")
else:
    # 선택된 기업의 데이터 필터링
    df_filtered = df_market_cap[df_market_cap["Company"].isin(selected_companies)]

    # Plotly를 사용한 인터랙티브 라인 차트 생성
    fig = px.line(
        df_filtered,
        x="Date",
        y="Market Cap (Trillion USD)",
        color="Company",
        title="선택된 기업들의 시가총액 변화",
        markers=True,
        labels={"Date": "날짜", "Market Cap (Trillion USD)": "시가총액 (조 USD)", "Company": "기업명"}
    )

    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="시가총액 (조 USD)",
        legend_title_text='기업명',
        hovermode="x unified" # 여러 라인의 값을 동시에 보여줌
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("데이터 테이블")
    st.dataframe(df_filtered.style.format({"Market Cap (Trillion USD)": "{:.2f}T"}))

    # 데이터 출처 및 참고사항
    st.markdown("""
    ---
    **데이터 참고:**
    - 기업 목록은 Forbes India (2025년 5월 21일) 자료를 참고했습니다.
    - 그래프에 사용된 시가총액 데이터는 실제 데이터가 아닌, 데모 목적으로 생성된 **임의의 값**입니다.
    - 실제 금융 데이터는 금융 데이터 제공 API(예: Yahoo Finance, Alpha Vantage 등)를 통해 주기적으로 업데이트하여 사용하는 것이 정확합니다.

    **사용된 라이브러리:** Streamlit, Pandas, Plotly, Numpy
    """)
