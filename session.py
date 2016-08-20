#A script to check and org for all VM's for memory size and filter the ones above set limit. A csv file with
#the filename is created
from vcloud_report import *
from list_ad_objects import *
import sys, getopt
import json


#import all the classes
w = list_ad_objects()
x = vCloud_session()

def main(argv):

    inputfile = ''
    outputfile = ''
    try:
      opts, args = getopt.getopt(argv,"ho:",["org="])
    except getopt.GetoptError:
        print 'session.py -o <organization name>'
        sys.exit(2)
    for opt, arg in opts:

        if opt == '-h':
            print 'session.py -o <organization name>'
            sys.exit()
        elif opt in ("-o", "--org"):
            org = arg
    return org

if __name__ == "__main__":
    org = main(sys.argv[1:])

    with open('config.json') as data_file:
        data = json.load(data_file)

    username = data[org]["username"]
    password = data[org]["password"]
    url = data[org]["url"]
    memory_size = data[org]["memory_size"]
    to_email = data[org]["to_email"]
    x.sessions(username, org, password, url)

    #get the list of all the vm's
    vm_list = x.cache_vm(memory_size,org,to_email)