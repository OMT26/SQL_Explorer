import mysql.connector as MC
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')

co = MC.connect(host = HOST, user = USER, password = PASSWORD, port = PORT, database = DATABASE)
cursor = co.cursor()

def get_sql(table,condition = None):
    if(condition == None):
        req = 'SELECT * FROM {}'.format(table)
    else:
        req = 'SELECT * FROM {} WHERE {}'.format(table,condition)
    cursor.execute(req)
    return  cursor.fetchall()

DB = get_sql('COLUMNS')

database = {}
ordinal_pos = {}
primary_key = {}
nullable = {}
typing_int = {}
data_type_int = ['int','bigint','tinyint']
typing_str = {}
data_type_str = ['char','varchar','longtext','tinytext','mediumtext','smallint']
typing_float = {}
data_type_float = ['double','float','decimal']
typing_date = {}
data_type_date = ['date']
typing_datetime = {}
data_type_datetime = ['datetime','timestamp','time']
typing_sql = {}

for base in DB:
    if (base[1] in database) == False:
        database[base[1]] = {}  
        ordinal_pos[base[1]] = {}
        primary_key[base[1]] = {}
        nullable[base[1]] = {}
        typing_int[base[1]] = {}
        typing_str[base[1]] = {}
        typing_float[base[1]] = {}
        typing_date[base[1]] = {}
        typing_datetime[base[1]] = {}
        typing_sql[base[1]] = {}
    if (base[2] in database[base[1]]) == False:
        database[base[1]][base[2]] = []
        ordinal_pos[base[1]][base[2]] = []
        primary_key[base[1]][base[2]] = []
        nullable[base[1]][base[2]] = []
        typing_int[base[1]][base[2]] = []
        typing_str[base[1]][base[2]] = []
        typing_float[base[1]][base[2]] = []
        typing_date[base[1]][base[2]] = []
        typing_datetime[base[1]][base[2]] = []
        typing_sql[base[1]][base[2]] = {}
    database[base[1]][base[2]].append(base[3]) 
    ordinal_pos[base[1]][base[2]].append(base[4])
    typing_sql[base[1]][base[2]][base[3]] = base[7]
    if (base[16] == 'PRI' and base[17] == 'auto_increment'):
        primary_key[base[1]][base[2]].append(base[3])
    if (base[6] == 'YES'):
        nullable[base[1]][base[2]].append(base[3])
    if base[7] in data_type_int:
        typing_int[base[1]][base[2]].append(base[3])
    if base[7] in data_type_str:
        typing_str[base[1]][base[2]].append(base[3])
    if base[7] in data_type_float:
        typing_float[base[1]][base[2]].append(base[3])
    if base[7] in data_type_date:
        typing_date[base[1]][base[2]].append(base[3])
    if base[7] in data_type_datetime:
        typing_datetime[base[1]][base[2]].append(base[3])


