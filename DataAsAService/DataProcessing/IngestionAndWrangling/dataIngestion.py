# @author Hongwei
import boto3
import json
import datetime
import logging
import pandas as pd
import scipy


def main():
    # Log
    logger = save_logs()

    # Config.json location
    configFile = 'config.json'
    with open(configFile) as globalSettings:
        config = json.load(globalSettings)

    # Loading Global settings
    rawData = str(config['rawDataFileName'])
    fileName = str(config['cleanDataFileName'])
    teamNum = str(config['team'])
    ACCESS_KEY = str(config['AWSAccess'])
    SECRET_KEY = str(config['AWSSecret'])
    region = str(config['region'])
    receiver = str(config['notificationEmail'])
    sender = str(config['sender'])
    assignNum = str(config['assignNum'])
    # Variables
    bucketName = 'team' + str(teamNum) + 'assignment' + assignNum

    # Load data and clean
    logger.info('Starting Cleansing Raw DataSet')
    print('###### Starting Cleansing Raw DataSet ######')
    # Clean Raw Data and Save to local
    data = pd.read_csv(rawData, sep=',')
    clean(data, fileName)
    logger.info('DataSet Cleansing Completed')
    print('###### DataSet Cleansing Completed ######')

    # Connect to S3
    s3Session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=region
    )
    s3 = s3Session.resource('s3')
    logger.info('S3 Connected.')

    # Create Bucket in S3
    bucket = create_bucket(s3, bucketName, logger, region)

    # Upload File to S3
    upload_to_s3(s3, bucket, fileName, logger)

    # Program END
    logger.info('###### DataIngestion Finished ######')
    print('###### Find logs in ddmmyyHHMMSS.log ######')


def save_logs():
    # Log File Setting
    time = datetime.datetime.now()
    logFileName = str(time.strftime('%d%m%y%H%M%S')) + '.log'
    logging.basicConfig(filename=logFileName,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)
    return logger


def create_bucket(s3, bucketName, logger, region):
    # Create a Bucket (Name should not be uppercase)
    # Check Whether the bucket has been created
    bucket = None
    isCreated = False
    for bucket in s3.buckets.all():
        if bucket.name == bucketName:
            isCreated = True
            print('Skip: ' + 'Bucket(' + bucketName + ')' + ' Already Created.')
            logger.warning('Bucket(' + bucketName + ')' + ' Already Created.')
            break
    if not isCreated:
        bucket = s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={
            'LocationConstraint': region})
        logger.info('Bucket(' + bucketName + ')' + 'Created')
        bucket.Acl().put(ACL='public-read')
        logger.info('Bucket Set to Public')
    return bucket


def check_file(curr_bucket, filename):
    for key in curr_bucket.objects.all():
        if key.key == filename:
            print('Skip: ' + 'File(' + filename + ')' + ' Already Exists.')
            return True


def upload_to_s3(s3, bucket, fileName, logger):
    # Check Whether File Exists
    logger.info('Checking Whether File Exists on S3...')
    isExist = check_file(bucket, fileName)
    if not isExist:
        # Upload data to S3
        logger.info('Starting Upload Data to S3')
        s3.Object(bucket.name, fileName).put(Body=open(fileName, 'rb'))
        s3.Object(bucket.name, fileName).Acl().put(ACL='public-read')
        print('Upload: Success')
        logger.info('Data Upload Succeed')
    else:
        logger.warning('File(' + fileName + ')' + ' Already Exists on S3.')


def clean(data, fileName):
    # replace missing value with 0
    print("replace missing value with 0")
    data['basementsqft'] = data['basementsqft'].fillna(0)
    data['fireplacecnt'] = data['fireplacecnt'].fillna(0)
    data['calculatedbathnbr'] = data['calculatedbathnbr'].fillna(0)
    data['garagecarcnt'] = data['garagecarcnt'].fillna(0)
    data['garagetotalsqft'] = data['garagetotalsqft'].fillna(0)

    # replace missing value with mean
    print("replace missing value with mean")
    data['finishedsquarefeet12'] = data['finishedsquarefeet12'].fillna(scipy.mean(data['finishedsquarefeet12']))
    data['calculatedfinishedsquarefeet'] = data['calculatedfinishedsquarefeet'].fillna(scipy.mean(data['calculatedfinishedsquarefeet']))
    data['fullbathcnt'] = data['fullbathcnt'].fillna(round(scipy.mean(data['fullbathcnt'])))
    data['lotsizesquarefeet'] = data['lotsizesquarefeet'].fillna(round(scipy.mean(data['lotsizesquarefeet'])))

    # replace missing value with False
    print("replace missing value with False")
    data['fireplaceflag'] = data['fireplaceflag'].fillna(False)
    data['hashottuborspa'] = data['hashottuborspa'].fillna(False)

    # Save Data to local
    print("Save Data to local")
    data.to_csv(fileName, sep=',', encoding='utf-8')
    print("Data Saved.")


if __name__ == '__main__':
    main()

