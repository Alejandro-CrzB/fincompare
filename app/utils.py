# comparador
import yfinance as yf
from datetime import datetime, timedelta

def calcular_rendimiento_real(monto_inicial, tasa_bruta, anios, comision_anual, tasa_isr):
    monto = monto_inicial
    for _ in range(anios):
        monto *= (1 + tasa_bruta)
        monto *= (1 - comision_anual)
    ganancia = monto - monto_inicial
    ganancia_neta = ganancia * (1 - tasa_isr)
    return round(monto_inicial + ganancia_neta, 2)

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
