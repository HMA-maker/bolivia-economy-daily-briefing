import json
import re
import html

def get_risk_colors(risk_level):
    level = str(risk_level).lower()
    if "crit" in level or "rojo" in level or "red" in level:
        return {
            "bg": "#fef2f2",
            "border": "#ef4444",
            "text": "#991b1b",
            "badge_bg": "#dc2626",
            "badge_text": "#ffffff",
            "icon": "🔴",
            "label": "RIESGO CRÍTICO"
        }
    elif "alt" in level or "amber" in level or "amar" in level:
        return {
            "bg": "#fffbeb",
            "border": "#f59e0b",
            "text": "#92400e",
            "badge_bg": "#d97706",
            "badge_text": "#ffffff",
            "icon": "🟡",
            "label": "RIESGO ALTO"
        }
    else:
        return {
            "bg": "#f0fdf4",
            "border": "#22c55e",
            "text": "#166534",
            "badge_bg": "#16a34a",
            "badge_text": "#ffffff",
            "icon": "🟢",
            "label": "RIESGO MODERADO"
        }

def format_markdown_body_to_html(markdown_content):
    """Convierte el cuerpo en markdown a bloques HTML limpios y semánticos."""
    if not markdown_content:
        return ""
        
    html_blocks = []
    # Normalizar saltos de línea
    paragraphs = markdown_content.replace("\r\n", "\n").split("\n\n")
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
            
        if p.startswith("# "):
            # Título 1 principal (se maneja en el hero, pero por si acaso)
            html_blocks.append(f"<h2 class='section-title-h1'>{html.escape(p[2:].strip())}</h2>")
        elif p.startswith("## "):
            title_text = p[3:].strip()
            html_blocks.append(f"<h2 class='section-title'>{html.escape(title_text)}</h2>")
        elif p.startswith("### "):
            title_text = p[4:].strip()
            html_blocks.append(f"<h3 class='subsection-title'>{html.escape(title_text)}</h3>")
        elif p.startswith("#### "):
            title_text = p[5:].strip()
            html_blocks.append(f"<h4 class='card-title-h4'>{html.escape(title_text)}</h4>")
        elif p.startswith("---"):
            html_blocks.append("<hr class='content-divider' />")
        elif p.startswith("- ") or p.startswith("* "):
            items = []
            for line in p.split("\n"):
                line_s = line.strip()
                if line_s.startswith("- ") or line_s.startswith("* "):
                    content = line_s[2:].strip()
                    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
                    items.append(f"<li>{content}</li>")
            html_blocks.append(f"<ul class='content-list'>{''.join(items)}</ul>")
        elif p.startswith(">"):
            # Blockquote
            clean_bq = p.replace(">", "").strip()
            clean_bq = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', clean_bq)
            html_blocks.append(f"<blockquote class='content-quote'>{clean_bq}</blockquote>")
        else:
            formatted_p = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p)
            formatted_p = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted_p)
            html_blocks.append(f"<p class='content-p'>{formatted_p}</p>")
            
    return "\n".join(html_blocks)

