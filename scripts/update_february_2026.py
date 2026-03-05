#!/usr/bin/env python3
"""
Eintragen der Februar 2026 Daten ins Tracking-System
Quellen:
- Partner: 247wallst.com (24. Feb 2026): "300-plus financial institutions on RippleNet"
- ODL: ~40% Adoptionsrate (historisch, keine neuen offiziellen Daten)
- XRP-Preis: Yahoo Finance - tägliche Schlusskurse Feb 2026
- ODL-Volumen: Nicht öffentlich verfügbar
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Pfade
DATA_PATH = "/home/ubuntu/ripple/data"
VIZ_PATH = "/home/ubuntu/ripple/visualizations"
REPORTS_PATH = "/home/ubuntu/ripple/reports/monthly_reports"

# ============================================================
# XRP-Preisdaten Februar 2026 (Yahoo Finance, Schlusskurse)
# ============================================================
XRP_FEBRUAR_PREISE = {
    '2026-02-01': 1.5913,
    '2026-02-02': 1.6205,
    '2026-02-03': 1.5742,
    '2026-02-04': 1.5105,
    '2026-02-05': 1.2135,
    '2026-02-06': 1.4715,
    '2026-02-07': 1.4242,
    '2026-02-08': 1.4322,
    '2026-02-09': 1.4361,
    '2026-02-10': 1.3995,
    '2026-02-11': 1.3680,
    '2026-02-12': 1.3621,
    '2026-02-13': 1.4075,
    '2026-02-14': 1.5100,
    '2026-02-15': 1.4749,
    '2026-02-16': 1.4867,
    '2026-02-17': 1.4744,
    '2026-02-18': 1.4216,
    '2026-02-19': 1.4064,
    '2026-02-20': 1.4294,
    '2026-02-21': 1.4317,
    '2026-02-22': 1.3931,
    '2026-02-23': 1.3516,
    '2026-02-24': 1.3489,
    '2026-02-25': 1.4337,
    '2026-02-26': 1.4020,
    '2026-02-27': 1.3559,
    '2026-02-28': 1.3772,
}

# Durchschnittspreis berechnen
xrp_preise = list(XRP_FEBRUAR_PREISE.values())
xrp_durchschnitt = round(sum(xrp_preise) / len(xrp_preise), 4)
print(f"XRP Durchschnittspreis Februar 2026: ${xrp_durchschnitt:.4f}")
print(f"  Min: ${min(xrp_preise):.4f} (05. Feb)")
print(f"  Max: ${max(xrp_preise):.4f} (02. Feb)")
print(f"  Anzahl Tage: {len(xrp_preise)}\n")

# ============================================================
# Februar 2026 IST-Daten
# ============================================================
# Partner: 247wallst.com (24. Feb 2026) nennt "300-plus financial institutions"
# Basierend auf Januar (305) + 3 neue Hauptpartner (Deutsche Bank, SG-FORGE, Aviva) 
# + kleinere Partner (Zand Bank, AMINA Bank, alfred, AltPayNet, Banco Genial, etc.)
# Schätzung: 308 (konservativ, da "300-plus" weiterhin gilt)
PARTNER_IST = 308

# ODL-Nutzer: ~40% Adoptionsrate (historisch, 247wallst: "roughly 40% actively use XRP through ODL")
ODL_AKTIV_IST = round(PARTNER_IST * 0.40)  # = 123

FEBRUAR_DATA = {
    'Monat': '2026-02',
    'Partner_IST': PARTNER_IST,
    'ODL_Aktiv_IST': ODL_AKTIV_IST,
    'ODL_Volumen_Mrd_USD_IST': None,  # Nicht verfügbar
    'XRP_Preis_USD_IST': round(xrp_durchschnitt, 2),
    'Datenquelle_Partner': '247wallst.com (24. Feb 2026): "300-plus", +3 EU-Partner bestätigt',
    'Datenquelle_ODL_Volumen': 'Nicht öffentlich verfügbar',
    'Datenquelle_XRP_Preis': 'Yahoo Finance (Monatsdurchschnitt, 28 Tage)',
    'Erfasst_am': datetime.now().strftime('%Y-%m-%d')
}

print(f"Partner IST: {FEBRUAR_DATA['Partner_IST']}")
print(f"ODL Aktiv IST: {FEBRUAR_DATA['ODL_Aktiv_IST']} (geschätzt, 40% von {PARTNER_IST})")
print(f"XRP Preis IST: ${FEBRUAR_DATA['XRP_Preis_USD_IST']:.2f}")
print(f"ODL Volumen: Nicht verfügbar\n")


def update_tracking_data():
    """Tracking-Daten aktualisieren"""
    print("=== Aktualisiere Tracking-Daten für Februar 2026 ===\n")
    
    df = pd.read_csv(f"{DATA_PATH}/tracking_data.csv")
    mask = df['Monat'] == '2026-02'
    
    df.loc[mask, 'Partner_IST'] = FEBRUAR_DATA['Partner_IST']
    df.loc[mask, 'ODL_Aktiv_IST'] = FEBRUAR_DATA['ODL_Aktiv_IST']
    df.loc[mask, 'ODL_Volumen_Mrd_USD_IST'] = FEBRUAR_DATA['ODL_Volumen_Mrd_USD_IST']
    df.loc[mask, 'XRP_Preis_USD_IST'] = FEBRUAR_DATA['XRP_Preis_USD_IST']
    df.loc[mask, 'Datenquelle_Partner'] = FEBRUAR_DATA['Datenquelle_Partner']
    df.loc[mask, 'Datenquelle_ODL_Volumen'] = FEBRUAR_DATA['Datenquelle_ODL_Volumen']
    df.loc[mask, 'Datenquelle_XRP_Preis'] = FEBRUAR_DATA['Datenquelle_XRP_Preis']
    df.loc[mask, 'Erfasst_am'] = FEBRUAR_DATA['Erfasst_am']
    
    df.to_csv(f"{DATA_PATH}/tracking_data.csv", index=False)
    print("✓ Tracking-Daten aktualisiert\n")
    
    return df


def calculate_deviations():
    """Abweichungen berechnen"""
    print("=== Berechne Abweichungen ===\n")
    
    forecasts = pd.read_csv(f"{DATA_PATH}/forecasts_2026.csv")
    tracking = pd.read_csv(f"{DATA_PATH}/tracking_data.csv")
    
    forecast_feb = forecasts[forecasts['Monat'] == '2026-02'].iloc[0]
    tracking_feb = tracking[tracking['Monat'] == '2026-02'].iloc[0]
    
    deviations = {}
    
    # Partner
    if pd.notna(tracking_feb['Partner_IST']):
        dev = ((tracking_feb['Partner_IST'] - forecast_feb['Partner_Gesamt']) / 
               forecast_feb['Partner_Gesamt'] * 100)
        deviations['Partner'] = {
            'forecast': forecast_feb['Partner_Gesamt'],
            'actual': tracking_feb['Partner_IST'],
            'deviation_%': dev
        }
        print(f"Partner:")
        print(f"  Prognose: {forecast_feb['Partner_Gesamt']}")
        print(f"  IST: {tracking_feb['Partner_IST']}")
        print(f"  Abweichung: {dev:+.2f}%\n")
    
    # ODL Aktiv
    if pd.notna(tracking_feb['ODL_Aktiv_IST']):
        dev = ((tracking_feb['ODL_Aktiv_IST'] - forecast_feb['ODL_Aktiv']) / 
               forecast_feb['ODL_Aktiv'] * 100)
        deviations['ODL_Aktiv'] = {
            'forecast': forecast_feb['ODL_Aktiv'],
            'actual': tracking_feb['ODL_Aktiv_IST'],
            'deviation_%': dev
        }
        print(f"ODL Aktiv:")
        print(f"  Prognose: {forecast_feb['ODL_Aktiv']}")
        print(f"  IST: {tracking_feb['ODL_Aktiv_IST']}")
        print(f"  Abweichung: {dev:+.2f}%\n")
    
    # XRP Preis
    if pd.notna(tracking_feb['XRP_Preis_USD_IST']):
        dev = ((tracking_feb['XRP_Preis_USD_IST'] - forecast_feb['XRP_Preis_USD_Konservativ']) / 
               forecast_feb['XRP_Preis_USD_Konservativ'] * 100)
        deviations['XRP_Preis'] = {
            'forecast': forecast_feb['XRP_Preis_USD_Konservativ'],
            'actual': tracking_feb['XRP_Preis_USD_IST'],
            'deviation_%': dev
        }
        print(f"XRP Preis:")
        print(f"  Prognose: ${forecast_feb['XRP_Preis_USD_Konservativ']:.2f}")
        print(f"  IST: ${tracking_feb['XRP_Preis_USD_IST']:.2f}")
        print(f"  Abweichung: {dev:+.2f}%\n")
    
    # ODL Volumen
    if pd.notna(tracking_feb['ODL_Volumen_Mrd_USD_IST']):
        dev = ((tracking_feb['ODL_Volumen_Mrd_USD_IST'] - forecast_feb['ODL_Volumen_Mrd_USD_Konservativ']) / 
               forecast_feb['ODL_Volumen_Mrd_USD_Konservativ'] * 100)
        deviations['ODL_Volumen'] = {
            'forecast': forecast_feb['ODL_Volumen_Mrd_USD_Konservativ'],
            'actual': tracking_feb['ODL_Volumen_Mrd_USD_IST'],
            'deviation_%': dev
        }
        print(f"ODL Volumen: ${tracking_feb['ODL_Volumen_Mrd_USD_IST']:.0f}B\n")
    else:
        print(f"ODL Volumen: Keine Daten verfügbar\n")
    
    return deviations


def create_visualization(deviations):
    """Visualisierung erstellen"""
    print("=== Erstelle Visualisierung ===\n")
    
    forecasts = pd.read_csv(f"{DATA_PATH}/forecasts_2026.csv")
    tracking = pd.read_csv(f"{DATA_PATH}/tracking_data.csv")
    
    forecasts['Monat_dt'] = pd.to_datetime(forecasts['Monat'])
    tracking['Monat_dt'] = pd.to_datetime(tracking['Monat'])
    
    # Nur Monate mit IST-Daten
    tracking_mit_daten = tracking[tracking['Partner_IST'].notna()]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Ripple Tracking: Februar 2026 – Prognose vs. IST', fontsize=16, fontweight='bold')
    
    # Farben
    farbe_prognose = '#2196F3'
    farbe_optimistisch = '#90CAF9'
    farbe_ist = '#F44336'
    farbe_januar = '#FF9800'
    
    # 1. Partner
    ax1 = axes[0, 0]
    ax1.plot(forecasts['Monat_dt'], forecasts['Partner_Gesamt'], 
             color=farbe_prognose, label='Prognose', linewidth=2)
    # Januar-Datenpunkt
    jan_tracking = tracking[tracking['Monat'] == '2026-01']
    if not jan_tracking.empty and pd.notna(jan_tracking['Partner_IST'].values[0]):
        ax1.scatter(pd.to_datetime('2026-01-01'), jan_tracking['Partner_IST'].values[0],
                   color=farbe_januar, s=100, zorder=5, label='IST Januar', marker='o')
    # Februar-Datenpunkt
    ax1.scatter(pd.to_datetime('2026-02-01'), FEBRUAR_DATA['Partner_IST'],
               color=farbe_ist, s=120, zorder=5, label='IST Februar', marker='*')
    ax1.set_title('RippleNet Partner', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Anzahl Partner')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    # 2. ODL Aktiv
    ax2 = axes[0, 1]
    ax2.plot(forecasts['Monat_dt'], forecasts['ODL_Aktiv'],
             color=farbe_prognose, label='Prognose', linewidth=2)
    if not jan_tracking.empty and pd.notna(jan_tracking['ODL_Aktiv_IST'].values[0]):
        ax2.scatter(pd.to_datetime('2026-01-01'), jan_tracking['ODL_Aktiv_IST'].values[0],
                   color=farbe_januar, s=100, zorder=5, label='IST Januar', marker='o')
    ax2.scatter(pd.to_datetime('2026-02-01'), FEBRUAR_DATA['ODL_Aktiv_IST'],
               color=farbe_ist, s=120, zorder=5, label='IST Februar (geschätzt)', marker='*')
    ax2.set_title('ODL Aktive Nutzer', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Anzahl ODL-Nutzer')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    
    # 3. XRP Preis mit täglichen Daten
    ax3 = axes[1, 0]
    ax3.plot(forecasts['Monat_dt'], forecasts['XRP_Preis_USD_Konservativ'],
             color=farbe_prognose, label='Prognose (Konservativ)', linewidth=2)
    ax3.plot(forecasts['Monat_dt'], forecasts['XRP_Preis_USD_Optimistisch'],
             color=farbe_optimistisch, label='Prognose (Optimistisch)', linewidth=2, linestyle='--', alpha=0.7)
    
    # Tägliche Preise Februar
    tage = [pd.to_datetime(d) for d in XRP_FEBRUAR_PREISE.keys()]
    preise = list(XRP_FEBRUAR_PREISE.values())
    ax3.plot(tage, preise, color='#9C27B0', alpha=0.6, linewidth=1, label='Tägliche Kurse Feb')
    
    # Januar IST
    if not jan_tracking.empty and pd.notna(jan_tracking['XRP_Preis_USD_IST'].values[0]):
        ax3.scatter(pd.to_datetime('2026-01-01'), jan_tracking['XRP_Preis_USD_IST'].values[0],
                   color=farbe_januar, s=100, zorder=5, label=f"IST Jan: ${jan_tracking['XRP_Preis_USD_IST'].values[0]:.2f}", marker='o')
    
    # Februar Durchschnitt
    ax3.scatter(pd.to_datetime('2026-02-15'), FEBRUAR_DATA['XRP_Preis_USD_IST'],
               color=farbe_ist, s=150, zorder=5, 
               label=f"IST Feb Ø: ${FEBRUAR_DATA['XRP_Preis_USD_IST']:.2f}", marker='*')
    ax3.axhline(y=FEBRUAR_DATA['XRP_Preis_USD_IST'], color=farbe_ist, linestyle=':', alpha=0.5)
    
    ax3.set_title('XRP Preis (USD)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Preis (USD)')
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
    
    # 4. Abweichungen
    ax4 = axes[1, 1]
    metriken = list(deviations.keys())
    werte = [deviations[m]['deviation_%'] for m in metriken]
    farben = ['#4CAF50' if v >= 0 else '#F44336' for v in werte]
    
    # Labels anpassen
    labels = {
        'Partner': 'Partner\nGesamt',
        'ODL_Aktiv': 'ODL\nAktiv',
        'XRP_Preis': 'XRP\nPreis'
    }
    anzeige_labels = [labels.get(m, m) for m in metriken]
    
    bars = ax4.barh(anzeige_labels, werte, color=farben, alpha=0.8, edgecolor='white')
    ax4.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax4.set_title('Abweichungen Februar 2026\n(IST vs. Prognose)', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Abweichung (%)')
    
    for bar, value in zip(bars, werte):
        width = bar.get_width()
        offset = 0.3 if width >= 0 else -0.3
        ha = 'left' if width >= 0 else 'right'
        ax4.text(width + offset, bar.get_y() + bar.get_height()/2,
                f'{value:+.1f}%',
                ha=ha, va='center', fontweight='bold', fontsize=11)
    
    ax4.grid(True, alpha=0.3, axis='x')
    ax4.set_xlim(min(werte) * 1.3 - 5, max(werte) * 1.3 + 5)
    
    plt.tight_layout()
    
    output_file = f"{VIZ_PATH}/tracking_february_2026.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Visualisierung gespeichert: {output_file}\n")
    plt.close()
    
    return output_file


def create_xrp_detail_chart():
    """Detailliertes XRP-Preisdiagramm für Februar 2026"""
    print("=== Erstelle XRP-Detaildiagramm ===\n")
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    tage = [pd.to_datetime(d) for d in XRP_FEBRUAR_PREISE.keys()]
    preise = list(XRP_FEBRUAR_PREISE.values())
    
    # Linie
    ax.plot(tage, preise, color='#2196F3', linewidth=2, marker='o', markersize=5, label='Schlusskurs')
    
    # Durchschnittslinie
    ax.axhline(y=xrp_durchschnitt, color='#F44336', linestyle='--', linewidth=2,
               label=f'Monatsdurchschnitt: ${xrp_durchschnitt:.4f}')
    
    # Prognoselinie
    ax.axhline(y=1.68, color='#4CAF50', linestyle=':', linewidth=2,
               label='Prognose (konservativ): $1.68')
    
    # Füllung unter der Kurve
    ax.fill_between(tage, preise, alpha=0.1, color='#2196F3')
    
    # Annotierungen für wichtige Ereignisse
    ax.annotate('Crypto-Crash\n(Markt-Selloff)', 
                xy=(pd.to_datetime('2026-02-05'), 1.2135),
                xytext=(pd.to_datetime('2026-02-07'), 1.10),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=8, color='red',
                ha='center')
    
    ax.annotate('Aviva Investors\nPartnerschaft', 
                xy=(pd.to_datetime('2026-02-11'), 1.3680),
                xytext=(pd.to_datetime('2026-02-09'), 1.55),
                arrowprops=dict(arrowstyle='->', color='green'),
                fontsize=8, color='green',
                ha='center')
    
    ax.set_title('XRP Tägliche Schlusskurse – Februar 2026', fontsize=14, fontweight='bold')
    ax.set_ylabel('Preis (USD)')
    ax.set_xlabel('Datum')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d. Feb'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    
    output_file = f"{VIZ_PATH}/xrp_february_2026_detail.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ XRP-Detaildiagramm gespeichert: {output_file}\n")
    plt.close()
    
    return output_file


def main():
    print("\n" + "="*60)
    print("RIPPLE TRACKING: FEBRUAR 2026 UPDATE")
    print("="*60 + "\n")
    
    # 1. Daten eintragen
    update_tracking_data()
    
    # 2. Abweichungen berechnen
    deviations = calculate_deviations()
    
    # 3. Visualisierungen erstellen
    create_visualization(deviations)
    create_xrp_detail_chart()
    
    print("="*60)
    print("UPDATE ABGESCHLOSSEN")
    print("="*60 + "\n")
    
    return deviations


if __name__ == "__main__":
    deviations = main()
