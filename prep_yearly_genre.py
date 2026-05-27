"""
prep_yearly_genre.py

Builds CSV for the stacked area chart 6:
- For each year, counts AU games per genre
- One game can belong to multiple genres (counted in each)
- Drops the smallest genres so the stack stays readable

OUTPUT: data/steam_au_yearly_genre.csv
Columns: release_year, genre, n_games

USAGE:
    Run from project root.
        python prep_yearly_genre.py
"""

import pandas as pd

games = pd.read_csv('data/steam_au_games.csv')
print(f"Loaded {len(games)} games")

# Keep only rows with a valid release_year
games = games.dropna(subset=['release_year']).copy()
games['release_year'] = games['release_year'].astype(int)

# Explode genres
rows = []
for _, game in games.iterrows():
    if not isinstance(game['Genres'], str):
        continue
    for g in [x.strip() for x in game['Genres'].split(',') if x.strip()]:
        rows.append({'release_year': game['release_year'], 'genre': g})

long_df = pd.DataFrame(rows)
print(f"  exploded to {len(long_df)} (year, genre) pairs")

# Aggregate
counts = long_df.groupby(['release_year', 'genre']).size().reset_index(name='n_games')

# Drop genres that are too rare to show up meaningfully — bottom genres collapsed into nothing
genre_totals = counts.groupby('genre')['n_games'].sum().reset_index(name='total')
keep = genre_totals[genre_totals['total'] >= 5]['genre'].tolist()
print(f"\nKeeping {len(keep)} genres (>= 5 games total):")
for g in sorted(keep):
    total = int(genre_totals[genre_totals['genre'] == g]['total'].iloc[0])
    print(f"  - {g}: {total}")

counts = counts[counts['genre'].isin(keep)]

# Filter year range to keep chart readable
counts = counts[(counts['release_year'] >= 2007) & (counts['release_year'] <= 2025)]
counts = counts.sort_values(['release_year', 'genre'])

counts.to_csv('data/steam_au_yearly_genre.csv', index=False)
print(f"\nWROTE: data/steam_au_yearly_genre.csv  ({len(counts)} rows)")
print(f"\nSample:")
print(counts.head(20).to_string(index=False))
