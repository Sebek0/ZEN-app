import uvicorn


host="127.0.0.1" # For development only, in prod use 0.0.0.0
port=8002
app_name="app.main:app"



if __name__ == '__main__':
    uvicorn.run(app_name, host=host, port=port)