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

for base in DB:
    if (base[1] in database) == False:
        database[base[1]] = {}  
    if (base[2] in database[base[1]]) == False:
        database[base[1]][base[2]] = []
    database[base[1]][base[2]].append(base[3])  
    
for db in database:
    print(db)
    i = input("Continue? y | n \n")
    if i != 'n' and i != 'N':
        script = 'import mysql.connector as MC\n\n'
        script += 'HOST = "'+HOST+'"\n'
        script += 'USER = "'+USER+'"\n'
        script += 'PASSWORD = "'+PASSWORD+'"\n'
        script += 'PORT = "'+PORT+'"\n'
        script += 'DATABASE = "'+db+'"\n\n'
        script += "co = MC.connect(host = HOST, user = USER, password = PASSWORD, port = PORT, database = DATABASE)\n"
        script += "cursor = co.cursor()\n\n"
        
        for table in database[db]:
            script += "class "+table.capitalize()+":\n"
            script += "    def __init__(self,"
            i = 1
            for columns in database[db][table]:
                if(i != len(database[db][table])):
                    script += columns+","
                else:    
                    script += columns
                i += 1    
            script += "):\n"
            for columns in database[db][table]:
                script += "        self."+columns+" = "+columns+"\n"
            script += "\n"
            script += "    def to_dict(self):\n"
            script += "        dict = {\n"
            for columns in database[db][table]:
                script += "            '"+columns+"' : self."+columns+",\n"  
            script += "        }\n"
            script += "        return dict\n\n"
            script += "    def update(self,update,condition):\n"
            script += "        co = MC.connect(host = '"+HOST+"', user = '"+USER+"', password = '"+PASSWORD+"', port = '"+PORT+"', database = '"+db+"')\n"
            script += "        cursor = co.cursor()\n"
            script += "        req = f"+'"'+"UPDATE "+table+" SET {"+"update"+"} WHERE {"+"condition"+"}"+'"'+"\n"
            script += "        cursor.execute(req)\n"
            script += "        co.commit()\n\n"
            script += "    def delete(self,condition):\n"
            script += "        co = MC.connect(host = '"+HOST+"', user = '"+USER+"', password = '"+PASSWORD+"', port = '"+PORT+"', database = '"+db+"')\n"
            script += "        cursor = co.cursor()\n"
            script += "        req = f"+'"'+"DELETE FROM "+table+" WHERE {"+"condition"+"}"+'"'+"\n"
            script += "        cursor.execute(req)\n"
            script += "        co.commit()\n\n"
            script += "    def insert(self):\n"
            script += "        co = MC.connect(host = '"+HOST+"', user = '"+USER+"', password = '"+PASSWORD+"', port = '"+PORT+"', database = '"+db+"')\n"
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
            script += "        cursor.execute(msg,value_list)\n"
            script += "        co.commit()\n\n"
        
        script += "def get_sql(table,condition = None):\n"
        script += "    if(condition == None):\n"
        script += "        req = 'SELECT * FROM {}'.format(table)\n"
        script += "    else:\n"
        script += "        req = 'SELECT * FROM {} WHERE {}'.format(table,condition)\n"
        script += "    cursor.execute(req)\n"
        script += "    return  cursor.fetchall()\n\n"
        
        for table in database[db]:    
            script += "def get_"+table+"(condition = None):\n"
            script += "    SQL = get_sql('"+table+"',condition)\n"
            script += "    object_list = []\n"
            script += "    for p in SQL:\n"
            script += "        object = "+table.capitalize()+"("
            i = 1
            for columns in database[db][table]:
                if(i != len(database[db][table])):
                    script += "p["+str(i-1)+"],"
                else:    
                    script += "p["+str(i-1)+"]"
                i += 1  
            script += ")\n"
            script += "        object_list.append(object)\n"
            script += "    return object_list\n\n"
        i = input("Do you want save the script 'SQL_"+db+".py' ? y | n ")
        if i != 'n' and i != 'N':
            f = open("SQL_"+db+".py", "w")
            f.write(script)
            f.close()
