# @author Hongwei
import boto3
import json
import pandas as pd
import io
import requests
import datetime
import urllib.request
import logging


def check_file(curr_bucket, filename):
    for key in curr_bucket.objects.all():
        if key.key == filename:
            print('Skip: ' + 'File(' + filename + ')' + ' Already Exists.')
            return True


def main():
    # Log File Setting
    time = datetime.datetime.now()
    logFileName = str(time.strftime('%d%m%y%H%M%S')) + '.log'
    logging.basicConfig(filename=logFileName,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # Config.json location
    configFile = 'config.json'
    with open(configFile) as globalSettings:
        config = json.load(globalSettings)

    # Loading Global settings
    teamNum = str(config['team'])
    state = str(config['state']).lower()
    ACCESS_KEY = str(config['AWSAccess'])
    SECRET_KEY = str(config['AWSSecret'])
    link = str(config['link'])
    email = str(config['notificationEmail'])
    assignNum = 1
    # Variables
    bucketName = 'team' + str(teamNum) + state + 'assignment' + str(assignNum)

    # Connect to S3
    s3Session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    s3 = s3Session.resource('s3')
    logger.info('S3 Connected.')

    # Create a Bucket (Name should not be uppercase)
    # Check Whether the bucket has been created
    isCreated = False
    bucket = None
    for bucket in s3.buckets.all():
        if bucket.name == bucketName:
            isCreated = True
            print('Skip: ' + 'Bucket(' + bucketName + ')' + ' Already Created.')
            logger.warning('Bucket(' + bucketName + ')' + ' Already Created.')
            break
    if not isCreated:
        bucket = s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={
            'LocationConstraint': 'us-west-2'})
        logger.info('Bucket(' + bucketName + ')' + 'Created')
        bucket.Acl().put(ACL='public-read')
        logger.info('Bucket Set to Public')

    # Access LCD
    print('###### Trying to Access LCD DataSet ######')
    try:
        request = requests.get(link)
        content = request.content
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        logger.error(e)
        logger.error("No LCD DataSet Found, DataIngestion Stopped.")
        print('###### No LCD DataSet Found, DataIngestion Stopped. ######')
        return
    data = pd.read_csv(io.StringIO(content.decode('utf-8')), dtype=str, sep=',')
    logger.info('Reading DataSet from URL')
    stationId = str(data.ix[0, 'STATION'])
    station, id = stationId.split(':')
    date = time.date().strftime('%d%m%Y')
    fileName = str(config['state']) + '_' + date + '_' + station + '_' + id + '.csv'
    print('###### LCD DataSet Loading Completed ######')

    # Upload File to S3
    # Check Whether File Exists
    logger.info('Checking Whether File Exists on S3...')
    isExist = check_file(bucket, fileName)
    # for key in bucket.objects.all():
    #     if key.key == fileName:
    #         isExist = True
    #         print('Skip: ' + 'File(' + fileName + ')' + ' Already Exists.')
    #         break
    if not isExist:
        # Download to local file system
        logger.info('No Data on S3: Try Downloading DataSet from URL')
        # fileNameForToday = 'OneDay' + '_' + fileName
        # urllib.request.urlretrieve(link, fileNameForToday)
        urllib.request.urlretrieve(link, fileName)
        logger.info('Download Completed')

        # Upload Today's data to S3
        logger.info('Starting Upload Data till Today to S3')
        s3.Object(bucketName, fileName).put(Body=open(fileName, 'rb'))
        s3.Object(bucketName, fileName).Acl().put(ACL='public-read')
        print('Upload: Success')
        logger.info('Data till Today Upload Succeed')
    else:
        logger.warning('File(' + fileName + ')' + ' Already Exists on S3.')

    # Program END
    logger.info('###### DataIngestion Finished ######')
    print('###### Find logs in ddmmyyHHMMSS.log ######')

if __name__ == '__main__':
    main()

