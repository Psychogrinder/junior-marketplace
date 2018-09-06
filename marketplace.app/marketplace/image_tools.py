from PIL import Image
import os
from marketplace import celery


def resize_image_if_it_larger_than_needed(image, to_width, to_height):
    width, height = image.size
    if width > to_width or height > to_height:
        image.thumbnail((to_width, to_height))
    return image


def change_filename(image, new_format=None, new_path=None):
    format = new_format or image.format
    name = new_path or image.filename
    if new_format and new_path is None:
        path, extension = os.path.splitext(name)
        name = f'{path}.{new_format}'
    return name, format


def get_static_name(path):
    path_after_static = path.split('static/')[1]
    return f'static/{path_after_static}'


@celery.task(bind=True, name='image_tools.change_image')
def change_image(
    self,
    image_path,
    size,
    new_format=None,
    new_path=None,
    remove_original=False
):
    image = Image.open(image_path)
    image = resize_image_if_it_larger_than_needed(image, size[0], size[1])
    name, format = change_filename(image, new_format=new_format, new_path=new_path)
    try:
        image.save(name, format=format)
    except IOError:
        self.retry(max_retries=3, interval_start=0.1)
    else:
        if remove_original and (new_path or new_format):
            os.remove(image_path)
    return get_static_name(name)
