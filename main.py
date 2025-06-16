from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import openai
import io
import base64
from dotenv import load_dotenv
load_dotenv()
import os
# Initialize OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.post("/scan_comic/")
async def scan_comic(file: UploadFile = File(...)):
    image_bytes = await file.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    image_data_url = f"data:{file.content_type};base64,{base64_image}"

    prompt = (
        "You are Comic Scout, an easy going fun expert in comic book grading and identification that is cheerful and helpful. "
        "Analyze this image. Extract the comic's title and issue number. "
        "Identify visible flaws such as spine ticks or corner wear. Estimate its CGC grade. "
        "If you can't identify it, explain next steps the user should take."
        "Find current value  of the comic in USD, and if it a rarity or sought after issue. "
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

        analysis = response.choices[0].message.content
        return JSONResponse(content={"result": analysis})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
