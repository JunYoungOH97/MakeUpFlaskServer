from flask import Flask, request
import requests

from m_connection import s3_connection, s3_put_object, s3_get_image_path
# from model import model
from model.beautyGAN import beautyGAN

import keys

s3 = s3_connection()
app = Flask(__name__)

# @app.route('/')
@app.route('/makeup', methods = ['POST'])
def upload():
    # response = requests.get("https://jsonplaceholder.typicode.com/users/1")
    # source = s3_get_image_path(response.json()['source'])
    # target = s3_get_image_path(response.json()['target'])
    
    # source = s3_get_image_path("KakaoTalk_Photo_2022-03-09-16-55-15")
    # target = s3_get_image_path("KakaoTalk_Photo_2022-03-09-16-55-09")

    uuid = request.json["file"]

    source = s3_get_image_path(f"{uuid}/source/source.png")
    target = s3_get_image_path(f"{uuid}/target/target.png")

    resultImage = beautyGAN(source, target).test()
    
    ## /{uuid}/result/result.png
    result = f"{uuid}/result/result.png"
    ret = s3_put_object(s3, resultImage, result)

    if ret :
        print("파일 저장 성공")
        return result

    else:
        print("파일 저장 실패")
        return "False"

    # return s3_get_image_path(key_name)

if(__name__ == "__main__"):
    app.run(host=keys.ip, port=keys.port, debug=True)