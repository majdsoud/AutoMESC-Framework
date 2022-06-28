# util.py
from asyncio.windows_events import NULL
from datetime import datetime
from pickle import NONE
from re import I
import sys
from tkinter import N
import pyodbc
import pandas as pd
import itertools
import logging 
import pandas as pd
import pyodbc
import operator
import json
import pandas as pd
import os
database_name= "NVD"


# A function to Create NVD to check if the database exist 
# if Exsit the use the database 
# if not create database and schema the use it 

#-------------------------------------- a function to check Connection ---------------------#
def connectSqlServer(database_name):
    drivers = pyodbc.drivers()
    #print(drivers)
    DR=drivers[-1]
    logger=logging.getLogger("std.log")
    logger.setLevel(logging.DEBUG)
    #Main Parameters to connect to our database ;
    
    cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
            user="sa", password="nvddatabase!2022",autocommit=True)
    crsr = cnxn.cursor() 
    try:
            logger.info("try to connect with connection Configuration on local host")
        #connection Configuration 
            cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
            user="sa", password="nvddatabase!2022",autocommit=True)
        # try to connect with connection Configuration   
            crsr = cnxn.cursor()
            crsr.execute("SELECT name FROM master.dbo.sysdatabases where name=?;"
            ,(database_name,))
            data=crsr.fetchall()
            logger.info("Connection Exist")
        # if its Connected to Server and there is no Database with name NVD
            if not data:
                logger.info("database do not exist")
        # create the Database
                try :
                    logger.info("if there is a connection try to create NVD Database")
                    crsr.execute("CREATE DATABASE {}".format(database_name))
                    crsr.execute("USE {}".format(database_name))
                    crsr.execute("CREATE SCHEMA {}".format(database_name+"schema"))
                    crsr.close()
                    cnxn.close()
                    logger.info(" create NVD Database")
                except :
                    logger.warning("Not Connected to NVD")
                    return False
            else:
        # If NVD EXIST use it 
                try:
                    logger.info("If NVD EXIST use it ")
                    crsr.execute("USE {}".format(database_name))
                    crsr.close()
                    cnxn.close()
                    logger.info("NVD Dose Exist, and ready to be used ")
                except :
                    logger.warning(" NVD Dose not Exist")
                    return False

    except:
        return False
        
    return True
        

# -------------------------A function to Check List Of Tables if its exsir or not ---------------------------#            
def Check_Tables(Table_name, databaename):
    logger=logging.getLogger("std.log")
    logger.setLevel(logging.DEBUG)

    #connection Configuration 
    cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost", user="sa", password="nvddatabase!2022",autocommit=True)
    crsr = cnxn.cursor()

    #check if the Table Exist 
    try :
        logger.info("Check Table "+ Table_name +" if Exist")
        query = ''' SELECT 1 FROM INFORMATION_SCHEMA.TABLES
         WHERE TABLE_NAME={} ''' .format("'"+Table_name+"'")
        data=crsr.execute("USE {}".format(databaename))
     
       
        try:

            crsr.execute(query)
            data=crsr.fetchall()
            
    #if its Not Exist Create One 
            if   not data :
                logger.info("table "+ Table_name +" do not Exist, try to ctrate it ")
                query=Tables(Table_name).choose_table_query()
                cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost", database=databaename ,user="sa", password="nvddatabase!2022",autocommit=True)
                #print("connected to databse")
                crsr = cnxn.cursor()
                crsr.execute(query)
                
                cnxn.commit()
                print("Done")
                logger.info("table "+ Table_name +" was created Sucssfully ")
            else:
               logger.info("table "+ Table_name +"Already In the database ")  
            
        except pyodbc.Error as ex:
            print(  ex.args[1])
            print("Exeption In Cheking Data")
            logger.warning("Exeption In Cheking Data")

    except:
        logger.warning("No Database Founded with the Name {} ".format(databaename))
        print("No Database Founded with the Name {} ".format(databaename))
    finally:
        crsr.close()
        cnxn.close()
        print("Done")






#---------------------------------------------------------------------------------------------#
#------------------------------------ Create Tables Class-------------------------------------#
#---------------------------------------------------------------------------------------------#


class Table:
    #-------------------- Class Variables -------------------#
    table_name=""
    columns_array={}
    primary_key=[]
    Forign_Kry =""
    refrece_tables=[]

    #------------ Instantiate class for table ---------------#
    def __init__(self ,table_name , columns, primarkey,forighkey=""):
        self.table_name=table_name
        self.columns_array=columns
        self.primary_key=primarkey
        self.forighkey=forighkey

    #---------------- Create Table Class --------------------#
    def create_Table_query(self):

        # generate the colums 
        columns_gnenerated =""
        for key , value in self.columns_array.items():
           # check if this column is a primary key
            if key in self.primary_key:
                columns_gnenerated+= " {}  {} primary key,".format(key, value) 

            else:
                 columns_gnenerated+= " {}  {},".format(key, value) 
        
        columns_gnenerated+= self.forighkey
        # create a full query string to create a table
        quer=  '''
		        CREATE TABLE {} ({} )
               '''.format(self.table_name, columns_gnenerated)
        print(quer)
        #returning the result query
        #print(quer)
        return quer

