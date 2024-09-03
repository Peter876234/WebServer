# JSON_WebService

## Introduction of each file
- ProjectServer.py  
ProjectServer.py which contains two JSON web services on the client and interacts to 
the given quote server.

- quote_server.py  
This given server will get quote information and interact with ProjectServer.py.

- Mypytest.py  
Mypytest.py has different test cases to test servers. 

- UserData.json  
UserData.json contains user information which has two columns: username and number_of_requests.

- test(with_different_inputs)  
This would provide different inputs to test each case for the server.

## Requirements
- User Authentication:
  
  All requests must include valid user credentials, ensuring secure access.
  
- Statistics Management:

  The server must track and persist user request statistics, implementing mutual exclusion to handle concurrent access effectively.
  
- Functional Services:
  
  A pi web service that employs Monte Carlo simulations to compute π, with adjustable simulation counts and concurrency levels.
  
  A quote web service that retrieves quotes from a provided quote server, accommodating TCP and UDP protocols.

- Testing:
  
  Comprehensive automated testing must demonstrate the server’s compliance with functional requirements and error handling.

## Instructions for setting up and executing the project server
-Python version used: 3.11.7 
First, click in the folder open the terminal, and install flask 3.0.0 by the command:

`pip install flask`

Second, execute the ProjectServer.py by the command in the terminal.

`python .\ProjectServer.py`

## For testing server
install the pytest 7.4.3 by the command in the terminal:

`pip install pytest`

Second, execute the ProjectServer.py, quote_server.py, and Mypytest.py by the command in the terminal.
```
python .\ProjectServer.py
python .\quote_server.py 
python -m pytest .\Mypytest.py 
```
*Kindly remind: After running the Mypytest.py, .pytest_cache and __pycache__ folder would be generated as results.


