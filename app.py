
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
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoQ2xhc3MiOiJMb2NhdGlvbiIsImF1dGhDbGFzc0lkIjoiSmNqUjYxSU9hWENOb1pmRHpaWm4iLCJzb3VyY2UiOiJJTlRFR1JBVElPTiIsInNvdXJjZUlkIjoiNjg3YWE3NTQwMGJkMWZiNjc1ZGFhNzVmLW1kOTh6MGlzIiwiY2hhbm5lbCI6Ik9BVVRIIiwicHJpbWFyeUF1dGhDbGFzc0lkIjoiSmNqUjYxSU9hWENOb1pmRHpaWm4iLCJvYXV0aE1ldGEiOnsic2NvcGVzIjpbInNvY2lhbHBsYW5uZXIvb2F1dGgud3JpdGUiXSwiY2xpZW50IjoiNjg3YWE3NTQwMGJkMWZiNjc1ZGFhNzVmIiwidmVyc2lvbklkIjoiNjg3YWE3NTQwMGJkMWZiNjc1ZGFhNzVmIiwiY2xpZW50S2V5IjoiNjg3YWE3NTQwMGJkMWZiNjc1ZGFhNzVmLW1kOTh6MGlzIn0sImlhdCI6MTc1Mjg3Mzc0MS41NCwiZXhwIjoxNzUyOTYwMTQxLjU0fQ.Fp4l_AZW6X-7fG5DBqSofJIMY05jR9o2josCkETuak40I1RrSQVepuCcZdu424aVD-Cx68eVtmrAHT5bUi84S1zkOtKbPQy_0Nns4_-NLef7Q46-irgVyu9P7OKBkua0thgppwHIQiP0hpAZPLhxuxObO3t36foh0gJtlB5CTy8dlviNi8fAy6Bq2J4dopaa79o_pmSH4oSy6wZbdAW3KULw5b1X69kBaFFJXYHABpIWS8s2FViyWOuGlHJwEpoMuUQ60h7kr3VEZoK2Ip8cjy660MNkw1wYTQHW8vtFlQKYnWwm6eVS8bB2j-vi6j1Agu6WtuvDTrfmOuJRtRB3_a8mFJFPWV3KPK9wgwI4dU1J4S-FoBUPYOkL4VLowePmH116fEpT7E9Lgn6mFi14nTJW7CioEFg0XFwQY1PuHCMjeBOnrEUri1DHwhRRM_9-eRBjAwtU93DMV1ZSI2wVJ6UON6OXHiFjeFWqWnjWahn3R6O_6YUPjQGjjmTDoooqoD8zw7FibBhmeZkM-4CYTKq-UDGzghVv48DWyd9O1XIAiFIPZ94FO_TB_V9e3G20-NBB_sWYr66k-bBVsoOCXCOXzyb_CVwp7P9C2APrd5vbK1YxVTDgg55CPxxv1C2scpnApkia7QVszJQh-7N7_G3r_zzjy3dHePdXSY4tW_Y",  # Replace with env or secure storage
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
