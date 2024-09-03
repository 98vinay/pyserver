from fastapi import FastAPI, File, UploadFile, HTTPException,Form
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

# Directory to store uploaded files
uploads_dir = 'uploads/'
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

# list images endpoint
@app.get("/getImages")
async def get_images():
    files = os.listdir(uploads_dir)
    # return images list
    return JSONResponse(content=files)

#Download endpoint
@app.get("/downloadImage")
async def download_image(image: str):
    file_path = os.path.join(uploads_dir, image)
    if os.path.exists(file_path):
        headers = {"Content-Disposition": f"attachment; filename={image}"}
        #Send file response header
        return FileResponse(file_path, filename=image, media_type='application/octet-stream', headers=headers)
    raise HTTPException(status_code=404, detail="File not found")

#index route
@app.get("/")
async def root():
    return """
    <html>
        <head>
            <title>Demo Server</title>
        </head>
        <body>
            <h1>Hello, World!</h1>
        </body>
    </html>
    """
#upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...), filename: str = Form(None)):
    #update the filename, if user send an filename
    if filename is not None:
        original_ext = file.filename.split('.')[-1]
        filename = filename + '.' + original_ext
    else:
        filename = file.filename        
    try:
        # Store in the directory
        file_path = os.path.join(uploads_dir, filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
            #return success message
        return {"message": "File uploaded successfully"}
    except Exception as e:
        # Raise an exception
        raise HTTPException(status_code=400, detail=str(e))
    
#main - Run
if __name__ == '__main__':
    import uvicorn
    #Server
    uvicorn.run(app, host="0.0.0.0", port=3001)