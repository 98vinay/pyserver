# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import FileResponse, JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# import os

# app = FastAPI()

# # add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['*'],
#     allow_credentials=True,
#     allow_methods=['GET', 'POST'],
#     allow_headers=['*']
# )

# # define uploads directory
# uploads_dir = 'E:/CV demo/uploads/'
# if not os.path.exists(uploads_dir):
#     os.makedirs(uploads_dir)

# @app.get('/getImages',status_code=200)
# async def get_images():
#     files = os.listdir(uploads_dir)
#     if len(files) > 0:
#         return JSONResponse(content=files)
#     else:
#         return []

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='localhost', port=3002)

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi 
import json
from urllib.parse import urlparse, parse_qs

# server config
hostname = '0.0.0.0'
port = 3001

# directory to store uploaded files
uploads_dir = 'E:/CV demo/uploads/'
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)

class DemoServer(BaseHTTPRequestHandler):
    # GET request handler
    def do_GET(self):
        if self.path == '/getImages':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            files = os.listdir(uploads_dir)
            if len(files) > 0:
                response = json.dumps(files)
                self.wfile.write(response.encode('utf-8'))
            else:
                response = []
                self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path.startswith('/downloadImage'):
            query = urlparse(self.path).query
            params = parse_qs(query)
            file_name = params['image'][0]
            file_path = os.path.join(uploads_dir, file_name)
            print(file_path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-type', 'application/octet-stream')
                    self.send_header('Content-Disposition', 'attachment; filename=' + file_name)
                    self.end_headers()
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(bytes('File not found', 'utf-8'))
            
    
        elif self.path == '/':
            # send 200 OK response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes('<html><head><title>Demo Server</title></head>', 'utf-8'))
            self.wfile.write(bytes('<h1>Hello, World!</h1>', 'utf-8'))
            self.wfile.write(bytes('</html>', 'utf-8'))


    # POST request handler
    def do_POST(self):
        # parse data from form
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
        
        # check if file is uploaded
        if 'file' in form:
            file_data = form['file']
            file_name = file_data.filename
            with open(os.path.join(uploads_dir, file_name), 'wb') as f:
                f.write(file_data.file.read())
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes('File uploaded successfully', 'utf-8'))
        else:
            self.send_response(400)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes('No file uploaded', 'utf-8'))
    

if __name__ == '__main__':
    # Server instance
    httpd = HTTPServer((hostname, port), DemoServer)
    print(f'Starting server on {hostname}:{port}')
    try:
        # Run server
        httpd.serve_forever()
    except KeyboardInterrupt:
        # Stop server
        pass
    # Close server connection
    httpd.server_close()
    print('Stopping server')
    