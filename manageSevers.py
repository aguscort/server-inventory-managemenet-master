#!/usr/bin/env python
from serverMgm import *
import sys
import urllib

def runQuery():
    query4 = "http://ocvlp-add002/api/v1.0/data/search?query=SEARCH%20DatabaseDetail%20HOW%20*&limit=10"
    f = urllib.urlopen(query4)
    print f.read()


if len(sys.argv) <= 1:
	print ("arguments: get, check, add, remove, move, switch, apply")
else:
	if str(sys.argv[1]) == 'get':
		#
		# 1. Get the files from their origin, populate the database and remove the files
		#
		#get_unix_server_files()
		#get_ping_server_files()
		get_server_files()

		#
		# 2. Check the number of server in each agent
		#
		#agents_load_from_files()
		
		#
		# Create the table when the changes will be applied from now on
		#
		#create_servers_table()
		#create_agents_table()

		#
		# 3 .Fill the table with the files content currently
		#
		populate_servers_table()
		#populate_agents_table()
		#
		# Check the value from both sources
		#
		agents_load_from_db()
		#agents_load_from_files()

		#
		# Remove files
		# 
		#backup_config_files()
		#remove_local_files()
	
	elif  str(sys.argv[1]) == 'ping':
                get_ping_server_files()
		set_new_ping_server_DR_files(ext='tst')
	elif  str(sys.argv[1]) == 'reubicate':
		reubicate_servers_acording_their_location()
	
	elif  str(sys.argv[1]) == 'check':
		#
		# Confirm if a couple of servers are actually monitored and from which agent
		#
		check_unix_servers()
		#agents_load_from_files()
		agents_load_from_db()
	elif  str(sys.argv[1]) == 'add':
		#
		# Perform modifications
		#
		#agents_load_from_db()
		#to_add = [('ccvlp-apt042.tmdn.org', 'ocvlp-bmc013'),
		#       ('ccvlp-apt073.tmdn.org', 'ocvlp-bmc013')]
		add_servers()
		agents_load_from_db()
	elif  str(sys.argv[1]) == 'remove':
                #
                # Perform modifications
                #
                #agents_load_from_db()
                #to_delete = ['ccvlp-apa002.tmdn.org','ccvlp-apt004.tmdn.org','ccvlp-apt005.tmdn.org']
                remove_servers()
                #to_add = [('ccvlp-apt042.tmdn.org', 'ocvlp-bmc013'),
                #       ('ccvlp-apt073.tmdn.org', 'ocvlp-bmc013')]
                agents_load_from_db()
	elif  str(sys.argv[1]) == 'move':
		#
		# Move all the servers in an agent to another one
		#
		#agents_load_from_db()
		assign_servers_to_new_agent(sys.argv[2], sys.argv[3])
		agents_load_from_db()
	elif  str(sys.argv[1]) == 'switch':
		#
		# Switch the server beetwen two agents
		#
		#agents_load_from_db()
		switch_agents(sys.argv[2], sys.argv[3])
		agents_load_from_db()
	elif  str(sys.argv[1]) == 'apply':
		#
		# Apply the changes in new config files
		#
		recreate_unix_server_files()
		#recreate_ping_unix_server_files()
		#recreate_ping_windows_server_files()
		#recreate_windows_server_files()
		#publish()
		#
		# Upload the data to the diferents agents
		#
		set_new_unix_server_files('ocvlp-bmc007',ext = 'tst')
		#set_new_unix_server_files('orvlp-bmc012', ext =  'tst')
		#set_new_unix_server_files('orvlp-bmc013', ext = 'tst')
		#set_new_unix_server_files('ocvlp-bmc015',ext = 'tst')
                #set_new_unix_server_files('ocvlp-bmc016', ext =  'tst')
		#set_new_unix_server_files('orvlp-bmc406', ext =  'tst')
		#set_new_ping_server_files(ext='tst')
		#set_new_windows_server_files('orvwp-bmc402', ext = 'tst')
		#et_new_windows_server_files('ocvwp-bmc007', ext = 'tst')
		#set_new_windows_server_files('ocvwp-bmc008', ext = 'tst')
		#set_new_windows_server_files('orvwp-bmc401', ext = 'tst')
		#pass
	elif  str(sys.argv[1]) == 'test':
		runQuery()
