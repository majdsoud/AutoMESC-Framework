
import json
import os
import threading
import time
import util
from dbInteraction import connectSqlServer,Check_Tables
from GitHub_repo_collecter import get_repos_within_a_period
from datetime import datetime
from tkinter import * 
import logging 
import environ

#------------------------------------------------------------------#
#-------------------- a function to run docker thread -------------#
#------------------------------------------------------------------#
logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def tools_thread_pool():
    tools= [  "solhint","smartcheck","securify","slither","osiris","mythril","maian","honeybadger" ]

    for item in tools:
        thread= threading.Thread(target=util.Check_image, args=[item])
        thread.start()
        time.sleep(5)
        while  thread.is_alive():
            print("thread is still alive for image " +item )
            time.sleep(1)

#-------------------- Check database Connection and tables -----------#
#-----------------------------Scedual Connection ---------------------#

def main_func(logFile,fram=""):
    
    env = environ.Env()
    environ.Env.read_env()

    githubToken = env("token")
    print(githubToken+"888888888888")
    # ------------------- Setup Enviroment Variables ---------------------#
    os.environ['token'] = githubToken # Github Token
    os.environ['last_date_for_repo_search']="2015" #last date reached in the last loop
    os.environ['Database']="NVD" #database name
    os.environ['languages']="Solidity" #needed Languages
    
    data={}

    f = open('data.json')
    data = json.load(f)
    f.close()
    
    try:
    #----------------- Make Sure Of the Connection ----------------#
        while not connectSqlServer("NVD") :#to make sure that there is a connection before starting anything
            print("not connected")
            logFile.critical("not connected")
            time.sleep(40)
    #--------------------- Check Tables In DataBase ------------------#
        tables=["repository","commits","file_change","fixes","toolresult","CVE","nodes","userProfile","refrences"]
    #------------------------------------------------------------------#
        for table in tables :
            try:
               value= Check_Tables(table,"NVD");
            except Exception as rxc:
                logFile.critical("Somthing Happend While Checking Table :"+table +" Error:"+rxc)
    #-------------------- build Inner Images osiris ---------------------------#
        
    except:
        logFile.critical(" DataBase is not connected or Crashed")
    
    
    #---------------------------------------------------------------------------------#
    #--------------------------- Docker tools Section Check --------------------------#
    #---------------------------------------------------------------------------------#
    try:
        #------------------------ Write Error to log File -----------------------#
        tools= [  "solhint","smartcheck","securify","slither","osiris","mythril","maian","honeybadger" ]
        # check docker if exist 
        if not util.Check_Docker():
           
            #------------------------ Write Error to log File -----------------------#
            logFile.error("No Docker Found In You Machin was detected")
            return
        else:
            try:
            #--------------- start threads of Doacker Tools Image Checking ----------#
                tools_thread_pool()
            except:
                logFile.error("Some Docker Tools Are not Installed , due to some erroes")

       
 
    except:
        #----------------- Write Exceptions To LogFile -------------------------#
        logFile.error("Some Docker Tools Are not Installed , due to some erroes")
    
    #------------------------Update json file variables ---------------#
    #try:
        #-------------- Increase Time of Use By 1----------------------#
       # data['first_time_use']+=1
        #---------------- Write data in the file ----------------------#
        #with open("data.json", "w") as jsonFile:
            #json.dump(data, jsonFile)
        #---------------- close the file ----------------------#
        #jsonFile.close()
    #except Exception as e:
        #---------------- Write Error in LogFile ----------------------#
        #logFile.error("Oops!", e.__class__, "occurred.")

    



        

     


