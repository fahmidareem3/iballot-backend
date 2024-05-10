from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import cloudinary
from cloudinary.uploader import upload
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from auth.jwt_bearer import JWTBearer
from config.config import initiate_database, Settings
from routes.user import router as UserRouter
from routes.file_routes import router as FileRouter
from routes.organization import router as OrganizationRouter

app = FastAPI()

# Configuring settings
settings = Settings()

# Configuring Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

# Setting up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def app_startup():
    # Database initialization
    await initiate_database()

async def app_shutdown():
    pass  # Here you can add cleanup code if necessary

app.add_event_handler("startup", app_startup)
app.add_event_handler("shutdown", app_shutdown)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to Iballot"}

# Including routers
app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(FileRouter, tags=["File Upload"], prefix="/files")
app.include_router(OrganizationRouter, tags=["Organization"], prefix="/organization")
