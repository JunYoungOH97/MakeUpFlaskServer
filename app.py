from flask import Flask, request
from m_connection import s3_connection, s3_put_object, s3_get_image_path
from model.beautyGAN import beautyGAN
from celery import Celery
import keys

s3 = s3_connection()

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL=f'redis://{keys.ip}:{keys.port}',
    CELERY_RESULT_BACKEND=f'redis://{keys.ip}:{keys.port}'
)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task()
def task(uuid):
    source = s3_get_image_path(f"{uuid}/source/source.png")
    target = s3_get_image_path(f"{uuid}/target/target.png")

    resultImage = beautyGAN(source, target).test()
    
    result = f"{uuid}/result/result.png"
    ret = s3_put_object(s3, resultImage, result)

    return result, ret


@app.route('/makeup', methods = ['POST'])
def upload():
    uuid = request.json["file"]

    result, ret = task(uuid)

    return result if(ret) else "False"

if(__name__ == "__main__"):
    app.run(host=keys.ip, port=keys.port, debug=True)