#---------------------------------------------------------------------------------------------#
# -----------------------------------Table Defenition ----------------------------------------#
#---------------------------------------------------------------------------------------------#


class Tables:
    #------------------------------ Class Variables -------------------------------#
    table_name=""
    tables_colums= {
         #--------------------------------- CVE Table -----------------------------#
        "CVE":Table("CVE",
    {
        "CVE_ID":"VARCHAR(15)",
        "published_date":"VARCHAR(30)",
        "last_Modified_Date":"VARCHAR(30)",
        "discription":"VARCHAR(max)",
        "severity":"VARCHAR(50)",
        "obtain_all_privilege":"INT",
        "obtain_user_privilege":"INT",
        "user_interacrion_required":"INT",
        "cvss2_vector_string":"VARCHAR(100)",
        "cvss2_access_vector":"VARCHAR(50)",
        "cvss2_access_complixity":"VARCHAR(50)",
        "cvss2_authentication":"VARCHAR(50)",
        "cvss2_confidentiality_impact":"VARCHAR(50)",
        "cvss2_base_score":"float",
        "cvss3_vectore_string":"VARCHAR(100)",
        "cvss3_attack_vector":"VARCHAR(50)",
        "cvss3_attack_complixity":"VARCHAR(50)",
        "cvss3_privileges_required":"VARCHAR(50)",
        "cvss3_user_interaction":"VARCHAR(50)",
        "cvss3_scope":"VARCHAR(50)",
        "cvss3_confidentiality_impact":"VARCHAR(50)",
        "cvss3_integrity_impact":"VARCHAR(50)",
        "cvss3_base_score":"INT",
        "cvss3_base_severity":"VARCHAR(20)",
        "impact_score":"float",
        "ac_insuf_info":"INT",
        "problemtype_json":"VARCHAR(20)",
    },["CVE_ID"]) ,
     #----------------------------- cwe_claaification Table -----------------------#
      "nodes":Table("nodes",
        {
        "cpe23Uri":"VARCHAR(100)",
        "ID":" INT IDENTITY (1, 1) NOT NULL",
        "CVE_ID":"VARCHAR(15) FOREIGN KEY REFERENCES CVE(CVE_ID) ON DELETE CASCADE ON UPDATE CASCADE",
        "vulnerable":"VARCHAR(15)"
        
        }
        ,["ID"],
      ),
      #----------------------------- cwe_claaification Table -----------------------#
      "refrences":Table("refrences",
        {
        "refrenc":"VARCHAR(200)",
        "ID":" INT IDENTITY (1, 1) NOT NULL",
        "CVE_ID":"VARCHAR(15) FOREIGN KEY REFERENCES CVE(CVE_ID) ON DELETE CASCADE ON UPDATE CASCADE",
        "repo":"VARCHAR(50)",
        "owner":"VARCHAR(50)",
        "hash":"VARCHAR(100)",
        "language":"VARCHAR(20)"
 
        }
        ,["ID"],''' 
         CONSTRAINT AK_ref_cve UNIQUE (refrenc, CVE_ID) '''
         ),
    #--------------------------------- Fixes Table -----------------------------#
    "fixes":Table("fixes",
    {
    "hash":"VARCHAR(100) FOREIGN KEY REFERENCES commits(hash) ON DELETE CASCADE ON UPDATE CASCADE",
    "checked":"BIT ",
    

    } 
    ,["hash"] 
    ),
    #--------------------------------- Fixes Table -----------------------------#
    "userProfile":Table("userProfile",
    {
    "userEmail":"VARCHAR(150) ",
    "userName":"VARCHAR(150) ",
    "notifyme":"bit",
    "id":"int IDENTITY (1, 1) NOT NULL"

    } 
    ,["id"] 
    ),

    #------------------------------ Tools Results ------------------------------#
    "toolresult":Table("toolresult",
    {
    "tool_name":"VARCHAR(40)",
    "value":"VARCHAR(max)",
    "hash":"VARCHAR(100) not NULL FOREIGN KEY REFERENCES fixes(hash) ON DELETE CASCADE ON UPDATE CASCADE" ,
    "file_id":"VARCHAR(100) not NULL  ",
    "NumberOfErrors":"int"
    } 
    ,["result_id"] ,''' 
    CONSTRAINT AK_Password UNIQUE (file_id, hash) '''
    ),
    #----------------------------- cwe_claaification Table -----------------------#
      "cwe_claaification":Table("cwe_claaification",
        {
        "cve_id":"VARCHAR(100)",
        "cwe_id":"VARCHAR(100)",
        }
        ,["cve_id","cwe_id"]
      ),
    #--------------------------------- cwe Table --------------------------------#
       "cwe_claaification":Table("cwe",
          {
          "cwe_id":"INT",
          "cwe_name":"VARCHAR(100)",
          "discription":"VARCHAR(100)",
          "extented_discription":"VARCHAR(100)",
          "url":"VARCHAR(100)",
          "is_category":"VARCHAR(100)",
          },["cwe_id"]
      ),
      #-------------------------------- repository ---------------------------------#
     "repository":Table("repository",
          {
          "repo_name":"varchar(50)",
          "repo_url":"VARCHAR(200)",
          "repo_id":"varchar(20)",
          "discription":"VARCHAR(500)",
          "date_created":"datetime",
          "date_last_push":"datetime",
          "homepage":"VARCHAR(200)",
          "repo_language":"VARCHAR(20)",
          "forks_count":"INT",
          "stars_count":"FLOAT",
          "owner":"VARCHAR(100)",
          "n_branches":" INT  NULL"
          },["repo_id"]
      ), 

     #-------------------------------- commits ---------------------------------#
     "commits":Table("commits",
          {
          "hash":"VARCHAR(100) NOT NULL",
          "repo_id":"varchar(20) NOT NULL  FOREIGN KEY REFERENCES repository(repo_id) ON DELETE CASCADE ON UPDATE CASCADE",
          "auther":"VARCHAR(100) NOT NULL",
          "auther_date":"datetime NOT NULL",
          "committer":"VARCHAR(100) NOT NULL",
          "committer_date":"datetime NOT NULL",
          "msg":"VARCHAR(2000)",
          "merge2":"VARCHAR(100)",
          "num_lines_add":"int NOT NULL",
          "num_lines_deleted":"int NOT NULL",
          "dmm_unit_size":"int NOT NULL",
          },["hash","repo_url"],
      ), 

          #-------------------------------- method_change ---------------------------------#
     "method_change":Table("method_change",
          {
          "method_change_id":"INT",
          "file_change_id":"VARCHAR(100) FOREIGN KEY REFERENCES file_change(file_change_id) ",
          "name":"VARCHAR(100)",
          "signature":"VARCHAR(100)",
          "start_line":"VARCHAR(100)",
          "end_line":"VARCHAR(100)",
          "code":"VARCHAR(100)",
          "cloc":"VARCHAR(100)",
          "complixity":"VARCHAR(100)",
          "token_count":"VARCHAR(100)",
          "top_nesting_level":"VARCHAR(100)",
          "befor_change":"VARCHAR(100)",
          },["method_change_id"]
      ),
    #-------------------------------- file_change ---------------------------------#
         "file_change":Table("file_change",
          {
          "file_change_id":"VARCHAR(100) NOT NULL",
          "hash":"VARCHAR(100) NOT NULL FOREIGN KEY REFERENCES commits(hash) ON DELETE CASCADE ON UPDATE CASCADE",
          "filename":"VARCHAR(100) NOT NULL",
          "old_path":"VARCHAR(400)",
          "new_path":"VARCHAR(400)",
          "change_type":"VARCHAR(20) NOT NULL",
          "diff":"VARCHAR(500) NOT NULL",
          "num_lines_added":"INT NOT NULL",
          "num_lines_delete":"INT NOT NULL",
          "code_after":"varchar(max) ",
          "cod_befor":"varchar(max) ",
          "nolc":"int",
          "programming_language":"VARCHAR(20)",
          },["file_change_id"],
      ),
    }

    #---------------------- Instantiate and Evaluate Varibles --------------------#
    def __init__(self,table_name):
        #print(table_name)
        self.table_name=table_name

    # --------A function ro select query Creator Depending on Table Name ---------#
    def choose_table_query( self):
       return self.tables_colums[self.table_name].create_Table_query()
        

