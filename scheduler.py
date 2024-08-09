# Main
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Custom Middlewares
from middlewares.log_headers import log_headers

# Routers
from routes.hello import router as hello_router

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
