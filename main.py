import requests
import datetime
from bs4 import BeautifulSoup

BOT_TOKEN = "7741253350:AAHljqj2LoSRRTSgc1HZeWQKUPiCpLi9hK8"
CHAT_ID = "394927619"

NSE_STOCKS = {
    "Reliance": "RELIANCE",
    "TCS": "TCS",
    "Infosys": "INFY",
    "HDFC Bank": "HDFCBANK",
    "ICICI Bank": "ICICIBANK",
    "SBIN": "SBIN",
    "ONGC": "ONGC",
    "Tata Motors": "TATAMOTORS"
}

MCX_COMMODITIES = {
    "Gold": "gold",
    "Silver": "silver",
    "Crude Oil": "crudeoil",
    "Natural Gas": "naturalgas"
}

def get_price(symbol):
    try:
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)
        response = session.get(url, headers=headers)
        data = response.json()
        return data['priceInfo']['lastPrice']
    except:
        return "N/A"

def get_nifty_spot():
    try:
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)
        response = session.get(url, headers=headers)
        data = response.json()
        spot_price = data["records"]["underlyingValue"]
        return round(spot_price, 2)
    except:
        return "N/A"

def get_mcx_price(symbol):
    # Placeholder (normally you'd need an API like mcxindia.com or commodity API)
    fake_prices = {
        "gold": "71650",
        "silver": "92000",
        "crudeoil": "6870",
        "naturalgas": "227"
    }
    return fake_prices.get(symbol.lower(), "N/A")

def get_news():
    try:
        url = "https://news.google.com/search?q=Nifty%20stock%20market%20India&hl=en-IN&gl=IN&ceid=IN:en"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        headlines = soup.select("article h3")[:3]
        news_list = [f"🗞 {h.get_text()}" for h in headlines]
        return "\n".join(news_list)
    except:
        return "🛑 Unable to fetch news"

def create_message():
    today = datetime.datetime.now().strftime("%d %b %Y (%A)")
    msg = f"📢 *MARKET REPORT – {today}*\n"
    msg += "⚠️ *High Sensitivity: Global cues | FII flows | Commodity trends*\n\n"

    msg += f"📈 *Nifty Spot:* ₹{get_nifty_spot()}\n\n"
    msg += "*📊 NSE Stocks:*\n"
    msg += "`{:<15} {:>10}`\n".format("Stock", "Price")
    msg += "`{:<15} {:>10}`\n".format("─" * 15, "─" * 10)
    for name, symbol in NSE_STOCKS.items():
        price = get_price(symbol)
        msg += "`{:<15} {:>10}`\n".format(name, str(price))

    msg += "\n🛢 *MCX Commodities:*\n"
    msg += "`{:<15} {:>10}`\n".format("Commodity", "Price")
    msg += "`{:<15} {:>10}`\n".format("─" * 15, "─" * 10)
    for name, key in MCX_COMMODITIES.items():
        price = get_mcx_price(key)
        msg += "`{:<15} {:>10}`\n".format(name, price)

    msg += "\n📰 *Top Market News:*\n"
    msg += get_news()
    msg += "\n\n📌 *Strategy:* Use 15-min chart | Trail SL | Watch macro news"

    return msg

def send_alert():
    msg = create_message()
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    send_alert()
