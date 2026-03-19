import sqlite3
import json
import os
import re

DB_PATH = "ron.db"
API_DIR = "public/api"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def clean_text(text):
    if not text:
        return ""
    # Remove basic formatting marks or empty spaces if needed for search
    return text.replace('\n', ' ').strip()

def export_api():
    ensure_dir(API_DIR)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    print("Exporting categories...")
    cursor.execute("SELECT * FROM categories WHERE IsVisible=1 ORDER BY Number")
    categories = cursor.fetchall()
    with open(f"{API_DIR}/categories.json", "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False)

    ensure_dir(f"{API_DIR}/category")
    ensure_dir(f"{API_DIR}/subindex")
    ensure_dir(f"{API_DIR}/lines")

    # Keep track of search items
    search_index = []

    print("Exporting category contents...")
    for cat in categories:
        cat_id = cat['Id']
        cursor.execute("SELECT * FROM subindex WHERE CategoryId=? AND Level=0 AND IsVisible=1 ORDER BY Number", (cat_id,))
        items = cursor.fetchall()
        with open(f"{API_DIR}/category/{cat_id}.json", "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False)

    print("Exporting all subindex children and lines...")
    cursor.execute("SELECT * FROM subindex WHERE IsVisible=1")
    all_subindices = cursor.fetchall()

    for item in all_subindices:
        sub_id = item['Id']

        # If it has children, export the children
        if item['HasChildren']:
            cursor.execute("SELECT * FROM subindex WHERE ParentId=? AND Level>0 AND IsVisible=1 ORDER BY Number", (sub_id,))
            children = cursor.fetchall()
            with open(f"{API_DIR}/subindex/{sub_id}.json", "w", encoding="utf-8") as f:
                json.dump(children, f, ensure_ascii=False)

        # Export lines for this subindex
        cursor.execute("""
            SELECT l.*
            FROM lines l
            JOIN linesmetadata lm ON l.Id = lm.LinesId
            WHERE lm.SubindexId = ?
            ORDER BY lm.Number
        """, (sub_id,))
        lines = cursor.fetchall()

        # Write lines.json
        with open(f"{API_DIR}/lines/{sub_id}.json", "w", encoding="utf-8") as f:
            json.dump(lines, f, ensure_ascii=False)

        # Add to search index if it has lines OR if it has children (so users can search for categories)
        if len(lines) > 0 or item['HasChildren']:
            # Combine text for search
            combined_arabic = []
            combined_eng = []
            combined_ur = []
            combined_ru = []
            combined_gu = []

            for line in lines:
                # Concatenate all arabic texts from ArabicText1 to ArabicText20
                for i in range(1, 21):
                    val = line.get(f'ArabicText{i}')
                    if val: combined_arabic.append(clean_text(val))

                if line.get('English'): combined_eng.append(clean_text(line['English']))
                if line.get('Urdu'): combined_ur.append(clean_text(line['Urdu']))
                if line.get('RUrdu'): combined_ru.append(clean_text(line['RUrdu']))
                if line.get('Gujarati'): combined_gu.append(clean_text(line['Gujarati']))

            search_item = {
                "id": sub_id,
                "type": "subindex" if item['HasChildren'] else "lines",
                "cat_id": item['CategoryId'],
                "title_en": item.get('EnglishIndexName', ''),
                "title_ur": item.get('UrduIndexName', ''),
                "title_ru": item.get('RUrduIndexName', ''),
                "title_gu": item.get('GujaratiIndexName', ''),
                "text_ar": " ".join(combined_arabic),
                "text_en": " ".join(combined_eng),
                "text_ur": " ".join(combined_ur),
                "text_ru": " ".join(combined_ru),
                "text_gu": " ".join(combined_gu)
            }
            search_index.append(search_item)

    print("Exporting search index...")
    # Keep search index compact
    with open(f"{API_DIR}/search_index.json", "w", encoding="utf-8") as f:
        # no formatting to save space
        json.dump(search_index, f, ensure_ascii=False, separators=(',', ':'))

    print("Done! All static APIs generated.")

if __name__ == "__main__":
    export_api()
