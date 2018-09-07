import os
import time

from werkzeug.utils import secure_filename

from marketplace import db, app
from marketplace.api_folder.utils.abortions import no_file_part_in_request, no_image_presented

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_image(uploader, files, producer_id, product_id=None):
    if files:
        if 'image' not in files:
            no_file_part_in_request()
        image = files['image']
        if image.filename == '':
            no_image_presented()
        if image and allowed_extension(image.filename):
            image_url = os.path.join(app.config['UPLOAD_FOLDER'], str(producer_id),
                                     f'{hash(str(time.time()))}_' + secure_filename(image.filename))
            image.save(image_url)
            image_url = '/'.join(image_url.split('/')[-5:])
            uploader.set_photo_url(image_url)
            db.session.commit()
        return '/' + image_url
    else:
        return False
