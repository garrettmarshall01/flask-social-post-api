
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

app = Flask(__name__)

def extract_main_image(page_url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ImageScraper/1.0)"}
    resp = requests.get(page_url, headers=headers, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    for attr, name in [('property', 'og:image'), ('name', 'twitter:image'), ('name', 'image')]:
        tag = soup.find("meta", {attr: name})
        if tag and tag.get("content"):
            return urljoin(page_url, tag["content"])

    img = soup.find("img")
    if img and img.get("src"):
        return urljoin(page_url, img["src"])

    return None

@app.route("/create-social-post", methods=["POST"])
def create_social_post():
    data = request.get_json()
    source_url = data.get("url")
    category_id = data.get("categoryId")
    if not category_id:
        return jsonify({"error": "Missing 'categoryId'"}), 400
    if not source_url:
        return jsonify({"error": "Missing 'url'"}), 400

    try:
        image_url = extract_main_image(source_url)
        if not image_url:
            return jsonify({"error": "No image found at URL"}), 404
    except Exception as e:
        return jsonify({"error": f"Error extracting image: {str(e)}"}), 500

    json_data = {
        "userId": "I9VZlLtgWN8UYrWRxgi6",
        "accountIds": [
            "67894a07ff96da90cbac088f_JcjR61IOaXCNoZfDzZZn_F4B2LFRy78_profile"
        ],
        "summary": data.get("summary", "Hello World"),
        "media": [
            {
                "url": image_url,
                "caption": data.get("caption", "Auto-generated image"),
            }
        ],
        "status": data.get("status", "draft"),
        "followUpComment": source_url,
        "type": "post",
        "categoryId": data["categoryId"],
    }

    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoQ2xhc3MiOiJMb2NhdGlvbiIsImF1dGhDbGFzc0lkIjoiSmNqUjYxSU9hWENOb1pmRHpaWm4iLCJzb3VyY2UiOiJJTlRFR1JBVElPTiIsInNvdXJjZUlkIjoiNjg3YWE3NTQwMGJkMWZiNjc1ZGFhNzVmLW1kOTh6MGlzIiwiY2hhbm5lbCI6Ik9BVVRIIiwicHJpbWFyeUF1dGhDbGFzc0lkIjoiSmNqUjYxSU9hWENOb1pmRHpaWm4iLCJvYXV0aE1ldGEiOnsic2NvcGVzIjpbInNvY2lhbHBsYW5uZXIvb2F1dGgud3JpdGUiLCJzb2NpYWxwbGFubmVyL29hdXRoLnJlYWRvbmx5Iiwic29jaWFscGxhbm5lci9wb3N0LndyaXRlIiwic29jaWFscGxhbm5lci9hY2NvdW50LnJlYWRvbmx5Iiwic29jaWFscGxhbm5lci9hY2NvdW50LndyaXRlIiwic29jaWFscGxhbm5lci9jYXRlZ29yeS5yZWFkb25seSJdLCJjbGllbnQiOiI2ODdhYTc1NDAwYmQxZmI2NzVkYWE3NWYiLCJ2ZXJzaW9uSWQiOiI2ODdhYTc1NDAwYmQxZmI2NzVkYWE3NWYiLCJjbGllbnRLZXkiOiI2ODdhYTc1NDAwYmQxZmI2NzVkYWE3NWYtbWQ5OHowaXMifSwiaWF0IjoxNzUzMDMyOTM5LjA5MywiZXhwIjoxNzg0NTY4OTM5LjA5MywidW5pcXVlSWQiOiI4MjVhZTY0My0yZDM5LTRmYzItOGMxYi0yOTAzMDBmNDk0MmQiLCJ2IjoiMiJ9.axsNyBsCEQdElN_KWdOQ89Wm6vAaVRaZX3--fkC0Yu4uSGBJq5_Xjw_a6q9RRNeertO0Q8cGtE8Z4IF6EuyEkrMt05IJC0kvmn-5RKD2-0NV3Jav_jv50QwFk6brkTpxRMw8M3-bJrABVPNVloXw0YN2wCDVKRuEUhU_SK_j4VHvC0SVxJzjFzdTl84RQk27muNEW8ywD2jLwEMuxPi0gfU1xEUsm1NVWcNk5GxSTY7O-9SgtBskD2hSEnPc_9ix3YTrH_QQbqhVsH_-LzAxce4jTH5otL-HK6gIo9uD6dVaWASuZUDbsPZGrxGXQE33YZ-DNJXC1GpKQnhgbKabXtfTNAbsox5G6_Z40o2nzLXocz1pmaaTi1t-Ir5Qq4POxNfCvtsqCOfelKZNVesRQwFMNOswjqoMikaDrczbHeRAl_XoiK4Ao8Mzr5HNn9hIbCIuLm6_h5XBgcDcUr1R0ORCxfG5MpV907CE-fVM4uLvfCuwhtoq3y-osysb-m5MkVEa6JKBowHwZnzb0dQ5gtcmJogBjJwB4IE3ZWbOZf2xpospvwWoZZajWElfbdlVEO0CTHVhJvVVybmOqsIumjQUmEL7P3mEQhW0FKtyiwQcXod_cI94jiuVZGuTK8YsO1K8YFdYjDgl0AgA-pTqzRknf7BPRw6LtdU2s7O3Iv0",  # Replace with env or secure storage
        "Content-Type": "application/json",
        "Version": "2021-07-28",
    }

    try:
        response = requests.post(
            "https://services.leadconnectorhq.com/social-media-posting/JcjR61IOaXCNoZfDzZZn/posts",
            headers=headers,
            json=json_data,
        )
        return jsonify({
            "status_code": response.status_code,
            "response": response.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