def generate_email_hook_html(data, image_url, web_report_url):
    """
    Genera la plantilla de correo electrónico optimizada (El Gancho)
    con CSS Inline 100% compatible con clientes de correo móviles y de escritorio.
    """
    fecha = data.get("fecha", "")
    preheader = data.get("preheader", "Resumen Ejecutivo de Macroeconomía Boliviana.")
    riesgo = data.get("riesgo_general", {})
    nivel_riesgo = riesgo.get("nivel", "Alto")
    colors = get_risk_colors(nivel_riesgo)
    alerta_principal = riesgo.get("alerta_principal", "")
    accion_recomendada = riesgo.get("accion_recomendada", "")
    
    kpis = data.get("kpis", {})
    tc_oficial = kpis.get("tipo_cambio_oficial", "6.86 / 6.96")
    tc_paralelo = kpis.get("tipo_cambio_paralelo", "11.00 BOB/USDT")
    
    bloques = data.get("bloques_resumidos", {})
    rin_txt = bloques.get("rin_divisas", "RIN estables concentradas en oro.")
    comercio_txt = bloques.get("comercio_exterior", "Déficit comercial persistente.")
    banca_txt = bloques.get("inflacion_banca", "Inflación con presión en importados.")

    # URL base para activos (usando el web_report_url si viene limpio, o asumiendo el dominio)
    base_assets_url = "https://informe.consultoramaldonado.com"
    logo_url = f"{base_assets_url}/assets/logo.png"

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🇧🇴 Resumen Ejecutivo: Macroeconomía de Bolivia — {fecha}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">
  
  <!-- PREHEADER OCULTO -->
  <div style="display:none; font-size:1px; color:#333333; line-height:1px; max-height:0px; max-width:0px; opacity:0; overflow:hidden;">
    {preheader}
  </div>

  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f1f5f9; padding: 20px 0;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 650px; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08); border: 1px solid #e2e8f0;">
          
          <!-- CABECERA INSTITUCIONAL (FONDO BLANCO, TEXTO OSCURO, DETALLES NARANJAS) -->
          <tr>
            <td style="background-color: #ffffff; padding: 24px 28px; text-align: left; border-bottom: 3px solid #E76F2D;">
              <table width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                  <td>
                    <!-- LOGO PLACEHOLDER: Sube tu logo a la carpeta assets/logo.png -->
                    <img src="{logo_url}" alt="Consultora Maldonado" style="max-height: 50px; margin-bottom: 15px; display: block;" />
                    <h1 style="color: #2d2d2d; margin: 0 0 4px 0; font-size: 21px; font-weight: 800; letter-spacing: -0.5px; line-height: 1.3;">🇧🇴 Resumen Ejecutivo: Macroeconomía de Bolivia</h1>
                    <p style="color: #64748b; margin: 0; font-size: 13px;">Fecha de análisis: {fecha}</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- CUERPO PRINCIPAL -->
          <tr>
            <td style="padding: 24px 28px;">

              <!-- 1. MATRIZ DE ALERTAS (TL;DR) -->
              <div style="background-color: {colors['bg']}; border-left: 4px solid {colors['border']}; border-radius: 8px; padding: 16px; margin-bottom: 24px;">
                <table width="100%" cellspacing="0" cellpadding="0" border="0">
                  <tr>
                    <td>
                      <span style="background-color: {colors['badge_bg']}; color: {colors['badge_text']}; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase;">
                        {colors['label']}
                      </span>
                      <p style="margin: 10px 0 6px 0; font-size: 14px; line-height: 1.5; color: #1e293b;">
                        <strong>🚨 Alerta Central:</strong> {alerta_principal}
                      </p>
                      <p style="margin: 0; font-size: 14px; line-height: 1.5; color: #2d2d2d;">
                        <strong>🎯 Acción Sugerida:</strong> {accion_recomendada}
                      </p>
                    </td>
                  </tr>
                </table>
              </div>

              <!-- 2. TABLERO DE INDICADORES CLAVE (HTML NATIVO) -->
              <h2 style="font-size: 16px; color: #2d2d2d; margin: 0 0 14px 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px;">
                📊 Tablero de Indicadores Clave
              </h2>

              <!-- Bloque 1: RIN y Divisas -->
              <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 16px; margin-bottom: 12px; border-left: 4px solid #E76F2D;">
                <div style="font-size: 14px; font-weight: bold; color: #E76F2D; margin-bottom: 4px;">
                  💰 1. Reservas Internacionales & Divisas
                </div>
                <div style="font-size: 13px; color: #334155; line-height: 1.5;">
                  {rin_txt}
                </div>
                <div style="font-size: 12px; color: #64748b; margin-top: 6px; padding-top: 6px; border-top: 1px dashed #cbd5e1;">
                  Oficial: <strong>{tc_oficial}</strong> | Paralelo/USDT: <strong>{tc_paralelo}</strong>
                </div>
              </div>

              <!-- Diseño a dos columnas para Comercio e Inflación -->
              <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-bottom: 20px;">
                <tr>
                  <!-- Bloque 2: Comercio Exterior -->
                  <td width="48%" valign="top" style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; border-left: 4px solid #0d3b66;">
                    <div style="font-size: 13px; font-weight: bold; color: #0d3b66; margin-bottom: 4px;">
                      🚢 2. Comercio Exterior
                    </div>
                    <div style="font-size: 12px; color: #334155; line-height: 1.4;">
                      {comercio_txt}
                    </div>
                  </td>
                  <td width="4%"></td> <!-- Espaciador -->
                  <!-- Bloque 3: Inflación y Banca -->
                  <td width="48%" valign="top" style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; border-left: 4px solid #059669;">
                    <div style="font-size: 13px; font-weight: bold; color: #059669; margin-bottom: 4px;">
                      🏦 3. Inflación y Banca
                    </div>
                    <div style="font-size: 12px; color: #334155; line-height: 1.4;">
                      {banca_txt}
                    </div>
                  </td>
                </tr>
              </table>

              <!-- 3. LLAMADA A LA ACCIÓN (BOTÓN PRINCIPAL ALTO CONTRASTE) -->
              <div style="text-align: center; margin: 28px 0 20px 0;">
                <a href="{web_report_url}" target="_blank" style="background-color: #E76F2D; color: #ffffff; text-decoration: none; padding: 16px 32px; border-radius: 8px; font-weight: bold; font-size: 15px; display: inline-block; box-shadow: 0 4px 14px rgba(231, 111, 45, 0.4); text-transform: uppercase; letter-spacing: 0.5px;">
                  Ver Informe Completo en la Web ↗
                </a>
                <p style="font-size: 12px; color: #64748b; margin: 10px 0 0 0;">
                  Incluye desglose de Bonos Soberanos, Finanzas Públicas e historial interactivo.
                </p>
              </div>

              <!-- 4. FUENTES CONSULTADAS -->
              <div style="border-top: 1px solid #e2e8f0; padding-top: 14px; margin-top: 20px; font-size: 11px; color: #64748b; line-height: 1.5;">
                <strong>📚 Fuentes de Consulta:</strong> Banco Central de Bolivia (BCB), Instituto Nacional de Estadística (INE), Autoridad de Supervisión del Sistema Financiero (ASFI), MEFP, ASOBAN e IBCE.
              </div>

            </td>
          </tr>

          <!-- PIE DE PÁGINA Y DESCARGO LEGAL -->
          <tr>
            <td style="background-color: #f8fafc; border-top: 1px solid #e2e8f0; padding: 18px 28px; text-align: center;">
              <p style="font-size: 11px; color: #94a3b8; margin: 0 0 8px 0; line-height: 1.4;">
                <strong>Descargo de Responsabilidad:</strong> La presente información no constituye asesoría profesional, legal, contable ni recomendación de inversión. Es un análisis informativo elaborado por Consultora Maldonado.
              </p>
              <p style="font-size: 11px; color: #64748b; margin: 0;">
                © {fecha.split()[-1] if len(fecha.split()) > 0 else '2026'} Consultora Maldonado • <a href="https://www.consultoramaldonado.com" style="color: #E76F2D; text-decoration: none; font-weight: bold;">www.consultoramaldonado.com</a>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

