import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request, send_from_directory

BASE = Path(__file__).resolve().parent
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024


def safe_ikea_url(value: str) -> bool:
    try:
        host = (urlparse(value).hostname or "").lower()
        return host == "ikea.com" or host.endswith(".ikea.com")
    except ValueError:
        return False


def walk(obj):
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from walk(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from walk(value)


def number(value):
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        match = re.search(r"\d+(?:[.,]\d+)?", value)
        if match:
            return float(match.group().replace(",", "."))
    return None


def from_json(soup):
    name = image = None
    dimensions = {}
    for tag in soup.select('script[type="application/ld+json"], script#__NEXT_DATA__'):
        try:
            payload = json.loads(tag.string or tag.get_text())
        except (ValueError, TypeError):
            continue
        for item in walk(payload):
            item_name = str(item.get("name", ""))
            key = item_name.lower().strip()
            value = number(item.get("value") or item.get("valueMetric") or item.get("valueText"))
            unit = str(item.get("unitCode") or item.get("unitText") or "").lower()
            if value and key in {"width", "depth", "height", "largeur", "profondeur", "hauteur"}:
                if unit in {"m", "mtr"}: value *= 100
                if unit in {"mm", "mmt"}: value /= 10
                dimensions[{"largeur":"width", "profondeur":"depth", "hauteur":"height"}.get(key, key)] = value
            if not name and item.get("@type") == "Product":
                name = item.get("name")
                raw_image = item.get("image")
                image = raw_image[0] if isinstance(raw_image, list) else raw_image
    return name, image, dimensions


def from_text(soup):
    text = " ".join(soup.stripped_strings)
    labels = {
        "width": r"(?:Width|Largeur)\s*[:：]?\s*(\d+(?:[.,]\d+)?)\s*cm",
        "depth": r"(?:Depth|Profondeur|Length|Longueur)\s*[:：]?\s*(\d+(?:[.,]\d+)?)\s*cm",
        "height": r"(?:Height|Hauteur)\s*[:：]?\s*(\d+(?:[.,]\d+)?)\s*cm",
    }
    return {key: float(m.group(1).replace(",", ".")) for key, pattern in labels.items() if (m := re.search(pattern, text, re.I))}


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/assets/<path:name>")
def assets(name):
    return send_from_directory(BASE / "assets", name)


@app.post("/api/ikea")
def ikea_product():
    url = (request.json or {}).get("url", "").strip()
    if not safe_ikea_url(url):
        return jsonify(error="Please use a product link from ikea.com."), 400
    try:
        response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0 FloorPlanner/1.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        name, image, dims = from_json(soup)
        dims.update({k: v for k, v in from_text(soup).items() if k not in dims})
        title = soup.title.get_text(" ", strip=True) if soup.title else "IKEA furniture"
        name = name or re.sub(r"\s*-\s*IKEA.*$", "", title, flags=re.I)
        if "width" not in dims or "depth" not in dims:
            return jsonify(error="I found the product, but IKEA did not expose its footprint. Enter width and depth manually.", name=name, image=image), 422
        return jsonify(name=name, image=image, width=dims["width"], depth=dims["depth"], height=dims.get("height"), source=url)
    except requests.RequestException:
        return jsonify(error="IKEA could not be reached. You can still enter the dimensions manually."), 502


@app.get("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")), debug=os.getenv("FLASK_DEBUG") == "1")
