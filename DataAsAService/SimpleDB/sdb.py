# @author Hongwei
import boto3
import json
import pandas as pd


def main():
    # Config.json location
    configFile = 'config.json'
    with open(configFile) as globalSettings:
        config = json.load(globalSettings)

    # Loading Global settings
    domainName = str(config['name'])
    ACCESS_KEY = str(config['AWSAccess'])
    SECRET_KEY = str(config['AWSSecret'])
    region = str(config['region'])
    cleanData = str(config['cleanDataFileName'])

    # Connect to SDB
    Session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=region
    )
    sdb = Session.client('sdb')

    # List domains
    response = sdb.list_domains(
    )
    print(response)
    if 'DomainNames' in response:
        print("Current domains: %s" % response['DomainNames'])

    # Create domain
    if 'DomainNames' not in response:
        create_domain(sdb, domainName)
    else:
        if domainName not in response['DomainNames']:
            create_domain(sdb, domainName)
        else:
            print(domainName + ': Already exists in SimpleDB')

    # Delete domain
    # print('Delete Domain')
    # response = sdb.delete_domain(
    #     DomainName=domainName
    # )

    # Load original data
    data = pd.read_csv(cleanData, sep=',')
    # Only upload parcelid, latitude, longitude
    data = data.ix[:, ['parcelid', 'latitude', 'longitude']]
    # print(data)

    # Put items
    put_items(sdb, domainName, data)


def create_domain(sdb, domainName):
        print('Creating Domain:' + domainName + 'in SimpleDB')
        response = sdb.create_domain(
            DomainName=domainName
        )


def put_items(sdb, domainName, data):
    numOfItems = len(data)
    print('Total: ' + str(numOfItems) + ' Items')

    # start to put
    print("###### Start to Put Items ######")
    items_per_batch = []
    for row in data.itertuples():
        items_per_batch.append(generate_one_item(row))
        # put 25 items each time
        if (row[0] % 25 == 24) or (row[0] == numOfItems - 1):
            print('Start: ' + str(row[0] // 25 + 1) + ' Put')
            put_items_one_batch(sdb, domainName, items_per_batch)
            # reset items to []
            items_per_batch = []
    print("###### All Items have been put into SimpleDB ######")


def put_items_one_batch(sdb, domainName, items_per_batch):
    # print(items_per_batch)
    response = sdb.batch_put_attributes(
                DomainName=domainName,
                Items=items_per_batch
            )


def generate_one_item(row):
    # index, parcelid, latitude, longitude
    parcelid = str(row[1])
    latitude = str(row[2])
    longitude = str(row[3])
    item = {
                'Name': parcelid,
                'Attributes': [
                    {
                        'Name': 'latitude',
                        'Value': latitude,
                        'Replace': True
                    },
                    {
                        'Name': 'longitude',
                        'Value': longitude,
                        'Replace': True
                    },
                ]
            }
    return item


if __name__ == '__main__':
    main()
