import yfinance as yf
from django.http import JsonResponse
from datetime import datetime, timedelta
from .utils import calcular_rendimiento_real, obtener_rendimiento_yahoo


# Fixed parameters
RENDIMIENTO_PROMEDIO_AFORE = 0.065  # 6.5% per annum net historical
COMISION_AFORE = 0.009
COMISION_VANGUARD = 0.002
ISR_INVERSION = 0.20
ISR_AFORE = 0.0 #If kept till retirement is cero

# Function for calculating net yield
def calcular_rendimiento_real(monto_inicial, tasa_bruta, anios, comision_anual, tasa_isr):
    monto = monto_inicial
    for _ in range(anios):
        monto *= (1 + tasa_bruta)
        monto *= (1 - comision_anual)
    ganancia = monto - monto_inicial
    ganancia_neta = ganancia * (1 - tasa_isr)
    return round(monto_inicial + ganancia_neta, 2)

# Function for calculating net yield with Yahoo Finance
def obtener_rendimiento_yahoo(ticker, anios):
    hoy = datetime.now()
    inicio = hoy - timedelta(days=anios * 365)

    data = yf.download(ticker, start=inicio.strftime('%Y-%m-%d'), end=hoy.strftime('%Y-%m-%d'), progress=False)

    if data.empty:
        return None

    precio_inicio = data["Adj Close"].iloc[0]
    precio_fin = data["Adj Close"].iloc[-1]

    tasa_total = (precio_fin / precio_inicio) - 1
    tasa_anual = (1 + tasa_total) ** (1 / anios) - 1
    return tasa_anual

# Main view
def comparar_inversion(request):
    try:
        monto = float(request.GET.get('monto', 10000))
        anios = int(request.GET.get('anios', 10))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Parámetros inválidos. Usa ?monto=10000&anios=10"})

    resultados = {}

    # AFORE (fixed value)
    resultados["AFORE (promedio histórico)"] = calcular_rendimiento_real(
        monto, RENDIMIENTO_PROMEDIO_AFORE, anios, COMISION_AFORE, ISR_AFORE
    )

    # Yahoo Finance tickers
    tickers = {
        "SP500": "^GSPC",
        "NASDAQ": "^IXIC",
        "APPLE": "AAPL",
        'AMAZON': 'AMZN',
        'GOOGLE': 'GOOGL',
        'META': 'META',
        'NETFLIX': 'NFLX'
    }

    for nombre, ticker in tickers.items():
        tasa = obtener_rendimiento_yahoo(ticker, anios)
        if tasa is None:
            resultados[nombre] = "Error al obtener datos"
        else:
            resultados[nombre] = calcular_rendimiento_real(
                monto, tasa, anios, COMISION_VANGUARD, ISR_INVERSION
            )

    return JsonResponse(resultados)
