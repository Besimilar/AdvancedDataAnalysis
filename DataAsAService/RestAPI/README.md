# Configuration
1. Add your AWS key in zillow/static/config.json
2. Unzip zillow/static/ZillowData.csv.zip
3. Or Download ZillowData.csv from kaggle:

	* https://www.kaggle.com/c/zillow-prize-1
	* save under zillow/static/

# Virtualenv
1. Install virtualenv
	```
	$ sudo pip install virtualenv
	```
2. Create your own environment
	```
	$ mkdir myproject
	$ cd myproject
	$ virtualenv <envName>
	```
3. Active environment if needed
	```
	$ . <envName>/bin/activate
	```
4. Deactivate after finishing
	```
	$ deactivate
	```

# Flask
Tutorial: http://flask.pocoo.org/

1. Install Flask
	```
	$ pip install Flask
	```
2. Install this application:
	```
	# run in project root directory, zillow/
	$ pip install --editable .
	```
2. Start application
	```
	$ export FLASK_APP=zillow
	$ flask run
	```
3. Listen to all public IPs
	```
	$ flask run --host=0.0.0.0
	```
4. Debug mode for development 
	```
	$ export FLASK_DEBUG=1
	$ flask run
