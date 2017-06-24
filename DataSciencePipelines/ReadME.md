# Docker Hub
1. Name: besimilar/advanced-data-analysis:final

2. Docker Folder Structure:
	* dataIngestion.py:
		```
		cd /Assignment1/DataIngestion
		```
	* wrangle.py:
		```
		cd /Assignment1/DataWrangling
		```
# Detailed Instruction
See 1-Report_DataProcessing.docx

# Data Ingestion & Data Wrangling
1. Configuration (Brief)
	* Document: http://boto3.readthedocs.io/en/latest/guide/migrations3.html
	* Amazon IAM Console: 	
		1. create your credentials: Add Policy
		2. download private key file
	* Set your credentials file locally
		``` 
		$ aws configure 
		```
	* config.json & configWrangle.json:
		* Add AWS Keys in this file
		* Add raw Data Link to them
		* Add Team Information 
		* Add Email Sender and Receiver
		* Save them using required names
			* config.json
			* configWrangle.json
2. dataingestion.py & wrangle.py
	* For Both Processing simply run Code below:
		```
		# I use root, you can modify based on your need 
		$ sudo /bin/sh run.sh 
		```
	* See log files for more information After running.
	
3. Run in docker:
	1. Start Container
		```
		# port for Jupyter notebook
		$ docker run -it -p 8888:8888 <image> /bin/bash
		```
	2. Run *.py:
		```
		# I use root here
		$ sudo /bin/sh run.sh
		```
	3. Run EDA on Jupyter in docker:	
		```
		# I use root here
		$ jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
		```
	4. Summary:
		* Docker : docker run -it -p 8888:8888 image:version 
		* Container : jupyter notebook --ip 0.0.0.0 --no-browser 
		* Host : localhost:8888/tre

# Docker (How to create this image by yourself)
1. Modify the Creator:
	* in process.py:
		```
		python-pip3 --> python3-pip
		RUN pip3 packages --> RUN pip3 install packages
		```
	* The code from GitHub is out of date.
2. Make Docker Images
	1. Run Docker Creator:
		```
		$ cd ~/your/path/Data-Science-in-the-Cloud/webApp
		$ python manage.py runserver 8000
		```
	2. Included Pakages: Python3.4
		* pandas
		* numpy
		* Matplotlib
		* IPython
3. Configure Images & Container
	1. basic:
	```
	$ docker images
	$ docker tag <IMAGE-ID> <IMAGE-NAME>
	```

	2. install packages:
	```
	$ pip3 install --upgrade pip
	$ pip3 install boto3
	$ pip3 install jupyter
	$ pip3 install seaborn
	```
4. Start Container
	```
	# port for Jupyter notebook
	$ docker run -it -p 8888:8888 <image> /bin/bash
	```
5. Copy File to Container
6. Commit the container:
	```
	$ docker commit container-name
	$ docker tag <image-to-be-committed> <repository name>
	```
7. Public images:
	```
	$ docker push <repository-name>
	```
# AWS Batch
1. Image: besimilar/advanced-data-analysis:final 
2. COMMAND: 
	* /bin/bash -c Ref::code
	* code : cd /Assignment1/Data* ; sudo /bin/sh run.sh
	* Ref::code refers to command above
	* Data*: for DataIngestion or DataWrangling folders



		

