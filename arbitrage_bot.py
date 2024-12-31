import os
from dotenv import load_dotenv
import ccxt
import logging
from apscheduler.schedulers.background import BackgroundScheduler

# Load environment variables
load_dotenv()

# Initialize exchanges
okx = ccxt.okx({
    'apiKey': os.getenv('OKX_API_KEY'),
    'secret': os.getenv('OKX_SECRET'),
})

bybit = ccxt.bybit({
    'apiKey': os.getenv('BYBIT_API_KEY'),
    'secret': os.getenv('BYBIT_SECRET'),
})

coinbase = ccxt.coinbase({
    'apiKey': os.getenv('COINBASE_API_KEY'),
    'secret': os.getenv('COINBASE_SECRET'),
})

# Configure logging
logging.basicConfig(filename='arbitrage_bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_prices():
    """Fetch ETH/USDT prices from the exchanges."""
    try:
        okx_price = okx.fetch_ticker('ETH/USDT')['last']
        bybit_price = bybit.fetch_ticker('ETH/USDT')['last']
        coinbase_price = coinbase.fetch_ticker('ETH/USDT')['last']
        logging.info(f"Prices fetched - OKX: {okx_price}, Bybit: {bybit_price}, Coinbase: {coinbase_price}")
        return okx_price, bybit_price, coinbase_price
    except Exception as e:
        logging.error(f"Error fetching prices: {e}")
        return str(e), str(e), str(e)

def fetch_balances():
    print('begining')
    """Fetch account balances from the exchanges."""
    try:
        print("begining of try catch block")
        # okx_balance = okx.fetch_balance()
        bybit_balance = bybit.fetch_balance()
        coinbase_balance = coinbase.fetch_balance()
        print("below bybit and coinbase fetch")
        print(bybit_balance['total'])
        print('hello world')

        # logging.info("OKX Balances: %s", okx_balance['total'])
        logging.info("Bybit Balances: %s", bybit_balance['total'])
        logging.info("Coinbase Balances: %s", coinbase_balance['total'])

        return {
            # "OKX": okx_balance['total'],
            "Bybit": bybit_balance['total'],
            "Coinbase": coinbase_balance['total'],
        }
    except Exception as e:
        logging.error(f"Error fetching balances: {e}")
        return str(e), "error"


print(fetch_balances())



# def scheduled_task():
#     """Perform scheduled tasks like checking arbitrage opportunities and fetching balances."""
#     prices = fetch_prices()
#     balances = fetch_balances()
#     logging.info(f"Prices: {prices}")
#     logging.info(f"Balances: {balances}")

# # Start the scheduler
# scheduler = BackgroundScheduler()
# scheduler.add_job(scheduled_task, 'interval', minutes=1)  # Check every minute
# scheduler.start()

# # Keep the script running
# try:
#     while True:
#         pass
# except (KeyboardInterrupt, SystemExit):
#     scheduler.shutdown()


