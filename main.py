import base64
import os
import openai
import json
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://comicvault-2854f.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/scan_comic/")
async def scan_comic(file: UploadFile = File(...)):
    image_bytes = await file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    prompt = (
        "You are Comic Scout, an expert comic grader. Analyze this comic book cover image and return ONLY valid JSON with these keys: "
        "title, issue, grade, defects, value_usd, rarity, notes. "
        "If you can't identify something, leave that value blank. Respond only in pure JSON with no other text."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image", "image": {"data": base64_image}}
                    ]
                }
            ],
            max_tokens=1000
        )

        analysis = response.choices[0].message.content
        print("AI RAW RESPONSE:", analysis)

        # Try to parse the AI's response as JSON
        try:
            data = json.loads(analysis)
        except Exception:
            # If parsing fails, just return the raw string in "notes"
            data = {
                "title": "",
                "issue": "",
                "grade": "",
                "defects": "",
                "value_usd": "",
                "rarity": "",
                "notes": analysis
            }

        return JSONResponse(content=data)

    except Exception as e:
        return JSONResponse(content={"error": str(e)})
