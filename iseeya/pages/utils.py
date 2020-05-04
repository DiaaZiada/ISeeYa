import os
import secrets
import numpy as np
import cv2
from PIL import Image
from flask import current_app

def save_picture(form_picture, size=None):
    # best size for cover is (1579, 960)

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static','page_pics', picture_fn)

    i = Image.open(form_picture)
    image = np.array(i)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if size != None:       
        image = cv2.resize(image, size)
    cv2.imwrite(picture_path, image)
    return picture_fn


def delete_picture(picture_fn):
    path  = os.path.join(current_app.root_path, 'static/page_pics', picture_fn)
    if os.path.exists(path):
        os.remove(path)