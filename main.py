import base64
import os
import openai
import json
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

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
    image_data_url = f"data:{file.content_type};base64,{base64_image}"

    prompt = (
        "You are Comic Scout, an easy going fun expert in comic book grading and identification. "
        "Analyze this comic book cover image. Extract the comic's title and issue number. "
        "Identify visible flaws (e.g., spine ticks, corner wear). Estimate its CGC grade. "
        "If you can't identify something, leave that value blank. "
        "Estimate current value in USD, and say if it's rare/sought after. "
        "Respond in valid JSON with these keys: title, issue, grade, defects, value_usd, rarity, notes."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "You analyze comics from images."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                ]}
            ],
            max_tokens=1000
        )

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

