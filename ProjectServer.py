import os
import json
import socket
import threading
from random import random
import multiprocessing,timeit
from flask import Flask, request, jsonify

app = Flask(__name__)
mylock=threading.Lock() #Create threading lock   

#Requirement 1
#Checking username and password, correct return True , incorrect return False 
def ValidUserData(username, password):

    #For username validing
    #  if username not string type, username not number type, lenght not equal 4 , return false
    if not isinstance(username, str) or not username.isdigit() or len(username) != 4:
        return False
    
    #For password validing 
    # Not start with username and not end with "-pw" , return false
    if password != username + '-pw':
        return False
    
    #If username & password not problem , return true
    if password == username + '-pw':
        return True
    

    
#Requirement 2 
# find the "UserData.json" file 
program_path = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_PATH = os.path.join(program_path, 'UserData.json')

#update the user request times
def update_user_request_times(username):
    with mylock:
        #if there are not file exist , just create a new one 
        if not os.path.exists(DATA_FILE_PATH):
            data = {'username': {}}

        else:
            #When find out the file, just load and read the data 
            with open(DATA_FILE_PATH, 'r') as userdata_file:
             data = json.load(userdata_file)

        userdata = data['username']

        #When the username in "UserData.json", increase 1 for the requests time
        if username in userdata:
            userdata[username]['number_of_requests'] += 1
            
        #If the username not in "UserData.json", create the new user and make 1 requests time for he/she
        else:
            new_user = {'number_of_requests': 1}
            userdata[username] = new_user

        # Save(write) "UserData.json" in local
        with open(DATA_FILE_PATH, 'w') as file:
            json.dump(data, file, indent=4)


#Requirement 3 
#study from lab02
def partition(simulations, concurrency):
    size = simulations // concurrency 
    starts = list(range(0, simulations+1, size))[0:concurrency] 
    stops = list(range(0, simulations+1, size))[1:concurrency] + [simulations+1] 
    return list(zip(starts, stops))

def count_in_circle(size, results):
    count = 0
    for i in range(size):
        x = random()
        y = random()
        if x * x + y * y < 1:
            count += 1
    results.put(count)

@app.route('/pi', methods=['POST'])
def pi_service():
    #Requirement1 
    userdata = request.get_json()
    
    username = userdata.get('username')
    password = userdata.get('password')

    #1st check: Key missing case
    if username is not None and password is not None :
        username= userdata['username']
        password= userdata['password']
    else:
        return jsonify({'error': 'user info error'}), 401
    
    # 2nd check: username / password  info error case 
    if not ValidUserData(username, password):
        return jsonify({'error': 'user info error'}), 401
    
    #Requirement2 update user request times 
    update_user_request_times(username)

    #Requirement 3 
    # find the Number of simulations 
    simulations = userdata.get('simulations')
    concurrency = userdata.get('concurrency',1)

    # When simulations Key not find , return error
    if simulations is None:
        return jsonify({'error': 'missing field simulations'}), 400
    
    # When it is not int, <100, > int(1e8), return error
    if not isinstance(simulations, int) or simulations < 100 or simulations > 100000000:
        return jsonify({'error': 'invalid field simulations'}), 400

    # When it is not int, <1, >8 , return error
    if not isinstance(concurrency, int) or concurrency < 1 or concurrency > 8:
        return jsonify({'error': 'invalid field concurrency'}), 400
    
    results = multiprocessing.Queue()
    processes = []

    start_time = timeit.default_timer()
    for start, stop in partition(simulations, concurrency):
        size = stop - start
        process = multiprocessing.Process(target=count_in_circle, args=[size, results])
        processes.append(process)
    for pr in processes: pr.start() 
    for pr in processes: pr.join()
    sum = 0
    while not results.empty():
        sum += results.get() #sum the reuslt if not empty
    pi = sum / simulations * 4
    end_time = timeit.default_timer()
    total_time= end_time - start_time # calcuate total time

    return jsonify({
        'simulations': simulations,
        'concurrency': concurrency,
        'pi value': pi,
        'processing time': total_time})

#Requirement 4
#function to apply TCP / UDP
def GetQuote(protocol):
        
        global quotes
        #set localhost and port=1700
        QuoteServerAddress = 'localhost'  
        QuoteServerPort = 1700
        #for TCP protocol
        if protocol == 'tcp':
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TcpSocket:
                TcpSocket.connect((QuoteServerAddress, QuoteServerPort ))
                quotes.append(TcpSocket.recv(1024).decode('utf-8'))
        else: 
            #for UDP protocol
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UdpSocket:
                UdpSocket.sendto(b"", (QuoteServerAddress, QuoteServerPort ))
                quote, _ = UdpSocket.recvfrom(1024)
                quotes.append(quote.decode('utf-8'))

@app.route('/quote', methods=['POST'])
def quote():

    #Requirement1 
    userdata = request.get_json()
    
    username = userdata.get('username')
    password = userdata.get('password')

    #1st check: Key missing case
    if username is not None and password is not None :
        username= userdata['username']
        password= userdata['password']
    else:
        return jsonify({'error': 'user info error'}), 401
    
    # 2nd check: username / password  info error case 
    if not ValidUserData(username, password):
        return jsonify({'error': 'user info error'}), 401
    
    #Requirement2 update user request times 
    update_user_request_times(username)

    #Get protocol and concurrency
    protocol = userdata.get('protocol')
    concurrency = userdata.get('concurrency', 1)

    #if the protocol key missing, return error
    if protocol is None:
        return jsonify({'error': 'missing field protocol'}), 400
    
    #if the protocol key not in tcp/udp, return error
    if protocol not in ('tcp', 'udp'):
        return jsonify({'error': 'invalid field protocol'}), 400
    
    #if the number of concurrenvy int, smaller 1 , bigger 8 , then return error 
    if not isinstance(concurrency, int) or concurrency < 1 or concurrency > 8:
        return jsonify({'error': 'invalid field concurrency'}), 400

    #create a quotes list 
    global quotes
    quotes = []
    threads = []
    start_time = timeit.default_timer() # start timer

    # References from lab
    for _ in range(concurrency):
        thread = threading.Thread(target=GetQuote,args=(concurrency,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = timeit.default_timer() # end timer
    total_time= end_time - start_time #how long to execte
    
    return jsonify({
        'protocol': protocol,
        'concurrency': concurrency,
        'quotes': quotes,
        'processing time': total_time,
    })

# run the server
if __name__ == "__main__":
    app.run()