import re

def update_main():
    file_path = r"c:\Users\HMA\Documents\Antigravity\Publicacion Web Consultora Maldonado\main.py"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update EXA Query
    old_query = '"query": "Noticias económicas Bolivia reservas escasez de dólares inflación site:bcb.gob.bo",'
    new_query = '"query": "Noticias económicas Bolivia reservas inflación tipo de cambio oficial ponderado flexible bcb",'
    content = content.replace(old_query, new_query)

    # Update Prompt for strict exchange rate rule
    old_rule = "Tu objetivo es analizar rigurosamente estos datos y generar una respuesta con DOS PARTES. REGLA ESTRICTA: El tipo de cambio oficial extráelo de las noticias del BCB (o asume el variable actual). El tipo de cambio paralelo DEBE ser EXACTAMENTE el valor de Binance P2P ({binance_p2p_rate}). Calcula la brecha matemática. Si la brecha > 50%, el riesgo DEBE ser RIESGO ALTO o CRÍTICO."
    new_rule = "Tu objetivo es analizar rigurosamente estos datos y generar una respuesta con DOS PARTES. REGLA ESTRICTA ANTI-ALUCINACIÓN: Bolivia implementó un régimen cambiario flexible; el tipo de cambio oficial hoy ronda los 11.58 BOB/USD. ¡QUEDA ESTRICTAMENTE PROHIBIDO usar o mencionar el tipo de cambio histórico de 6.86 / 6.96! Extrae el tipo de cambio oficial real actual de las noticias provistas. El tipo de cambio paralelo DEBE ser EXACTAMENTE el valor de Binance P2P ({binance_p2p_rate}). Calcula la brecha matemática entre ambos."
    content = content.replace(old_rule, new_rule)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated main.py")

if __name__ == "__main__":
    update_main()
