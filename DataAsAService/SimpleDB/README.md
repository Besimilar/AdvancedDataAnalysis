# Upload data to AWS SimpleDB
1. Add your AWS key in config.json
2. Modify cleanDataFileName in config.json
3. Save clean DataSet to this directory


# Core Code to realize uploading
```python
# Only Upload 'parcelid', 'latitude', 'longitude' to SimpleDB
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
```