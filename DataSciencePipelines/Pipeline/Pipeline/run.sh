#!/usr/bin/env bash
# start container
docker start Team3Assign1

# For test
#docker exec -it Team3Assign1 /bin/bash -c 'cd /Assignment1/DataIngestion ; ls'

# start job in container
docker exec -it Team3Assign1 /bin/bash -c 'cd /Assignment1/DataIngestion ; sudo /bin/sh run.sh'
