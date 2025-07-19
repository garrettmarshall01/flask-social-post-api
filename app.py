
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
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoQ2xhc3MiOiJMb2NhdGlvbiIsImF1dGhDbGFzc0lkIjoiSmNqUjYxSU9hWENOb1pmRHpaWm4iLCJzb3VyY2UiOiJJTlRFR1JBVElPTiIsInNvdXJjZUlkIjoiNjg3YWE3NTQwMGJkMWZiNjc1ZGFhNzVmLW1kOTh6MGlzIiwiY2hhbm5lbCI6Ik9BVVRIIiwicHJpbWFyeUF1dGhDbGFzc0lkIjoiSmNqUjYxSU9hWENOb1pmRHpaWm4iLCJvYXV0aE1ldGEiOnsic2NvcGVzIjpbInNvY2lhbHBsYW5uZXIvb2F1dGgud3JpdGUiLCJzb2NpYWxwbGFubmVyL29hdXRoLnJlYWRvbmx5Iiwic29jaWFscGxhbm5lci9wb3N0LndyaXRlIiwic29jaWFscGxhbm5lci9hY2NvdW50LnJlYWRvbmx5Iiwic29jaWFscGxhbm5lci9hY2NvdW50LndyaXRlIiwic29jaWFscGxhbm5lci9jYXRlZ29yeS5yZWFkb25seSJdLCJjbGllbnQiOiI2ODdhYTc1NDAwYmQxZmI2NzVkYWE3NWYiLCJ2ZXJzaW9uSWQiOiI2ODdhYTc1NDAwYmQxZmI2NzVkYWE3NWYiLCJjbGllbnRLZXkiOiI2ODdhYTc1NDAwYmQxZmI2NzVkYWE3NWYtbWQ5OHowaXMifSwiaWF0IjoxNzUyOTY3MzIzLjI5LCJleHAiOjE3NTMwNTM3MjMuMjl9.jvJFrO-57tib0LHyypwB_kIQu88E6DT8nZgLWXthVqAACqsXnJA6Ihpf9eZz2W5lWKMK4Cqe1bgwJgBHh3isD7ZJjc8PmVj1IfhIn-qGZ4LcNJ3o_CArhHbDFPiSYGjAOiuGxajOoQKQyJUydX0Wklgr-WzgHIe4LUZRa-LZjYqKhEmVghJg0_USdPTWtQu4pAfwwzn1iypWoIFbWqhRhswvQ7zPliEv1dCIlRqwr695MWat24WI-uJg1qyT-BNGR1aEkGZ4HAkhgRM84Yq-hQIN85UhmjcJkHB6XJkCczIw1wI4Z6265vO0CZbDZVLNXyXhfrJO02V4o6tejZkfuVQ3I9L0LuvEBRkno3oWnzyZLf2owXtvLiS0aSFQu1KRejfM4durtaVMhE00OZHIhs41gAWDRLptYYp2e4RFhOeI2fLUBQERdBQkQxS8yyD8aBe3ZGPwiKrqfWNAkPYAUqhAUUAnHcdCfHfdEta-bNFtFYpmRUuekqfG8y6da0WD91Mb5jhvfWSFYhItRzAhWS2VJKCh1k5dFBFb3pdCERsEH6F8ICMa-adzW04L4tOeFWCzPkBphEKu0zCjg8s5YFl_Ei3Ii1XFMu2SXW8BMJ6v530khEkawJrFm21bUu2Ei6_arlSmF_BZzYwKAO564RG0CSGUYrQU9UsOe3V2jCE", "token_type": "Bearer", "expires_in": "86399", "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRoQ2xhc3MiOiJMb2NhdGlvbiIsImF1dGhDbGFzc0lkIjoiSmNqUjYxSU9hWENOb1pmRHpaWm4iLCJzb3VyY2UiOiJJTlRFR1JBVElPTiIsInNvdXJjZUlkIjoiNjg3YWE3NTQwMGJkMWZiNjc1ZGFhNzVmLW1kOTh6MGlzIiwiY2hhbm5lbCI6Ik9BVVRIIiwicHJpbWFyeUF1dGhDbGFzc0lkIjoiSmNqUjYxSU9hWENOb1pmRHpaWm4iLCJvYXV0aE1ldGEiOnsic2NvcGVzIjpbInNvY2lhbHBsYW5uZXIvb2F1dGgud3JpdGUiLCJzb2NpYWxwbGFubmVyL29hdXRoLnJlYWRvbmx5Iiwic29jaWFscGxhbm5lci9wb3N0LndyaXRlIiwic29jaWFscGxhbm5lci9hY2NvdW50LnJlYWRvbmx5Iiwic29jaWFscGxhbm5lci9hY2NvdW50LndyaXRlIiwic29jaWFscGxhbm5lci9jYXRlZ29yeS5yZWFkb25seSJdLCJjbGllbnQiOiI2ODdhYTc1NDAwYmQxZmI2NzVkYWE3NWYiLCJ2ZXJzaW9uSWQiOiI2ODdhYTc1NDAwYmQxZmI2NzVkYWE3NWYiLCJjbGllbnRLZXkiOiI2ODdhYTc1NDAwYmQxZmI2NzVkYWE3NWYtbWQ5OHowaXMifSwiaWF0IjoxNzUyOTY3MzIzLjI5NywiZXhwIjoxNzg0NTAzMzIzLjI5NywidW5pcXVlSWQiOiJiNTU1MjViOS1iMzIzLTRiNTEtODQzYi1kZGZiNmVjZmQ3NzEiLCJ2IjoiMiJ9.AGNLnUqHmtt2mcHIlEqXY0Um_7h6niZJ1aq1wECtMCtywkwEBvY4_4DuT3ckkaGbhRxdqAfthWe5gvJZaz5XF1qV-uhTRpfVyFz0KqtivsYRE0dnPz8XD3YhyXSfQkWOEJMNB-XpjXpLvfh7sf7aD8eJEoaS_VfbBIgOxiwFx_LkgUdsJHhiEwXpRTXn4DcwxDFbC7UGXS0Z5X0Hk26lRoLY1OWnA_fOSEKzCds2YcNY2Qpo7K8jLAdfgJlrNj-Z90A2TTORgYW4MmPWDo0l7O6lXZBrRGvxGHWSwkMAOAHC5EFDBAhwnW-zzrPKlb3pFrBJpyW-wFlMdOhUnydBLnq4LLqSUFEHGjTJLNn4DKXQLqfjTLEciQQZpVaTYHkZ6erxzP4z4YOphyGN6e3ydAdLS5w6J4jDRuaqkscat1jAyidDPeLaeC9q2jD-Nmdo2X2kmwcasKnguA68hG__aMJrknyzX5Vz_8nciq2ISVekszo9ph_-a8cX5qX-3oWPQktDxkm-jyV45SG8cOWxV8kW9Jv1R9lSR9xxZUwb9EBzQUYq6RF0LEaAoFyf2tZ-Cu__xXsHHO0E8_8SJFYN84WWVs4pPBFCPQfz-_-GJ9UNec18VCOKTo595qZ05RtJk1C0pZEHripKX0LCxdGA7M0riq0tEbbc7yefYqPrqpw",  # Replace with env or secure storage
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
