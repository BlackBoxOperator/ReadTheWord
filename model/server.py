from argparse import ArgumentParser
import base64
import datetime
import hashlib

import cv2
from flask import Flask
from flask import request
from flask import jsonify
import numpy as np

from PIL import Image
from inference import inf_launch
from io import BytesIO

app = Flask(__name__)

####### PUT YOUR INFORMATION HERE #######
CAPTAIN_EMAIL = 'nobodyzxc.tw@gmail.com'#
SALT = 'blakboxoperator'                #
#########################################

#[API 開發說明文件] : https://hackmd.io/@wendy81214/BygUwgs4u
#[API 規格說明文件] : https://hackmd.io/@wendy81214/ByDht0bVu

def generate_server_uuid(input_string):
    """ Create your own server_uuid.

    @param:
        input_string (str): information to be encoded as server_uuid
    @returns:
        server_uuid (str): your unique server_uuid
    """
    s = hashlib.sha256()
    data = (input_string + SALT).encode("utf-8")
    s.update(data)
    server_uuid = s.hexdigest()
    return server_uuid


def base64_to_binary_for_cv2(image_64_encoded):
    """ Convert base64 to numpy.ndarray for cv2.

    @param:
        image_64_encode(str): image that encoded in base64 string format.
    @returns:
        image(numpy.ndarray): an image.
    """
    img_base64_binary = image_64_encoded.encode("utf-8")
    img_binary = base64.b64decode(img_base64_binary)
    image = cv2.imdecode(np.frombuffer(img_binary, np.uint8), cv2.IMREAD_COLOR)
    return image

def base64_to_binary_for_PIL(image_64_encoded):
    """ Convert base64 to numpy.ndarray for PIL.

    @param:
        image_64_encode(str): image that encoded in base64 string format.
    @returns:
        image(numpy.ndarray): an image.
    """
    #img_base64_binary = image_64_encoded.encode("utf-8")
    #img_binary = base64.b64decode(img_base64_binary)
    #image = Image.fromarray(np.frombuffer(img_binary, np.uint8), 'RGB')
    image = Image.open(BytesIO(base64.b64decode(image_64_encoded)))
    return image



#def predict(image):
#    """ Predict your model result.
#
#    @param:
#        image (numpy.ndarray): an image.
#    @returns:
#        prediction (str): a word.
#    """
#
#    ####### PUT YOUR MODEL INFERENCING CODE HERE #######
#    prediction = '陳'
#
#
#    ####################################################
#    if _check_datatype_to_string(prediction):
#        return prediction


def _check_datatype_to_string(prediction):
    """ Check if your prediction is in str type or not.
        If not, then raise error.

    @param:
        prediction: your prediction
    @returns:
        True or raise TypeError.
    """
    if isinstance(prediction, str):
        return True
    raise TypeError('Prediction is not in string type.')


@app.route('/inference', methods=['POST'])
def inference():
    """ API that return your model predictions when E.SUN calls this API. """
    data = request.get_json(force=True)

    # 自行取用，可紀錄玉山呼叫的 timestamp
    esun_timestamp = data['esun_timestamp']

    # 取 image(base64 encoded) 並轉成 PIL 可用格式
    image_64_encoded = data['image']
    image = base64_to_binary_for_PIL(image_64_encoded)
    #image = base64_to_binary_for_cv2(image_64_encoded)

    t = datetime.datetime.now()
    ts = str(int(t.utcnow().timestamp()))
    server_uuid = generate_server_uuid(CAPTAIN_EMAIL + ts)

    try:
        answer = predict([image])
    except TypeError as type_error:
        # You can write some log...
        raise type_error
    except Exception as e:
        # You can write some log...
        raise e

    server_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({'esun_uuid': data['esun_uuid'],
                    'server_uuid': server_uuid,
                    'answer': answer,
                    'server_timestamp': server_timestamp})


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8080, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    predict = inf_launch('--model tf_efficientnet_b5_ns --pretrained --checkpoint ./output/train/20210514-133801-tf_efficientnet_b5_ns-256/checkpoint-29.pth.tar -b 1 --input-size 3 256 256 -j 8 --num-classes 801')

    if not predict:
        print("invalid model args")
        exit(1)

    app.run(debug=options.debug, port=options.port)
