import yfinance as yf
from django.http import JsonResponse

def compare_returns(request):
    amount = float(request.GET.get('amount', 10000))
    years = int(request.GET.get('years', 5))

    tickers = {
        'AFORE': 0.05,
        'SP500': '^GSPC',
        'NASDAQ': '^IXIC',
        'DOWJONES': '^DJI',
        'APPLE': 'AAPL',
        'AMAZON': 'AMZN',
        'GOOGLE': 'GOOGL',
        'META': 'META',
        'NETFLIX': 'NFLX'
    }

    results = {}

    for key, val in tickers.items():
        if key == 'AFORE':
            future_value = amount * ((1 + val) ** years)
        else:
            data = yf.Ticker(val).history(period=f"{years}y")
            if len(data) == 0:
                continue
            start_price = data['Close'][0]
            end_price = data['Close'][-1]
            rate = (end_price - start_price) / start_price
            future_value = amount * (1 + rate)

        results[key] = round(future_value, 2)

    return JsonResponse(results)
