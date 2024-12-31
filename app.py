from flask import Flask, render_template, jsonify
import ccxt
from urllib3 import HTTPResponse


app = Flask(__name__)

# Initialize exchanges
okx = ccxt.okx({
    'apiKey': 'CEF2FC90397F22D5BEDC1C7ED2B3E349',
    'secret': '18678ce7-33f9-44c2-9be2-1d7e55377fba',
})

bybit = ccxt.bybit({
    'apiKey': 'Opc7smRQyAOHZ6nnSQ',
    'secret': 'CpbQOCTNlshoTIHSKUiFWBJjxTPRFJUnme43',
})

coinbase = ccxt.coinbase({
    'apiKey': 'organizations/62059b1e-7757-4d20-9d5f-62a228594945/apiKeys/ef287208-6c3b-48a9-aa4d-d63433ecd327',
    'secret': '-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIMNK3j6o2HffRCwk6ZBWUbVqdOmsy82h8XPsxdFyWge6oAoGCCqGSM49\nAwEHoUQDQgAEOuRpZhk2/5peJ5Gg3cCfTQcPB5XkstbKk/IoCYl7n1/A+xsN0uOB\nmr91tfoWC7pSJ7Mv2lya3E9IgG+zyg6HCQ==\n-----END EC PRIVATE KEY-----\n',
})

def fetch_prices():
    try:
        okx_price = okx.fetch_ticker('ETH/USDT')['last']
        bybit_price = bybit.fetch_ticker('ETH/USDT')['last']
        coinbase_price = coinbase.fetch_ticker('ETH/USDT')['last']
        return okx_price, bybit_price, coinbase_price
    except Exception as e:
        return str(e), str(e), str(e)

def check_arbitrage_opportunity():
    okx_price, bybit_price, coinbase_price = fetch_prices()
    if isinstance(okx_price, str) or isinstance(bybit_price, str) or isinstance(coinbase_price, str):
        return "Error fetching prices."

    opportunities = []
    if okx_price < bybit_price:
        opportunities.append("Buy on OKX, Sell on Bybit")
    if okx_price < coinbase_price:
        opportunities.append("Buy on OKX, Sell on Coinbase Pro")
    if bybit_price < okx_price:
        opportunities.append("Buy on Bybit, Sell on OKX")
    if bybit_price < coinbase_price:
        opportunities.append("Buy on Bybit, Sell on Coinbase Pro")
    if coinbase_price < okx_price:
        opportunities.append("Buy on Coinbase Pro, Sell on OKX")
    if coinbase_price < bybit_price:
        opportunities.append("Buy on Coinbase Pro, Sell on Bybit")

    if opportunities:
        return "Arbitrage Opportunities: " + "; ".join(opportunities)
    else:
        return "No arbitrage opportunity found."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prices', methods=['GET'])
def prices():
    okx_price, bybit_price, coinbase_price = fetch_prices()
    return jsonify({
        'okx_price': okx_price,
        'bybit_price': bybit_price,
        'coinbase_price': coinbase_price
    })

@app.route('/arbitrage', methods=['GET'])
def arbitrage():
    message = check_arbitrage_opportunity()
    print(message)
    return render_template('arbitrage.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
 





#ARBITRAGE BOT



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
    """Fetch account balances from the exchanges."""
    try:
        okx_balance = okx.fetch_balance()
        bybit_balance = bybit.fetch_balance()
        coinbase_balance = coinbase.fetch_balance()

        logging.info("OKX Balances: %s", okx_balance['total'])
        logging.info("Bybit Balances: %s", bybit_balance['total'])
        logging.info("Coinbase Balances: %s", coinbase_balance['total'])

        print(okx_balance)

        return {
            "OKX": okx_balance['total'],
            "Bybit": bybit_balance['total'],
            "Coinbase": coinbase_balance['total'],
        }
    except Exception as e:
        logging.error(f"Error fetching balances: {e}")
        return str(e)

def scheduled_task():
    """Perform scheduled tasks like checking arbitrage opportunities and fetching balances."""
    prices = fetch_prices()
    balances = fetch_balances()
    logging.info(f"Prices: {prices}")
    logging.info(f"Balances: {balances}")

# Start the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'interval', minutes=1)  # Check every minute
scheduler.start()

# Keep the script running
try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
