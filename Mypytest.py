import pytest
import math
from ProjectServer import app

#Requirement 5
@pytest.fixture
def client():
    with app.test_client() as client: #Connect to the web server
        yield client

# seperate 2 functions to check username & password in pi and quote server
def test_invalid_username_and_password_in_pi_server(client):
    # Invalid username case:
    # Invalid username case: username length more than 4 
    userdata={'username':"666666","password":"6666-pw"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'

    # Invalid username case: username lesser more than 4 
    userdata={'username':"666","password":"666-pw"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'

    # Invalid username case: username not string type integer
    userdata={'username': 1111,"password":"1111-pw"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'

    # Invalid password case:
    # Invalid password case: not end with "-pw"
    userdata={'username':"1111","password":"1111-p"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'

    #Invalid password case: not start with username
    userdata={'username':"1111","password":"234-pw"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'

    # Missing key case:
    # Missing username key case
    userdata={"password":"1111-pw"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'
    
    # Missing password key case
    userdata={'username':"1111"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'

def test_invalid_username_and_password_in_quote_server(client):
    # Invalid username case:
    # Invalid username case: username length more than 4 
    userdata={'username':"666666","password":"6666-pw"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'

    # Invalid username case: username lesser more than 4 
    userdata={'username':"666","password":"666-pw"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'

    # Invalid username case: username not string type integer
    userdata={'username': 1111,"password":"1111-pw"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'

    # Invalid password case:
    # Invalid password case: not end with "-pw"
    userdata={'username':"1111","password":"1111-p"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'

    #Invalid password case: not start with username
    userdata={'username':"1111","password":"234-pw"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'

    # Missing key case:
    # Missing username key case
    userdata={"password":"1111-pw"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'
    
    # Missing password key case
    userdata={'username':"1111"}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 401
    assert data['error'] == 'user info error'


def test_pi_server_returns_correct(client):
    # Successful case of correct username, password, simulations and concurrency 
    userdata={'username':"1111","password":"1111-pw","simulations":int(1e8),"concurrency":8}
    res = client.post('/pi',json=userdata)
    data = res.get_json()
    assert res.status_code == 200
    #Assume that the deviation value of pi in 0.05
    assert (data['pi value']-math.pi)<0.05

def test_pi_server_concurrency_processing_time(client):
    # Testing the processing time of higher level of concurrency(8) lesser than lower level of concurrency(1)
    # Using concurrency(8) & concurrency(1) can see the different clearly 

    high_concurrency_userdata={'username':"1111","password":"1111-pw","simulations":int(1e8),"concurrency":8}
    high_concurrency_res = client.post('/pi',json=high_concurrency_userdata)
    high_concurrency_data = high_concurrency_res.get_json()
    assert high_concurrency_res.status_code == 200
    #When the simulations and concurrency changed , check the deviation again 
    assert 0.01 > abs(high_concurrency_data['pi value']-math.pi)

    mid_concurrency_userdata={'username':"1111","password":"1111-pw","simulations":int(1e8),"concurrency":5}
    mid_concurrency_res = client.post('/pi',json=mid_concurrency_userdata)
    mid_concurrency_data = mid_concurrency_res.get_json()
    #When the simulations and concurrency changed , check the deviation again 
    assert 0.01 > abs(mid_concurrency_data['pi value']-math.pi)

    low_concurrency_userdata={'username':"1111","password":"1111-pw","simulations":int(1e8),"concurrency":1}
    low_concurrency_res = client.post('/pi',json=low_concurrency_userdata)
    low_concurrency_data = low_concurrency_res.get_json()
    #When the simulations and concurrency changed , check the deviation again 
    assert 0.01 > abs(low_concurrency_data['pi value']-math.pi)

    #Ensure that the high level concurrency processing time < median level concurrency processing time < low level concurrency processing time
    assert high_concurrency_data['processing time'] < mid_concurrency_data['processing time'] <low_concurrency_data['processing time']

def test_quote_server_requested_number_of_quotes(client):
    #Checking the quote server with TCP return the correct quotes number(1-8)
    for i in range(1,9):
        userdata={'username':"1111","password":"1111-pw","protocol":'tcp',"concurrency":i}
        returns_num = userdata['concurrency']
        res = client.post('/quote',json=userdata)
        data = res.get_json()
        assert res.status_code == 200
        assert  len(data['quotes'])==returns_num

    #Checking the quote server with UDP return the correct quotes number(1-8)
    for i in range(1,9):
        userdata={'username':"1111","password":"1111-pw","protocol":'udp',"concurrency":i}
        returns_num = userdata['concurrency']
        res = client.post('/quote',json=userdata)
        data = res.get_json()
        assert res.status_code == 200
        assert  len(data['quotes'])==returns_num


def test_pi_server_and_quote_server_field_missing_or_invalid_request_and_return_400(client):
    
    # Test pi server:

    # Missing concurrency key , concurrency would default to 1 and run 
    userdata = {'username': "1111", "password": "1111-pw", "simulations": 100}  
    res = client.post('/pi', json=userdata)
    data = res.get_json()
    assert res.status_code == 200

    # Invalid concurrency case: concurrency < 1 
    userdata = {'username': "1111", "password": "1111-pw", "simulations": 100,"concurrency":0}  
    res = client.post('/pi', json=userdata)
    data = res.get_json()
    assert res.status_code == 400
    assert data['error']=='invalid field concurrency'

    # Invalid concurrency case: concurrency > 8 
    userdata = {'username': "1111", "password": "1111-pw", "simulations": 100, "concurrency": 9}  
    res = client.post('/pi', json=userdata)
    data = res.get_json()
    assert res.status_code == 400
    assert data['error'] == 'invalid field concurrency'

    # Successful case
    userdata = {'username': "1111", "password": "1111-pw", "simulations": 100, "concurrency": 8}  
    res = client.post('/pi', json=userdata)
    data = res.get_json()
    assert res.status_code == 200

    # Missing simulations key 
    userdata = {'username': "1111", "password": "1111-pw", "concurrency": 8}
    res = client.post('/pi', json=userdata)
    data = res.get_json()
    assert res.status_code == 400
    assert data['error'] == 'missing field simulations'

    # Invalid simulations case: simulations > 100 
    userdata = {'username': "1111", "password": "1111-pw", "simulations": 99, "concurrency": 1}  
    res = client.post('/pi', json=userdata)
    data = res.get_json()
    assert res.status_code == 400
    assert data['error']=='invalid field simulations'

    # Invalid simulations case: simulations > 100000000
    userdata = {'username': "1111", "password": "1111-pw", "simulations": 1000000000, "concurrency": 1}  
    res = client.post('/pi', json=userdata)
    data = res.get_json()
    assert res.status_code == 400
    assert data['error'] == 'invalid field simulations'

    # Test quote server:

    # protocol test 
    # Successful case with TCP
    userdata = {'username': "1111", "password": "1111-pw", "protocol": 'tcp', "concurrency": 1}
    res = client.post('/quote', json=userdata)
    data = res.get_json()
    assert res.status_code == 200

    # Successful case with UDP
    userdata = {'username': "6666", "password": "6666-pw", "protocol": 'udp', "concurrency": 1}
    res = client.post('/quote', json=userdata)
    data = res.get_json()
    assert res.status_code == 200

    # Mising protocol case 
    userdata = {'username': "5555", "password": "5555-pw", "concurrency": 8}
    res = client.post('/quote', json=userdata)
    data = res.get_json()
    assert res.status_code == 400
    assert data['error'] == 'missing field protocol'

    # Invalid protocol case: not in tcp/udp
    userdata = {'username': "4444", "password": "4444-pw", "concurrency": 8,"protocol":"uup"}
    res = client.post('/quote', json=userdata)
    data = res.get_json()
    assert res.status_code == 400
    assert data['error'] == 'invalid field protocol'

    # Invalid protocol case: not in tcp/udp
    userdata = {'username': "3333", "password": "3333-pw", "concurrency": 8, "protocol": "ttt"}
    res = client.post('/quote', json=userdata)
    data = res.get_json()
    assert res.status_code == 400
    assert data['error'] == 'invalid field protocol'

    # Invalid protocol case: not in tcp/udp (NULL)
    userdata = {'username': "2222", "password": "2222-pw", "concurrency": 8, "protocol": ""}
    res = client.post('/quote', json=userdata)
    data = res.get_json()
    assert res.status_code == 400
    assert data['error'] == 'invalid field protocol'