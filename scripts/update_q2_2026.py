import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Pfade definieren
csv_path = 'data/tracking_data.csv'
viz_dir = 'visualizations'
os.makedirs(viz_dir, exist_ok=True)

# Daten laden
df = pd.read_csv(csv_path)

# Neue Daten für April 2026
april_data = {
    'Monat': '2026-04',
    'Partner_IST': 313,
    'ODL_Aktiv_IST': 125,
    'XRP_Preis_USD_IST': 1.3811,
    'Datenquelle_Partner': 'DXE Technology, Deutsche Bank (2026 Deals)',
    'Datenquelle_ODL_Volumen': 'Nicht öffentlich verfügbar',
    'Datenquelle_XRP_Preis': 'CoinMarketCap (Monatsdurchschnitt)',
    'Erfasst_am': datetime.now().strftime('%Y-%m-%d')
}

# Neue Daten für Mai 2026
mai_data = {
    'Monat': '2026-05',
    'Partner_IST': 315,
    'ODL_Aktiv_IST': 126,
    'XRP_Preis_USD_IST': 1.3867,
    'Datenquelle_Partner': 'Société Générale, JPMorgan (2026 Deals)',
    'Datenquelle_ODL_Volumen': 'Nicht öffentlich verfügbar',
    'Datenquelle_XRP_Preis': 'CoinMarketCap (Monatsdurchschnitt)',
    'Erfasst_am': datetime.now().strftime('%Y-%m-%d')
}

# Zeilen aktualisieren statt neu hinzufügen (da 2026-04/05 bereits als leere Zeilen existieren)
for data in [april_data, mai_data]:
    mask = df['Monat'] == data['Monat']
    if mask.any():
        for key, value in data.items():
            df.loc[mask, key] = value
    else:
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

# Speichern
df.to_csv(csv_path, index=False)
print(f"Daten für April und Mai 2026 in {csv_path} gespeichert.")

# Visualisierung erstellen
plt.figure(figsize=(12, 8))

# Subplot 1: Partner & ODL Nutzer
plt.subplot(2, 1, 1)
plt.plot(df['Monat'], df['Partner_IST'], marker='o', label='RippleNet Partner (IST)')
plt.plot(df['Monat'], df['ODL_Aktiv_IST'], marker='s', label='ODL Nutzer (IST)')
plt.title('RippleNet Adoption & ODL Usage (2026)')
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 2: XRP Preis
plt.subplot(2, 1, 2)
plt.plot(df['Monat'], df['XRP_Preis_USD_IST'], marker='o', color='green', label='XRP Preis (IST)')
plt.title('XRP Preisentwicklung (IST)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{viz_dir}/tracking_may_2026.png')
print(f"Visualisierung gespeichert in {viz_dir}/tracking_may_2026.png")

# XRP Detail Chart für Mai
plt.figure(figsize=(10, 6))
mai_prices = [
    1.3313, 1.3383, 1.3283, 1.3135, 1.3062, 1.3277, 1.3494, 1.3500, 1.3575, 1.3337,
    1.3721, 1.3654, 1.3606, 1.3892, 1.4009, 1.4140, 1.4337, 1.4841, 1.4263, 1.4361,
    1.4768, 1.4728, 1.4201, 1.4183, 1.3871, 1.4247, 1.4131, 1.3920, 1.3876, 1.3932, 1.3847
]
plt.plot(range(1, 32), mai_prices, marker='.', color='blue')
plt.title('XRP Preisverlauf Mai 2026 (Täglich)')
plt.xlabel('Tag im Mai')
plt.ylabel('Preis in USD')
plt.grid(True, alpha=0.3)
plt.savefig(f'{viz_dir}/xrp_may_2026_detail.png')
print(f"Detail-Visualisierung gespeichert in {viz_dir}/xrp_may_2026_detail.png")
