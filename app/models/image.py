from pydantic import BaseModel, Field
from fastapi import UploadFile
from typing import Optional


class ImageParametersModel(BaseModel):
    image: UploadFile
    font_size: Optional[int]
    background_alpha: Optional[float]
