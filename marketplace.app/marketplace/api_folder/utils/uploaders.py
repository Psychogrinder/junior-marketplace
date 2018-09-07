import base64
import os
import time

from werkzeug.utils import secure_filename

from marketplace import db, app
from marketplace.api_folder.utils.abortions import no_file_part_in_request, no_image_presented

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_image(uploader, producer_id, image_data):
    """
    :param uploader: instance of an object, either Producer or Product
    :param producer_id: is used to find the necessary directory
    :param image_data: image bytes in string format, base64
    """

    # turn string to bytes
    image_data = bytes(image_data, encoding='utf-8')
    # make a unique name for the image
    filename = f'{hash(str(time.time()))}' + '.jpeg'
    # attach the producer image directory to the filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(producer_id), filename)
    print()
    # write bytes to a file
    with open(file_path, "wb") as fh:
        fh.write(base64.decodebytes(image_data))
    # -5 because we go as far as the static folder: static/img/user_images/producer_id/filename.jpg
    photo_url = '/'.join(file_path.split('/')[-5:])
    # set photo_url attribute of the object
    uploader.set_photo_url(photo_url)
    db.session.commit()
    return True