#----------------------------------------------------------------------------------#
#--------------------------------- DATABASE QUERYES -------------------------------#
#----------------------------------------------------------------------------------#
def Update_Repos_Data(json):
       
    
        # ------------------ Connect To Database ------------------------#
        cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                user="sa", password="nvddatabase!2022",autocommit=True)
        crsr = cnxn.cursor()
        data=crsr.execute("USE {}".format(database_name))
        #print(json[0])
        
        #----------------------- Loop Throw json -----------------------#
        for item in json:
            #print( item["created_at"])
            Insertquery="INSERT INTO "
            try :
                data=crsr.execute(Insertquery)
            except:
                pass

#-----------------------------------------------------------------------------------------#
#----------------------------------------Insert Repos ------------------------------------#
#-----------------------------------------------------------------------------------------#
def insert_repos(item):
    
     # ------------------make sure Connect To Database ------------------------#
    cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                user="sa", password="nvddatabase!2022",autocommit=True)
    
    crsr = cnxn.cursor()
    data=crsr.execute("USE {}".format(database_name))
    
    #--------------------------------- Insert statment gos here --------------#
    try:
    
        crsr.execute(''' INSERT INTO repository 
            (repo_name,
            repo_url,
            repo_id,
            discription,
            date_created,
            date_last_push,
            homepage,
            repo_language,
            forks_count,
            stars_count, owner)
                VALUES 
            (?,?,?,?,?,?,?,?,?,?,?)''',
            [
            item['repo_name'],
            item['repo_url'],
            item['repo_id'],
            item['discription'],
            item['date_created'],
            item['date_last_push'],
            item['homepage'],
            item['repo_language'],
            item['forks_count'],
            item['stars_count'],
            item['owner']
            ])
        #print( "insert_repos")
        cnxn.commit()
        
        
    #------------------------------- Handiling Error ------------------------#
    except pyodbc.Error as error:
         print("Failed to insert record into MySQL table {}".format(error.args[1]))

    #------------------------------- after Done Every thing Close------------#
    finally:
        
            crsr.close()
            cnxn.close()
            #print("MySQL connection is closed")

