import boto3
from botocore import UNSIGNED
from botocore.client import Config

def s3_unsigned_session():
    return boto3.client('s3', config=Config(signature_version=UNSIGNED))

s3 = s3_unsigned_session()

s3_bucket = 'spacenet-dataset'
output_dir = '/mnt/d/06_PESSOAIS/spacenet-dataset/'

for key in s3.list_objects(Bucket=s3_bucket)['Contents']:
    print(key['Key'].split('/')[-1])

for key in s3.list_objects(Bucket=s3_bucket)['Contents']:
    s3.download_file(s3_bucket, key['Key'], f"{output_dir}{key['Key'].split('/')[-1]}")

# s3.download_file(s3_bucket, 'spacenet/SN3_roads/tarballs/SN3_roads_train_AOI_3_Paris.tar.gz', f"{output_dir}{'SN3_roads_train_AOI_3_Paris.tar.gz'}")