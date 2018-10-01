# Exercise

Setup the following tools:
- Local Postgres DB
- Local Redis DB

The program should be a python job that runs every 5 seconds, to read data from the Postgres database and saves it in 
Redis. Demonstrated usage of multiprocessing techniques will be a big plus.


## Getting Started

Clone the github repo to get the source.

```
git clone https://github.com/rguigoures/coding_exercise.git
```


### Prerequisites

Python3, Anaconda, Postgres and Redis must be installed. 

### Running the code

The script called run_scripts.sh will run all the steps described below.

```
bash run_scripts.sh
```

### Installing

The following command will create a conda environment with all necessary packages.

```
conda env create -f environment.yml
```

To start the conda environment. Run the following command:
```
source activate coding_exercise
```

### Environment variables

The following environment variables must be defined:

- _HOST_: ip of the server running Postgres and Redis
- _USER_NAME_: the username to connect to the postgres database. 
- _PASSWORD_: the password to connect to the postgres database. 
- _DBNAME_: name of the postgres database. 
- _NR_PROCESS_: number of processes to run in parallel when updating Redis
- _BATCH_SIZE_: size of the data batch to be fetched from Postgres and updated to Redis

```
export HOST=127.0.0.1
export USERNAME=test_user
export PASSWORD=test_password
export DBNAME=test_database
export NR_PROCESS=4
export BATCH_SIZE=1000
```

### Set up Postgres and Redis

First step consists in creating the user role and the database

```
createdb
psql -c "CREATE ROLE $USERNAME WITH LOGIN PASSWORD '$PASSWORD';"
psql -c "CREATE DATABASE $DBNAME OWNER $USERNAME;"
```
Then a first script runs creates a user table if it does not exists, truncates it and loads $10^5$ data points.
This script also flushes Redis

```
python main_setups.py
```

### Trigger data updates

A second script runs in the background and inserts or updates new data at irregular time intervals.

```
python main_data_loading.py &
```

### Update Redis every 5 second

A third script launches several 4 threads (environment parameter), each of them running batch updates of Redis from Postgres.

```
python main_data_loading.py &
```