import os

DBNAME = os.getenv("DBNAME")
USERNAME = os.getenv("USERNAME")
HOST = os.getenv("HOST")
PASSWORD = os.getenv("PASSWORD")
NR_PROCESS = int(os.getenv("NR_PROCESS"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE"))