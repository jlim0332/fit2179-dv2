"""
prep_butterfly.py

Reshapes steam_genres_au_vs_global.csv into long format for a butterfly chart.
Each genre gets TWO rows: one for AU (negative value, plots left) and one for
Global (positive value, plots right). Using one table + one chart avoids the
hconcat row-sync problem.

OUTPUT: data/steam_genre_butterfly.csv
Columns: genre, side, pct, signed_pct, au_pct (for sort)

USAGE:
    python prep_butterfly.py   (run from project root)
"""

import pandas as pd

df = pd.read_csv('data/steam_genres_au_vs_global.csv')

# Keep only genres with AU share >= 1%
df = df[df['au_pct'] >= 1].copy()

rows = []
for _, r in df.iterrows():
    # AU side — negative so it plots to the LEFT of zero
    rows.append({
        'genre': r['genre'],
        'side': 'Australia',
        'pct': r['au_pct'],
        'signed_pct': -r['au_pct'],
        'au_pct_sort': r['au_pct']
    })
    # Global side — positive, plots RIGHT
    rows.append({
        'genre': r['genre'],
        'side': 'All of Steam',
        'pct': r['global_pct'],
        'signed_pct': r['global_pct'],
        'au_pct_sort': r['au_pct']
    })

out = pd.DataFrame(rows)
out.to_csv('data/steam_genre_butterfly.csv', index=False)

print(f"WROTE: data/steam_genre_butterfly.csv  ({len(out)} rows)")
print(out.to_string(index=False))