#-----------------------------------------------------------------------------------------#
#----------------------------------------Insert Commit ------------------------------------#
#-----------------------------------------------------------------------------------------#
def insert_Commit(item):
    #print(item)
     # ------------------make sure Connect To Database ------------------------#
    cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                user="sa", password="nvddatabase!2022",autocommit=True)
    cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='latin1')
    cnxn.setencoding('latin1')
    
    crsr = cnxn.cursor()
    data=crsr.execute("USE {}".format(database_name))
    
    #--------------------------------- Insert statment gos here --------------#
    #try:
   
    crsr.execute(''' INSERT INTO commits 
            (hash,
            repo_id,
            auther,
            auther_date,
            committer,
            committer_date,
            msg,
            merge2,
            num_lines_add,
            num_lines_deleted,
            dmm_unit_size
             )
                VALUES 
            (?,?,?,?,?,?,?,?,?,?,?)''',
            [
            item['hash'],
            item['repo_id'],
            item['auther'],
            item['auther_date'],
            item['committer'],
            item['committer_date'],
            item['msg'],
            item['merge2'],
            item['num_lines_add'],
            item['num_lines_deleted'],
            item['dmm_unit_size']
            ])
    cnxn.commit()
    try:
        
        crsr.execute(''' INSERT INTO fixes 
                (hash,
                checked
                )
                VALUES 
                (?,?)''',
                [
                item['hash'],0
                ])
    except pyodbc.Error as error:
       
        print(error)
    #print( "insert_Commit")
    #print( "insert_Commit")
    cnxn.commit()
   
#----------------------------------------------------------------------------------#
#---------------------------------- File Change Insert ----------------------------#
#----------------------------------------------------------------------------------#

