import time
import re
ip_pattern = re.compile(r'(^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
uri_pattern = re.compile(r'\/([a-zA-Z/?&=._/0-9]{9,})')
method_pattern = re.compile(r'GET|POST|PUT|TRACE|DELETE|OPTIONS')
code_pattern = re.compile(r'200|404|402|301|302|500|501')
def find_ips():
    ipsfile=open('Ips.txt','w+')
    for i in lines:

        ips = re.findall(ip_pattern,i)
        for ip in ips:
            ipsfile.write(ip+"\n")

    ipsfile.close()
def find_URI():
    urifile=open('URI.txt','w+')
    for i in lines:
        uris = re.search(uri_pattern,i)
        urifile.write(uris.group(0)+"\n")
    urifile.close()

def find_Methods():
    methodfile=open('methods.txt','w+')
    for i in lines:
        methods = re.findall(method_pattern,i)
        for method in methods:
            methodfile.write(method+"\n")
    methodfile.close()

def find_agents():
    global agents
    agents=[]
    agentfile = open("agents.txt",'w+')
    for line in lines:
        #agents.append(re.findall(agents_pattern,line))
        agent = line.split('"')[5]#.split(" ")[0]
        if agent not in agents:
            agent = str(agent)
            agentfile.write(agent+"\n")
    agentfile.close()

def extract_unique_ips():
    ips = []
    unique_ips=open("UniqueIps.txt","w+")
    ipfile = open("Ips.txt","r")
    iplines = ipfile.readlines()
    for ip in iplines:
        if ip not in ips:
            ips.append(ip)
            unique_ips.write(ip)
    unique_ips.close()
    ipfile.close()

def ip_input(user_ip):
    try:
        unique_ip = open("UniqueIps.txt","r")
    except (NameError , FileNotFoundError):
        Print("File not found..")
    unique_ipline = unique_ip.readlines()
    for line in lines:
        ip = re.findall(ip_pattern,line)
        uri = re.findall(uri_pattern,line)
        method = re.findall(method_pattern,line)

        if user_ip == ip[0]:
            print("URI: ", uri[0],"\n")
            print("Method: " ,method[0],"\n")

    unique_ip.close()

def find_code(input_code):
    print("URI for this code is \n")
    for line in lines:
        code = line.split(" ")[8]
        if input_code == code:
            URIs = re.search(uri_pattern,line)
            print(URIs.group(0))

try:
    log_file = open("access_log.txt","r")
    lines = log_file.readlines()
except (FileNotFoundError):
    print("The file is not found..\nByee!!")
    exit()

find_ips()
find_URI()
find_Methods()
find_agents()
extract_unique_ips()
try:
    print("Log Parser Application")
    print("-----------------------")
    choice = int(input("1) choose an IP to return all his requests.\n2) Choose between different status codes and return the URIs that are requested and replied with these codes\nChoice :  "))
    if choice == 1:
        ip_int = input("Enter ip to get it's request: ")
        ip_input(ip_int)
    elif choice == 2:
        code_int = input("Enter the code: ")
        code_int = str(code_int)
        find_code(code_int)
except (ValueError):
    print("Invalid value")
    exit()
log_file.close()
