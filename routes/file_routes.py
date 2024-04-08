from fastapi import APIRouter, UploadFile, File, HTTPException
import cloudinary.uploader

router = APIRouter()


@router.post("/upload")
async def upload_file_to_cloudinary(file: UploadFile = File(...)):
    try:
        file_contents = await file.read()
        upload_result = cloudinary.uploader.upload(
            file_contents,
            folder="your_folder_name",

        )

        return {"url": upload_result["secure_url"]}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to upload file: {e}")
