import requests

def get_top(screener_Id):
    url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
    params = {"scrIds": screener_Id, "count": 250}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, params=params, headers=headers)
        data = res.json()
        results = data.get("finance", {}).get("result", [])
        quotes = results[0].get("quotes", [])
        return [{"symbol": q["symbol"], "name": q.get("shortName", "N/A")} for q in quotes]
    except Exception as e:
        print("Error fetching data:", e)
        return []
