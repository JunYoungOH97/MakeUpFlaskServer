import boto3

from m_config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY
from m_config import AWS_S3_BUCKET_NAME, AWS_S3_BUCKET_REGION

def s3_connection():
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
        print("s3 bucket connected!")
        return s3

def s3_put_object(s3, result_image, access_key):
    try:
        s3.put_object(Bucket = AWS_S3_BUCKET_NAME,
                      Body = result_image,
                      Key = access_key,
                      ContentType='image/png')

    except Exception as e:
        print(e)
        return False
    return True
    
def s3_get_object(s3, object_name, file_name):
    try:
        s3.download_file(AWS_S3_BUCKET_NAME, object_name, file_name)
    except Exception as e:
        print(e)
        return False
    return True

def s3_get_image_path(key_name):
    return f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_S3_BUCKET_REGION}.amazonaws.com/{key_name}"