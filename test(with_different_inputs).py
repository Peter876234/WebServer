import requests
import json

def testingpi(username=None, password=None, simulations=None, concurrency=None,testing_data=None):
    url = "http://localhost:5000/pi"
    headers = {"Content-Type": "application/json"}
    if testing_data is not None:
        data = testing_data
 
        for key in data.keys():
            if key == "username":
                data['username'] = username
            if key == "password":
                data["password"] = password
            if key == "simulations":
                data["simulations"] = simulations
            if key == "concurrency":
                data["concurrency"] = concurrency
        
    else:
        data = {
            "username": username,
            "password": password,
            "simulations": simulations,
            "concurrency":concurrency
        }
    
    res= requests.post(url, headers=headers, data=json.dumps(data))
    error_code=res.status_code
    if res.status_code == 200:
        print(res.json(),"\n")
    else:
        print("Error code:",error_code)
        print("Error messsage:", res.text)

def testingquote(username, password,protocol,concurrency=None, testing_data=None):
    
    url = "http://localhost:5000/quote"
    headers = {"Content-Type": "application/json"}

    if testing_data is not None:
        data = testing_data
 
        for key in data.keys():
            if key == "username":
                data['username'] = username
            if key == "password":
                data["password"] = password
            if key == "simulations":
                data["protocol"] = protocol
            if key == "concurrency":
                data["concurrency"] = concurrency
    
    else:
        data = {
            "username": username,
            "password": password,
            "protocol": protocol,
            "concurrency":concurrency
        }
    
    res = requests.post(url, headers=headers, data=json.dumps(data))
    error_code=res.status_code
    #Server connection works then:
    if res.status_code == 200:        
        result = res.json()
        Quotes = result.get("quotes")
        print("quotes:")
        #print all quotes one by one
        for quote in Quotes:
            print("   ", quote)
        print()
    else:
        print("Error code:",error_code,"\n")
        print("Error messsage:", res.json(),"\n")

# 1. For the user information testing
# 1.1 username key missing case 
testing_data = {
            #"username":"",
            "password":"",
            "simulations":"",
            "concurrency":""
        }
print("1.1 username key missing case:" )
testingpi("1234-pw", 100, 8, testing_data)

# 1.2 password key missing case 
testing_data = {
            "username":"",
            #"password":"",
            "simulations":"",
            "concurrency":""
        }
print("1.2 password key missing case:" )
testingpi("1234", 100, 8, testing_data)

# 1.3 username key int type case
print("1.3 username key int type case:" )
testingpi(1234,"1234-pw", 100, 8)

# 1.4 username key not digit in string type case
print("1.4 username key not digit in string type case:" )
testingpi("a234","1234-pw", 100, 8)

# 1.5 the length of username key more than 4 case
print("1.5 the lenght of username key more than 4 case:" )
testingpi("12345","1234-pw", 100, 8)

# 1.6 the length of username key lesser than 4 case
print("1.6 the lenght of username key lesser than 4 case:" )
testingpi("123","1234-pw", 100, 8)

# 1.7 password key not start with username case
print("1.7 password key not start with username case:" )
testingpi("1234","1111-pw", 100, 8)

# 1.8 password key not end with '-pw' case
print("1.8 password key not end with '-pw' case:" )
testingpi("1234","1111-pp", 100, 8)

# 1.9 successful case(correct username & password)
print("1.9 successful case(correct username & password):" )
testingpi("1234","1234-pw", 10000, 5)

# 2. For testing /pi server 

# 2.1 simulations key missing case
testing_data = {
            "username":"",
            "password":"",
            #"simulations":"",
            "concurrency":""
        }
print("2.1 simulations key missing case:" )
testingpi("1234","1234-pw", 8, testing_data)

# 2.2 simulations key not int type case
print("2.2 simulations key missing case:" )
testingpi("1234","1234-pw", "abc", 8)

# 2.3 simulations key < 100 case
print("2.3 simulations key < 100 case:" )
testingpi("1234","1234-pw", 99, 8)

# 2.4 simulations key > 100000000 case
print("2.4 simulations key > 100000000 case:" )
testingpi("1234","1234-pw", 100000001, 8)

# 2.5 concurrency key not int type case
print("2.5 concurrency key not int type case:" )
testingpi("1234","1234-pw", 1000, "abc")

# 2.6 concurrency key < 1 case
print("2.6 concurrency key < 1 case:" )
testingpi("1234","1234-pw", 1000, 0)

# 2.7 concurrency key > 8 case
print("2.7 concurrency key > 8 case:" )
testingpi("1234","1234-pw", 1000, 9)

# 2.8 missing input concurrency value case (concurrency will default 1)
testing_data = {
            "username":"",
            "password":"",
            "simulations":"",
            #"concurrency":""
        }
print("2.8 missing input concurrency value case (concurrency will default 1)" )
testingpi("1234","1234-pw", 100000000,None ,testing_data)

# 2.9 successful case(concurrency 8)
print("2.9 successful case:(concurrency 8)" )
testingpi("1234","1234-pw", 100000000, 8)


# 3 For testing quote of number 
# 3.1 missing protocol key case 
testing_data = {
        "username":"",
        "password":"",
        #"protocol":"",
        "concurrency":""
        }

print("3.1 missing protocol key case:" )
testingquote("1234","1234-pw" , 5, testing_data)

# 3.2 protocol key not in tcp/udp case 
print("3.2 protocol key not in tcp/udp case:" )
testingquote("1234","1234-pw", "abc" , 5, )

# 3.3 concurrency key not int type case
print("3.3 concurrency key not int type case:" )
testingquote("1234","1234-pw", "tcp", "abc")

# 3.4 concurrency key < 1 case
print("3.4 concurrency key < 1 case:" )
testingquote("1234","1234-pw", "udp", 0)

# 3.5 concurrency key >8 case
print("3.5 concurrency key > 8 case:" )
testingquote("1234","1234-pw","tcp", 9)

# 3.6 missing input concurrency value case (concurrency will default 1)
testing_data = {
        "username":"",
        "password":"",
        "protocol":"",
        #"concurrency":""
        }

print("3.6 missing input concurrency value case (concurrency will default 1)" )
testingquote("1234","1234-pw", "udp" , None ,testing_data)

# 3.7 successful tcp quotes with 1 concurrency case 
print("3.7 successful tcp quotes with 1 concurrency case:")
testingquote("1234","1234-pw", "tcp" , 1)

# 3.8 successful tcp quotes with 8 concurrency case 
print("3.8 successful tcp quotes with 8 concurrency case:")
testingquote("1234","1234-pw", "tcp" , 8)

# 3.9 successful udp quotes with 1 concurrency case 
print("3.9 successful udp quotes with 1 concurrency case:")
testingquote("1234","1234-pw", "udp" , 1)

# 3.10 successful udp quotes with 8 concurrency case 
print("3.10 successful udp quotes with 8 concurrency case:")
testingquote("1234","1234-pw", "udp" , 8)













