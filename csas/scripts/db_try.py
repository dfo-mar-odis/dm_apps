import mysql.connector

initial_args = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "dmapps_user",
    "password": "Bio+13579"
};

# Create initial connection
db = mysql.connector.connect(
    **connect_args
)

print(
    "MySQL connection ID for db: {0}".format(db.connection_id)
    # "Initial MySQL connection ID ...: {0}".format(db.connection_id)
)

db.close()

