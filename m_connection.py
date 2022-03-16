import boto3

from m_config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY
from m_config import AWS_S3_BUCKET_NAME, AWS_S3_BUCKET_REGION

def connectionS3():
    try:
        s3 = boto3.client(
            service_name='s3',
            region_name=AWS_S3_BUCKET_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

    except Exception as e:
        print(e)
    else:
        return s3

def putObjectS3(s3, resultImage, accessPath):
    try:
        s3.put_object(Bucket = AWS_S3_BUCKET_NAME,
                      Body = resultImage,
                      Key = accessPath,
                      ContentType='image/png')

    except Exception as e:
        print(e)
        return False
    return True
    
def getObjectS3(s3, objectName, fileName):
    try:
        s3.download_file(AWS_S3_BUCKET_NAME, objectName, fileName)
    except Exception as e:
        print(e)
        return False
    return True

def getImagePathS3(keyName):
    return f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_S3_BUCKET_REGION}.amazonaws.com/{keyName}"