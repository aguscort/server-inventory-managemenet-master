# This script imports the configuration files among the linux agents
import os, time
import sqlite3

# Path
scriptPath = '/home/opsmon/scripts/server-inventory-managemenet/'

# Servers
unixServers =  ['ocvlp-bmc012','orvlp-bmc012','ocvlp-bmc013','orvlp-bmc013','ocvlp-bmc015','ocvlp-bmc016','orvlp-bmc406']
windowsServers = ['orvwp-bmc402','ocvwp-bmc007','ocvwp-bmc008','orvwp-bmc401','ocvwp-bmc016','ocvwp-bmc017']
pingFiles = ['Ping-Servidores-Linux.txt', 'Ping-Servidores-Windows.txt']

# Thresholds
unixThreshold= 125
windowsThreshold = 275


#
# Get files from sources
#
#########################
def get_server_files(ext = 'txt'):
    get_unix_server_files(ext)
    get_windows_server_files()
    get_ping_server_files()

def get_unix_server_files(ext = 'txt'):
    for server in unixServers:
        try:
            copyFile = 'rsync -P -e ssh opsmon@' + server + ':/opt/bmc/servrem-'+ \
                        server + '.' + ext + ' ./files'
            result = os.system(copyFile)
            if result == 0:
                print 'File copied successfully'
        except Exception as e: 
            print("An exception of type {0} occurred. \
                 Arguments:\n{1!r}".format(type(e).__name__, e.args))

def get_windows_server_files():
    pass

def get_ping_server_files():
    for pingFile in pingFiles:
        try:
            copyFile = 'rsync -P -e ssh opsmon@ocvlp-bmc011:/opt/bmc/patrol/Patrol3/PPM/Conf/' + \
                        pingFile + ' ./files'
            result = os.system(copyFile)
            if result == 0:
                print ('File copied successfully')
        except Exception as e:
	    print("An exception of type {0} occurred. \
                Arguments:\n{1!r}".format(type(e).__name__, e.args))


#
# Replace with new files into sources
#
#####################################
def set_new_unix_server_files(server = None, path = 'files', ext='tst'):
     if server:
        try:
            copyFile = 'rsync -P -e ssh ./' + path + '/servrem-'+ \
                        server + '.txt  opsmon@'  + server + \
			':/opt/bmc/servrem-' + server + '.' + ext
            result = os.system(copyFile)
	    os.system('ssh opsmon@' +  server + ' sudo chown '+ \
                      'truesight.truesight /opt/bmc/servrem-' + server + '.' + ext)
            if result == 0:
                print 'File copied successfully'
        except Exception as e:
            print("An exception of type {0} occurred. \
                 Arguments:\n{1!r}".format(type(e).__name__, e.args))

def set_new_windows_server_files():
    pass

def set_new_ping_server_files(path = 'files', ext = 'tst'):
    for pingFile in pingFiles:
        try:
            copyFile = 'rsync y -P -e ssh ./' + path + '/' + pingFile + \
                       	' opsmon@ocvlp-bmc011:/opt/bmc/patrol/Patrol3/PPM/Conf/' + \
			pingFile[:-3] + '.' + ext			
	    result = os.system(copyFile)
            os.system('ssh opsmon@ocvlp-bmc011 sudo chown '+ \
                      'truesight.truesight /opt/bmc/patrol/Patrol3/PPM/Conf/' + pingFile[:-3] + '.' + ext)
	    if result == 0:
                print 'File copied successfully'
        except Exception as e:
            print("An exception of type {0} occurred. \
                 Arguments:\n{1!r}".format(type(e).__name__, e.args))

def set_new_ping_server_DR_files(path = 'files', ext = 'tst'):
    for pingFile in pingFiles:
        try:
            copyFile = 'rsync y -P -e ssh ./' + path + '/' + pingFile + \
                        ' opsmon@orvlp-bmc011:/opt/bmc/patrol/Patrol3/PPM/Conf/' + \
                        pingFile[:-3] + '.' + ext
            result = os.system(copyFile)
            if result == 0:
                print 'File copied successfully'
        except Exception as e:
            print("An exception of type {0} occurred. \
                 Arguments:\n{1!r}".format(type(e).__name__, e.args))


