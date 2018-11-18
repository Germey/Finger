import json
from flask import Flask, render_template, request
import logging
from flask_cors import CORS as cors
import base64
from io import BytesIO
from PIL import Image
import time
from os.path import join

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
app = Flask(__name__)

cors(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save', methods=['GET', 'POST'])
def emotion():
    """
    receive image, get emotion
    :return:
    """
    if request.method == 'POST':
        # get image
        image = request.form['image']
        number = request.form['number']
        # save and recognize
        file_path = join('images', str(number) + '_' + str(time.time()) + '.jpg')
        # save image to image
        save_image(image, file_path)
        return json.dumps({
            'ok': 1
        }, ensure_ascii=False)


def save_image(data, file_path):
    """
    save binary base64 data to jpg
    :param data: base64 data
    :param file_path: file path
    :return: flag
    """
    with open(file_path, 'wb'):
        prefix = 'data:image/webp;base64,'
        data = data[len(prefix):]
        byte_data = base64.b64decode(data)
        image_data = BytesIO(byte_data)
        img = Image.open(image_data)
        img.save(file_path)
    return True


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            threaded=True,
            ssl_context='adhoc',
            port=5557)
