# Celery Pipelines
1. Installation Celery
	```
	$ pip install -U Celery
	```
2. Install rabbitmq:
	```
	brew install rabbitmq
	# To have launchd start rabbitmq now and restart at login:
 	#  		brew services start rabbitmq
	# Or, if you don't want/need a background service you can just run:
 	#  		rabbitmq-server
	```

		* start the server:
		```
		$ sudo rabbitmq-server
		```
		* run it in the background:
		```
		$ sudo rabbitmq-server -detached
		```
		* stop the server:
		```
		$ sudo rabbitmq-server stop
		```
3. Start Worker:
	```
	$ celery -A proj worker -l info
	```
4. Start Scheduling:
	```
	# easy way
	$ celery -A proj worker -B -l info
	#
	$ celery -A proj beat -l info
	```

5. Before Start Pipelines: 
	
	* Don't forget to add AWS key into config.json in Container.