def generate_landing_page_html(data, markdown_content, archive_list=None, base_url="https://informe.consultoramaldonado.com", canonical_url=None):
    """
    Genera el HTML5 completo de la Landing Page diaria de alto rendimiento,
    optimizada para SEO, GEO (AI Citations), OpenGraph y lectura ejecutiva.
    """
    fecha = data.get("fecha", "")
    fecha_iso = data.get("fecha_iso", "")
    riesgo = data.get("riesgo_general", {})
    nivel_riesgo = riesgo.get("nivel", "Alto")
    colors = get_risk_colors(nivel_riesgo)
    alerta_principal = riesgo.get("alerta_principal", "")
    accion_recomendada = riesgo.get("accion_recomendada", "")
    
    kpis = data.get("kpis", {})
    rin_total = kpis.get("rin_total_usd", "$1,980 M")
    rin_oro = kpis.get("rin_oro_usd", "$1,820 M")
    rin_oro_pct = kpis.get("rin_oro_pct", "92%")
    rin_divisas = kpis.get("rin_divisas_usd", "$160 M")
    rin_divisas_pct = kpis.get("rin_divisas_pct", "8%")
    tc_oficial = kpis.get("tipo_cambio_oficial", "6.86 / 6.96")
    tc_paralelo = kpis.get("tipo_cambio_paralelo", "11.00 BOB/USDT")
    brecha = kpis.get("brecha_cambiaria_pct", "+58.0%")
    inflacion_m = kpis.get("inflacion_mensual", "0.65%")
    inflacion_a = kpis.get("inflacion_acumulada", "6.8%")
    balanza = kpis.get("balanza_comercial", "-$320 M")
    
    page_title = f"Resumen Ejecutivo: Macroeconomía de Bolivia — {fecha} | Consultora Maldonado"
    meta_desc = f"Informe ejecutivo diario de macroeconomía de Bolivia al {fecha}. Indicadores de RIN ({rin_total}), brecha cambiaria ({brecha}), inflación ({inflacion_m}) y análisis de riesgo financiero."
    
    if not canonical_url:
        canonical_url = f"{base_url}/"
        
    og_image_url = f"{base_url}/assets/infografia-latest.png"
    
    # Renderizar el cuerpo del informe
    rendered_body = format_markdown_body_to_html(markdown_content)
    
    # Generar opciones de archivo histórico
    archive_options_html = ""
    if archive_list:
        for item in archive_list:
            selected = "selected" if item.get("iso") == fecha_iso else ""
            archive_options_html += f'<option value="{item.get("url")}" {selected}>{item.get("date")}</option>\n'

    # Schema.org JSON-LD estructurado
    schema_json = {
        "@context": "https://schema.org",
        "@type": "FinancialNewsArticle",
        "headline": f"Resumen Ejecutivo: Macroeconomía de Bolivia — {fecha}",
        "description": meta_desc,
        "datePublished": f"{fecha_iso}T07:00:00-04:00",
        "dateModified": f"{fecha_iso}T07:00:00-04:00",
        "author": {
            "@type": "Organization",
            "name": "Consultora Maldonado",
            "url": "https://www.consultoramaldonado.com"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Consultora Maldonado",
            "url": "https://www.consultoramaldonado.com",
            "logo": {
                "@type": "ImageObject",
                "url": f"{base_url}/assets/logo.png"
            }
        },
        "mainEntityOfPage": canonical_url,
        "image": og_image_url
    }

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(page_title)}</title>
  <meta name="description" content="{html.escape(meta_desc)}">
  <link rel="canonical" href="{canonical_url}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  
  <!-- OpenGraph / Social Media -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html.escape(page_title)}">
  <meta property="og:description" content="{html.escape(meta_desc)}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="{og_image_url}">
  <meta property="og:site_name" content="Consultora Maldonado">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(page_title)}">
  <meta name="twitter:description" content="{html.escape(meta_desc)}">
  <meta name="twitter:image" content="{og_image_url}">
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {json.dumps(schema_json, ensure_ascii=False, indent=2)}
  </script>

  <style>
    :root {{
      --primary-navy: #091a2b;
      --navy-light: #0d3b66;
      --accent-blue: #0284c7;
      --accent-cyan: #38bdf8;
      --accent-gold: #f59e0b;
      --bg-slate: #f8fafc;
      --text-dark: #0f172a;
      --text-muted: #64748b;
      --card-bg: #ffffff;
      --card-border: #e2e8f0;
      --font-heading: 'Plus Jakarta Sans', -apple-system, sans-serif;
      --font-body: 'Inter', -apple-system, sans-serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: var(--font-body);
      background-color: var(--bg-slate);
      color: var(--text-dark);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }}

    /* BARRA SUPERIOR DE NAVEGACIÓN INSTITUCIONAL */
    .top-nav {{
      background-color: var(--primary-navy);
      color: #ffffff;
      padding: 14px 24px;
      border-bottom: 1px solid #1e3a5f;
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(8px);
    }}

    .nav-container {{
      max-width: 1080px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .brand-logo {{
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: #ffffff;
      font-family: var(--font-heading);
      font-weight: 800;
      font-size: 17px;
      letter-spacing: -0.3px;
    }}

    .brand-tag {{
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent-cyan);
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      font-weight: 700;
    }}

    .nav-links {{
      display: flex;
      gap: 20px;
      align-items: center;
    }}

    .nav-links a {{
      color: #cbd5e1;
      text-decoration: none;
      font-size: 13.5px;
      font-weight: 500;
      transition: color 0.2s ease;
    }}

    .nav-links a:hover {{
      color: var(--accent-cyan);
    }}

    /* HERO SECTION */
    .hero-section {{
      background: linear-gradient(180deg, var(--primary-navy) 0%, var(--navy-light) 100%);
      color: #ffffff;
      padding: 48px 24px 60px 24px;
      text-align: center;
    }}

    .hero-container {{
      max-width: 860px;
      margin: 0 auto;
    }}

    .hero-badge {{
      display: inline-block;
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #f8fafc;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 16px;
    }}

    .hero-title {{
      font-family: var(--font-heading);
      font-size: 32px;
      font-weight: 800;
      line-height: 1.25;
      letter-spacing: -0.8px;
      margin-bottom: 12px;
    }}

    .hero-subtitle {{
      color: #94a3b8;
      font-size: 15px;
      font-weight: 400;
    }}

    /* CONTENEDOR PRINCIPAL */
    .main-wrapper {{
      max-width: 900px;
      margin: -35px auto 40px auto;
      padding: 0 20px;
    }}

    /* MATRIZ DE ALERTA TL;DR */
    .alert-card {{
      background-color: {colors['bg']};
      border: 1px solid {colors['border']};
      border-left: 6px solid {colors['border']};
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 28px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
    }}

    .alert-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .alert-badge {{
      background-color: {colors['badge_bg']};
      color: {colors['badge_text']};
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.5px;
    }}

    .alert-title {{
      font-family: var(--font-heading);
      font-size: 18px;
      font-weight: 700;
      color: #0f172a;
    }}

    .alert-body {{
      font-size: 14.5px;
      color: #1e293b;
      line-height: 1.6;
    }}

    .alert-body strong {{
      color: {colors['text']};
    }}

    /* DASHBOARD KPIS GRID */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 18px;
      margin-bottom: 32px;
    }}

    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
      position: relative;
      overflow: hidden;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .kpi-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
    }}

    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
    }}

    .kpi-card.blue::before {{ background: #0284c7; }}
    .kpi-card.gold::before {{ background: #f59e0b; }}
    .kpi-card.green::before {{ background: #10b981; }}

    .kpi-tag {{
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-muted);
      letter-spacing: 0.5px;
      margin-bottom: 4px;
    }}

    .kpi-title {{
      font-family: var(--font-heading);
      font-size: 15px;
      font-weight: 700;
      color: #1e293b;
      margin-bottom: 10px;
    }}

    .kpi-value {{
      font-family: var(--font-heading);
      font-size: 30px;
      font-weight: 800;
      color: var(--navy-light);
      margin-bottom: 12px;
      letter-spacing: -0.5px;
    }}

    .kpi-details {{
      font-size: 12.5px;
      color: var(--text-muted);
      line-height: 1.5;
      border-top: 1px dashed var(--card-border);
      padding-top: 10px;
    }}

    /* TARJETA DE INFOGRAFÍA VISUAL EMBEBIDA */
    .infographic-showcase {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px;
      margin-bottom: 32px;
      box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
      text-align: center;
    }}

    .infographic-showcase img {{
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}

    .infographic-caption {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 8px;
    }}

    /* CUERPO DEL REPORTE DETALLADO */
    .report-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 36px 32px;
      margin-bottom: 32px;
      box-shadow: 0 4px 16px rgba(15, 23, 42, 0.03);
    }}

    .section-title {{
      font-family: var(--font-heading);
      font-size: 20px;
      font-weight: 800;
      color: var(--navy-light);
      margin: 28px 0 12px 0;
      padding-bottom: 8px;
      border-bottom: 2px solid #e2e8f0;
      letter-spacing: -0.3px;
    }}

    .section-title:first-child {{
      margin-top: 0;
    }}

    .subsection-title {{
      font-family: var(--font-heading);
      font-size: 16px;
      font-weight: 700;
      color: #1e293b;
      margin: 18px 0 8px 0;
    }}

    .content-p {{
      font-size: 14.5px;
      color: #334155;
      line-height: 1.7;
      margin-bottom: 14px;
    }}

    .content-list {{
      padding-left: 20px;
      margin-bottom: 16px;
    }}

    .content-list li {{
      font-size: 14px;
      color: #334155;
      line-height: 1.6;
      margin-bottom: 8px;
    }}

    .content-list li strong {{
      color: var(--navy-light);
    }}

    .content-divider {{
      border: none;
      border-top: 1px solid var(--card-border);
      margin: 28px 0;
    }}

    /* SELECTOR HISTÓRICO Y ACCIONES */
    .archive-bar {{
      background: #f1f5f9;
      border-radius: 10px;
      padding: 16px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
      margin-bottom: 32px;
      font-size: 13.5px;
    }}

    .archive-select {{
      padding: 8px 12px;
      border-radius: 6px;
      border: 1px solid #cbd5e1;
      background: #ffffff;
      font-size: 13.5px;
      font-family: var(--font-body);
      color: var(--text-dark);
      cursor: pointer;
    }}

    .share-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--navy-light);
      color: #ffffff;
      padding: 8px 14px;
      border-radius: 6px;
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      transition: background 0.2s ease;
      cursor: pointer;
      border: none;
    }}

    .share-btn:hover {{
      background: #1e3a8a;
    }}

    /* DESCARGO LEGAL */
    .legal-disclaimer {{
      background: #f8fafc;
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 18px 20px;
      font-size: 12px;
      color: #64748b;
      line-height: 1.5;
      margin-bottom: 40px;
    }}

    .legal-disclaimer strong {{
      color: #334155;
    }}

    /* FOOTER */
    .site-footer {{
      background: var(--primary-navy);
      color: #94a3b8;
      padding: 32px 24px;
      text-align: center;
      font-size: 13px;
      border-top: 1px solid #1e3a5f;
    }}

    .site-footer a {{
      color: var(--accent-cyan);
      text-decoration: none;
    }}

    @media (max-width: 768px) {{
      .hero-title {{
        font-size: 24px;
      }}
      .report-card {{
        padding: 24px 18px;
      }}
      .nav-links {{
        display: none;
      }}
    }}
  </style>
