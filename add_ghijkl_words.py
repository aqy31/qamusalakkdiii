import pandas as pd
import json
import re

# Read Excel file (G.H.I.J.K.L) — data is taken verbatim, nothing is altered
df = pd.read_excel(' G.H .I.J.K.L.xlsx', header=None)
df = df.astype(object).where(pd.notnull(df), None)


def clean(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def split_sign(sign):
    """Split '167 (GABA-RAḪ)' -> labat '167', sumerian '(GABA-RAḪ)'.
    The two parts concatenated reproduce the original text exactly."""
    if not sign:
        return "", ""
    i = sign.find('(')
    if i == -1:
        if re.match(r'^[\d\s,]+$', sign):
            return sign, ""
        return "", sign
    return sign[:i].strip(), sign[i:].strip()


def make_reading(ar, sign):
    labat, sumerian = split_sign(sign)
    return {"arabic": ar, "sumerian": sumerian, "cuneiform": "", "labat": labat}


entries = []
current_entry = None

for idx, row in df.iterrows():
    if idx == 0:  # header row
        continue
    akk, ar, sign = clean(row[0]), clean(row[1]), clean(row[2])
    ar2, sign2 = clean(row[3]), clean(row[4])

    if akk:
        if current_entry is not None:
            entries.append(current_entry)
        base_id = re.sub(r'[^a-zA-Z0-9_]', '', akk.lower().replace(' ', '_'))
        current_entry = {
            "id": f"{base_id}_ghijkl_{len(entries)}",
            "nameAr": ar,
            "nameAkk": akk,
            "sumerianReadings": [],
            "keywords": [ar] if ar else []
        }

    if current_entry is None:
        continue

    if ar or sign:
        current_entry["sumerianReadings"].append(make_reading(ar, sign))
        if not akk and ar and ar not in current_entry["keywords"]:
            current_entry["keywords"].append(ar)

    if ar2 or sign2:
        current_entry["sumerianReadings"].append(make_reading(ar2, sign2))
        if ar2 and ar2 not in current_entry["keywords"]:
            current_entry["keywords"].append(ar2)

if current_entry is not None:
    entries.append(current_entry)

new_items_str = ""
for e in entries:
    new_items_str += ",\n" + json.dumps(e, ensure_ascii=False, indent=4).replace('\n', '\n    ')

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = """    }
]
            },

            // ============================================
            // المدن — CITIES"""

replacement = """    }""" + new_items_str + """
]
            },

            // ============================================
            // المدن — CITIES"""

if content.count(target) == 1:
    content = content.replace(target, replacement)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully added {len(entries)} new entries to index.html")
else:
    print("Could not find a unique insertion point in index.html")
