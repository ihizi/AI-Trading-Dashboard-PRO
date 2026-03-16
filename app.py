import streamlit as st
from data import get_data
from indicators import apply_indicators
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="AI Trading Dashboard", layout="wide")

st.title("📊 AI Trading Dashboard PRO")

st.sidebar.header("Settings")

symbols = st.sidebar.text_input(
    "Tickers (max 4)",
    "AAPL,TSLA,NVDA,MSFT"
)

days = st.sidebar.slider(
    "Days",
    30,
    365,
    120
)

tickers = [s.strip() for s in symbols.split(",")][:4]


def draw_chart(ticker):

    df = get_data(ticker)

    if df is None:
        return None

    df = apply_indicators(df)
    df = df.tail(days)

    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.55,0.15,0.15,0.15],
        vertical_spacing=0.02
    )

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        ),
        row=1,
        col=1
    )

    fig.add_trace(go.Scatter(x=df.index,y=df["MA10"],line=dict(color="green")),row=1,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["MA20"],line=dict(color="red")),row=1,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["MA50"],line=dict(color="blue")),row=1,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["MA120"],line=dict(color="white")),row=1,col=1)

    fig.add_trace(
        go.Bar(x=df.index,y=df["Volume"]),
        row=2,col=1
    )

    fig.add_trace(
        go.Scatter(x=df.index,y=df["RSI"],line=dict(color="orange")),
        row=3,col=1
    )

    colors = ["red" if v >= 0 else "blue" for v in df["MACD_hist"]]

    fig.add_trace(
        go.Bar(x=df.index,y=df["MACD_hist"],marker_color=colors),
        row=4,col=1
    )

    fig.add_trace(go.Scatter(x=df.index,y=df["MACD"],line=dict(color="white")),row=4,col=1)
    fig.add_trace(go.Scatter(x=df.index,y=df["Signal"],line=dict(color="yellow")),row=4,col=1)

    fig.update_layout(
        template="plotly_dark",
        height=420,
        margin=dict(l=10,r=10,t=30,b=10),
        showlegend=False
    )

    return fig


for r in range(2):

    cols = st.columns(2)

    for c in range(2):

        idx = r*2 + c

        if idx < len(tickers):

            with cols[c]:

                ticker = tickers[idx]

                st.subheader(ticker)

                fig = draw_chart(ticker)

                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Data error")