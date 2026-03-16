import yfinance as yf

def get_data(ticker):

    try:

        df = yf.download(
            ticker,
            period="2y",
            interval="1d",
            progress=False
        )

        if df.empty:
            return None

        return df

    except:

        return None