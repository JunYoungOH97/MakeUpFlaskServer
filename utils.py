from m_connection import connectionS3, putObjectS3, getImagePathS3
from model.beautyGAN import beautyGAN
from flask import Flask, request, abort
from celery import Celery
import keys
import ssl

def saveResultImage(uuid, resultImage, s3):
    resultPath = f"{uuid}/result/result.png"
    state = putObjectS3(s3, resultImage, resultPath)
    return resultPath, state

def getResultImage(source, target):
    return beautyGAN(source, target).test()

def getAWSImage(uuid):
    source = getImagePathS3(f"{uuid}/source/source.png")
    target = getImagePathS3(f"{uuid}/target/target.png")

    return source, target

def getS3():
    return connectionS3()

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

def limitAddr():
    if(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) not in keys.allowIp):
        abort(403)

def runApp(app):
    app.run(host=keys.ip, port=keys.port)
    # app.run(host=keys.ip, port=keys.port, debug=True)
    # app.run(host=keys.ip, port=keys.port, ssl_context = getSSL(), debug=True)

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

def getSSL():
    sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS)
    sslContext.load_cert_chain(certfile=keys.SSLCrt, keyfile= keys.SSLKey)

    return sslContext