from fastapi import APIRouter, Form, UploadFile

from ..services.convert_image_to_ascii import convert_image_to_ascii

router = APIRouter(prefix="/api/image_to_ascii")


@router.post("/")
async def post_image(
    image: UploadFile, background_alpha: float = Form(...), font_size: int = Form(...)
):
    return await convert_image_to_ascii(
        image=image, font_size=font_size, background_alpha=background_alpha
    )
