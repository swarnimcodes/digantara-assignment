# Main
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading

# Modules
from utils.utils import run_jobs

# Custom Middlewares
from middlewares.log_headers import log_headers

# Routers
from routes.hello import router as hello_router
from routes.create_jobs import router as create_job_router
from routes.get_all_jobs import router as get_all_jobs_router
from routes.get_job_by_id import router as get_job_by_id_router


app = FastAPI()

# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Registering Custom Middlewares
app.middleware("http")(log_headers)

# Routes
app.include_router(hello_router)
app.include_router(create_job_router)
app.include_router(get_all_jobs_router)
app.include_router(get_job_by_id_router)


threading.Thread(target=run_jobs, daemon=True).start()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