def insert_File_Change(item):
    #print(item)
     # ------------------make sure Connect To Database ------------------------#
    cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                user="sa", password="nvddatabase!2022",autocommit=True)
    
    
    crsr = cnxn.cursor()
    data=crsr.execute("USE {}".format(database_name))
    
    #--------------------------------- Insert statment gos here --------------#
    #try:
   
    crsr.execute(''' INSERT INTO file_change 
            (file_change_id,
            hash,
            filename,
            old_path,
            new_path,
            diff,
            num_lines_added,
            num_lines_delete,
            change_type,
            code_after,
            cod_befor,
            nolc,
            programming_language
             )
                VALUES 
            (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            [
            item['file_change_id'],
            item['hash'],
            item['filename'],
            item['old_path'],
            item['new_path'],
            item['diff'],
            item['numlines_add'],
            item['numlines_deleted'],
            item['change_type'],
            item['code_after'],
            item['code_befor'],
            item['nloc'],
            item['programming_language']
            ])
    
    cnxn.commit()


#--------------------------------------------------------------------------------#
#-------------------------Upadet Fix Table query --------------------------------#
#--------------------------------------------------------------------------------#
def update_fix_table(fix_id):
       # ------------------make sure Connect To Database ------------------------#
    cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                user="sa", password="nvddatabase!2022",autocommit=True)
    
    
    crsr = cnxn.cursor()
    data=crsr.execute("USE {}".format(database_name))
    #--------------------------------- Upadet statment gos here --------------#

    crsr.execute(''' UPDATE fixes 
                     SET checked = 1
                     WHERE hash = ?''',
                     [fix_id])
    cnxn.commit()
    crsr.close()
    cnxn.close()

#--------------------------------------------------------------------------------#
#--------------------- get all recorde without processing  ----------------------#
#--------------------------------------------------------------------------------#
def get_unproccessed_Recoeds():

    data=[]
    # ------------------make sure Connect To Database ------------------------#
    cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                user="sa", password="nvddatabase!2022",autocommit=True)
    crsr = cnxn.cursor()
    datause=crsr.execute("USE {}".format(database_name))
    try:
        #--------------------------------- Upadet statment gos here --------------#
        crsr.execute(''' SELECT  fixes.hash,programming_language, file_change.new_path
                        ,checked,file_change.file_change_id
                        FROM fixes  INNER JOIN commits ON fixes.[hash] =commits.[hash] 
                        JOIN file_change on commits.[hash] =file_change.[hash]
                        WHERE checked=0''',
                        )
        #-------------------------- Convert data to dic --------------------------#
        desc = crsr.description
        column_names = [col[0] for col in desc]
        data = [dict(itertools.zip_longest(column_names, row))  
               for row in crsr.fetchall()]
        print(len(data))
        crsr.close()
        cnxn.close()
        return data
       
    #--------------- Catch Exception in select -------------#
    except pyodbc.Error as error:
        print(error)
        crsr.close()
        cnxn.close()


#-------------------------------------------------------------------------------#
#-------------------------------- Insert Into Tool Result ----------------------#
#-------------------------------------------------------------------------------#

def Inser_tool_Result(tool,value,commit_id,file_change_id,errorscount):

    # ------------------make sure Connect To Database ------------------------#
    cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                    user="sa", password="nvddatabase!2022",autocommit=True)
    crsr = cnxn.cursor()
    datause=crsr.execute("USE {}".format(database_name))

    if value[0]=="Not Found":
        print("Trying to insert Not Found Error")
        #try:
            #-------------------- Upadet statment gos here -----------------------#
        crsr.execute('''  INSERT INTO toolresult 
                (  tool_name,value,hash,file_id,NumberOfErrors) values (?,?,?,?,?)''' ,
                ["Checked By All tools","Not Found",commit_id,file_change_id,0]
                            )
        cnxn.commit()

        update_fix_table(commit_id,)
        #except pyodbc.Error as ex:
            #print(ex)
    else:

    # print(tool, commit_id,"----",file_change_id)
        text= " ".join(value)
    
        try:
            #-------------------- Upadet statment gos here -----------------------#
            crsr.execute('''  INSERT INTO toolresult 
                (  tool_name,value,hash,file_id,NumberOfErrors) values (?,?,?,?,?)''' ,
                [tool,text,commit_id,file_change_id,errorscount]
                            )
            cnxn.commit()

            update_fix_table(commit_id,)
        except pyodbc.Error as ex:
            print(ex)

#--------------------------------------------------------------------------------#
#--------------------- get commit related to a CVE  -----------------------------#
#--------------------------------------------------------------------------------#
def get_commit_for_cv(hash, repo, owner):
    exist=False
    data=[]
    # ------------------make sure Connect To Database ------------------------#
    cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                user="sa", password="nvddatabase!2022",autocommit=True)
    crsr = cnxn.cursor()
    datause=crsr.execute("USE {}".format(database_name))
    try:
        #--------------------------------- Upadet statment gos here --------------#
        crsr.execute(''' SELECT  [hash], commits.repo_id
            FROM [NVD].[dbo].[commits]
            INNER join repository ON repository.repo_id = commits.repo_id
            WHERE repository.repo_name=? AND repository.owner=?  ''' ,
            [repo,owner]
                        )
        #-------------------------- Convert data to dic --------------------------#
        
        data =crsr.fetchall()
        if len(data) >=1:
            #print(str(len(data)) +"exisit -----------------------------")
            exist=True
        else:
           #print(str(len(data)) +" do not exisit") 
           exist=False
        crsr.close()
        cnxn.close()
        return exist
       
    #--------------- Catch Exception in select -------------#
    except pyodbc.Error as error:
        print(error)
        crsr.close()
        cnxn.close()
        return exist

#--------------------------------------------------------------------------------#
#------------------------- Insert CVE Record ------------------------------------#
#--------------------------------------------------------------------------------#
def insert_Refrences(refrences,CVE_ID):
   
    #print(refrences)


    for ref in refrences:
        #print(ref, CVE_ID.strip())
        #query="INSERT INTO refrences (refrenc,CVE_ID) values ({},{}) ".format(ref,CVE_ID)

    
        # ------------------make sure Connect To Database ------------------------#
        cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                    user="sa", password="nvddatabase!2022",autocommit=True)
        
        try:
               crsr = cnxn.cursor()
               crsr.execute("USE {}".format(database_name))
               crsr.execute("""INSERT INTO 
               [NVD].[dbo].[refrences] 
                (
                refrenc,
                repo,
                owner,
                hash,
                CVE_ID,
                language
                ) 
                VALUES (?,?,?,?,?,?)""",
               [
               ref['url'],
               ref['repo'],
               ref['owner'],
               ref['hash'],
               CVE_ID,
               ref['language']]
               )
            
        except pyodbc.Error as ex:
                print(ex)
        finally:
                cnxn.commit()
                crsr.close()
                cnxn.close()
        
#--------------------------------------------------------------------------------#
#------------------------- Insert CVE Record ------------------------------------#
#--------------------------------------------------------------------------------#
def Insert_CVE(CVE):
    #--------------- Formate Insert Columns and values part of the query String ---------#
    columns= " ( " 
    values= "("
    for key, value in CVE.items()  :
        if value!= NONE or value != NULL:
            columns += key + " ,"  
            if type(value) == type(1) or type(value) ==type(1.0):
                values+=str(value) +","
            else:
                values+="'"+ str(value) + "' ,"
    #--------------- Fix the end of the line  ---------#
    columns=columns[:-1]
    columns+=")"
    values=values[:-1]
    values+=")"
    #--------------- Full Query String -----------------#
    query ="INSERT INTO CVE  " +columns +" VALUES "+values

    #--------------- Insert Command ---------------------#
    # ------------------make sure Connect To Database ------------------------#
    cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                user="sa", password="nvddatabase!2022",autocommit=True)
    
    crsr = cnxn.cursor()
    crsr.execute("USE {}".format(database_name))
    crsr.execute(query)

    cnxn.commit()
    crsr.close()
    cnxn.close()
#------------------------------------------------------------------------------#
#-----------------------------Insert CVE Node ---------------------------------#
#------------------------------------------------------------------------------#

def Insert_Nodes(nodesjsdon, Cve_id):
    
    #--------------- Insert Command ---------------------#

    cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                user="sa", password="nvddatabase!2022",autocommit=True)
    try:
        for node in nodesjsdon[0]['cpe_match'] :
            
            
            try:
               crsr = cnxn.cursor()
               crsr.execute("USE {}".format(database_name))
               crsr.execute("""INSERT INTO nodes 
            (cpe23Uri,vulnerable,cve_id) VALUES (?,?,?)""",[node['cpe23Uri'],node['vulnerable'],Cve_id])
            except pyodbc.Error as ex:
                print(ex)
            finally:
                cnxn.commit()
                crsr.close()
                cnxn.close()

    except:
        print("except")
#------------------------------------------------------------------------------#
#--------------------------- Create CSV from Tables----------------------------#
#------------------------------------------------------------------------------#
def CSV_Query(table):
    quey = ' select * from NVD.dbo.{}'.format(table)
    return quey

#--------------------------------------------------------------------------------#
#------------------------- Create csv from tables -------------------------------#
#--------------------------------------------------------------------------------#   

def Create_csv():
    
    tablesArra=['repository','file_change','commits','CVE','toolresult','fixes','nodes',"userProfile","refrences"]
    
   
    for table in tablesArra :  
        print('{}\\{}_exported_data_.csv'.format(os.path.expanduser('~'),table)+"===============================") 
        f = open('{}\\{}_exported_data_.csv'.format(os.path.expanduser('~'),table), 'w')
        #connection Configuration 
        cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                user="sa", password="nvddatabase!2022",autocommit=True)

        cursor = cnxn.cursor()
        # Execute the query
        cursor.execute(CSV_Query(table))
        while True:
        # Read the data
            df = pd.DataFrame(cursor.fetchmany(1000))
            # We are done if there are no data
            if len(df) == 0:
                break
            # Let's write to the file
            else:
                df.to_csv(f, header=False)
        

        #sql_query = pd.read_sql_query(CSV_Query(table)
                           #   ,cnxn)
       # df = pd.DataFrame(sql_query)
        #print(sql_query)
        #df.to_csv (r'C:\\Users\\nane\\Desktop\\{}_exported_data_.csv'.format(table), index = False) # place 'r' before the path name                    
        f.close()
        cursor.close()
        cnxn.close()
#------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------- Staticsts ---------------------------------------------#
#------------------------------------------------------------------------------------------------------------------#

""" 
---------------------------------------------------------------------------------------------------
                            Total Number Of files , commits for eacg repo
--------------------------------------------------------------------------------------------------- 
"""
def get_totals():
    data=[]
    finalTotals=[]
    try :
            # ------------------make sure Connect To Database ------------------------#
            cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                        user="sa", password="nvddatabase!2022",autocommit=True)
            crsr = cnxn.cursor()
            datause=crsr.execute("USE {}".format(database_name))
            try:
                #--------------------------------- Upadet statment gos here --------------#
                crsr.execute(''' SELECT repository.repo_id as id,[NVD].[dbo].[commits].[repo_id] , repository.repo_name as name,
                COUNT([NVD].[dbo].[commits].[hash]) as commitcounts FROM [NVD].[dbo].[commits], repository
                GROUP BY repository.repo_id ,[NVD].[dbo].[commits].[repo_id],repository.repo_name
                HAVING repository.repo_id = [NVD].[dbo].[commits].[repo_id]
                ORDER BY name ''',
                                )
                #-------------------------- Convert data to dic --------------------------#
                desc = crsr.description
                column_names = [col[0] for col in desc]
                data = [dict(itertools.zip_longest(column_names, row))  
                    for row in crsr.fetchall()]
                
                
                for  repo in data :
                   
                    #--------------------------------- Upadet statment gos here --------------#
                    crsr.execute(''' SELECT  
                    count([NVD].[dbo].[file_change].[file_change_id]) as filecount,
                    SUM([NVD].[dbo].[file_change].num_lines_added) as totalAdded,
                    SUM([NVD].[dbo].[file_change].num_lines_delete) as totaldeleted,
                    SUM([NVD].[dbo].[file_change].nolc)as totalnumberoflines
                    FROM [NVD].[dbo].[file_change] 
                    WHERE [NVD].[dbo].[file_change].[hash] in
                    ( 
                        (SELECT  [NVD].[dbo].[commits].[hash] FROM [NVD].[dbo].[commits]
                        WHERE [NVD].[dbo].[commits].[repo_id] in
                        ( 
                        select [NVD].[dbo].[repository].[repo_id] 
                    FROM [NVD].[dbo].[repository] WHERE repo_id =?
                    )        
                    )
                    )''',[repo['id']]
                    )
                    #-------------------------- Convert data to dic --------------------------#
                    desc = crsr.description
                    column_names = [col[0] for col in desc]
                    data2 = [dict(itertools.zip_longest(column_names, row))  
                        for row in crsr.fetchall()]

                    
                    
                    #------------------------- put all togather -----------------------------#
                    finalTotals.append(  { "repo_name":repo['name'],
                    "total_Commits":repo['commitcounts'],
                    "total_file_changes":data2[0]['filecount'],
                    "total_lines_added":data2[0]['totalAdded'],
                    "total_lines_Deleted":data2[0]['totaldeleted'],
                    "total_numberof_lines":data2[0]['totalnumberoflines'],

                       })
                
                finalTotals.sort(key=operator.itemgetter('total_file_changes'), reverse=True)
                Headings = [
                " Repo Name",
                "Total # Commits",
                "Total # Files changes",
                "Total lines added",
                "Total lines Deleted",
                "Total # of lines",
                 ]
                column_names=[
                "repo_name",
                "total_Commits",
                "total_file_changes",
                "total_lines_added",
                "total_lines_Deleted",
                "total_numberof_lines",
                ]
                
                return finalTotals[0:10],column_names,Headings
            except :
                print("error")
                return []
    except:
        return []



"""
--------------------------------------------------------
get percentage of unchange - delete - add for key words
--------------------------------------------------------
"""
def get_KeyWords_statistics():

    data =[]
    column_names=[]
    Headings=[]

    #-----------------------------------------------------------------------------#
    #---------------------------- Open datesetFile Here --------------------------#
    #-----------------------------------------------------------------------------#
    f = open('docker-tools/tools/githubChanges.json',"r")
    datajson = json.load(f)
    f.close()
    for key, value in datajson.items():
        column_names.append(key)
        data.append()
        print(key)
        print(value)
    #githubChanges
    #return data,column_names ,Headings


#get_KeyWords_statistics()
""" 
--------------------------------------------------------
get total commits for each repo and total error by tools
--------------------------------------------------------
"""

def get_commits_errors_totals():

    # Our Main Select Statment to get total errors for each commit 
    query="""  
    SELECT top 10   que.repo_name,count(que.[hash]) as numberofCommits, sum(que.commintsum)  as numberOfErrors
     from ( 
         select repository.repo_name,
          commits.[hash],
          commits.repo_id ,
           d.commintsum from commits inner join
            (SELECT 
            [hash], 
            sum([NumberOfErrors]) as commintsum
            FROM [NVD].[dbo].[toolresult]
            GROUP by [hash]) as d 
            ON commits.[hash] = d.[hash] 
            JOIN repository on commits.repo_id =repository.repo_id) as que
            GROUP BY que.repo_name
            ORDER BY numberOfErrors DESC 
      """

    data=[]
    Headings = [" Repo Name", "# Of Commits","# of bugs Tools Detected"]
    finalTotals=[]
    try :
        # ------------------make sure Connect To Database ------------------------#
        cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                        user="sa", password="nvddatabase!2022",autocommit=True)
        crsr = cnxn.cursor()
        datause=crsr.execute("USE {}".format(database_name))
        crsr.execute(query)

        #-------------------------- Convert data to dic --------------------------#
        desc = crsr.description
        column_names = [col[0] for col in desc]
        data = [dict(itertools.zip_longest(column_names, row))  
            for row in crsr.fetchall()]
        Headings = [" Repo Name", "# Of Commits","# of bugs Tools Detected"]
       # print(data)
    except :
       print("Exception get commits errors totals")
       return [],[] ,Headings 
    finally:
        return data,column_names ,Headings


""" 
--------------------------------------------------------
get total commits for each repo and total error by tools
--------------------------------------------------------
"""

def get_number_of_buges_and_fixes():

    # Our Main Select Statment to get total errors for each commit 
    query="""  
    select nofixes.TotalCountWithNoFixes, fixes.TotalCountWithFixes 
    from (
    SELECT count([tool_name]) as TotalCountWithNoFixes
    FROM [NVD].[dbo].[toolresult]
    where [value] ='Not Found'
    ) as nofixes ,
    (  
    SELECT count([tool_name]) as TotalCountWithFixes
    FROM [NVD].[dbo].[toolresult]
    where [value] != 'Not Found' ) as fixes
    """
    #---------------------------------------------------------------------------------#
    #------------------------------- Gathering Avarage -------------------------------#
    #---------------------------------------------------------------------------------#
    queryAvarage="""
    select CAST(nofixes.TotalCountWithNoFixes AS DECIMAL(7,2) )/CAST(Totalcount.Total AS DECIMAL(7,2) ) *100 as AvarageNoFixe ,
    CAST(fixes.TotalCountWithFixes AS DECIMAL(7,2) ) /CAST(Totalcount.Total AS DECIMAL(7,2) ) *100 as AvarageFixe
    from (
    SELECT count([tool_name]) as TotalCountWithNoFixes
    
    FROM [NVD].[dbo].[toolresult]
    where [value] ='Not Found'
    ) as nofixes ,
     ( 
        
    SELECT count([tool_name]) as TotalCountWithFixes  
    FROM [NVD].[dbo].[toolresult]
    where [value] != 'Not Found' ) as fixes ,
    (
    SELECT count([tool_name]) as Total    
    FROM [NVD].[dbo].[toolresult]
    ) as Totalcount
        """

    data=[]
    finalTotals=[]
    Headings = ["#- AVG Buges Without Fixes", "#-AVG Buges With Fixes","Disc"]
    try :
        # ------------------make sure Connect To Database ------------------------#
        cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                        user="sa", password="nvddatabase!2022",autocommit=True)
        crsr = cnxn.cursor()
        datause=crsr.execute("USE {}".format(database_name))
        crsr.execute(query)

        #--------------------------Totals Convert data to dic --------------------------#
        desc = crsr.description
        column_names1 = [col[0] for col in desc]
       
        data = [dict(itertools.zip_longest(column_names1, row))  
            for row in crsr.fetchall()]
        data[0]["dis"]="Totals"
        
        column_names1.append("dis")
        #--------------------------AVG Convert data to dic --------------------------#
        crsr.execute(queryAvarage)
        desc = crsr.description
        column_names = [col[0] for col in desc]
        dataavg = [dict(itertools.zip_longest(column_names, row))  
            for row in crsr.fetchall()]
        dataavg[0]["dis"]="AVG"

       
        newval={}
        for key,item in dataavg[0].items():
            if key== "AvarageNoFixe" :
                newval["TotalCountWithNoFixes"]=item

            if key=="AvarageFixe" :
                newval["TotalCountWithFixes"]=item

            if key=="dis" :
                newval["dis"]=item
        data.append(newval)
        
        Headings = ["#- AVG Buges Without Fixes", "#-AVG Buges With Fixes","Disc"]
        crsr.close()
        cnxn.close()
        return data,column_names1 ,Headings

    except :
       crsr.close()
       cnxn.close()
       print("Exception get commits errors totals")
       return [],[] ,Headings
   

#--------------------------------------------------------------------------------#
#-------------------- Update Save User Information ------------------------------#
#--------------------------------------------------------------------------------#
def update_user_profile(name="", email="" ,notifyme="" ):
     # ------------------make sure Connect To Database ------------------------#
    try:
        query = "select count(*) from userProfile"
        cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                            user="sa", password="nvddatabase!2022",autocommit=True)
        crsr = cnxn.cursor()
        crsr.execute("USE {}".format(database_name))
        crsr.execute(query)
       
        data=  crsr.fetchall()
        keysdat = data[0][0]
        

        # In case we hace a row in the data we will update it if not we will insert one
        if  int(keysdat)==0:
            query = """INSERT INTO userProfile (userEmail, userName, notifyme)
                            VALUES ({},{},{})""".format("'"+email.strip()+"'","'"+name.strip()+"'",notifyme)
        else:
            query = """UPDATE userProfile 
                        SET userEmail = {} ,userName={},notifyme={}
                        WHERE id = 2""".format("'"+email.strip()+"'","'"+name.strip()+"'",notifyme)
        print(query)
        crsr.execute(query)
        cnxn.commit()
        retuendat= "Done"

    except pyodbc.Error as ex:
            print(  ex.args[1])
            print("Exeption In Cheking Data"+ex.args[1])
            retuendat= ex.args[1]
    finally :
        crsr.close()
        cnxn.close()
        return retuendat
    
#--------------------------------------------------------------------------------#
#-------------------- Get User Unformation from database  -----------------------#
#--------------------------------------------------------------------------------#
def get_Profile():

     # ------------------make sure Connect To Database ------------------------#
    try:
        query = "select * from userProfile"
        cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                            user="sa", password="nvddatabase!2022",autocommit=True)
        crsr = cnxn.cursor()
        crsr.execute("USE {}".format(database_name))
        crsr.execute(query)
        data = crsr.fetchall()
        print(data[0])
        if len(data[0]) >0:
            return data[0]
        else :
            return -1

    except :
        return -1

#update_user_profile()
#--------------------------------------------------------------------------------#
#-------------------- Import csv into database ----------------------------------#
#--------------------------------------------------------------------------------#


def import_from_CSV():
# Import CSV
        data = pd.read_csv (r'C:\Users\Ron\Desktop\Test\products.csv')   
        df = pd.DataFrame(data)

        # Connect to SQL Server

        cnxn = pyodbc.connect(driver='{SQL Server}', host="localhost",
                                            user="sa", password="nvddatabase!2022",autocommit=True)
        cursor = cnxn.cursor()

       

        # Create Table
        cursor.execute('''
                CREATE TABLE products (
                    product_id int primary key,
                    product_name nvarchar(50),
                    price int
                    )
                    ''')

        # Insert DataFrame to Table
        for row in df.itertuples():
            cursor.execute('''
                        INSERT INTO products (product_id, product_name, price)
                        VALUES (?,?,?)
                        ''',
                        row.product_id, 
                        row.product_name,
                        row.price
                        )
        cnxn.commit()