def backup_config_files():
    try:
    	os.system('git --git-dir=' + scriptPath + 'files/.git/ --work-tree=' + scriptPath + 'files/  add ' + scriptPath + 'files/')
	os.system('git --git-dir=' + scriptPath + 'files/.git/ --work-tree=' + scriptPath + 'files/ commit -m "Servers Status List at ' +  time.strftime('%d/%m/%Y')+ ' ' + time.strftime('%H:%M') + '"')
    except Exception as e:
            print("An exception of type {0} occurred. \
                 Arguments:\n{1!r}".format(type(e).__name__, e.args))

#
# Remove files from local 
#
#####################################
def remove_local_files():
	remove_local_unix_server_files()
	remove_local_windows_server_files() 
	remove_local_ping_files()


def remove_local_unix_server_files():
    for server in unixServers:
        try:
	    if os.path.isfile(os.path.join('.','files', 'servrem-' + server + '.txt')):
            	os.remove(os.path.join('.','files', 'servrem-' + server + '.txt'))
        except Exception as e: 
            print("An exception of type {0} occurred. \
                 Arguments:\n{1!r}".format(type(e).__name__, e.args))


def remove_local_windows_server_files():
    for server in windowsServers:
        try:
	    if os.path.isfile(os.path.join('.','files', 'servrem-' + server + '.txt')):
            	os.remove(os.path.join('.','files', 'servrem-' + server + '.txt'))
        except Exception as e:
            print("An exception of type {0} occurred. \
                 Arguments:\n{1!r}".format(type(e).__name__, e.args))


def remove_local_ping_files():
    for pingFile in pingFiles:
        try:
            if os.path.isfile(os.path.join('.','files',pingFile)):
		os.remove(os.path.join('.','files', pingFile))
        except Exception as e:
            print("An exception of type {0} occurred. \
                 Arguments:\n{1!r}".format(type(e).__name__, e.args))

