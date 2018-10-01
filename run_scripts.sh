conda env create -f environment.yml
source activate coding_exercise

export HOST=127.0.0.1
export USERNAME=test_user
export PASSWORD=test_password
export DBNAME=test_database
export BATCH_SIZE=1000
export NR_PROCESS=4

createdb
psql -c "CREATE ROLE $USERNAME WITH LOGIN PASSWORD '$PASSWORD';"
psql -c "CREATE DATABASE $DBNAME OWNER $USERNAME;"

redis-server &

python main_setups.py
python main_data_loading.py &
python main_update_redis.py &
