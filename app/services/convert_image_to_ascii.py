from PIL import Image, ImageDraw, ImageFont
from fastapi import UploadFile
from fastapi.responses import JSONResponse
from .convert_image_to_ascii_utils import get_small_scale_dimensions
from io import BytesIO
import os
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
import base64


async def convert_image_to_ascii(
    image: UploadFile, font_size: int, background_alpha: float
):
    load_dotenv()

    # The font size is a string first dou to it being part of a multipart form
    # font_size = int(font_size)
    # local_server_path = os.getenv("LOCAL_SERVER_PATH")
    # background_alpha = float(background_alpha/100)
    # Read image
    image_contents = await image.read()
    img = Image.open(BytesIO(image_contents))

    # File conversion to PNG since it can be converted to RGBA
    try:
        png_buffer = BytesIO()
        img.save(png_buffer, format="PNG")
        img = Image.open(png_buffer)
    except Exception as e:
        print("Error converting to PNG:", e)
    try:
        img = img.convert("RGBA")
    except Exception as e:
        print("Error converting image to RGBA:", e)
    # img.show()

    original_img_size = img.size
    # print(img.size)

    new_width, new_height = get_small_scale_dimensions(img.size, font_size)
    # print("New:", new_width, new_height)
    img = img.resize((new_width, new_height))

    # Convert the image to grayscale
    img_gray = img.convert("L")

    # Define a set of ASCII characters from darkest to lightest
    ascii_chars = "012345679"

    # Calculate the intensity range for mapping
    intensity_range = 255 / (len(ascii_chars) - 1)

    # Generate ASCII art
    # font_path = "../assets/fonts/Roboto/Roboto-Black.ttf"
    current_directory = os.path.dirname(__file__)
    app_directory = os.path.dirname(current_directory)
    font_path = os.path.join(
        app_directory, "assets", "fonts", "Roboto", "Roboto-Black.ttf"
    )
    # print("current directory", current_directory)
    # print("app directory", app_directory)

    font = ImageFont.truetype(font_path, font_size)

    # Blank Image
    ascii_image = Image.new(
        "RGBA", (new_width * font_size, new_height * font_size), "black"
    )
    ascii_draw = ImageDraw.Draw(ascii_image)

    y_position = 0

    for y in range(new_height):
        for x in range(new_width):
            gs = img_gray.getpixel((x, y))
            r, g, b, alpha = img.getpixel((x, y))
            ascii_index = int(gs / intensity_range)

            # Use ANSI escape codes to set text color
            char = ascii_chars[ascii_index]

            # Calculate the position of the rectangle
            rect_x = x * font_size
            rect_y = y_position
            rect_width = font_size
            rect_height = font_size

            # Set the fill color for the rectangle
            rectangle_color = (r, g, b, int(alpha * background_alpha))

            # Draw the rectangle just behind the character
            ascii_draw.rectangle(
                [rect_x, rect_y, rect_x + rect_width, rect_y + rect_height],
                fill=rectangle_color,
            )

            text_colour = (r, g, b, alpha)
            # Adding Letter to Image
            ascii_draw.text(
                (x * font_size, y_position), char, font=font, fill=text_colour
            )

        y_position += font_size

    # Print or save the ASCII art
    ascii_image = ascii_image.resize(original_img_size, resample=Image.NEAREST)
    # ascii_image.show()

    with NamedTemporaryFile(delete=False) as temp_file:
        ascii_img_byte_array = BytesIO()
        ascii_image.save(ascii_img_byte_array, format="PNG")
        ascii_img_bytes = ascii_img_byte_array.getvalue()

        temp_file.write(ascii_img_bytes)
        temp_file.seek(0)
        ascii_img_bytes = temp_file.read()
    # return StreamingResponse(BytesIO(ascii_img_bytes), media_type="image/png")

    # with bf.BlobFile(temp_file.name) as f:
    #     print(f.name)
    # print("blob url: ", f.get_url())
    # print("content: ", f.content())

    ascii_img_base64 = base64.b64encode(ascii_img_bytes).decode()
    # data_url = f""
    # print("ASCII base 64 stuff", ascii_img_base64)

    # return FileResponse(temp_file.name, media_type="image/png")
    return JSONResponse(content=ascii_img_base64)
