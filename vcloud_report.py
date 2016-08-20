#A script to check and org for all VM's for memory size and filter the ones above set limit. A csv file with
#the filename is created
import base64
import requests
import xml.etree.ElementTree as ET
import math
from list_ad_objects import *
import csv
from mailerlist import *
import datetime


class vCloud_session(object):

        def __init__(self):
                # type: () -> object

                self.login = None
                self.headers = None
                self.endpoint = None
                self.org = None
                self.root = None
                self.vapp_template = None
                self.vapp = None
                self.to_email = None
		self.x = vCloud_Logger()

        def sessions(self, username, org, password, endpoint):

		self.endpoint = endpoint
                self.login = {'Accept':'application/*+xml;version=5.5', \
                           'Authorization':'Basic  '+ base64.b64encode(username + "@" + org + ":" + password)}
                p = requests.post(self.endpoint + 'sessions', headers = self.login)
                self.headers = {'Accept':'application/*+xml;version=5.5'}

                for k,v in p.headers.iteritems():
                        if k == 'x-json':
                                access_token_value = 'Bearer %s' % v[21:57]
                                self.headers["Authorization:"]=access_token_value
                        if k == "x-vcloud-authorization" : self.headers[k]=v
		self.x.log(lvl='i',msg=("session headers created ...OK"))

        def cache_vm(self,max_memsize,org,to_email):

            #get formatted date
            mydate=[]
            today = datetime.date.today()
            mydate.append(today)
            date_string = str(mydate[0])

            subject = 'vCloud Weekly Audit for '+ org + ' ' + date_string
            text = 'This is an email with attachment'
            #file_path_list = 'openedge.csv'

        #query cannot use int variables so this needs to be convered before url modification
            current_pages = 1
            current_pages = str(current_pages)
            file_path_list = []
            self.x = vCloud_Logger()
            self.w = list_ad_objects()
            self.mailsent = email_sent()
            e = requests.get(self.endpoint + 'query?type=vm&pageSize=128&page=' + current_pages + '&filter=(isVAppTemplate==false)',
            headers=self.headers)
            root = ET.fromstring(e.content)
            # get the number of pages of the result
            total_query = root.get("total")
            total_query = int(total_query)
            #total / number of results per page
            num_pages = total_query / 128.0
            #round off to higher number to find max pages
            num_pages = math.ceil(num_pages)
            current_pages = int(current_pages)
            #Open csv module to write list
            #make the filename same as org
            csv_filename = org
            csv_filename = csv_filename+'.csv'
            with open(csv_filename, 'wb') as fp:
                csv_file = csv.writer(fp,)
                data = ['VM','Memory Size','numberOfCpus','guestOs','vApp Name','Power Status','Email','Name']
                csv_file.writerow(data)
                while (current_pages <= num_pages):
                    current_pages = str(current_pages)
                    g = requests.get(self.endpoint + 'query?type=vm&pageSize=128&page='+current_pages+
                    '&filter=(isVAppTemplate==false)', headers = self.headers)
                    root = ET.fromstring(g.content)
                    current_pages = int(current_pages)
                    current_pages = current_pages + 1

                    for child in root:

                        self.vm_memsize = child.get("memoryMB")
                        #None type returned needs to be takes care of
                        if self.vm_memsize == None:
                            pass
                        else:
                            #convert to int for comparision
                            #Build the csv
                            self.vm_memsize = int(self.vm_memsize)
                            max_memsize = int(max_memsize)
                            if self.vm_memsize > max_memsize:
                                #get the owner for the vApp
                                self.vm_name = child.get("name")
                                self.power_state = child.get("status")
                                self.vm_href = child.get("container")
                                self.container_name = child.get('containerName')
                                self.number_cpu = child.get('numberOfCpus')
                                self.guest_os = child.get('guestOs')
                                vm_size_list = [self.vm_name, self.vm_memsize, self.number_cpu, self.guest_os,self.container_name, self.power_state]
                                h = requests.get(self.vm_href + '/' + 'owner', headers = self.headers)
                                root1 = ET.fromstring(h.content)
                                for owner in root1.iter('{http://www.vmware.com/vcloud/v1.5}User'):
                                    self.owner_name =  owner.attrib['name']
                                    self.owner_name = self.owner_name + "@example.com"
                                    self.display_name = self.w.user_object(self.owner_name)
                                    blist = [self.owner_name, self.display_name]
                                    vm_size_list.extend(blist)
                                csv_file.writerow(vm_size_list)
                            else:
                                pass
            csv_filename = str(csv_filename)
            file_path_list.append(csv_filename)
            self.mailsent.send_mail(to_email, subject, text, file_path_list)