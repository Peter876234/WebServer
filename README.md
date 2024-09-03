# JSON_WebService

# Introduction of each file
## ProjectServer.py
ProjectServer.py which contains two JSON web services on the client and interacts to 
the given quote server.

## quote_server.py
This given server will get quote information and interact with ProjectServer.py.

## Mypytest.py
Mypytest.py has different test cases to test servers. 

## UserData.json
UserData.json contains user information which has two columns: username and number_of_requests.

## test(with_different_inputs)
This would provide different inputs to test each case for the server.

# Instructions for setting up and executing the project server
-Python version used: 3.11.7 
First, click in the folder open the terminal, and install the flask 3.0.0 by the command:
`pip install flask`
Second, execute the ProjectServer.py by the command in the terminal.
`python .\ProjectServer.py`

## For testing service
install the pytest 7.4.3 by the command in terminal:
`pip install pytest`

Second, execute the ProjectServer.py, quote_server.py, and Mypytest.py by the command in the terminal.
```
python .\ProjectServer.py
python .\quote_server.py 
python -m pytest .\Mypytest.py 
```
*Kindly remind: After running the Mypytest.py, .pytest_cache and __pycache__ folder would be generated as results.


