import xmlrpclib
import subprocess
import threading

# update the link delays with current latency between links  based on ping results
def cur_ping_status():
   threading.Timer(6.0, cur_ping_status).start()
	 #run shell script in the background every 'n' seconds
	 subprocess.Popen(['./h1_ping.sh'])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# RPC 

proxy = xmlrpclib.Server('http://localhost:8081', allow_none=True)
try:
    #print proxy.disp_msg('Hello')
    print proxy.set_left_delay(get_current_delay())
    #print proxy.get_delays()

except Exception, err:
    print 'Fault code:', err.faultCode
    print 'Message   :', err.faultString
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# retrives current latency values from the files and returns average delay 

# tokenize the line written in the file and store each column in array
tokens = []
def read_by_tokens(fileobj):
    for line in fileobj:
        for token in line.split():
            tokens.append(token)

# get the average delay between host 1  or host 2 and isp
def get_current_delay():
	filename = "host1.txt"
	with open(filename,"r") as f:
		global tokens
		read_by_tokens(f)
		cur_delay = tokens[5]
		tokens = []
		return cur_delay
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
