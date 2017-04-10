## Description

This API service is developed using **flask** framework, with a few other libraries for webscraping(**requests**, **lxml**)
and unit test(**pytest**, **mock**)

## To start the API service

Create a new virtual environment and switch to the environment
```
mkvirtualenv message_parser
workon message_parser
```

Install dependencies
```
pip install -r requirements/prod.txt
```

Configure the app
```
export FLASK_APP=app.py
```

Then start the API service
```
flask run
```
This runs the server at localhost:5000, you can test it out using curl or POSTMAN.
If you need to encode your query param, http://meyerweb.com/eric/tools/dencoder/ is
a handy tool to encode/decode your message.

Example using POSTMAN:
```
GET localhost:5000/parsed_message?message=%40bob%20(omg)%20Olympics%20are%20starting%20soon%3B%20http%3A%2F%2Fwww.nbcolympics.com
```

## To run the tests

This will also do lint check for the code
```
tox
```

## Further improvements

Caching can be implemented to optimize the service at several places.
One is caching the valid emoticon list, since the list is unlikely to change frequently.
Another is caching the title of the url, since some viral links tend to get discussed a lot
during a short amount of time, and reaching out to an external endpoint could be time consuming.

Also, the web scrapping could consume a lot of time depending on the state of the endpoint, and
regex matching could take a lot of cpu/memory resource, these can be considered to move to worker
processes, and communicate with the api service thru a message queue.

More tests should also be added to achieve better test coverage. External service mocking is also
needed for integration testing.
