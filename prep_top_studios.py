"""
prep_top_studios.py
Outputs a clean top-15 studios CSV sorted by total reviews.
No window/rank transform needed in Vega-Lite.

OUTPUT: data/steam_top15_studios.csv
"""
import pandas as pd

df = pd.read_csv('data/steam_au_studios_summary.csv')
top = df.sort_values('total_reviews', ascending=False).head(15)
top = top[['studio_name', 'n_games', 'total_reviews', 'avg_review_pct_positive', 'state']]
top.to_csv('data/steam_top15_studios.csv', index=False)

print(f"WROTE: data/steam_top15_studios.csv ({len(top)} studios)")
print(top.to_string(index=False))
