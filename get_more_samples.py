import urllib.request
import urllib.parse
import json
import os

phrases = [
    "Ja-arigatou.ogg",
    "Ja-ohayou_gozaimasu.ogg",
    "Ja-hajimemashite.ogg",
    "Ja-sayonara.ogg",
]

for phrase in phrases:
    info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles=File:{urllib.parse.quote(phrase)}&prop=imageinfo&iiprop=url&format=json"
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
                print(f"Found {phrase} -> {url}")
                req2 = urllib.request.Request(
                    url, headers={"User-Agent": "KoeBridge-Test/1.0"}
                )
                local_path = f"sample_{phrase}"
                with (
                    urllib.request.urlopen(req2, timeout=10) as r2,
                    open(local_path, "wb") as f,
                ):
                    f.write(r2.read())
                print(f"Saved {local_path} ({os.path.getsize(local_path)} bytes)")
    except Exception as e:
        print(f"Error for {phrase}: {e}")
