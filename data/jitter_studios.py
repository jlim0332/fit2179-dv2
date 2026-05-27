"""
jitter_studios.py

Reads steam_au_studios_summary.csv, joins with city coordinates,
adds a small random offset to each studio's lat/lng so they spread
visibly on the map (rather than stacking at the city centre).

Outputs: steam_au_studios_summary.csv (overwrites the existing file)
         — same columns + 2 new ones: lat, lng

USAGE:
    Put this in the same folder as au_cities.csv and steam_au_studios_summary.csv
    then run:
        python jitter_studios.py
"""

import pandas as pd
import random

random.seed(42)  # fixed seed so jitter is consistent each run

# Load data
studios = pd.read_csv('steam_au_studios_summary.csv')
cities = pd.read_csv('au_cities.csv')

print(f"Loaded {len(studios)} studios and {len(cities)} cities")

# Make a quick lookup: city -> (lat, lng)
city_coords = {row['city']: (row['latitude'], row['longitude']) for _, row in cities.iterrows()}

# Function to generate a random offset within a small radius around a centre
# Larger cities (Melbourne, Sydney) get a bigger spread because they have more studios
def spread_for_city(city, n_studios_in_city):
    # Base spread is 0.4 degrees. If a city has lots of studios, spread wider.
    base = 0.4
    return base + min(n_studios_in_city, 30) * 0.02  # caps growth at ~30 studios

# Count studios per city to size the spread radius
city_counts = studios['city'].value_counts().to_dict()

# Add lat/lng with jitter
lats = []
lngs = []
for _, row in studios.iterrows():
    city = row['city']
    if not isinstance(city, str) or city not in city_coords:
        lats.append(None)
        lngs.append(None)
        continue
    base_lat, base_lng = city_coords[city]
    spread = spread_for_city(city, city_counts.get(city, 1))
    # Random offset within the spread, evenly across lat/lng
    lat_offset = (random.random() - 0.5) * spread
    lng_offset = (random.random() - 0.5) * spread
    lats.append(base_lat + lat_offset)
    lngs.append(base_lng + lng_offset)

studios['lat'] = lats
studios['lng'] = lngs

# Save back
studios.to_csv('steam_au_studios_summary.csv', index=False)

# Report
print(f"\nUpdated steam_au_studios_summary.csv")
print(f"  - Added 'lat' and 'lng' columns to {studios['lat'].notna().sum()} studios")
print(f"  - {studios['lat'].isna().sum()} studios had no matching city (left blank)")
print("\nSample of jittered locations:")
print(studios[['studio_name', 'city', 'lat', 'lng']].head(15).to_string(index=False))
