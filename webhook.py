import requests
import json

WEBHOOK_URL = "https://discord.com/api/webhooks/1338715281324904489/IjKApLuEqk6OoxH7Lz2cp71HiF7-0hC0vSUwgmplF1J8NSkIqoBJnEMg8WnAq0JjiV2l"
def send_discord_alert(company_data:dict, rsi:float):
    print(company_data)
    """
    Sends a formatted message to a Discord webhook with stock RSI data.
    """
    price = float(company_data.get('lastsale').replace("$", ""))
    pct_change = float(company_data.get('pctchange').replace("%", ""))
    volume = float(company_data.get('volume'))
    symbol = str(company_data.get('symbol'))
    message = {
        "embeds": [
            {
                "title": f"📈 Stock Alert: {symbol}",
                "color": 0x3498db if rsi > 70 else 0xe74c3c if rsi < 30 else 0x2ecc71,  # Blue for overbought, Red for oversold, Green otherwise
                "fields": [
                    {"name": "💰 Current Price", "value": f"${price:.2f}", "inline": True},
                    {"name": "⛷️% change", "value": f"${pct_change:.2f}", "inline": True},
                    {"name": "📊 RSI Value", "value": f"{rsi:.2f}", "inline": True},
                    {"name": "📉 Volume", "value": f"{volume:.2f}", "inline": True}
                ],
                "footer": {"text": "Stay informed!"}
            }
        ]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(WEBHOOK_URL, data=json.dumps(message), headers=headers)
    
    if response.status_code == 204:
        print(f"✅ Alert sent for {symbol}")
    else:
        print(f"❌ Failed to send alert: {response.text}")

# Example usage:
# send_discord_alert("AAPL", 72.5, 182.34, 5.67)

def send_message(message:str):
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data = {
        "content" : message,
        "username" : "custom username"
    }

    # leave this out if you dont want an embed
    # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"] = [
        {
            "description" : "text in embed",
            "title" : "embed title"
        }
    ]

    result = requests.post(WEBHOOK_URL, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print(f"Payload delivered successfully, code {result.status_code}.")