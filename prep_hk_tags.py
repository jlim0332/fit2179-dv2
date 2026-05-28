"""
prep_hk_tags.py

Explodes Hollow Knight's Steam tags into a CSV for the tag-bubble chart.
Steam lists tags roughly in popularity order, so we weight each tag by its
position (first tag = highest weight). This gives bubble sizes that reflect
how defining each tag is.

OUTPUT: data/hk_tags.csv
Columns: tag, rank, weight

USAGE:
    python prep_hk_tags.py   (run from project root)
"""

import pandas as pd

df = pd.read_csv('data/steam_au_games.csv')

# Get Hollow Knight's tag string (the base game, not Silksong)
hk = df[(df['Name'] == 'Hollow Knight')]
tag_string = hk.iloc[0]['Tags']

tags = [t.strip() for t in tag_string.split(',') if t.strip()]
print(f"Hollow Knight has {len(tags)} tags")

rows = []
n = len(tags)
for i, tag in enumerate(tags):
    rank = i + 1
    # Weight: first tag gets highest weight, decreasing down the list.
    # Using a gentle decay so later tags are still visible.
    weight = round(100 * (n - i) / n, 1)
    rows.append({'tag': tag, 'rank': rank, 'weight': weight})

out = pd.DataFrame(rows)
out.to_csv('data/hk_tags.csv', index=False)

print(f"\nWROTE: data/hk_tags.csv ({len(out)} tags)")
print(out.to_string(index=False))
