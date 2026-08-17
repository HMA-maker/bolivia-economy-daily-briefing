import re

def update_html():
    file_path = r"c:\Users\HMA\Documents\Antigravity\Publicacion Web Consultora Maldonado\html_templates.py"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add Greeting
    old_greeting_marker = '<!-- 1. MATRIZ DE ALERTAS (TL;DR) -->'
    greeting_html = """<!-- SALUDO PERSONALIZADO -->
              <p style="font-size: 15px; color: #334155; margin-bottom: 20px; line-height: 1.5;">
                Estimado/a <strong>{{nombre_cliente | default: email}}</strong>,<br><br>
                A continuación, te presentamos la síntesis ejecutiva del estado macroeconómico de Bolivia para el día de hoy:
              </p>
              
              <!-- 1. MATRIZ DE ALERTAS (TL;DR) -->"""
    content = content.replace(old_greeting_marker, greeting_html)

    # 2. Refactor KPI Cards to HTML Tables
    # Card 1
    old_card1 = """              <!-- Bloque 1: RIN y Divisas -->
              <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 16px; margin-bottom: 12px; border-left: 4px solid #E76F2D;">
                <div style="font-size: 14px; font-weight: bold; color: #E76F2D; margin-bottom: 4px;">
                  1. Reservas Internacionales & Divisas
                </div>
                <div style="font-size: 13px; color: #334155; line-height: 1.5;">
                  {rin_txt}
                </div>
                <div style="font-size: 12px; color: #64748b; margin-top: 6px; padding-top: 6px; border-top: 1px dashed #cbd5e1;">
                  Oficial: <strong>{tc_oficial}</strong> | Paralelo/USDT: <strong>{tc_paralelo}</strong>
                </div>
              </div>"""

    new_card1 = """              <!-- Bloque 1: RIN y Divisas (TABLA HTML) -->
              <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-bottom: 12px;">
                <tr>
                  <td width="4" bgcolor="#E76F2D" style="font-size:1px; line-height:1px;">&nbsp;</td>
                  <td bgcolor="#f8fafc" style="border: 1px solid #e2e8f0; border-left: none; padding: 14px 16px; border-top-right-radius: 8px; border-bottom-right-radius: 8px;">
                    <div style="font-size: 14px; font-weight: bold; color: #E76F2D; margin-bottom: 4px;">
                      1. Reservas Internacionales & Divisas
                    </div>
                    <div style="font-size: 13px; color: #334155; line-height: 1.5;">
                      {rin_txt}
                    </div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 6px; padding-top: 6px; border-top: 1px dashed #cbd5e1;">
                      Oficial: <strong>{tc_oficial}</strong> | Paralelo/USDT: <strong>{tc_paralelo}</strong>
                    </div>
                  </td>
                </tr>
              </table>"""
    content = content.replace(old_card1, new_card1)

    # Cards 2 and 3
    old_cards_2_3 = """              <!-- Diseño a dos columnas para Comercio e Inflación -->
              <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-bottom: 20px;">
                <tr>
                  <!-- Bloque 2: Comercio Exterior -->
                  <td width="48%" valign="top" style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; border-left: 4px solid #0d3b66;">
                    <div style="font-size: 13px; font-weight: bold; color: #0d3b66; margin-bottom: 4px;">
                      2. Comercio Exterior
                    </div>
                    <div style="font-size: 12px; color: #334155; line-height: 1.4;">
                      {comercio_txt}
                    </div>
                  </td>
                  <td width="4%"></td> <!-- Espaciador -->
                  <!-- Bloque 3: Inflación y Banca -->
                  <td width="48%" valign="top" style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; border-left: 4px solid #059669;">
                    <div style="font-size: 13px; font-weight: bold; color: #059669; margin-bottom: 4px;">
                      3. Inflación y Banca
                    </div>
                    <div style="font-size: 12px; color: #334155; line-height: 1.4;">
                      {banca_txt}
                    </div>
                  </td>
                </tr>
              </table>"""

    new_cards_2_3 = """              <!-- Diseño a dos columnas para Comercio e Inflación (TABLAS HTML) -->
              <table width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-bottom: 20px;">
                <tr>
                  <!-- Bloque 2: Comercio Exterior -->
                  <td width="48%" valign="top">
                    <table width="100%" cellspacing="0" cellpadding="0" border="0">
                      <tr>
                        <td width="4" bgcolor="#0d3b66" style="font-size:1px; line-height:1px;">&nbsp;</td>
                        <td bgcolor="#f8fafc" style="border: 1px solid #e2e8f0; border-left: none; padding: 12px; border-top-right-radius: 8px; border-bottom-right-radius: 8px;">
                          <div style="font-size: 13px; font-weight: bold; color: #0d3b66; margin-bottom: 4px;">
                            2. Comercio Exterior
                          </div>
                          <div style="font-size: 12px; color: #334155; line-height: 1.4;">
                            {comercio_txt}
                          </div>
                        </td>
                      </tr>
                    </table>
                  </td>
                  
                  <td width="4%"></td> <!-- Espaciador -->
                  
                  <!-- Bloque 3: Inflación y Banca -->
                  <td width="48%" valign="top">
                    <table width="100%" cellspacing="0" cellpadding="0" border="0">
                      <tr>
                        <td width="4" bgcolor="#059669" style="font-size:1px; line-height:1px;">&nbsp;</td>
                        <td bgcolor="#f8fafc" style="border: 1px solid #e2e8f0; border-left: none; padding: 12px; border-top-right-radius: 8px; border-bottom-right-radius: 8px;">
                          <div style="font-size: 13px; font-weight: bold; color: #059669; margin-bottom: 4px;">
                            3. Inflación y Banca
                          </div>
                          <div style="font-size: 12px; color: #334155; line-height: 1.4;">
                            {banca_txt}
                          </div>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>"""
    content = content.replace(old_cards_2_3, new_cards_2_3)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated html_templates.py")

if __name__ == "__main__":
    update_html()
