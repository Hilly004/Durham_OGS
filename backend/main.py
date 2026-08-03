from fastapi import FastAPI

from backend.api.mount import router as mount_router

app = FastAPI(title='Durham OGS API')

app.include_router(mount_router, prefix='/mount')

@app.get('/')
def root():
    return {
        'message': 'Durham OGS API',
        'status': 'running'
    }


