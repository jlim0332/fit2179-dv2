"""
prep_studio_genre.py

Builds a CSV ready for the studio-genre ribbon chart:
- Takes top 20 AU studios (by total reviews)
- For each studio, counts games per genre (one game can be multiple genres)
- Outputs long-format CSV: studio_name, genre, n_games

USAGE:
    Run from project root (where 'data/' folder is).
        python prep_studio_genre.py
"""

import pandas as pd

# Load
games = pd.read_csv('data/steam_au_games.csv')
studios = pd.read_csv('data/steam_au_studios_summary.csv')

print(f"Loaded {len(games)} games, {len(studios)} studios")

# Pick top 20 studios by total reviews
top_studios = studios.sort_values('total_reviews', ascending=False).head(20)['studio_name'].tolist()
print(f"\nTop 20 studios by reviews:")
for i, s in enumerate(top_studios, 1):
    print(f"  {i:2}. {s}")

# Filter games to just these studios
top_games = games[games['studio_name'].isin(top_studios)].copy()
print(f"\nGames belonging to top 20 studios: {len(top_games)}")

# Explode genres
def explode_genres(row):
    if not isinstance(row['Genres'], str):
        return []
    return [g.strip() for g in row['Genres'].split(',') if g.strip()]

# Build long format: one row per (studio, genre) game
rows = []
for _, game in top_games.iterrows():
    genres = explode_genres(game)
    for g in genres:
        rows.append({'studio_name': game['studio_name'], 'genre': g})

long_df = pd.DataFrame(rows)

# Aggregate: count games per (studio, genre)
counts = long_df.groupby(['studio_name', 'genre']).size().reset_index(name='n_games')

# Drop very small genres (only 1 game across the whole dataset) to reduce clutter
genre_totals = counts.groupby('genre')['n_games'].sum().reset_index(name='genre_total')
keep_genres = genre_totals[genre_totals['genre_total'] >= 2]['genre'].tolist()
counts = counts[counts['genre'].isin(keep_genres)]

# Save
counts = counts.sort_values(['studio_name', 'n_games'], ascending=[True, False])
counts.to_csv('data/steam_au_studio_genre.csv', index=False)

# Report
print(f"\nFinal output: {len(counts)} rows")
print(f"\nGenres kept ({len(keep_genres)}): {sorted(keep_genres)}")
print(f"\nSample of output:")
print(counts.head(20).to_string(index=False))
print(f"\nWROTE: data/steam_au_studio_genre.csv")
