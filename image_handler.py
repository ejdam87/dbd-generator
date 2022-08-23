from PIL import ImageTk, Image
from typing import Tuple, List

def load_image(path: str) -> Image:

    return Image.open(path)


def resize_image(new_dimensions: Tuple[int, int], image: Image) -> Image:
    
    return image.resize(new_dimensions)


def get_tk_image(image: Image) -> ImageTk.PhotoImage:
    
    return ImageTk.PhotoImage(image)


def get_images(folder: str, name_list: List[str], new_dimensions: Tuple[int, int]) -> List["Image"]:
    
    return [get_tk_image(resize_image(new_dimensions, load_image(f"{folder}\\{name}.webp"))) for name in name_list]
