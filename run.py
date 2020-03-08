import uvicorn

from core.api import light_novel_app

if __name__ == "__main__":
    uvicorn.run(light_novel_app, host="0.0.0.0", port=8000)
