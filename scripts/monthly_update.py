#!/usr/bin/env python3
"""
Monatliches Update-Script für Ripple-Tracking
Wird automatisch am 5. jeden Monats ausgeführt
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

# Konfiguration
REPO_PATH = "/home/ubuntu/ripple"
DATA_PATH = f"{REPO_PATH}/data"
REPORTS_PATH = f"{REPO_PATH}/reports/monthly_reports"
VIZ_PATH = f"{REPO_PATH}/visualizations"

def load_data():
    """Lade Prognosen und Tracking-Daten"""
    forecasts = pd.read_csv(f"{DATA_PATH}/forecasts_2026.csv")
    tracking = pd.read_csv(f"{DATA_PATH}/tracking_data.csv")
    return forecasts, tracking

def calculate_deviations(forecasts, tracking, month):
    """Berechne Abweichungen für einen Monat"""
    forecast_row = forecasts[forecasts['Monat'] == month].iloc[0]
    tracking_row = tracking[tracking['Monat'] == month].iloc[0]
    
    deviations = {}
    
    if pd.notna(tracking_row['Partner_IST']):
        deviations['Partner'] = {
            'forecast': forecast_row['Partner_Gesamt'],
            'actual': tracking_row['Partner_IST'],
            'deviation_%': ((tracking_row['Partner_IST'] - forecast_row['Partner_Gesamt']) / 
                           forecast_row['Partner_Gesamt'] * 100)
        }
    
    if pd.notna(tracking_row['ODL_Volumen_Mrd_USD_IST']):
        deviations['ODL_Volumen'] = {
            'forecast': forecast_row['ODL_Volumen_Mrd_USD_Konservativ'],
            'actual': tracking_row['ODL_Volumen_Mrd_USD_IST'],
            'deviation_%': ((tracking_row['ODL_Volumen_Mrd_USD_IST'] - 
                           forecast_row['ODL_Volumen_Mrd_USD_Konservativ']) / 
                           forecast_row['ODL_Volumen_Mrd_USD_Konservativ'] * 100)
        }
    
    if pd.notna(tracking_row['XRP_Preis_USD_IST']):
        deviations['XRP_Preis'] = {
            'forecast': forecast_row['XRP_Preis_USD_Konservativ'],
            'actual': tracking_row['XRP_Preis_USD_IST'],
            'deviation_%': ((tracking_row['XRP_Preis_USD_IST'] - 
                           forecast_row['XRP_Preis_USD_Konservativ']) / 
                           forecast_row['XRP_Preis_USD_Konservativ'] * 100)
        }
    
    return deviations

def create_monthly_report(month, deviations):
    """Erstelle Monatsbericht"""
    report = f"""# Ripple Tracking-Bericht: {month}

**Erstellt am:** {datetime.now().strftime('%d.%m.%Y %H:%M')}

---

## IST-Daten {month}

"""
    
    for metric, data in deviations.items():
        report += f"### {metric}\n"
        report += f"- **Prognose:** {data['forecast']:.2f}\n"
        report += f"- **IST:** {data['actual']:.2f}\n"
        report += f"- **Abweichung:** {data['deviation_%']:+.2f}%\n\n"
    
    # Interpretation
    report += "## Interpretation\n\n"
    
    avg_deviation = np.mean([d['deviation_%'] for d in deviations.values()])
    
    if avg_deviation > 5:
        report += "✅ **POSITIV:** Die Entwicklung übertrifft die Prognosen deutlich.\n\n"
        report += "**Investment-These:** Bestätigt\n\n"
    elif avg_deviation > 0:
        report += "✅ **POSITIV:** Die Entwicklung liegt leicht über den Prognosen.\n\n"
        report += "**Investment-These:** Bestätigt\n\n"
    elif avg_deviation > -5:
        report += "⚠️ **NEUTRAL:** Die Entwicklung liegt leicht unter den Prognosen.\n\n"
        report += "**Investment-These:** Teilweise bestätigt\n\n"
    else:
        report += "❌ **NEGATIV:** Die Entwicklung liegt deutlich unter den Prognosen.\n\n"
        report += "**Investment-These:** Nicht bestätigt\n\n"
    
    return report

def main():
    """Hauptfunktion"""
    print(f"\\n=== Monatliches Ripple-Tracking Update ===")
    print(f"Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}\\n")
    
    # Aktuellen Monat bestimmen
    current_month = datetime.now().strftime('%Y-%m')
    
    # Daten laden
    forecasts, tracking = load_data()
    
    # Prüfen ob Daten vorhanden
    tracking_row = tracking[tracking['Monat'] == current_month]
    if tracking_row.empty or pd.isna(tracking_row.iloc[0]['Partner_IST']):
        print(f"⚠️ Noch keine Daten für {current_month} vorhanden.")
        print("Bitte tragen Sie die Daten in tracking_data.csv ein.")
        return
    
    # Abweichungen berechnen
    deviations = calculate_deviations(forecasts, tracking, current_month)
    
    # Bericht erstellen
    report = create_monthly_report(current_month, deviations)
    
    # Bericht speichern
    report_file = f"{REPORTS_PATH}/report_{current_month}.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Bericht erstellt: {report_file}")
    print("\\n=== Update abgeschlossen ===\\n")

if __name__ == "__main__":
    main()
