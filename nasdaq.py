import requests

# For some reason this api works with these headers enabled
HEADERS = {
    "User-Agent": "PostmanRuntime/7.43.0"
}

"""
    Fetches market overview data from NASDAQ API and returns it as a list. [{
            "symbol": "Symbol",
            "name": "Name",
            "lastsale": "Last Sale",
            "netchange": "Net Change",
            "pctchange": "% Change",
            "marketCap": "Market Cap",
            "country": "Country",
            "ipoyear": "IPO Year",
            "volume": "Volume",
            "sector": "Sector",
            "industry": "Industry",
            "url": "Url"
            }]
        """
def market_overview() -> dict:
    return requests.get("https://api.nasdaq.com/api/screener/stocks?tableonly=true&offset=0&download=true", headers=HEADERS).json().get("data").get("rows")