# United Remote User Manager Example API

This project was made for the competence test provided by United Remote.
The database used for this project was sqlite3

## Requirements
Python 3.11 (although it could possibly work on lower python3 versions)

python-pip

## Setup
Ideally, you want to set up a virtual environment for this, and activate it.
cd to the root folder of the project and run:
`virtualenv venv`

And to activate it:

Linux
`source venv/Scripts/activate`

Windows
`venv/Scripts/activate`



To install dependencies simply run:
`pip install -r requirements.txt`

Which should take care of installing all of the requirements for you.

Database migrations will be done automatically on first run of the application. Should there be an issue/the need to re-migrate, simply go to `instance` and remove `userinfo.db`

## Startup
To start the API, run `python main.py` from the project's root folder

Once you get a confirmation in the CLI ( Running on http://127.0.0.1:port), the API is active and the following endpoints are available:

`/users` - Supports GET requests to retrieve all users, and POST requests to insert single and multiple users. Sorted by ID by default, but supports `?sortby=name` as a parameter to sort by name

`/users/id` - Supports GET requests to return the specific user, by their ID

`users/id/delete` - Supports POST requests to delete a user of the given ID

`users/id/modify` - Supports PUT requests to modify a user of the given ID


## Payload format

The payload for creating and modifying user is in accordance with https://jsonplaceholder.typicode.com/users

The primary keys for the users table are: `name, username, email and phone`, with the exception of `name` they also have to be unique

To create a single user, make sure to send a json dict, and to create multiple users make sure to send a list of dicts, i.e.

```
Single User
 {
    "name": "Leonard Graham",
    "username": "legra",
    "email": "legrah@may.biz",
    "address": {
      "street": "Kulas Light",
      "suite": "Apt. 556",
      "city": "Gwenborough",
      "zipcode": "92998-3874"
    },
    "phone": "1-770-736-8031 x56443",
    "company": {
      "name": "Romaguera-Crona",
      "catchPhrase": "Multi-layered client-server neural-net",
      "bs": "harness real-time e-markets"
    }
  }

Multiple Users
 [{
    "name": "Leonard Graham",
    "username": "legra",
    "email": "legrah@may.biz",
    "phone": "1-770-736-8031 x56443"
  },
   {
    "name": "Steve Mould",
    "username": "smold",
    "email": "smold@yt.biz",
    "phone": "1-770-736-8031 x1234"
  }]
```

To modify a user, simply provide a json payload that matches the creation format, i.e.
`{"name": "SomeNewName"}`

## Tests

To run the solitary unit test, execute the following command:

`pytest application\tests\unit_tests`

There is no need to start up the API for the unit test.

To run the functional tests, make sure you do start the API beforehand, and in a separate CLI session run:

`pytest application\tests\functional_tests\`

## Troubleshooting
If, after installing the dependencies from requirements.txt, running main.py or tests results in a ModuleNotFoundError, make sure to add the project's root folder to your pythonpath:

Linux

`export PYTHONPATH=$PYTHONPATH:/absolute/path/to/project`

Windows

`set PYTHONPATH=%PYTHONPATH%;absolute/path/to/project`


If you have issues with port 5000, change the port to a desired one in line 23 of `main.py`


## Known Issues/Improvements
- The free geolocation service is not the most accurate and thus if it cannot locate the given address, it will set the latitude/longitude values to -1 as a fallback
- Validate_fields logic might not be intuitive at first, due to returning a list, however it makes error handling/user experience better, as a trade-off
- The user_dict dictionary is not built dynamically to ensure proper order of key/values on requests, as jsonify scrambles them around
- The print output in functional tests could be improved a bit
- There is no db cleanup for functional tests, in case they fail unexpectedly. For test_create_valid_user this means that should the user be created but fail to be validated, they need to currently be removed from the database by hand (fastest way is to remove the entire DB and re-initialize it by restarting the Flask app)
- While input is being sanitized (both for SQL and XSS) more security would be needed to not even allow posting such data into the DB in the first place
- Normally the functional tests would be their own, separate project. But for the sake of brevity I elected to make them a part of the project proper
