import os
import time

from werkzeug.utils import secure_filename
from marketplace import models
from marketplace import image_tools
from marketplace import db, app, celery
from marketplace.api_folder.utils.abortions import (
    no_file_part_in_request,
    no_image_presented
)


def allowed_extension(filename):
    extension = os.path.splitext(filename)[1].lower().replace('.', '')
    return extension in app.config['ALLOWED_UPLOAD_EXTENSIONS']


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


def upload_image(uploader, files, producer_id, size, product_id=None):
    if files:
        if 'image' not in files:
            no_file_part_in_request()
        image = files['image']
        if image.filename == '':
            no_image_presented()
        if image and allowed_extension(image.filename):
            image_url = os.path.join(
                app.config['UPLOAD_FOLDER'],
                str(producer_id),
                f'{hash(time.time())}_' + secure_filename(image.filename)
            )
            image.save(image_url)
            save_upload_image(image_url, uploader, size)
        return '/'+image_tools.get_static_name(image_url)
    else:
        return False
