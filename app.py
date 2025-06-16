from flask import Flask, request, jsonify
from grader import grade_comic
from scraper import get_market_prices

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ ComicVault AI API is running. Use /api/grade for POST."
    
@app.route("/api/grade", methods=["POST"])
def grade():
    data = request.json
    title = data.get("title")
    issue = data.get("issue")
    image_data = data.get("image")
    grade_result, flaws = grade_comic(image_data)
    pricing = get_market_prices(title, issue, grade_result)
    return jsonify({"title": title, "issue": issue, "grade": grade_result, "flaws": flaws, "pricing": pricing})

if __name__ == "__main__":
    app.run(debug=True)

