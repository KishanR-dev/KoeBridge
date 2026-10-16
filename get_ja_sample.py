import urllib.request
import urllib.parse
import json
import os

search_terms = [
    "Ja-konnichiwa.ogg",
    "Ja-arigatou.ogg",
    "Ja-ohayou.ogg",
    "Ja-sayounara.ogg",
    "Ja-nihon.ogg",
]

for term in search_terms:
    info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles=File:{urllib.parse.quote(term)}&prop=imageinfo&iiprop=url&format=json"
    try:
        req = urllib.request.Request(
            info_url, headers={"User-Agent": "KoeBridge-Test/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read().decode())
            pages = d["query"]["pages"]
            first_pg = list(pages.values())[0]
            if "imageinfo" in first_pg:
                url = first_pg["imageinfo"][0]["url"]
                print(f"Found {term} -> {url}")
                req2 = urllib.request.Request(
                    url, headers={"User-Agent": "KoeBridge-Test/1.0"}
                )
                with (
                    urllib.request.urlopen(req2, timeout=10) as r2,
                    open("sample_ja.ogg", "wb") as f,
                ):
                    f.write(r2.read())
                print(
                    f"Successfully saved {term} to sample_ja.ogg ({os.path.getsize('sample_ja.ogg')} bytes)"
                )
                break
    except Exception as e:
        print(f"Error checking {term}: {e}")
