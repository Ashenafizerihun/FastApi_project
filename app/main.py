from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from . import models

from .routers import user, post, auth, vote

# Initialize FastAPI application
app = FastAPI()

# List of allowed origins (You can set specific domains)
origins = [
    "https://www.google.com",  # Example allowed origin
    "https://www.youtube.com"  # Local development
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origins allowed to access the API
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"Hello": "My API"}

# Include the routers for user and post
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)
