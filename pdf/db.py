import sqlite_utils
db = sqlite_utils.Database("./url.db")
# This line creates a "dogs" table if one does not already exist:

db["cat"].insert_all([
    {"name": "1Cleo", "age": 4},
    {"name": "1Pancakes", "age": 2}
], pk="id")