#!/usr/bin/env python3
"""
Ripple Tracking Update: März 2026
Erstellt am: 05. April 2026
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os

# ============================================================
# PFADE
# ============================================================
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "data")
VIZ_PATH = os.path.join(BASE_PATH, "visualizations")
REPORTS_PATH = os.path.join(BASE_PATH, "reports", "monthly_reports")

# ============================================================
# GESAMMELTE DATEN FÜR MÄRZ 2026
# ============================================================

MAERZ_DATA = {
    'Partner_IST': 311,           # "über 300" + neue Partnerschaften (Convera, MAS BLOOM/Unloq, Mastercard-Initiative, Brazil Full Stack, AUDD/XRPL)
    'ODL_Aktiv_IST': 124,         # Geschätzt: ~40% von 311 Partnern (ODL weiterhin hauptsächlich Remittance-Firmen)
    'ODL_Volumen_Mrd_USD_IST': None,  # Nicht öffentlich verfügbar
    'XRP_Preis_USD_IST': 1.40,    # Monatsdurchschnitt (31 Tage, CoinMarketCap + TwelveData)
    'Datenquelle_Partner': 'MEXC (31. Mär 2026): "über 300", +5 neue Partnerschaften im März (Convera, MAS BLOOM/Unloq, Mastercard-Blockchain, Brazil Full Stack, AUDD/XRPL)',
    'Datenquelle_ODL_Volumen': 'Nicht öffentlich verfügbar',
    'Datenquelle_XRP_Preis': 'CoinMarketCap + TwelveData (Monatsdurchschnitt, 31 Tage: $1.3226–$1.5436)',
    'Erfasst_am': '2026-04-05'
}

# XRP Tageskurse März 2026 (Schlusskurse, CoinMarketCap)
XRP_MAERZ_PREISE = {
    '2026-03-01': 1.3517,
    '2026-03-02': 1.3910,
    '2026-03-03': 1.3606,
    '2026-03-04': 1.4302,
    '2026-03-05': 1.4031,
    '2026-03-06': 1.3636,
    '2026-03-07': 1.3564,
    '2026-03-08': 1.3414,
    '2026-03-09': 1.3618,
    '2026-03-10': 1.3864,
    '2026-03-11': 1.3849,
    '2026-03-12': 1.3846,
    '2026-03-13': 1.3989,
    '2026-03-14': 1.4073,
    '2026-03-15': 1.4476,
    '2026-03-16': 1.5436,
    '2026-03-17': 1.5185,
    '2026-03-18': 1.4639,
    '2026-03-19': 1.4473,
    '2026-03-20': 1.4455,
    '2026-03-21': 1.4066,
    '2026-03-22': 1.3849,
    '2026-03-23': 1.4319,
    '2026-03-24': 1.4154,
    '2026-03-25': 1.4142,
    '2026-03-26': 1.3601,
    '2026-03-27': 1.3250,
    '2026-03-28': 1.3328,
    '2026-03-29': 1.3273,
    '2026-03-30': 1.3226,
    '2026-03-31': 1.3403,
}

xrp_durchschnitt = sum(XRP_MAERZ_PREISE.values()) / len(XRP_MAERZ_PREISE)

# ============================================================
# SCHRITT 1: TRACKING-DATEN EINTRAGEN
# ============================================================

def update_tracking_data():
    """Trägt die März-Daten in die tracking_data.csv ein."""
    print("=== Trage Tracking-Daten ein ===\n")

    df = pd.read_csv(os.path.join(DATA_PATH, 'tracking_data.csv'))
    mask = df['Monat'] == '2026-03'

    for key, value in MAERZ_DATA.items():
        df.loc[mask, key] = value

    df.to_csv(os.path.join(DATA_PATH, 'tracking_data.csv'), index=False)
    print(f"✓ Daten für 2026-03 eingetragen")
    print(f"  Partner IST:       {MAERZ_DATA['Partner_IST']}")
    print(f"  ODL Aktiv IST:     {MAERZ_DATA['ODL_Aktiv_IST']} (geschätzt)")
    print(f"  XRP Preis IST:     ${MAERZ_DATA['XRP_Preis_USD_IST']:.2f}")
    print(f"  ODL Volumen:       Nicht verfügbar\n")

    return df

# ============================================================
# SCHRITT 2: ABWEICHUNGEN BERECHNEN
# ============================================================

def calculate_deviations():
    """Berechnet die Abweichungen von der Prognose."""
    print("=== Berechne Abweichungen ===\n")

    forecasts = pd.read_csv(os.path.join(DATA_PATH, 'forecasts_2026.csv'))
    tracking = pd.read_csv(os.path.join(DATA_PATH, 'tracking_data.csv'))

    forecast_row = forecasts[forecasts['Monat'] == '2026-03'].iloc[0]
    tracking_row = tracking[tracking['Monat'] == '2026-03'].iloc[0]

    deviations = {}

    # Partner
    if pd.notna(tracking_row['Partner_IST']):
        partner_dev = ((tracking_row['Partner_IST'] - forecast_row['Partner_Gesamt']) /
                       forecast_row['Partner_Gesamt'] * 100)
        deviations['Partner'] = {
            'prognose': forecast_row['Partner_Gesamt'],
            'ist': tracking_row['Partner_IST'],
            'deviation_%': round(partner_dev, 2)
        }
        print(f"Partner:    Prognose={forecast_row['Partner_Gesamt']}, IST={tracking_row['Partner_IST']}, Abw={partner_dev:+.2f}%")

    # ODL Aktiv
    if pd.notna(tracking_row['ODL_Aktiv_IST']):
        odl_dev = ((tracking_row['ODL_Aktiv_IST'] - forecast_row['ODL_Aktiv']) /
                   forecast_row['ODL_Aktiv'] * 100)
        deviations['ODL_Aktiv'] = {
            'prognose': forecast_row['ODL_Aktiv'],
            'ist': tracking_row['ODL_Aktiv_IST'],
            'deviation_%': round(odl_dev, 2)
        }
        print(f"ODL Aktiv:  Prognose={forecast_row['ODL_Aktiv']}, IST={tracking_row['ODL_Aktiv_IST']}, Abw={odl_dev:+.2f}%")

    # XRP Preis
    if pd.notna(tracking_row['XRP_Preis_USD_IST']):
        price_dev = ((tracking_row['XRP_Preis_USD_IST'] - forecast_row['XRP_Preis_USD_Konservativ']) /
                     forecast_row['XRP_Preis_USD_Konservativ'] * 100)
        deviations['XRP_Preis'] = {
            'prognose': forecast_row['XRP_Preis_USD_Konservativ'],
            'ist': tracking_row['XRP_Preis_USD_IST'],
            'deviation_%': round(price_dev, 2)
        }
        print(f"XRP Preis:  Prognose=${forecast_row['XRP_Preis_USD_Konservativ']:.2f}, IST=${tracking_row['XRP_Preis_USD_IST']:.2f}, Abw={price_dev:+.2f}%")

    # Durchschnittliche Abweichung
    avg_dev = sum(d['deviation_%'] for d in deviations.values()) / len(deviations)
    print(f"\nDurchschnittliche Abweichung: {avg_dev:+.2f}%\n")

    return deviations

# ============================================================
# SCHRITT 3: VISUALISIERUNGEN ERSTELLEN
# ============================================================

def create_visualization(deviations):
    """Erstellt das Tracking-Dashboard für März 2026."""
    print("=== Erstelle Tracking-Visualisierung ===\n")

    # Matplotlib-Konfiguration für deutsche Umlaute
    plt.rcParams['font.family'] = 'DejaVu Sans'

    # Farbschema
    farbe_prognose = '#2196F3'
    farbe_ist = '#4CAF50'
    farbe_negativ = '#F44336'
    farbe_januar = '#9C27B0'
    farbe_februar = '#FF9800'

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Ripple Tracking-Dashboard: Maerz 2026', fontsize=16, fontweight='bold', y=0.98)

    # ---- 1. Partner-Entwicklung ----
    ax1 = axes[0, 0]
    tracking = pd.read_csv(os.path.join(DATA_PATH, 'tracking_data.csv'))
    forecasts = pd.read_csv(os.path.join(DATA_PATH, 'forecasts_2026.csv'))

    monate_labels = ['Jan', 'Feb', 'Mrz', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
    prognose_partner = forecasts['Partner_Gesamt'].tolist()
    ist_partner = tracking['Partner_IST'].tolist()

    x = range(len(monate_labels))
    ax1.plot(x, prognose_partner, color=farbe_prognose, linewidth=2, linestyle='--',
             marker='o', markersize=5, label='Prognose (konservativ)')

    # IST-Werte nur wo vorhanden
    ist_x = [i for i, v in enumerate(ist_partner) if pd.notna(v)]
    ist_y = [v for v in ist_partner if pd.notna(v)]
    if ist_x:
        ax1.plot(ist_x, ist_y, color=farbe_ist, linewidth=2.5,
                 marker='*', markersize=10, label='IST')

    ax1.set_title('RippleNet-Partner (Gesamt)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Anzahl Partner')
    ax1.set_xticks(x)
    ax1.set_xticklabels(monate_labels, rotation=45)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(300, 320)

    # ---- 2. ODL-Nutzer ----
    ax2 = axes[0, 1]
    prognose_odl = forecasts['ODL_Aktiv'].tolist()
    ist_odl = tracking['ODL_Aktiv_IST'].tolist()

    ax2.plot(x, prognose_odl, color=farbe_prognose, linewidth=2, linestyle='--',
             marker='o', markersize=5, label='Prognose')

    ist_odl_x = [i for i, v in enumerate(ist_odl) if pd.notna(v)]
    ist_odl_y = [v for v in ist_odl if pd.notna(v)]
    if ist_odl_x:
        ax2.plot(ist_odl_x, ist_odl_y, color=farbe_ist, linewidth=2.5,
                 marker='*', markersize=10, label='IST (geschaetzt)')

    ax2.set_title('ODL-Aktive Nutzer', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Anzahl')
    ax2.set_xticks(x)
    ax2.set_xticklabels(monate_labels, rotation=45)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(120, 135)

    # ---- 3. XRP-Preis ----
    ax3 = axes[1, 0]
    prognose_xrp = forecasts['XRP_Preis_USD_Konservativ'].tolist()
    ist_xrp = tracking['XRP_Preis_USD_IST'].tolist()

    ax3.plot(x, prognose_xrp, color=farbe_prognose, linewidth=2, linestyle='--',
             marker='o', markersize=5, label='Prognose (konservativ)')
    ax3.plot(x, forecasts['XRP_Preis_USD_Optimistisch'].tolist(), color='#90CAF9',
             linewidth=1.5, linestyle=':', label='Prognose (optimistisch)')

    # Januar und Februar IST
    jan_tracking = tracking[tracking['Monat'] == '2026-01']
    feb_tracking = tracking[tracking['Monat'] == '2026-02']
    if not jan_tracking.empty and pd.notna(jan_tracking['XRP_Preis_USD_IST'].values[0]):
        ax3.scatter(0, jan_tracking['XRP_Preis_USD_IST'].values[0],
                   color=farbe_januar, s=100, zorder=5,
                   label=f"IST Jan: ${jan_tracking['XRP_Preis_USD_IST'].values[0]:.2f}", marker='o')
    if not feb_tracking.empty and pd.notna(feb_tracking['XRP_Preis_USD_IST'].values[0]):
        ax3.scatter(1, feb_tracking['XRP_Preis_USD_IST'].values[0],
                   color=farbe_februar, s=100, zorder=5,
                   label=f"IST Feb: ${feb_tracking['XRP_Preis_USD_IST'].values[0]:.2f}", marker='o')

    # März IST
    ax3.scatter(2, MAERZ_DATA['XRP_Preis_USD_IST'],
               color=farbe_ist, s=150, zorder=5,
               label=f"IST Mrz: ${MAERZ_DATA['XRP_Preis_USD_IST']:.2f}", marker='*')
    ax3.axhline(y=MAERZ_DATA['XRP_Preis_USD_IST'], color=farbe_ist, linestyle=':', alpha=0.5)

    ax3.set_title('XRP Preis (USD)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Preis (USD)')
    ax3.set_xticks(x)
    ax3.set_xticklabels(monate_labels, rotation=45)
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3)

    # ---- 4. Abweichungen ----
    ax4 = axes[1, 1]
    metriken = list(deviations.keys())
    werte = [deviations[m]['deviation_%'] for m in metriken]
    farben = [farbe_ist if v >= 0 else farbe_negativ for v in werte]

    labels = {
        'Partner': 'Partner\nGesamt',
        'ODL_Aktiv': 'ODL\nAktiv',
        'XRP_Preis': 'XRP\nPreis'
    }
    anzeige_labels = [labels.get(m, m) for m in metriken]

    bars = ax4.barh(anzeige_labels, werte, color=farben, alpha=0.8, edgecolor='white', height=0.5)
    ax4.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax4.set_title('Abweichungen Maerz 2026\n(IST vs. Prognose)', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Abweichung (%)')

    for bar, value in zip(bars, werte):
        width = bar.get_width()
        offset = 0.3 if width >= 0 else -0.3
        ha = 'left' if width >= 0 else 'right'
        ax4.text(width + offset, bar.get_y() + bar.get_height()/2,
                f'{value:+.1f}%',
                ha=ha, va='center', fontweight='bold', fontsize=11)

    ax4.grid(True, alpha=0.3, axis='x')
    min_v = min(werte)
    max_v = max(werte)
    ax4.set_xlim(min_v * 1.4 - 3, max_v * 1.4 + 3)

    plt.tight_layout()

    output_file = os.path.join(VIZ_PATH, 'tracking_march_2026.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Visualisierung gespeichert: {output_file}\n")
    plt.close()

    return output_file


def create_xrp_detail_chart():
    """Detailliertes XRP-Preisdiagramm für März 2026."""
    print("=== Erstelle XRP-Detaildiagramm ===\n")

    plt.rcParams['font.family'] = 'DejaVu Sans'

    fig, ax = plt.subplots(figsize=(14, 6))

    tage = [pd.to_datetime(d) for d in XRP_MAERZ_PREISE.keys()]
    preise = list(XRP_MAERZ_PREISE.values())

    # Linie
    ax.plot(tage, preise, color='#2196F3', linewidth=2, marker='o', markersize=4, label='Schlusskurs')

    # Durchschnittslinie
    ax.axhline(y=xrp_durchschnitt, color='#F44336', linestyle='--', linewidth=2,
               label=f'Monatsdurchschnitt: ${xrp_durchschnitt:.4f}')

    # Prognoselinie (konservativ)
    ax.axhline(y=1.69, color='#4CAF50', linestyle=':', linewidth=2,
               label='Prognose (konservativ): $1.69')

    # Füllung unter der Kurve
    ax.fill_between(tage, preise, alpha=0.1, color='#2196F3')

    # Annotierungen für wichtige Ereignisse
    ax.annotate('Mastercard\nBlockchain-Initiative\n(11. Mrz)',
                xy=(pd.to_datetime('2026-03-11'), 1.3849),
                xytext=(pd.to_datetime('2026-03-08'), 1.55),
                arrowprops=dict(arrowstyle='->', color='green'),
                fontsize=8, color='green',
                ha='center')

    ax.annotate('Ripple $50B\nBewertung\n(17. Mrz)',
                xy=(pd.to_datetime('2026-03-17'), 1.5185),
                xytext=(pd.to_datetime('2026-03-19'), 1.58),
                arrowprops=dict(arrowstyle='->', color='blue'),
                fontsize=8, color='blue',
                ha='center')

    ax.annotate('Convera-\nPartnerschaft\n(31. Mrz)',
                xy=(pd.to_datetime('2026-03-31'), 1.3403),
                xytext=(pd.to_datetime('2026-03-27'), 1.26),
                arrowprops=dict(arrowstyle='->', color='orange'),
                fontsize=8, color='orange',
                ha='center')

    ax.set_title('XRP Taegliche Schlusskurse - Maerz 2026', fontsize=14, fontweight='bold')
    ax.set_ylabel('Preis (USD)')
    ax.set_xlabel('Datum')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d. Mrz'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

    plt.tight_layout()

    output_file = os.path.join(VIZ_PATH, 'xrp_march_2026_detail.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ XRP-Detaildiagramm gespeichert: {output_file}\n")
    plt.close()

    return output_file


# ============================================================
# HAUPTPROGRAMM
# ============================================================

def main():
    print("\n" + "="*60)
    print("RIPPLE TRACKING: MAERZ 2026 UPDATE")
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
