import yfinance as yf
import pandas as pd

def extraer_datos_limpios(fecha_fin="2026-03-11"):
    ticker_symbol = "XRP-USD"
    print(f"Descargando {ticker_symbol} de forma limpia...")

    # 1. Descarga normal
    df = yf.download(ticker_symbol, period="max", end=fecha_fin, actions=True)

    # 2. CORRECCIÓN: Si el DataFrame tiene columnas multinivel, las aplanamos
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # 3. Limpieza de nombres de columnas
    # Esto elimina espacios extraños y asegura que 'Date' sea una columna
    df = df.reset_index()
    
    # 4. Eliminar cualquier fila que sea totalmente nula o contenga nombres de columnas repetidos
    df = df.dropna(subset=['Close']) 

    # 5. Agregar metadatos básicos como columnas simples
    df['Ticker'] = ticker_symbol
    df['Currency'] = "USD"

    # Reordenar para que sea legible
    cols = ['Date', 'Ticker', 'Currency', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = df[cols]

    # 6. Guardar sin el índice de pandas para evitar columnas 'Unnamed: 0'
    nombre_archivo = "XRP_Data_Limpia.csv"
    df.to_csv(nombre_archivo, index=False)
    
    print(f"Archivo guardado exitosamente: {nombre_archivo}")
    print(df.head())

if __name__ == "__main__":
    extraer_datos_limpios()