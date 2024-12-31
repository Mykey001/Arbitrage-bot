import os
from binance.client import Client as BinanceClient
from bybit import bybit
from okx import Account

# Load API keys from environment variables
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET_KEY = os.getenv("BYBIT_SECRET_KEY")

OKX_API_KEY = os.getenv("OKX_API_KEY")
OKX_SECRET_KEY = os.getenv("OKX_SECRET_KEY")
OKX_PASSPHRASE = os.getenv("OKX_PASSPHRASE")

# Binance setup
def binance_balance_and_trade():
    binance_client = BinanceClient(BINANCE_API_KEY, BINANCE_SECRET_KEY)
    
    # Fetch account balance
    balance = binance_client.get_account()
    print("Binance Balances:", balance['balances'])

    # Place a trade example: Buy 0.01 BTC with USDT
    try:
        order = binance_client.create_order(
            symbol='BTCUSDT',
            side='BUY',
            type='MARKET',
            quantity=0.01
        )
        print("Binance Trade Executed:", order)
    except Exception as e:
        print("Binance Trade Error:", e)

# Bybit setup
def bybit_balance_and_trade():
    bybit_client = bybit(test=False, api_key=BYBIT_API_KEY, api_secret=BYBIT_SECRET_KEY)
    
    # Fetch account balance
    balance = bybit_client.Wallet.Wallet_getBalance(coin="USDT").result()
    print("Bybit Balance:", balance)

    # Place a trade example: Buy 0.01 BTC
    try:
        order = bybit_client.LinearOrder.LinearOrder_new(
            symbol='BTCUSDT',
            side='Buy',
            order_type='Market',
            qty=0.01,
            time_in_force='GoodTillCancel'
        ).result()
        print("Bybit Trade Executed:", order)
    except Exception as e:
        print("Bybit Trade Error:", e)

# OKX setup
def okx_balance_and_trade():
    okx_client = Account(api_key=OKX_API_KEY, api_secret=OKX_SECRET_KEY, passphrase=OKX_PASSPHRASE)
    
    # Fetch account balance
    balance = okx_client.get_account_balance()
    print("OKX Balances:", balance)

    # Place a trade example: Buy 0.01 BTC with USDT
    try:
        # OKX trading code here
        print("OKX Trade Executed: [Implement trade logic]")
    except Exception as e:
        print("OKX Trade Error:", e)

# Main function to execute
def main():
    print("Fetching Binance Balance and Trading...")
    binance_balance_and_trade()

    print("Fetching Bybit Balance and Trading...")
    bybit_balance_and_trade()

    print("Fetching OKX Balance and Trading...")
    okx_balance_and_trade()

if __name__ == "__main__":
    main()
