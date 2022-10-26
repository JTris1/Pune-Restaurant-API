# Pune Restaurant API
This API allows for a connection to a MongoDB database containing Restaurants and Neighborhoods in Pune, India. This is for a class project.

## How to Use
### Config
Copy `.env_template` to `.env` and add the connection URI from MongoDB.
### Virtual ENV
Use the following to create a virtual environment:
```
python3 -m venv env
```

Activate the virtual env with 
```
source <PROJECT_DIRECTORY>/env/bin/activate
```

Run the following to ensure the path returned is the python binary in the env directory.
```
which python3
```
 

Lastly, install the pip dependencies using
```
pip install -r requirements.txt
```

### Run Flask Server
Run the following command to start the Flask server
```
flask --app test run
```


## Endpoints
As of now, only restaurant endpoints are implemented.

### Restaurants
#### **/restaurants**
Retrieves all restaurants in the database.

Supports Query Strings

Example: 
----------
**/restaurants?name=Vohuman+Cafe**
