from m_connection import s3_connection, s3_put_object, s3_get_image_path
from model.beautyGAN import beautyGAN
from flask import Flask, request
from celery import Celery
import keys

def saveResultImage(uuid, resultImage, s3):
    result = f"{uuid}/result/result.png"
    state = s3_put_object(s3, resultImage, result)
    return result, state

def getResultImage(source, target):
    return beautyGAN(source, target).test()

def getAWSImage(uuid):
    source = s3_get_image_path(f"{uuid}/source/source.png")
    target = s3_get_image_path(f"{uuid}/target/target.png")

    return source, target

def getS3():
    return s3_connection()

def getApp():
    app = Flask(__name__)
    app.config.update(
        CELERY_BROKER_URL=f'redis://{keys.ip}:{keys.port}',
        CELERY_RESULT_BACKEND=f'redis://{keys.ip}:{keys.port}'
    )

    return app

def getCelery(app):
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery

def runApp(app):
    app.run(host=keys.ip, port=keys.port, debug=True)

def getUuid():
    return request.json["file"]

def returnToSpringServer(result, state):
    return result if(state) else "False"

def getObjects():
    app = getApp()
    return getS3(), app, getCelery(app)

def pipeLine(uuid, s3):
    source, target = getAWSImage(uuid)
    resultImage = getResultImage(source, target)
    result, state = saveResultImage(uuid, resultImage, s3)

    return result, state

