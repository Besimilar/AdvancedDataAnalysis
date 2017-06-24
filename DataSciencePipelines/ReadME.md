# Data Ingestion (dataIngestion.py)
1. Configuration (Brief)
		* Document: http://boto3.readthedocs.io/en/latest/guide/migrations3.html
		* Amazon IAM Console: 
				1. create your credentials: Add Policy
				2. download private key file
		* Set your credentials file locally
				$ aws configure
2. Creating a Bucket
		```python
		for bucket in s3.buckets.all():
		    if bucket.name == bucketName:
		        isCreated = True
		if not isCreated:
		    s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={
		        'LocationConstraint': 'us-west-2'})		
		```
3. Upload Dataset
		```python
		if not isExist:
        	s3.Object(bucketName, fileName).put(Body=open(fileName, 'rb'))
    	else:
        	logger.warning('File(' + fileName + ')' + ' Already Exists on S3.')
        ```


# Docker
1. Modify the Creator:
		process.py:
				python-pip3 --> python3-pip
				RUN pip3 packages --> RUN pip3 install packages
2. Make Docker Images
		1. Run Docker Creator:
				$ cd ~/your/path/Data-Science-in-the-Cloud/webApp
				$ python manage.py runserver 8000
		2. Included Pakages: Python3.4
				* pandas
				* numpy
				* Matplotlib
				* IPython
3. Configure Images & Container
		1. basic:
				$ docker images
				$ docker tag <IMAGE-ID> <IMAGE-NAME>
		2. install packages:
				$ pip3 install --upgrade pip
				$ pip3 install boto3
				$ pip3 install jupyter
				$ pip3 install seaborn

4. Start Container
		$ docker run -it -p 8888:8888 info7390 /bin/bash
5. Access Bash of Container After Stopping it:
		$ docker start <container-name/ID>
		$ docker exec -it <container-name/ID> bash
6. Copy File to Container
		$ docker cp dataIngestion.py Team3Assign1:/Assignment1/DataIngestion
		$ docker cp config.json Team3Assign1:/Assignment1/DataIngestion
		$ docker cp run.sh Team3Assign1:/Assignment1/DataIngestion
		Team3Assign1:/Assignment1/DataWrangling

		$ docker cp 
7. Run dataIngestion.py:
		$ sudo /bin/sh run.sh
8. Run EDA on Jupyter:	
		$ jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
		Summary:
				Docker : docker run -it -p 8888:8888 image:version 
				Container : jupyter notebook --ip 0.0.0.0 --no-browser 
				Host : localhost:8888/tree‌​


# Upload Docker to Docker Hub
1. Commit the container:
		$ docker commit container-name
		$ docker tag <image-to-be-committed> <repository name>
2. Public images:
		$ docker push <repository-name>
3. Pull images:
		$ docker pull <repository-name>


# AWS
sudo /bin/sh Assignment1/DataWrangling/run.sh

/bin/bash -c 'cd Assignment1/DataWrangling ; sudo /bin/bash run.sh'
docker run -w /Assignment1/DataWrangling -it besimilar/advanced-data-analysis:both sudo /bin/sh run.sh

COMMAND:
/bin/bash -c Ref::code
Parameters:
code : cd /Assignment1/DataWrangling ; sudo /bin/sh run.sh

AKIAIJL47Y6K5EW6UY3A
pQFBLX9bwi9g06gMNI/OyZ3xrvU+N10yAw+K7Ojf


		