for db in database:
    print(db)
    i = input("Continue? y | n \n")
    if i != 'n' and i != 'N':
        script = 'import mysql.connector as MC\n'
        script += 'import json\n\n'
        script += 'HOST = "'+HOST+'"\n'
        script += 'USER = "'+USER+'"\n'
        script += 'PASSWORD = "'+PASSWORD+'"\n'
        script += 'PORT = "'+PORT+'"\n'
        script += 'DATABASE = "'+db+'"\n\n'
        script += "co = MC.connect(host = HOST, user = USER, password = PASSWORD, port = PORT, database = DATABASE)\n"
        script += "cursor = co.cursor()\n\n"
        
        for table in database[db]:
            script += "class "+table.capitalize()+":\n"
            script += "    def __init__(self, "
            i = 1
            for columns in database[db][table]:
                if(i != len(database[db][table])):
                    if columns in nullable[db][table]:
                        script += columns+" = None, "
                    else:
                        if columns in typing_int[db][table]:
                            script += columns+" = 0, "
                        elif columns in typing_str[db][table]:
                            script += columns+" = '', "
                        elif columns in typing_float[db][table]:
                            script += columns+" = 0.0, "
                        else:  
                            script += columns+" = None, "  
                else:    
                    if columns in nullable[db][table]:
                        script += columns+" = None"
                    else:
                        if columns in typing_int[db][table]:
                            script += columns+" = 0"
                        elif columns in typing_str[db][table]:
                            script += columns+" = ''"
                        elif columns in typing_float[db][table]:
                            script += columns+" = 0.0"
                        else:  
                            script += columns+" = None" 
                i += 1    
            script += "):\n"
            for columns in database[db][table]:
                script += "        self."+columns+" = "+columns+"\n"
            script += "\n"
            script += "    def to_dict(self) -> dict:\n"
            script += "        \"\"\"Return all actual value and their name into a dictionary : {"+"'name'"+" : "+"value"+"}\"\"\"\n"
            script += "        dict = {\n"
            for columns in database[db][table]:
                script += "            '"+columns+"' : self."+columns+",\n"  
            script += "        }\n"
            script += "        return dict\n\n"
            script += "    def get_type(self) -> dict:\n"
            script += "        \"\"\"Return all type in python of value and their name into a dictionary : {"+"'name'"+" : type}\"\"\"\n"
            script += "        dict = {\n"
            for columns in database[db][table]:
                if columns in typing_int[db][table]:
                    script += "            '"+columns+"' : 'int',\n"  
                elif columns in typing_str[db][table]:
                    script += "            '"+columns+"' : 'str',\n"  
                elif columns in typing_float[db][table]:
                    script += "            '"+columns+"' : 'float',\n"  
                elif columns in typing_date[db][table]:
                    script += "            '"+columns+"' : 'date',\n"   
                elif columns in typing_datetime[db][table]:
                    script += "            '"+columns+"' : 'datetime',\n" 
                else:
                    script += "            '"+columns+"' : 'Any',\n"  
            script += "        }\n"
            script += "        return dict\n\n"
            script += "    def get_sql_type(self) -> dict:\n"
            script += "        \"\"\"Return all type in sql of value and their name into a dictionary : {"+"'name'"+" : type|nullable|primary} \"\"\"\n"
            script += "        dict = {\n"
            for columns in database[db][table]:
                if columns in nullable[db][table]:
                    if(len(primary_key[db][table]) != 0):
                        if primary_key[db][table][0] == columns:
                            script += "            '"+columns+"' : '"+typing_sql[db][table][columns]+"|nullable|primary',\n"  
                        else: 
                            script += "            '"+columns+"' : '"+typing_sql[db][table][columns]+"|nullable',\n"     
                    else:
                        script += "            '"+columns+"' : '"+typing_sql[db][table][columns]+"|nullable',\n"     
                else:
                    if(len(primary_key[db][table]) != 0):
                        if primary_key[db][table][0] == columns:
                            script += "            '"+columns+"' : '"+typing_sql[db][table][columns]+"|primary',\n"  
                        else: 
                            script += "            '"+columns+"' : '"+typing_sql[db][table][columns]+"',\n"     
                    else:
                        script += "            '"+columns+"' : '"+typing_sql[db][table][columns]+"',\n" 
            script += "        }\n"
            script += "        return dict\n\n"
            script += "    def update(self,update=None,condition=None):\n"
            script += "        \"\"\"Returns nothing if there are no errors. If the object contains a primary key, then the 'condition' entry is not required\"\"\"\n"
            script += "        if update == None: return print('Error nothing to update!')\n"
            if(len(primary_key[db][table]) == 0):
                script += "        if update == None: return print('Error nothing to update!')\n"
                script += "        if condition == None: return print('Error need condition for update!')\n"
            script += "        co = MC.connect(host = HOST, user = USER, password = PASSWORD, port = PORT, database = DATABASE)\n"
            script += "        cursor = co.cursor()\n"
            script += "        req = f"+'"'+"UPDATE "+table+" SET {"+"update"+"} WHERE {"+"condition"+"}"+'"'+"\n"
            if(len(primary_key[db][table]) != 0):
                script += "        if condition == None:\n"
                script += "            req = f"+'"'+"UPDATE "+table+" SET {"+"update"+"} WHERE "+primary_key[db][table][0]+" = {self."+primary_key[db][table][0]+"}"+'"'+"\n"
            script += "        try:\n"
            script += "            cursor.execute(req)\n"
            script += "        except Exception as error:\n"
            script += "            print(req)\n"
            script += "            print(error)\n"
            script += "        co.commit()\n\n"
            script += "    def delete(self,condition=None):\n"
            script += "        \"\"\"Returns nothing if there are no errors. If the object contains a primary key, then the 'condition' entry is not required\"\"\"\n"
            if(len(primary_key[db][table]) == 0):
                script += "        if condition == None: return print('Error need condition for delete!')\n"
            script += "        co = MC.connect(host = HOST, user = USER, password = PASSWORD, port = PORT, database = DATABASE)\n"
            script += "        cursor = co.cursor()\n"
            script += "        req = f"+'"'+"DELETE FROM "+table+" WHERE {"+"condition"+"}"+'"'+"\n"
            if(len(primary_key[db][table]) != 0):
                script += "        if condition == None:\n"
                script += "            req = f"+'"'+"DELETE FROM "+table+" WHERE "+primary_key[db][table][0]+" = {self."+primary_key[db][table][0]+"}"+'"'+"\n"
            script += "        try:\n"
            script += "            cursor.execute(req)\n"
            script += "        except Exception as error:\n"
            script += "            print(req)\n"
            script += "            print(error)\n"
            script += "        co.commit()\n\n"
            script += "    def insert(self):\n"
            script += "        \"\"\"Insert the object values into the database. If there is a primary key then it defines its primary key with thes last line written in the database\"\"\"\n"
            script += "        co = MC.connect(host = HOST, user = USER, password = PASSWORD, port = PORT, database = DATABASE)\n"
            script += "        cursor = co.cursor()\n"
            script += "        msg = f"+'"'+"INSERT INTO "+table+" ("+'"'+"\n"   
            script += "        value_list = []\n"
            script += "        i = 1\n"
            script += "        for a in self.to_dict().keys():\n"
            script += "            if i == len(self.to_dict()):\n"
            script += "                msg += f"+'"'+"{"+"a"+"}"+'"'+"\n"
            script += "            else:\n"
            script += "                msg += f"+'"'+"{"+"a"+"},"+'"'+"\n"
            script += "            i += 1\n"
            script += "        msg += ') VALUES ('\n" 
            script += "        i = 1\n"         
            script += "        for a in self.to_dict().values():\n"
            script += "            if i == len(self.to_dict()):\n"
            script += "                msg += "+'"'+'%s'+'"'+"\n"
            script += "            else:\n"
            script += "                msg += "+'"'+'%s,'+'"'+"\n"
            script += "            i += 1\n"
            script += "            value_list.append(a)\n"
            script += "        msg += "+'"'+")"+'"'+"\n"
            script += "        try:\n"
            script += "            cursor.execute(msg,value_list)\n"
            if(len(primary_key[db][table]) != 0):
                script += "            self."+primary_key[db][table][0]+" = cursor.lastrowid\n"
            script += "        except Exception as error:\n"
            script += "            print(msg)\n"
            script += "            print(value_list)\n"
            script += "            print(error)\n"
            script += "        co.commit()\n\n"
                
        script += "def get_sql(table,condition = None) -> list:\n"
        script += "    global HOST\n"
        script += "    global USER\n"
        script += "    global PASSWORD\n"
        script += "    global PORT\n"
        script += "    global DATABASE\n"
        script += "    co = MC.connect(host = HOST, user = USER, password = PASSWORD, port = PORT, database = DATABASE)\n"
        script += "    cursor = co.cursor()\n"
        script += "    if(condition == None):\n"
        script += "        req = 'SELECT * FROM {}'.format(table)\n"
        script += "    else:\n"
        script += "        req = 'SELECT * FROM {} WHERE {}'.format(table,condition)\n"
        script += "    cursor.execute(req)\n"
        script += "    return  cursor.fetchall()\n\n"
        
        for table in database[db]:    
            script += "def get_"+table+"(condition = None) -> list:\n"
            script += "    \"\"\"Does a get on the database, return one or more "+table.capitalize()+" objects in a list\"\"\"\n"
            script += "    response = get_sql('"+table+"',condition)\n"
            script += "    object_list = []\n"
            script += "    for p in response:\n"
            script += "        object = "+table.capitalize()+"("
            i = 1
            for columns in database[db][table]:
                if(i != len(database[db][table])):
                    script += "p["+str(int(ordinal_pos[db][table][i-1])-1)+"],"
                else:    
                    script += "p["+str(int(ordinal_pos[db][table][i-1])-1)+"]"
                i += 1  
            script += ")\n"
            script += "        object_list.append(object)\n"
            script += "    return object_list\n\n"
        script += "def exctract_all() -> dict:\n"
        script += "    \"\"\"Exctract all data in database into a dictionary\"\"\"\n"
        for table in database[db]:  
            script += "    "+table.capitalize()+" = []\n"
            script += "    for "+table+" in get_"+table+"():\n"
            script += "        "+table.capitalize()+".append("+table+".to_dict())\n"
        script += "    obj = {\n"
        for table in database[db]:  
            script += "        '"+table+"' : "+table.capitalize()+",\n"
        script += "    }\n"
        script += "    return obj\n"
        script += "def extract_to_json(name):\n"
        script += "    \"\"\"Exctract all data in database into a .json file\"\"\"\n"
        script += "    database = exctract_all()\n"
        script += "    for table in database:\n"
        script += "        i = 0\n"
        script += "        for line in database[table]:\n"
        script += "            for columns in line:\n"
        script += "                if str(type(line[columns])) == \"<class 'datetime.datetime'>\":\n"
        script += "                    database[table][i][columns] = str(database[table][i][columns])\n"
        script += "            i+=1\n"
        script += "    json_exctract = json.dumps(database)\n"
        script += "    file = open(f\"{"+"name"+"}.json\",'w')\n"
        script += "    file.write(json_exctract)\n"
        script += "    file.close()\n"
        i = input("Do you want save the script 'SQL_"+db+".py' ? y | n ")
        if i != 'n' and i != 'N':
            f = open("SQL_"+db+".py", "w")
            f.write(script)
            f.close()
