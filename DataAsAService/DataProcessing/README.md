# Upload data to AWS S3
1. DownLoad docker images and Start your container:
	```
	$ docker pull besimilar/advanced-data-analysis:dbaas
	```
1. Add your AWS key in config.json
2. Modify cleanDataFileName in config.json
3. Upload row DataSet to the project directory
4. Simply Run to start data Ingestion and data Wrangling:
	```
	# I use root, you can modify based on your need 
	$ sudo /bin/sh run.sh 
	```
