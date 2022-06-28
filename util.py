
from datetime import datetime
from email.policy import default
from time import sleep
from turtle import done
from unittest import result
import docker
import os
from tkinter import *
from numpy import place
import yaml
from yaml.loader import SafeLoader
from pathlib import Path
from datetime import date
import json
from time import gmtime, strftime, time
import requests
from os import getcwd
import re
from dbInteraction import Inser_tool_Result
import subprocess
from Parser import MaianPaser , conkasPaser,honeybadgerPaser,OsirisPaser,SlitherPaser,SmartcheckPaser,SolhintPaser,mythrilPaser
import logging 
import environ
import smtplib
from Difftool import craet_diff


env = environ.Env()
environ.Env.read_env()



#--------------------------------------------------------------------------------------#
#--------------------------------- Sending Emails -------------------------------------#
#--------------------------------------------------------------------------------------#

def Send_email():
    sender = 'nuhlamasri@gmail.com' 
    receivers = ['nane_kmj@hotmail.com']
    password=env.get_value('emailPassword')#"stbssevdzkyqyccr"

    message = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test

    This is a test e-mail message.
    """

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com',587)
        smtpObj.starttls()
        try:
            smtpObj.login(sender, password)
        except  smtplib.SMTPAuthenticationError as autErroe:
            print(autErroe, "SMTPAuthenticationError")
        except  smtplib.SMTPConnectError as autErroe:
            print(autErroe,"SMTPConnectError")
        except  smtplib.SMTPResponseException as autErroe:
            print(autErroe,"SMTPResponseException")
        smtpObj.sendmail(sender, receivers, message)         
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")


#--------------------------------------------------------------------------------------#
#-------------------- A function to get the raw file to process------------------------#
#--------------------------------------------------------------------------------------#
def deownload_raw(url , token ,lan="" ):
    # Define Our Varibles Here
    token=token

    #--------------------- Headers of the requrst ---------------#
    headers = {'Authorization': 'token ' + str(token)}
    url = url 
    pathurl=url.split(".")
    filetype=pathurl[len(pathurl)-1]
  
    #------------------- get the directory where we are going to save it -------------#
    directory = getcwd()
    filename=""
    if lan =="Solidity":
        filename = directory + '/docker-tools/contracts/anlyizing.sol'   
    else:
     filename = directory + '/docker-tools/contracts/anlyizing.vyp'
     
    #------------request the file to write --------------#
    res = requests.get(url, headers=headers)
    
   #------------------------- Open the File and Wite it -----------------#
    with open(filename, "w", encoding="utf-8") as f:
        f.write(res.content.decode("utf-8"))
    
    f.close()
    #------------------------- Clean Code -------------------------------#
    Clean_Code(filename)


#-----------------------------------------------------------------------------------#
#-------------------- a function to create intervals for github repo ---------------#
#-----------------------------------------------------------------------------------#
def get_Intervals():
    print("In Finction")
      #------- copy past Fram Configurations
    f = open('data.json')
    data = json.load(f)
    f.close()
    interval=""
    if data['first_time_use']==1 :
        interval = "2016"
        print("First Time Used")
        
    elif int(data["last_date_reached"])>=int(date.today().year):
        print("Current Year")
        print("in >=int(date.today().year ")
        print(data["last_date_reached"])
        interval ="2016"
        
    else :
        interval= int(data["last_date_reached"])+1
        print(interval)
        print("Next Year")
   
   

    return interval

#--------------------------------------------------------------------------#
#------------------------- Remove Commits Ftom File -----------------------#
#--------------------------------------------------------------------------#

def Clean_Code(path=""):
    
    
    if path==""   :
        path=os.path.dirname( 'docker-tools/') + '/'+"contracts/anlyizing.sol"

   
    #Open the File 
    stringData=""
    with open(path) as f:
        stringData = f.readlines()
    
    data=stringData[0]  #// SPDX-License-line
    
    for line in stringData:
        string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,line)
        string = re.sub(re.compile("//.*?\n" ) ,"" ,string)
        if string=="":
            continue
        else :
            data+=string 
   
     #------------------------- Open the File and Wite it -----------------#
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    
    f.close()



#------------------------------- List Of Images -----------------------------#
imeges = ["christoftorres/honeybadger",
    "smartbugs/maian:solc5.10",
    "smartbugs/solhint",
    "trailofbits/slither",
    "christoftorres/osiris",
    "qspprotocol/mythril-usolc"]
#--------------------------- Remove comments   
#------------------------------------------------------------------------------#
#----------------------------------- getCode ----------------------------------#
#------------------------------------------------------------------------------#
def clean(line):

    cleanCod=""
   
    string = re.sub(re.compile("\/*.*\ ? \\*.*",re.DOTALL ) ,"b" ,line)
    string = re.sub(re.compile("\/\*\*",re.DOTALL ) ,"b" ,string)
    string = re.sub(re.compile("//.*" ) ,"b" ,string)
    #print(string)
    #print("--------------------------------------------")
    if string.strip()=="b" :
        return None
    else :
        cleanCod=string 
     
    return cleanCod


def Search_for_KeyWords(line):
     #------------------ Create Oue RegExpressuin ----------------#
    words= ["break", "assert","case","catch",
            "continue", "do","for",
            "if","return","switch",
            "synchronization", "throw","try","while"
            ]
    regEx='(?:[\s]|^)(break|case|catch|continue|do|switch|throw|while|try|final|if|for|assert|return|abstract)(?=[\s]|$)'
    
    #----------------------- get keywords that starts or ends the line -------------------------#
    result = re.findall(regEx, line)

    substring = "assert"
    val=-1

    #------------ assert Section since asset could be assertTrue or assert False ----------------#
    try:
        val =line.index(substring)
    except ValueError:
       pass
    
    if val>-1:
        result.append("assert")
    
    #------------ sync Section since asset could be async or sync False ----------------#
    substring = "sync"
    try:
        val =line.index(substring)
    except ValueError:
        pass
    
    if val>-1:
        result.append("sync")

    
    
    #print(len(result))
    if len(result)>0:
        if val>-1:
            return result
        return result
    else:
        return None
  
#------------------------ CLEAN Code Befoe and after in the Same Time --------------------#
def getCode(code,data):

    parsedCode = code.split("\n")
    codeBefor = ""
    codeAfter =""
    #-------------------------- Clean Code ----------------------#
    cleanCod=""
    str=""
 
    for line in parsedCode:
        ArrayBefor = []
        ArrayAfter = []
        try:
            #---------------- get all the code Befoe ------------#
            if line[0]=="-" :
                str= line.replace("-", "", 1)
                cleanCode = clean(str)
                codeBefor+= cleanCode +"\n"
                ArrayBefor.append(cleanCode)
               
                
            #---------------- get all the code after ------------#
            elif line[0]=="+" :
                
                str= line.replace("+", "", 1)
                cleanCode = clean(str)
                ArrayAfter.append(cleanCode)
                codeAfter+= cleanCode +"\n"
                
            #-------------------- no Change Cod ------------------#
            elif line[0]==" " :
                cleanCod = clean(line)
                codeAfter+= cleanCod +"\n"
                codeBefor+= cleanCod +"\n"
            
            else :
                continue
        except:
            pass

    #-------------------- Check Diff by Diff Tool  --------------------------#

    #------------------- Get Statistices  on this file Change here ----------#
    data= craet_diff(codeBefor,codeAfter)
     
            
    return codeBefor,codeAfter,data



#------------------------------------------------------------------------------#
#------------------------------Check image if Exist ---------------------------#
#------------------------------------------------------------------------------#
def Check_Docker():
    logger=logging.getLogger("std.log")
     
    client = docker.from_env()
    if client :
         logger.info("Docker was found ")
         return client

    else:
        logger.info("Docker was not found ")
        return None



def chech_main_Image( ):
   
    client=Check_Docker() # get a connection to loal Docker 
    #-------------Open Yamel File --------------#
    data=None
    logger=logging.getLogger("std.log")
    
    print("------------- docker-compose ps --services -------------")
    try:
        #------------------------- Chech The Image in the docker Compose ---------------------------#
        p = subprocess.run("docker-compose ps --services" ,stdout=subprocess.PIPE, shell=True)
        if "sql-server-db" in p.stdout.decode("utf-8") :
            logger.info("mcr.microsoft.com/mssql and "+p.stdout.decode("utf-8")+" was found and ready to use: ")
       
        #----------------------------- Start the sql serves Again ---------------------------------#
        p = subprocess.run("docker-compose start  sql-server-db" ,stdout=subprocess.PIPE, shell=True)
        if "sql-server-db" in p.stdout.decode("utf-8") :
            logger.info("mcr.microsoft.com/mssql and "+p.stdout.decode("utf-8")+" was found and ready to use: ")
            return p
       

        #data= client.containers.get("mcr.microsoft.com/mssql/server:2019-latest")
        #logger.info("mcr.microsoft.com/mssql was found and ready to use: ")
        #try:
            
           # container = client.containers.run("mcr.microsoft.com/mssql/server:2019-latest",detach=True)
        #except :
         #   logger.error("unable to run mcr.microsoft.com/mssql")

        #logger.info("mcr.microsoft.com/mssql is Running ...")
        #return
        
    except:
        try :
          
            logger.info("mcr.microsoft.com/mssql was found and trying to pul it ")
            p = subprocess.run("docker-compose up -d" ,stdout=subprocess.PIPE, shell=True)
            return p
            
        except docker.errors.ImageNotFound as err:
           
            
            logger.critical("mcr.microsoft.com/mssql Image Error : "+err)
            return err
         
        


#------------------------------------------------------------------------------#
#------------------------------Check image if Exist ---------------------------#
#------------------------------------------------------------------------------#
def Check_image(imageString,TextLabel="",CodeString=""):
    client=None
    logger=logging.getLogger("std.log")
    
    try:
 
        client=Check_Docker() # get a connection to loal Docker 
        #-------------Open Yamel File --------------#
        data=None
        #--------- get the exact Directory  of the file ------------#
        script_location = Path(__file__).absolute().parent
        file_location=str(script_location)+'/docker-tools/'+imageString+'.yaml'
        
        with open(file_location) as f:
            data = yaml.load(f, Loader=SafeLoader)
           

        #-------get the image Name Correctly --------#
        defaultImage=data["docker_image"]["default"]

        #--------- get image Command line ------------#
        cmd= data["cmd"] 

        if client: 
            #--------- Print Line To The Window ------------#
            
            try :
                
                logger.info("Opening Image Descroprion file for Image: "+imageString)
                #--------- get the exact Directory  of the file ------------#
                script_location = Path(__file__).absolute().parent
                file_location=str(script_location)+'/docker-tools/'+imageString+'.yaml'
                

                #--------- check if the Image exist ------------#
                logger.info("Check If Image: "+imageString +"Exist")
                client.images.get(data["docker_image"]["default"]) 
                logger.info("Image: "+imageString +"Already Exist")
                
                
                return "Already Has An Image of "+imageString+" In Docker"

                #--------------------- Run The Image -----------------------#
                #----------------- Create The Real Container ---------------#
               
            
            except docker.errors.ImageNotFound as err:

                
                sleep(1)
               
                logger.info("Image: "+imageString +" dose not Exist and Trying tp pull it")
                client.images.pull(imageString)
                logger.info(imageString+' Is Pulled Successfully')
                return " Is Pulled Successfully"

                 #--------------------- Run The Image -----------------------#
                #----------------- Create The Real Container ---------------#
                

            except Exception as err:
                
                logger.info(imageString+' did not Pulled Successfully due to this error: ')
                logger.info(err)
                return err

    except docker.errors.APIError as err:
        logger.error(imageString+' did not Pulled Successfully due to this error: ')
        logger.error(err)
        
        
        

#------------------------------------------------------------------------------#
#--------------------------------- Pull Image ---------------------------------#
#------------------------------------------------------------------------------#

def pull_image(image, TextLabel=None):
    logger=logging.getLogger("std.log")
    
    try:
        client= docker.from_env() # get a connection to loal Docker 
        if client: 
            
            try :
                logger.info("trying to pull " +image)
                cmd= 'docker  pull '+image
                p1 = subprocess.run(cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
                output = p1.stdout
                logger.info("done to pull Image :" +image +"- "+output.decode('utf-8') )
                return "done to pull "
            except docker.errors.APIError as err:
                
              
                logger.info("An Error Accured While Truing ti pull  Image  :" +image +"\n "+err)
                
                return err
    except docker.errors.APIError as err:
        logger.info("An Error Accured While Truing ti pull  Image  :" +image +"\n "+err)

        return err
      

#------------------------------------------------------------------------------#
#------------------------------ Run Container ---------------------------------#
#------------------------------------------------------------------------------#

def Run_Image(image, cmd,Imagename,TextLabel):
    client=None
    volume_bindings =None
   
    try:
        client=Check_Docker() 
        
        
        volume_bindings= mount_volumes(os.path.dirname('docker-tools/'+image+'.yaml'))
        container = client.containers.run(Imagename,
                                              cmd,
                                              detach=True,
                                              # cpu_quota=150000,
                                              volumes=volume_bindings)
        try:
                container.wait(timeout=(30 * 60))
        except Exception as e:
                pass
    except:
        print("Somthing Went Wrong During Running Image: "+Imagename)
        #TextLabel.configure("Somthing Went Wrong During Running Image: "+Imagename)
#------------------------------------------------------------------------------#
#----------------------------- Create Image Volum------------------------------#
#------------------------------------------------------------------------------#
def mount_volumes(dir_path, logs=""):
    client=None
    try:
        client=Check_Docker() # get a connection to loal Docker 
        if client:
            volume_bindings = {os.path.abspath(
                dir_path): {'bind': '/' + dir_path, 'mode': 'rw'}}
           
            return volume_bindings
    except os.error as err:
        print(err)

#------------------------------------------------------------------------------#
#--------------------- Switch To get Parser Class -----------------------------#
#------------------------------------------------------------------------------#

def Create_Instance_From_Paeser(tool_name, output): 
    if tool_name =="conkas":
        return conkasPaser(output)
    if tool_name =="honeybadger":
        return honeybadgerPaser(output)
    if tool_name =="maian":
        return MaianPaser(output)
    if tool_name =="osiris":
        return OsirisPaser(output)
    if tool_name =="slither":
        return SlitherPaser(output)
    if tool_name =="smartcheck":
        return SmartcheckPaser(output)
    if tool_name =="solhint":
        return SolhintPaser(output)
    if tool_name =="mythril":
        return mythrilPaser(output)
    else:
        return None

#------------------------------------------------------------------------------#
#-------------------------------- Stop Container ------------------------------#
#------------------------------------------------------------------------------#
def stop_container(container):
    try:
        if container is not None:
            container.stop(timeout=0)
    except (docker.errors.APIError) as err:
        print(err)
        #logs.write(str(err) + '\n')
#------------------------------------------------------------------------------#
#------------------------------ Remove Container ------------------------------#
#------------------------------------------------------------------------------#
def remove_container(container):
    try:
        if container is not None:
            container.remove()
    except (docker.errors.APIError) as err:
        print(err)
     
#------------------------------------------------------------------------------#
#----------------------- a function to check the repo language ----------------#
#------------------------------------------------------------------------------#
def Check_repo_Lang(owner,reponame):
    try:
        url ="https://api.github.com/repos/{}/{}".format(owner, reponame)
      
        token=token = env("token")

        headers = {'Authorization': 'token ' + str(token)}
        res = requests.get(url, headers=headers)
        data=res.json()
        print(" Language is :"+data["language"])
        if data["language"] =="Solidity" or data["language"] =="Vyper":
            return True
        else :
            return False
    except:
        print("Error in Finding Languag")
        return False
#------------------------------------------------------------------------------#
#-------------------------------- Analyze Data --------------------------------#
#------------------------------------------------------------------------------#
def Analyze_Data_from_a_string(tool,lang="",commit_id=None, file_change_id=None):
    #-------------------- Initial Values --------------------------------------#
    inserted = False
    value,errorscount =[],0

    logger=logging.getLogger("std.log")
    

    cfg_path = os.path.abspath('docker-tools/'+tool+'.yaml')  
    with open(cfg_path, 'r', encoding='utf-8') as ymlfile:
            try:
                cfg = yaml.safe_load(ymlfile)
            except yaml.YAMLError as exc:
                print("yaml.YAMLError as exc")
  
    # check if we have imge and cmd line in the yml file 
    if 'default' not in cfg['docker_image'] or cfg['docker_image'] == None:
        print("default docker image not provided. please check you config file")
        if commit_id==None and file_change_id==None:
            return [],0
        return False
    elif  'cmd' not in cfg or cfg['cmd'] == None:
        print("commands not provided. please check you config file")
        if commit_id==None and file_change_id==None:
            return [],0
        return False

    volume_bindings = mount_volumes(os.path.dirname('docker-tools/'+tool+'.yaml'))
 
    client=None
    try:
        client=Check_Docker()
    except:
     print("Doker is not Running of is not installed")
     if commit_id==None and file_change_id==None:
            return [],0
     return False

    #-------------------- we need to clean code befor compiling -------------------#
    
    cmd = cfg['cmd']
    imag=cfg['docker_image']['default']
    
    if lang == "Solidity":

        if '{contract}' in cmd:
            cmd = cmd.replace('{contract}', '/' +  os.path.dirname('docker-tools/') + '/'+"contracts/anlyizing.sol")
        else:
            cmd += ' /' + os.path.dirname('docker-tools/') + '/'+"contracts/anlyizing.sol"
    else :
        if '{contract}' in cmd:
                cmd = cmd.replace('{contract}', '/' +  os.path.dirname('docker-tools/') + '/'+"contracts/anlyizing.vy")
        else:
            cmd += ' /' + os.path.dirname('docker-tools/') + '/'+"contracts/anlyizing.vy"
   

    container = None
    try :
        client.images.get(imag)
    except:
        if commit_id==None and file_change_id==None:
            return [],0
        return False

    try:
        container = client.containers.run(imag,
                                              cmd,
                                              detach=True,
                                              # cpu_quota=150000,
                                              volumes=volume_bindings)
        try:
            container.wait(timeout=(30 * 60))
        except : 
            if commit_id==None and file_change_id==None:
                return [],0 
            return False
        output = container.logs().decode('utf8').strip()
        if not output:
            if commit_id==None and file_change_id==None:
                return [],0
            return False

        if (output.count('Solc experienced a fatal error') >= 1 or output.count('compilation failed') >= 1 or output.count('No contract was analyzed')>=1):
               # print(
                #    '\x1b[1;31m' + 'ERROR: Solc experienced a fatal error. Check the results file for more info' + '\x1b[0m')
                logger.error('ERROR: Solc experienced a fatal error.')
                inserted= False
                if commit_id==None and file_change_id==None:
                    return [],0
                return False
                
        
        
        parser=Create_Instance_From_Paeser(tool,output)
       
        value,errorscount =parser.Decode()
        #if nothing Returend from the Parser retuen false to go to the nest one
        if errorscount ==0 or value ==[]:
            if commit_id==None and file_change_id==None:
                return [],0
            return False  
        try:
            if commit_id==None and file_change_id==None:
                return value,errorscount
            else:
                Inser_tool_Result(tool,value,commit_id,file_change_id,errorscount)
                inserted= True
        except:
            inserted= False
           

    except docker.errors.ContainerError as err:
        print("ContainerError: ")
        print(err)
        inserted= False
    except docker.errors.ImageNotFound as err:
        print("ImageNotFound: ")
        print(err)
        inserted= False
    except docker.errors.APIError as err:
        print("APIError: ")
        print(err)
        inserted= False

    finally:
        stop_container(container)
        remove_container(container)
        if commit_id==None and file_change_id==None:
                return value,errorscount
        return inserted
 
#Analyze_Data_from_a_string("slither","")

#deownload_raw()