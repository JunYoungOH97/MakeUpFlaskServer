import utils

s3, app, celery = utils.getObjects()

@celery.task()
def task(uuid):
    result, state = utils.pipeLine(uuid, s3)
    return result, state

@app.route('/makeup', methods = ['POST'])
def runModel():
    uuid = utils.getUuid()

    result, state = task(uuid)

    return utils.returnToSpringServer(result, state)

if(__name__ == "__main__"):
    utils.runApp(app)
