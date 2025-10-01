import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

def fetch_data(tickers, start, end):
    # yfinance로 Adjusted Close 가격 가져오기
    data = yf.download(tickers, start=start, end=end, progress=False)["Adj Close"]
    return data

def main():
    st.title("글로벌 시가총액 상위 기업들의 최근 1년 주가 변화")

    # 사용자로부터 종목 리스트 입력 가능하게
    default_tickers = ["NVDA", "MSFT", "AAPL", "AMZN", "GOOGL", "META", "AVGO", "TSM", "BRK-B", "TSLA"]
    tickers = st.text_input("Ticker들을 콤마로 구분하여 입력하세요", ",".join(default_tickers))
    tickers = [t.strip() for t in tickers.split(",")]

    # 기간: 오늘로부터 1년 전
    end = pd.Timestamp.now().date()
    start = end - pd.DateOffset(years=1)

    st.write(f"데이터 기간: {start.date()} ~ {end}")

    # 데이터 불러오기
    df = fetch_data(tickers, start, end)

    if df.empty:
        st.error("데이터를 불러오지 못했습니다. 티커를 확인해주세요.")
        return

    # 누적 수익률 계산 (기준일 대비 상대 변화)
    returns = df / df.iloc[0] - 1.0

    # Altair로 시각화
    df_long = returns.reset_index().melt("Date", var_name="Ticker", value_name="Return")

    chart = (
        alt.Chart(df_long)
        .mark_line()
        .encode(
            x="Date:T",
            y=alt.Y("Return:Q", axis=alt.Axis(format=".0%")),
            color="Ticker:N"
        )
        .properties(
            width=800,
            height=400,
            title="최근 1년 누적 수익률 (기준일 대비)"
        )
    )

    st.altair_chart(chart, use_container_width=True)

if __name__ == "__main__":
    main()