#
# Perform actions related to the database
#
##########################################
def create_servers_table():
    conn = sqlite3.connect(os.path.join('db','servers.db'))
    cursor = conn.cursor()
    # Create the servers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servers_inventory (
        serverName VARCHAR(50) PRIMARY KEY, 
        agentName VARCHAR(50),
        enabled BOOLEAN,
        os VARCHAR(10),
        location VARCHAR (3),
        scope VARCHAR(10)      
        )
        ''')
    # Create index
    cursor.execute('''
        CREATE UNIQUE INDEX idx_servers_serverName ON servers_inventory (serverName);  
        ''')    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()    

def create_servers_buffer_table():
    conn = sqlite3.connect(os.path.join('db','servers.db'))
    cursor = conn.cursor()
    # Create the servers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servers_buffer (
        serverName VARCHAR(50) PRIMARY KEY,
        enabled BOOLEAN,
        os VARCHAR(10),
        location VARCHAR (3),
        checked BOOLEAN,
	discarded BOOLEAN,
	function VARCHAR(50),
	app VARCHAR(50)
	)
        ''')
    # Create index
    cursor.execute('''
        CREATE UNIQUE INDEX idx_servers_buffer_serverName ON servers_buffer (serverName);
        ''')
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def create_agents_table():
    conn = sqlite3.connect(os.path.join('db','servers.db'))
    cursor = conn.cursor()
    # Create the alarms table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS  agents (
        agentName VARCHAR(50) PRIMARY KEY, 
        os VARCHAR(10),
        location VARCHAR (3),
        function VARCHAR (10)              
        )
        ''')
    # Create index
    cursor.execute('''
        CREATE UNIQUE INDEX idx_agents_agentName ON agents (agentName);  
        ''')

def populate_agents_table():
    conn = sqlite3.connect(os.path.join('db','servers.db'))
    cursor = conn.cursor()
    agents = [('ocvlp-bmc012','unix','AA','remote monitoring'),
		('orvlp-bmc012','unix','BUC','remote monitoring'),
		('ocvlp-bmc013','unix','AA','remote monitoring,exceptions'),
		('orvlp-bmc013','unix','BUC','remote monitoring,exceptions'),
		('orvwp-bmc402','windows','BUC','remote monitoring'),
		('ocvwp-bmc007','windows','AA','remote monitoring'),
		('ocvwp-bmc008','windows','AA','remote monitoring,out of domain'),
		('orvwp-bmc401','windows','BUC','remote monitoring,out of domain'),
		('ocvlp-bmc015','unix','AA','remote monitoring'),
		('ocvlp-bmc016','unix','AA','remote monitoring'),
		('orvlp-bmc406','unix','BUC','remote monitoring'),
		('ocvwp-bmc016','windows','AA','remote monitoring'),
		('ocvwp-bmc017','windows','AA','remote monitoring'),
		('orvwp-bmc402','windows','BUC','remote monitoring'),
		('ocvlp-bmc011','unix','AA','ping')]
    try:
        cursor.executemany('''
          INSERT OR IGNORE INTO agents (agentName, os, location, function)
                    VALUES (?, ?, ?, ?)
                    ''', agents)

    except Exception as e:
        print("An exception of type {0} occurred. \
                Arguments:\n{1!r}".format(type(e).__name__, e.args))
    else:
        conn.commit()
    conn.close()


def populate_servers_table():
    conn = sqlite3.connect(os.path.join('db','servers.db'))
    cursor = conn.cursor()
        
    cursor.execute('DELETE FROM servers_inventory')
    conn.commit()
    try:	
	for server in unixServers:
            with open(os.path.join('.','files', 'servrem-' + server + '.txt'),'r') as f:
                serversMonitored = f.read()
            serversMonitored = serversMonitored.split('\n')[0]
            toInsert =[]
            for i in range(0,len(serversMonitored.split(','))):
                toInsert.append((str(serversMonitored.split(',')[i]), server))
            cursor.executemany('''
                INSERT OR IGNORE INTO servers_inventory (serverName, agentName, os, enabled, scope) 
                    VALUES (?,?, "unix", 1, '')
                    ''', toInsert)
       	if True: 
            for server in windowsServers:
	    	if os.path.isfile(os.path.join('.','files', 'servrem-' + server + '.txt')):
			with open(os.path.join('.','files', 'servrem-' + server + '.txt'),'r') as f:
                		serversMonitored = f.read()
            		serversMonitored = serversMonitored.split('\n')[0]
            		toInsert =[]
            		for i in range(0,len(serversMonitored.split(','))):
                		toInsert.append((str(serversMonitored.split(',')[i]), server))
            		cursor.executemany('''
                		INSERT OR IGNORE INTO servers_inventory (serverName, agentName, os, enabled, scope)
                    		VALUES (?,?, "windows", 1, '')
                    		''', toInsert)
        
 	for pingFile in pingFiles:
	    if os.path.isfile(os.path.join('.','files', pingFile)):
		toInsert = []
            	with open(os.path.join('.','files', pingFile),'r') as f:
            		for line in f:
                		toInsert.append((str(line.split('\n')[0]), 'ping'))
                		del toInsert[-1]
            	cursor.executemany('''
                	INSERT OR IGNORE INTO servers_inventory (serverName, agentName, os, enabled, scope)
              	   	VALUES (?, '', '', 1, ?) 
                    	''', toInsert)
            
    except Exception as e:
        print("An exception of type {0} occurred. \
                Arguments:\n{1!r}".format(type(e).__name__, e.args))
    else:
        conn.commit()
    conn.close()

#
# Functions related to retrieve info about the servers/agents
#
#############################################################
def show_servers_unlocated():
    conn = sqlite3.connect(os.path.join('db','servers.db'))
    cursor = conn.cursor()
    servers = []
    try:
        result = cursor.execute('''
                SELECT *
                FROM servers_inventory
                WHERE location IS NULL
        ''').fetchall()
        for row in result:
                servers.append(({'serverName' : str(row[0]), 'agentName' : str(row[1])}))
    except Exception as e:
        print("An exception of type {0} occurred. \
                Arguments:\n{1!r}".format(type(e).__name__, e.args))
    conn.close()

    return servers

def count_servers_from_files(server = ''):
    if os.path.isfile(os.path.join('.','files', 'servrem-' + server + '.txt')):
    	with open(os.path.join('.','files', 'servrem-' + server + '.txt'),'r') as f:
        	    serversMonitored = f.read()
    	print 'Agent ' + server  +  ' has ' + str(len(serversMonitored.split(','))) + ' servers within.'

def agents_load_from_files():
    print '========= UNIX AGENTS (FILES) ============'
    for agent in unixServers:
            count_servers_from_files(agent)
    print '========= WINDOWS AGENTS (FILES) ============'
    for agent in windowsServers:
            count_servers_from_files(agent)


def count_servers_from_db(server = ''):
    conn = sqlite3.connect(os.path.join('db','servers.db'))
    cursor = conn.cursor()
    try:    
        result = cursor.execute('''SELECT COUNT(serverName) FROM servers_inventory  WHERE agentName LIKE ?''', (server,)).fetchone()
    except Exception as e:
        print("An exception of type {0} occurred. \
                Arguments:\n{1!r}".format(type(e).__name__, e.args))
    conn.close()
    print 'Agent ' + server  +  ' has ' + str(result[0]) + ' servers within.'


def agents_load_from_db():
    print '========= UNIX AGENTS (DB) ============'
    for agent in unixServers:
            count_servers_from_db(agent)        
    print '========= WINDOWS AGENTS (DB) ============'
    for agent in windowsServers:
            count_servers_from_db(agent)

def check_unix_servers(serverList = None, silent = False):
    if serverList == None:
	serverList = []
    	if os.path.isfile('list'):
        	with open(os.path.join('.','list'),'r') as f:
                	for line in f:
                        	serverList.append((line[:-1]))	
    resultString = ''
    conn = sqlite3.connect('/home/opsmon/scripts/server-inventory-managemenet/' + os.path.join('db','servers.db'))
    cursor = conn.cursor()
    try:    
       	for server in serverList:
        	result = cursor.execute('''SELECT serverName, agentName FROM servers_inventory WHERE serverName LIKE ?''', (server + '%',)).fetchone()
        	if result == None:
			if silent == False:
	            		print 'No server is registered as "' + server + '" in any agent.'
			resultString +=  server + ','
        	else:
			if silent == False:
            			print 'Server: "' + result[0] + '" is registered in agent: "'  + result[1] + '"'
			resultString +=   result[0] + ','  + result[1]  
    except Exception as e:
       	print("An exception of type {0} occurred. \
                Arguments:\n{1!r}".format(type(e).__name__, e.args))
    conn.close()
    return (resultString)


#
# Functions related to re-build the config files
#
#####################################################
def recreate_unix_server_files(path = 'files'):
    conn = sqlite3.connect(os.path.join('db','servers.db'))
    cursor = conn.cursor()
    try:    
        for server in unixServers:
            servers = ''
            for row in cursor.execute('''SELECT serverName FROM servers_inventory WHERE agentName LIKE ?''', (server,)):
                servers += row[0] + ','
            with open(os.path.join(path, 'servrem-' + server + '.txt'),'w') as f:
                f.write (servers[:-1])
    except Exception as e:
            print("An exception of type {0} occurred. \
                    Arguments:\n{1!r}".format(type(e).__name__, e.args))
    conn.close()

def recreate_windows_server_files(path = 'files'):
    conn = sqlite3.connect(os.path.join('db','servers.db'))
    cursor = conn.cursor()
    try:
        for server in windowsServers:
            servers = ''
            for row in cursor.execute('''SELECT serverName FROM servers_inventory WHERE agentName LIKE ?''', (server,)):
                servers += row[0] + ','
            with open(os.path.join(path, 'servrem-' + server + '.txt'),'w') as f:
                f.write (servers[:-1])
    except Exception as e:
            print("An exception of type {0} occurred. \
                    Arguments:\n{1!r}".format(type(e).__name__, e.args))
    conn.close()

def recreate_ping_unix_server_files(path = 'files'):
    conn = sqlite3.connect(os.path.join('db','servers.db'))
    cursor = conn.cursor()
    try:
        servers = ''
        for row in cursor.execute('''SELECT serverName FROM servers_inventory WHERE os LIKE "unix"'''):
            servers += row[0] + '\n'
	with open(os.path.join(path, 'Ping-Servidores-Linux.txt'),'w') as f:
            f.write (servers)
    except Exception as e:
            print("An exception of type {0} occurred. \
                    Arguments:\n{1!r}".format(type(e).__name__, e.args))
    conn.close()

def recreate_ping_windows_server_files(path = 'files'):
    conn = sqlite3.connect(os.path.join('db','servers.db'))
    cursor = conn.cursor()
    try:
        servers = ''
        for row in cursor.execute('''SELECT serverName FROM servers_inventory WHERE os LIKE "windows"'''):
            servers += row[0] + '\n'
        with open(os.path.join(path, 'Ping-Servidores-Linux.txt'),'w') as f:
            f.write (servers)
    except Exception as e:
            print("An exception of type {0} occurred. \
                    Arguments:\n{1!r}".format(type(e).__name__, e.args))
    conn.close()


#
# Functions related to manipulate the servers/agents
#
#####################################################
def add_servers(serverList = None):
        if serverList == None:
	    serverList = []
            if os.path.isfile('list'):
                with open(os.path.join('.','list'),'r') as f:
                    for line in f:
        		serverList.append((line.split(",")[0],line.split(",")[1][:-1]))
        conn = sqlite3.connect(os.path.join('db','servers.db'))
        cursor = conn.cursor()
	try:
            cursor.executemany('''
                    INSERT OR IGNORE INTO servers_inventory (serverName, agentName) 
                     VALUES (?,?)
                    ''', serverList)
            print 'There were ' + str(len(serverList)) + ' servers in the input but the number of servers actually added was ' + str(cursor.rowcount) 
        except Exception as e:
            print("An exception of type {0} occurred. \
                    Arguments:\n{1!r}".format(type(e).__name__, e.args))
        else:
            conn.commit()
        conn.close()


def remove_servers(serverList = None):   
        if serverList == None:
	    serverList = []
            if os.path.isfile('list'):
                with open(os.path.join('.','list'),'r') as f:
                    for line in f:
                        serverList.append(line[:-1])    
	conn = sqlite3.connect(os.path.join('db','servers.db'))
        cursor = conn.cursor()
        try:
		for server in serverList:
        		cursor.execute('''
				DELETE FROM servers_inventory WHERE serverName LIKE ?
				''', (server + '%',))
        except Exception as e:
            print("An exception of type {0} occurred. \
                    Arguments:\n{1!r}".format(type(e).__name__, e.args))
        else:
            conn.commit()
            print 'Servers removed'
        conn.close()


def assign_servers_to_new_agent(oldAgent, newAgent):   
        conn = sqlite3.connect(os.path.join('db','servers.db'))
        cursor = conn.cursor()
        try:
            cursor.execute('''UPDATE servers_inventory 
                                    SET agentName = ? 
                                    WHERE agentName LIKE ?''',
                                (newAgent, oldAgent))
            print str(cursor.rowcount) + ' servers moved from ' + oldAgent + ' to ' + newAgent
        except Exception as e:
            print("An exception of type {0} occurred. \
                    Arguments:\n{1!r}".format(type(e).__name__, e.args))
        else:
            conn.commit()            
        conn.close()


def switch_agents(agent1, agent2):
    	conn = sqlite3.connect(os.path.join('db','servers.db'))
    	cursor = conn.cursor()
    	try:
        	# Get servers from agent2
        	serversAgent2 = []
        	for row in cursor.execute('''SELECT serverName FROM servers_inventory WHERE agentName LIKE ?''', (agent2,)):
            		serversAgent2.append((row[0],agent1))
        	# Delete them
        	cursor.execute('''DELETE FROM servers_inventory WHERE agentName LIKE ?''', (agent2,))
    	except Exception as e:
        	print("An exception of type {0} occurred. \
                	Arguments:\n{1!r}".format(type(e).__name__, e.args))
    	else:
        	conn.commit()
   	conn.close()
    	# Move the servers to agent2
    	assign_servers_to_new_agent(agent1, agent2)
   	# Move the servers to agent1
	add_servers(serversAgent2)


#
# Functions related to publish info about the servers/agents
#
#############################################################
def publish():
	xmlPath = '/home/opsmon/scripts/server-inventory-managemenet/status/'
	xmlFile = 'files_config.html'
	configPath = '/home/opsmon/scripts/server-inventory-managemenet/'
	servers = []
	
	conn = sqlite3.connect(os.path.join('db','servers.db'))
        cursor = conn.cursor()

	infraestructure = {}
	#for server in windowsServers:
	#                for el in line.split(','):
	#                        serverInfo.update ({fields[index] : el})
	#                        index += 1
	#                servers.append(serverInfo)
	
	for agent in unixServers:
            servers = []
            for row in cursor.execute('''SELECT serverName FROM servers_inventory WHERE agentName LIKE ?''', (agent,)):
                servers.append(row[0])
	    infraestructure.update({"agent" : agent, "servers" : servers})	
	print infraestucture

	with open(xmlPath +  xmlFile, 'w') as f:
	        f.write('''
	        <style type="text/css">
	        .tg  {border-collapse:collapse;border-spacing:0;margin:0px auto;}
	        .tg td{font-family:Arial, sans-serif;font-size:14px;padding:4px 20px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
	        .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:4px 20px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
	        .tg .tg-1r1g{background-color:#fe0000;border-color:inherit;vertical-align:top}
	        .tg .tg-us36{border-color:inherit;vertical-align:top}
	        .tg .tg-ww61{background-color:#34ff34;border-color:inherit;vertical-align:top}
	        .tg .tg-iwoe{background-color:#68cbd0;border-color:inherit;vertical-align:top}
	        </style>
	        <table class="tg">
	        <tr><th class="tg-iwoe" colspan="8"><b>LINUX SERVERS<b></th></tr>
	        <tr>
	        <tr>
	        ''')
        	for field in fields:
	                f.write('<td class="tg-iwoe"><b>' + field + '</b></td>')
	        f.write('</tr>')
	
	        for server in servers:
	                f.write('<tr><td class="tg-us36">' + server["IT Family"] + '</td>')
	                f.write('<td class="tg-us36t">' + server["Application"] + '</td>')
        	        f.write('<td class="tg-us36t">' + server["vCenter"][4:] + '</td>')
	                f.write('<td class="tg-us36t">' + server["Host"] + '</td>')
	                f.write('<td class="tg-us36">' + server["location"] + '</td>')

	                result = check_unix_servers((server["Name"][:-1],), True)
	                #print result[5:5]
	                if result.split(",")[1] == '':
	                        f.write('<td class="tg-us36t">' + server["Name"][:-1] + '</td>')
	                        f.write('<td class="tg-1r1g">None</td>')
	                else:
	                        f.write('<td class="tg-us36t">' + result.split(",")[0] + '</td>')
	                        f.write('<td class="tg-ww61">'+ result.split(",")[1] + '</td>')
		                f.write('<td class="tg-us36"></td></tr>')
			f.write( time.strftime('<center><p>%d-%m-%Y %H:%M</p></center>'))

		conn.commit()
	        conn.close()