</head>
<body>

  <!-- BARRA DE NAVEGACIÓN INSTITUCIONAL -->
  <nav class="top-nav">
    <div class="nav-container">
      <a href="https://www.consultoramaldonado.com" class="brand-logo">
        <span>CONSULTORA MALDONADO</span>
        <span class="brand-tag">Macroeconomía</span>
      </a>
      <div class="nav-links">
        <a href="https://www.consultoramaldonado.com">Inicio</a>
        <a href="https://www.consultoramaldonado.com/cotizaci%C3%B3n-d%C3%B3lar">Cotización Dólar</a>
        <a href="https://www.consultoramaldonado.com/feriados-en-bolivia">Feriados</a>
        <a href="{base_url}">Informe Diario</a>
      </div>
    </div>
  </nav>

  <!-- HERO SECTION -->
  <header class="hero-section">
    <div class="hero-container">
      <div class="hero-badge">🇧🇴 Análisis Macroeconómico Diario</div>
      <h1 class="hero-title">Resumen Ejecutivo: Macroeconomía de Bolivia</h1>
      <p class="hero-subtitle">Informe de solvencia, mercado de divisas, reservas y riesgo crediticio • <strong>{fecha}</strong></p>
    </div>
  </header>

  <!-- MAIN WRAPPER -->
  <main class="main-wrapper">

    <!-- 1. MATRIZ DE ALERTA EJECUTIVA TL;DR -->
    <section class="alert-card">
      <div class="alert-header">
        <span class="alert-badge">{colors['label']}</span>
        <span style="font-size: 12.5px; color: #64748b;">Actualizado a las 07:00 AM (BOT)</span>
      </div>
      <div class="alert-body">
        <p style="margin-bottom: 8px;"><strong>🚨 Alerta Central:</strong> {alerta_principal}</p>
        <p><strong>🎯 Recomendación Directiva:</strong> {accion_recomendada}</p>
      </div>
    </section>

    <!-- 2. DASHBOARD DE KPIS PRINCIPALES -->
    <section class="kpi-grid">
      <!-- KPI 1 -->
      <div class="kpi-card blue">
        <div class="kpi-tag">Liquidez & Reservas</div>
        <div class="kpi-title">Reservas Netas (RIN)</div>
        <div class="kpi-value">{rin_total}</div>
        <div class="kpi-details">
          Oro: <strong>{rin_oro}</strong> ({rin_oro_pct})<br>
          Divisas Líquidas: <strong>{rin_divisas}</strong> ({rin_divisas_pct})
        </div>
      </div>

      <!-- KPI 2 -->
      <div class="kpi-card gold">
        <div class="kpi-tag">Mercado Cambiario</div>
        <div class="kpi-title">Brecha y Divisas</div>
        <div class="kpi-value">{brecha}</div>
        <div class="kpi-details">
          Oficial: <strong>{tc_oficial}</strong><br>
          Paralelo / USDT: <strong>{tc_paralelo}</strong>
        </div>
      </div>

      <!-- KPI 3 -->
      <div class="kpi-card green">
        <div class="kpi-tag">Precios & Comercio</div>
        <div class="kpi-title">Inflación (IPC)</div>
        <div class="kpi-value">{inflacion_m}</div>
        <div class="kpi-details">
          Acumulada 12M: <strong>{inflacion_a}</strong><br>
          Balanza Comercial: <strong>{balanza}</strong>
        </div>
      </div>
    </section>

    <!-- 3. INFOGRAFÍA VISUAL EMBEBIDA -->
    <section class="infographic-showcase">
      <img src="assets/infografia-latest.png" alt="Infografía Macroeconomía Bolivia - {fecha}" loading="lazy">
      <div class="infographic-caption">Infografía ejecutiva generada automáticamente para Consultora Maldonado</div>
    </section>

    <!-- 4. CUERPO DEL REPORTE COMPLETO -->
    <article class="report-card">
      {rendered_body}
    </article>

    <!-- 5. ARCHIVO HISTÓRICO Y COMPARTIR -->
    <section class="archive-bar">
      <div style="display: flex; align-items: center; gap: 8px;">
        <span>📅 <strong>Historial de Reportes:</strong></span>
        <select class="archive-select" onchange="if(this.value) window.location.href=this.value;">
          <option value="">Seleccionar fecha previa...</option>
          {archive_options_html}
        </select>
      </div>
      <div style="display: flex; gap: 8px;">
        <button class="share-btn" onclick="navigator.clipboard.writeText(window.location.href); alert('Enlace copiado al portapapeles!');">
          📋 Copiar Enlace
        </button>
        <a class="share-btn" href="https://api.whatsapp.com/send?text={html.escape(page_title)}%20{canonical_url}" target="_blank">
          📲 Compartir en WhatsApp
        </a>
      </div>
    </section>

    <!-- 6. DESCARGO LEGAL OBLIGATORIO -->
    <footer class="legal-disclaimer">
      <p><strong>Descargo de Responsabilidad Legal:</strong> La presente publicación tiene propósitos exclusivamente informativos, estadísticos y analíticos. No constituye ni debe interpretarse como asesoramiento financiero, tributario, contable o legal profesional, ni como recomendación explícita o implícita de compra/venta de activos, instrumentos financieros o divisas. Consultora Maldonado declina toda responsabilidad por decisiones tomadas a partir de estos datos.</p>
    </footer>

  </main>

  <!-- PIE DE PÁGINA -->
  <footer class="site-footer">
    <div style="max-width: 900px; margin: 0 auto;">
      <p style="margin-bottom: 8px;">© {fecha.split()[-1] if len(fecha.split()) > 0 else '2026'} <strong>Consultora Maldonado</strong> • Todos los derechos reservados.</p>
      <p style="font-size: 12px; color: #64748b;">Automatización Financiera Cloud • Fuentes oficiales: BCB, INE, ASFI, MEFP, ASOBAN, IBCE.</p>
    </div>
  </footer>

</body>
</html>
"""
