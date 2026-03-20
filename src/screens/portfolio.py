import streamlit as st
from utils.data import load_ibov_tickers, load_data, normalize_ticker, IBOV_FILE_PATH
from utils.volatility import annualized_volatility_from_prices


def display_portfolio_volatility(tab=None, period="1y", interval="1d"):
    if "portfolio_tickers" not in st.session_state:
        st.session_state.portfolio_tickers = []
    if "portfolio_volatilities" not in st.session_state:
        st.session_state.portfolio_volatilities = {}
    if "portfolio_period" not in st.session_state:
        st.session_state.portfolio_period = period
    if "portfolio_interval" not in st.session_state:
        st.session_state.portfolio_interval = interval

    if (
        st.session_state.portfolio_tickers
        and (
            st.session_state.portfolio_period != period
            or st.session_state.portfolio_interval != interval
        )
    ):
        st.session_state.portfolio_period = period
        st.session_state.portfolio_interval = interval
        for t in st.session_state.portfolio_tickers:
            df = load_data(t, period=period, interval=interval)
            if df is not None and not df.empty:
                vol = annualized_volatility_from_prices(df["Close"])
                st.session_state.portfolio_volatilities[t] = vol.values[0]

    try:
        suggestions = [t.replace(".SA", "") for t in load_ibov_tickers(IBOV_FILE_PATH)]
    except Exception:
        suggestions = []

    tab.subheader("Monte sua Carteira (Buy and Hold)")

    col_input, col_btn = tab.columns([3, 1])
    ticker_input = col_input.text_input(
        "Ticker",
        key="portfolio_ticker_input",
        placeholder="Ex: PETR4, VALE3, AAPL...",
        label_visibility="collapsed",
    )
    add_clicked = col_btn.button("Adicionar", key="portfolio_add_btn", use_container_width=True)

    if suggestions:
        tab.caption("Sugestões (Ibovespa): " + ", ".join(suggestions[:20]) + "...")

    if add_clicked:
        raw = ticker_input.strip()
        if not raw:
            tab.warning("Digite o código da ação antes de adicionar.")
        else:
            ticker = normalize_ticker(raw)
            if ticker in st.session_state.portfolio_tickers:
                tab.info(f"**{ticker}** já está na carteira.")
            else:
                df = load_data(ticker, period=period, interval=interval)
                if df is None or df.empty:
                    tab.error(
                        f"Não foi possível encontrar dados para **{ticker}**. Verifique o código.",
                        icon="🚨",
                    )
                else:
                    vol = annualized_volatility_from_prices(df["Close"])
                    st.session_state.portfolio_volatilities[ticker] = vol.values[0]
                    st.session_state.portfolio_tickers.append(ticker)

    if st.session_state.portfolio_tickers:
        tab.markdown("**Ativos na carteira:**")
        for t in list(st.session_state.portfolio_tickers):
            col_ticker, col_vol, col_remove = tab.columns([2, 2, 1])
            vol = st.session_state.portfolio_volatilities.get(t, "N/A")
            col_ticker.write(t)
            col_vol.write(f"Volatilidade: {vol}%")
            if col_remove.button("✕", key=f"remove_{t}", help=f"Remover {t}"):
                st.session_state.portfolio_tickers.remove(t)
                st.session_state.portfolio_volatilities.pop(t, None)
                st.rerun()

        if tab.button("Limpar carteira", key="portfolio_clear"):
            st.session_state.portfolio_tickers = []
            st.session_state.portfolio_volatilities = {}
            st.rerun()

    return list(st.session_state.portfolio_tickers)
