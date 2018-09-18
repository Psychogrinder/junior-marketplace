import base64
import os
import time
import base64

from marketplace import models
from marketplace import image_tools
from marketplace import db, app, celery


@celery.task()
def commit_change(image_url, cls, uploader_id):
    model = getattr(models, cls)
    instance = model.query.get(uploader_id)
    instance.set_photo_url(image_url)
    db.session.commit()


def save_upload_image(image_url, uploader, size):
    image_tools.change_image.apply_async(
        (image_url, size),
        link=commit_change.s(type(uploader).__name__, uploader.id)
    )


def upload_image(uploader, image_data, producer_id, size, product_id=None):
    """
    :param uploader: instance of an object, either Producer or Product
    :param producer_id: is used to find the necessary directory
    :param image_data: image bytes in string format, base64
    """
    if not image_data:
        return False
    # turn string to bytes
    image_data = bytes(image_data, encoding='utf-8')
    # make a unique name for the image
    filename = f'{hash(time.time())}' + '.jpeg'
    # attach the producer image directory to the filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(producer_id), filename)
    # write bytes to a file
    with open(file_path, "wb") as fh:
        fh.write(base64.decodebytes(image_data))
    save_upload_image(file_path, uploader, size)
    return True
