import os
import datetime
from PIL import Image, ImageDraw, ImageFont

def get_system_font(font_names, size):
    """Intenta cargar fuentes del sistema Windows/Linux con fallback a la fuente básica de PIL."""
    possible_dirs = [
        "C:\\Windows\\Fonts",
        "C:\\WINNT\\Fonts",
        "/usr/share/fonts",
        "/usr/local/share/fonts",
        "/usr/share/fonts/truetype"
    ]
    
    for font_name in font_names:
        for font_dir in possible_dirs:
            font_path = os.path.join(font_dir, font_name)
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except Exception:
                    continue
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            continue
            
    return ImageFont.load_default()

def generate_infographic_card(data, output_path="docs/assets/infografia-latest.png"):
    """
    Genera una infografía ejecutiva de alta resolución (1200x675 px)
    con la identidad visual de Consultora Maldonado.
    """
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    
    width = 1200
    height = 675
    
    # 1. Crear lienzo con degradado de fondo (Navy Blue Profundo)
    img = Image.new("RGB", (width, height), color="#091a2b")
    draw = ImageDraw.Draw(img)
    
    # Dibujar degradado sutil de fondo
    for y in range(height):
        ratio = y / height
        r = int(9 * (1 - ratio) + 13 * ratio)
        g = int(26 * (1 - ratio) + 43 * ratio)
        b = int(43 * (1 - ratio) + 74 * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    # Marco / Borde exterior sutil
    draw.rounded_rectangle([(20, 20), (width - 20, height - 20)], radius=20, outline="#1d3b5e", width=2)
    
    # Cargar tipografías
    font_badge = get_system_font(["seguisb.ttf", "segoeuib.ttf", "arialbd.ttf", "arial.ttf"], 15)
    font_title = get_system_font(["segoeuib.ttf", "arialbd.ttf", "trebucbd.ttf", "arial.ttf"], 36)
    font_subtitle = get_system_font(["segoeui.ttf", "arial.ttf", "calibri.ttf"], 18)
    font_card_title = get_system_font(["seguisb.ttf", "segoeuib.ttf", "arialbd.ttf", "arial.ttf"], 16)
    font_kpi_value = get_system_font(["segoeuib.ttf", "arialbd.ttf", "calibrib.ttf", "arial.ttf"], 38)
    font_kpi_sub = get_system_font(["segoeui.ttf", "arial.ttf", "calibri.ttf"], 15)
    font_alert_text = get_system_font(["segoeui.ttf", "arial.ttf", "calibri.ttf"], 16)
    font_footer = get_system_font(["segoeui.ttf", "arial.ttf", "calibri.ttf"], 14)
    
    # --- CABECERA ---
    # Badge superior de Consultora Maldonado
    draw.rounded_rectangle([(50, 45), (280, 75)], radius=6, fill="#0d2b45", outline="#204a6e")
    draw.text((62, 52), "CONSULTORA MALDONADO", font=font_badge, fill="#38bdf8")
    
    # Título Principal
    draw.text((50, 88), "RESUMEN EJECUTIVO: MACROECONOMÍA BOLIVIA", font=font_title, fill="#ffffff")
    
    # Fecha y subtítulo
    fecha_str = data.get("fecha", datetime.datetime.now().strftime("%d de %B de %Y"))
    draw.text((50, 134), f"Informe Financiero y Estratégico • {fecha_str}", font=font_subtitle, fill="#94a3b8")
    
    # Badge de Nivel de Riesgo (Esquina Superior Derecha)
    riesgo_info = data.get("riesgo_general", {})
    nivel_riesgo = riesgo_info.get("nivel", "Alto").upper()
    color_riesgo = riesgo_info.get("color", "amber").lower()
    
    badge_bg = "#dc2626" if "crit" in color_riesgo or "red" in color_riesgo else (
        "#d97706" if "alt" in color_riesgo or "amb" in color_riesgo or "amar" in color_riesgo else "#16a34a"
    )
    badge_border = "#ef4444" if "crit" in color_riesgo or "red" in color_riesgo else (
        "#f59e0b" if "alt" in color_riesgo or "amb" in color_riesgo or "amar" in color_riesgo else "#22c55e"
    )
    
    draw.rounded_rectangle([(width - 310, 45), (width - 50, 95)], radius=10, fill=badge_bg, outline=badge_border, width=2)
    draw.text((width - 290, 58), f"RIESGO: {nivel_riesgo}", font=font_badge, fill="#ffffff")
    
    # Separador horizontal
    draw.line([(50, 170), (width - 50, 170)], fill="#1d3b5e", width=1)
    
    # --- 3 TARJETAS DE KPIS PRINCIPALES ---
    kpis = data.get("kpis", {})
    card_width = 345
    card_height = 240
    card_y = 190
    card_xs = [50, 427, 805]
    
    cards_data = [
        {
            "tag": "LIQUIDEZ & RESERVAS",
            "title": "Reservas Netas (RIN)",
            "main_val": kpis.get("rin_total_usd", "$1,980 M"),
            "main_color": "#38bdf8",
            "details": [
                f"• Oro: {kpis.get('rin_oro_usd', '$1,820 M')} ({kpis.get('rin_oro_pct', '92%')})",
                f"• Divisas: {kpis.get('rin_divisas_usd', '$160 M')} ({kpis.get('rin_divisas_pct', '8%')})",
                f"• Var. Mensual: {kpis.get('rin_variacion', '+2.3%')}"
            ],
            "accent": "#0284c7"
        },
        {
            "tag": "MERCADO CAMBIARIO",
            "title": "Brecha y Divisas",
            "main_val": kpis.get("brecha_cambiaria_pct", "+58.0%"),
            "main_color": "#f59e0b",
            "details": [
                f"• Oficial: {kpis.get('tipo_cambio_oficial', '6.86 / 6.96 BOB')}",
                f"• Paralelo / USDT: {kpis.get('tipo_cambio_paralelo', '11.00 BOB')}",
                f"• Giros Ext: {kpis.get('comision_giros_exterior', '18% - 25%')}"
            ],
            "accent": "#d97706"
        },
        {
            "tag": "PRECIOS & COMERCIO",
            "title": "Inflación y Balanza",
            "main_val": kpis.get("inflacion_mensual", "0.65%") + " IPC",
            "main_color": "#34d399",
            "details": [
                f"• IPC Acumulado 12M: {kpis.get('inflacion_acumulada', '6.8%')}",
                f"• Balanza Com.: {kpis.get('balanza_comercial', '-$320 M')}",
                f"• Tasa Activa: {kpis.get('tasa_activa_promedio', '7.8%')}"
            ],
            "accent": "#059669"
        }
    ]
    
    for i, card in enumerate(cards_data):
        cx = card_xs[i]
        # Fondo de la tarjeta
        draw.rounded_rectangle([(cx, card_y), (cx + card_width, card_y + card_height)], radius=14, fill="#0d2438", outline="#1e3a58", width=1)
        # Barra de acento superior
        draw.rounded_rectangle([(cx, card_y), (cx + card_width, card_y + 6)], radius=3, fill=card["accent"])
        
        # Etiqueta de la tarjeta
        draw.text((cx + 20, card_y + 18), card["tag"], font=font_badge, fill="#64748b")
        # Título
        draw.text((cx + 20, card_y + 38), card["title"], font=font_card_title, fill="#e2e8f0")
        # Valor Principal
        draw.text((cx + 20, card_y + 70), card["main_val"], font=font_kpi_value, fill=card["main_color"])
        
        # Línea divisoria interna
        draw.line([(cx + 20, card_y + 130), (cx + card_width - 20, card_y + 130)], fill="#16324f", width=1)
        
        # Lista de detalles
        det_y = card_y + 142
        for det in card["details"]:
            draw.text((cx + 20, det_y), det, font=font_kpi_sub, fill="#94a3b8")
            det_y += 26

    # --- BLOQUE INFERIOR: ALERTA EJECUTIVA / TL;DR ---
    alert_box_y = 450
    alert_box_h = 145
    draw.rounded_rectangle([(50, alert_box_y), (width - 50, alert_box_y + alert_box_h)], radius=12, fill="#0a2136", outline="#1d3b5e", width=1)
    
    # Badge de Alerta
    draw.rounded_rectangle([(70, alert_box_y + 16), (230, alert_box_y + 44)], radius=6, fill="#1e3852")
    draw.text((82, alert_box_y + 22), "• SÍNTESIS DIRECTIVA", font=font_badge, fill="#fbbf24")
    
    alerta_principal = riesgo_info.get("alerta_principal", "Presión en la liquidez de divisas y brecha en mercado paralelo.")
    accion_sugerida = riesgo_info.get("accion_recomendada", "Calcular costos operativos con tipo de cambio de reposición.")
    
    # Truncar si es muy largo para que no se desborde
    if len(alerta_principal) > 130:
        alerta_principal = alerta_principal[:127] + "..."
    if len(accion_sugerida) > 130:
        accion_sugerida = accion_sugerida[:127] + "..."
        
    draw.text((70, alert_box_y + 58), f"• Diagnóstico: {alerta_principal}", font=font_alert_text, fill="#e2e8f0")
    draw.text((70, alert_box_y + 92), f"• Acción: {accion_sugerida}", font=font_alert_text, fill="#38bdf8")
    
    # --- PIE DE PÁGINA ---
    footer_y = 615
    draw.text((50, footer_y), "Consultora Maldonado • www.consultoramaldonado.com", font=font_footer, fill="#64748b")
    draw.text((width - 450, footer_y), "Fuente: BCB, INE, ASFI, MEFP, ASOBAN • Confidencial", font=font_footer, fill="#64748b")
    
    # Guardar imagen
    img.save(output_path, "PNG", quality=95)
    print(f"[+] Infografía ejecutiva generada exitosamente en: {output_path}")
    return output_path

if __name__ == "__main__":
    # Test básico de generación
    sample_data = {
        "fecha": "16 de agosto de 2026",
        "riesgo_general": {
            "nivel": "Alto",
            "color": "amber",
            "alerta_principal": "Brecha cambiaria en mercado paralelo/USDT supera el 50% con reservas líquidas en niveles de vigilancia.",
            "accion_recomendada": "Calcular costos operativos con tipo de cambio de reposición y escalonar compromisos en divisas."
        },
        "kpis": {
            "rin_total_usd": "$1,980 M",
            "rin_oro_usd": "$1,820 M",
            "rin_oro_pct": "92%",
            "rin_divisas_usd": "$160 M",
            "rin_divisas_pct": "8%",
            "rin_variacion": "+2.3%",
            "tipo_cambio_oficial": "6.86 / 6.96 BOB",
            "tipo_cambio_paralelo": "11.00 BOB/USDT",
            "brecha_cambiaria_pct": "+58.0%",
            "balanza_comercial": "-$320 M",
            "inflacion_mensual": "0.65%",
            "inflacion_acumulada": "6.8%",
            "tasa_activa_promedio": "7.8%",
            "comision_giros_exterior": "18% - 25%"
        }
    }
    generate_infographic_card(sample_data, "test_infografia.png")
