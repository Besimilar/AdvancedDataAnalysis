# @author Hongwei
import boto3
import json
import pandas as pd
import io
import requests
import datetime
import logging
from pandas import DataFrame


def check_file(curr_bucket, filename):
    for key in curr_bucket.objects.all():
        if key.key == filename:
            print('Skip: ' + 'File(' + filename + ')' + ' Already Exists.')
            return True


def cleanColumn(dataCleaned, columnName):
    for value in dataCleaned[columnName]:
        if type(value) is str:
            s = value
            value = value.replace('s', '')
            value = value.replace('*', '0')
            value = value.replace('V', '')
            value = value.replace('T', '0')
            try:
                dataCleaned.ix[dataCleaned[columnName] == s, columnName] = float(value)
            except ValueError:
                print(s)


def clean(dataCleaned, cleanDataName):
    dataCleaned = DataFrame(dataCleaned[dataCleaned['REPORTTPYE'] != 'SOD'])

    cleanColumn(dataCleaned, 'HOURLYDRYBULBTEMPF')
    cleanColumn(dataCleaned, 'HOURLYVISIBILITY')
    cleanColumn(dataCleaned, 'HOURLYPrecip')
    cleanColumn(dataCleaned, 'HOURLYRelativeHumidity')
    cleanColumn(dataCleaned, 'HOURLYWETBULBTEMPF')

    dataCleaned['DATE'] = pd.to_datetime(dataCleaned['DATE'], errors='raise')
    dataCleaned['DAY'] = dataCleaned['DATE'].map(lambda a : a.date())
    dataCleaned['MONTH'] = dataCleaned['DATE'].map(lambda a : int(a.month))
    dataCleaned['YEAR'] = dataCleaned['DATE'].map(lambda a : int(a.year))

    # Save Data to local
    dataCleaned.to_csv(cleanDataName, sep=',', encoding='utf-8')


def main():
    # Log File Setting
    time = datetime.datetime.now()
    logFileName = str(time.strftime('%d%m%y%H%M%S')) + '_clean.log'
    logging.basicConfig(filename=logFileName,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # Config.json location
    configFile = 'configWrangle.json'
    with open(configFile) as globalSettings:
        config = json.load(globalSettings)

    # Loading Global settings
    teamNum = str(config['team'])
    state = str(config['state']).lower()
    ACCESS_KEY = str(config['AWSAccess'])
    SECRET_KEY = str(config['AWSSecret'])
    rawDataLink = str(config['rawData'])
    cleanDataLink = str(config['cleanData'])
    receiver = str(config['notificationEmail'])
    sender = str(config['sender'])
    assignNum = 1
    # Variables
    bucketName = 'team' + str(teamNum) + state + 'assignment' + str(assignNum)

    # Connect to S3
    s3Session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name='us-west-2'
    )
    s3 = s3Session.resource('s3')
    logger.info('S3 Connected.')

    # Access S3 LCD Raw DataSet
    print('###### Trying to Access S3 LCD Raw DataSet ######')
    try:
        request = requests.get(rawDataLink)
        content = request.content
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        logger.error(e)
        logger.error("No Raw DataSet Found, Wrangling Stopped.")
        print('###### No Raw DataSet Found, Wrangling Stopped. ######')
        return
    # data = pd.read_csv(io.StringIO(content.decode('utf-8')), dtype=str, sep=',')
    data = pd.read_csv(io.StringIO(content.decode('utf-8')), sep=',')
    logger.info('Reading DataSet from URL')
    stationId = str(data.ix[0, 'STATION'])
    station, Id = stationId.split(':')
    date = time.date().strftime('%d%m%Y')
    fileName = str(config['state']) + '_' + date + '_' + station + '_' + Id + '_clean.csv'
    print('###### RAW LCD DataSet Loading Completed ######')

    # Check Whether clean File Exists
    bucket = s3.Bucket(bucketName)
    logger.info('Checking Whether File Exists on S3...')
    isExist = check_file(bucket, fileName)
    if isExist:
        logger.warning('File(' + fileName + ')' + ' Already Exists on S3.')

        # Download to local file system
        logger.info('Try Downloading Clean DataSet from URL')
        bucket.download_file(fileName, fileName)
        logger.info('Download Completed')
    else:
        logger.info('Starting Cleansing Raw DataSet')
        print('###### Starting Cleansing Raw DataSet ######')
        # Clean Raw Data
        ######
        clean(data, fileName)
        # Save Clean Data to local
        logger.info('DataSet Cleansing Completed')
        print('###### DataSet Cleansing Completed ######')

        # Upload Today's data to S3
        print('###### Starting Upload Clean Data till Today to S3 ######')
        logger.info('Starting Upload Clean Data till Today to S3')
        try:
            s3.Object(bucketName, fileName).put(Body=open(fileName, 'rb'))
            s3.Object(bucketName, fileName).Acl().put(ACL='public-read')
            print('Upload: Success')
            logger.info('Clean Data till Today Upload Succeed')

            cleanDataLink = s3Session.client('s3').generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': bucketName,
                    'Key': fileName}
            )

            # Modify clean Data url in configWrangle.json
            with open("configWrangle.json", "w") as newConfig:
                config['cleanData'] = cleanDataLink
                json.dump(config, newConfig)

            # Email
            text = "Download Clean DataSet: " + cleanDataLink
            try:
                s3Session.client('ses').send_email(
                    Destination={
                        'ToAddresses': [receiver]
                    },
                    Message={
                      'Body': {
                          'Text': {
                              'Data': text
                          }
                      },
                      'Subject': {
                          'Data': "Your Job Done By INFO7390Team3"
                      }
                    },
                    Source=sender
                )
            except Exception as e:
                print(e)

        except IOError as e:
            logger.error(e)
            logger.error('Clean Data till Today Upload Failed')
            print(e)

    # Program END
    logger.info('###### DataWrangling Finished ######')
    print('###### Find logs in ddmmyyHHMMSS_clean.log ######')

if __name__ == '__main__':
    main()

