from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from loguru import logger

import face_recognition
import os
import sys
import uvicorn


logger.remove()
logger.add(sys.stderr, level="DEBUG")

app = FastAPI()


async def validate_extensions(filename: str):
    if not (filename.endswith(".jpg") or filename.endswith(".png")):
        raise HTTPException(status_code=400, detail="Invalid file extension. Allowed extensions are .jpg and .png")   

@app.get("/", response_class=HTMLResponse)
async def redirect_to_index():
    return RedirectResponse(url="/index")

@app.post("/matchfaces", response_class=JSONResponse)
async def match_faces(known_file: UploadFile, unknown_file: UploadFile):
    # Save the uploaded files temporarily
    known_image_path = f"/tmp/{known_file.filename}"
    unknown_image_path = f"/tmp/{unknown_file.filename}"
    with open(known_image_path, "wb") as known_image_file:
        known_image_file.write(await known_file.read())
    with open(unknown_image_path, "wb") as unknown_image_file:
        unknown_image_file.write(await unknown_file.read())

    # Load images and perform face recognition
    logger.info("Started face comparison")
    known_image = face_recognition.load_image_file(known_image_path)
    unknown_image = face_recognition.load_image_file(unknown_image_path)

    known_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    results = face_recognition.compare_faces([known_encoding], unknown_encoding)
    logger.info(f"Face Comparison done: {results[0]}")
    # Delete temporary files
    os.remove(known_image_path)
    os.remove(unknown_image_path)

    return {"result": bool(results[0])}

@app.get("/index", response_class=HTMLResponse)
async def index():
    html_content = """
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    </head>
        <body>
            <h1>para k kieres saber eso jaja saludos!</h1>
            <p>Creo que lo que quieres ver es <a href="/docs">el swagger</a>.</p>
        </body>
    </html>
    """    
    return HTMLResponse(content=html_content)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
    a = 5
    
