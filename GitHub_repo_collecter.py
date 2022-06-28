

import re
from time import sleep
import requests
import json
import os
from datetime import datetime
from dbInteraction import insert_repos,insert_Commit,insert_File_Change,get_unproccessed_Recoeds,Inser_tool_Result
import re
from util import getCode, get_Intervals,deownload_raw,Analyze_Data_from_a_string
import environ
respo={}

#from dbController import update_data


#---------------------------
f = open('data.json')
data = json.load(f)
f.close()
#print(data['first_time_use'])



#+language:{}
env = environ.Env()
environ.Env.read_env()

githubToken = env("token")
print(githubToken +"------------------------------------ githubToken ----------------------")
headers = {'Authorization': 'token ' +githubToken}
page=1
language=["Solidity","Vyper"]
url ="https://api.github.com/search/repositories?q=language:Vyper+language:{}+created:{}&page=1&per_page=10&sort=created&order=asc".format(language[0],"2016")
total_count=0
total_loops=0
prea_data=[]
commits=None



#---------------------------- Insert Repos -------------------------#
#-------------------------------------------------------------------#
def insert_data_to_database(items):
    itemIndex=0
        
    for item in items:
      itemIndex+=1
      itemdat={'repo_name':item['name'],"repo_url":item["html_url"],
                "repo_id":item['id'],"discription":item['description'],
                "date_created":item['created_at'],"date_last_push":item['pushed_at'],
                "homepage":item['homepage'],"repo_language":item['language'],
                "forks_count":item['forks_count'],"stars_count":item['stargazers_count'],
                "owner":item['owner']['login']}

      try:
      
        insert_repos(itemdat)
      except:
        print("excption in Inserting Data")
        continue
      



#------------------------------------------------------------------------------------------#
#------------------------------- Get Repos for a Certain date period ----------------------#
#------------------------------------------------------------------------------------------#

def get_repos_within_a_period(startDate=os.environ.get("last_date_for_repo_search") ,numberOfRequest=1000):
   
    # Define Our Varibles Here
    env = environ.Env()
    environ.Env.read_env()

    githubToken = env("token")
    token=env("token") #"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"
    #print(str(os.environ.get("last_date_for_repo_search"))+"================="+str(env("token")) +"00000000000000"+ githubToken)

 
    headers = {'Authorization': 'token ' + str(token)}

  

    language=["Solidity","Vyper"]
    
    res=None

    try:
    # formate the URL
        url ="https://api.github.com/search/repositories?q=language:Vyper+language:{}+created:{}&page=1&per_page=10&sort=created&order=asc".format(language[0], startDate)
       
        #send the first request to get 'next' property
        res=requests.get(url,headers=headers)
        data=res.json()
        if 'message' in data.keys():
              print( "You Need to Change your Creditantails key")
              return
        numberOfRequest-=1
        if numberOfRequest>0 :
          pass
        else :
          return
        
       
        try:
          insert_data_to_database(data['items'])
        except Exception as e:
          print(e)
        #print(data)
        numberOfRequest=get_repos_commits(data['items'])

                                      
        #loop tell the last page in the response
        while 'next' in res.links.keys():
           
            #read next page and load it in the json file
            if numberOfRequest>0 :
              numberOfRequest-=1
              res=requests.get(res.links['next']['url'],headers=headers)
            else :
              return
         
            data = res.json() #convert data to json
            
            #Insert Repos to URL
            insert_data_to_database(data['items']) #insert data to json

            #Search for a commit 
            numberOfRequest=get_repos_commits(data['items'],numberOfRequest)

            sleep(1)

    except requests.exceptions.HTTPError as errh:
      print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
      print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
      print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
      print ("OOps: Something Else",err)
    finally :
         #-------------- Update the last date ---------------#
     pass

#----------------------------------------------------------------------#
#----------------- To Loop Throw all Arrays of Repos ------------------#
#----------------------------------------------------------------------#
def get_repos_commits(arrayOfItems , numberOfRequest=1000):
      newNumberOfRequrst =numberOfRequest
      for item in arrayOfItems:
            #print(item["id"] )
            newNumberOfRequrst= search_Commits_by_repo(numberOfRequest,item["id"],item["name"],item["owner"]["login"] )
      return newNumberOfRequrst
#----------------------------------------------------------------------#
#--------------- To Loop Throw all Arrays of one Repo -----------------#
#----------------------------------------------------------------------#
def search_Commits_by_repo(numberOfRequest,repo_id,repo_name="",user="",):
      
       # Define Our Varibles Here
  keywordsArray=["buge", "bug-fix", "fix", "problem", "solved","issue"]
  token=env("token")#"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"
  headers = {'Authorization': 'token ' + str(token)}
    
  #------------------------ get all branches -----------------------------#
  try:
        branches_url = "https://api.github.com/repos/{}/{}/branches".format(user,repo_name)
        res = requests.get(branches_url, headers=headers)   
        branchs=res.json()
        
        sleep(1)
       
        #--------- loop throw the brach to get commits for each branch --------#
        #for  branch in branchs :
        url ='''https://api.github.com/repos/{}/{}/commits?sha={}'''.format(user,repo_name,'master')
        
        if numberOfRequest <=0 :
             pass
        else :
             numberOfRequest-=1
        res = requests.get(url, headers=headers)

        sleep(1)
              #---------------- check the message of each commit --------#
              # ----------if it contains one if the key words -----------#
        commits = res.json()
        #print(commits)
        
        for commit in commits :
          commitAdded =False
          for key in keywordsArray : # check keywords in thhe message
            try :
             pass
            except:
              continue
            if  key in commit['commit']["message"]:

              url =commit['url'] # if yes get the commit url details page
              sha  =commit['sha']
              
              if numberOfRequest <=0 :
                 return 0
              else :
                  numberOfRequest-=1

              res = requests.get(url, headers=headers)# request the detaols page
              final_diffs=""
              file_change = res.json()
              
              sleep(1)
              # -------------------- Loop through files to make sure of its type-------------#
              for index,file in enumerate(file_change["files"]):
                try :
                 diffs=file['patch'].split("@@")
                except:
                  continue

                regex = r"(-?[0-9]).*(,+?[0-9])"

                # find all diff for the file for each file
                final_diffs=""

                for  diff in diffs:
                      try:
                        if re.search(regex, diff, re.MULTILINE).group(0):    
                              final_diffs+=" || "+str(re.search(regex, diff, re.MULTILINE).group(0))      
                      except:
                        continue      
                
            #------------------ check if the file type is sol or vpy ---------------------#

                filepath = file['filename'].split(".")# get the type of doc

                if filepath[len(filepath)-1] == "sol":
                      
                      if filepath[len(filepath)-1] == "sol":
                            
                          language ="Solidity"
                      else:
                          language ="Vyper"
                      if numberOfRequest <=0 :
                        return 0
                      else :
                          numberOfRequest-=1
                      res = requests.get(file['contents_url'], headers=headers)

                    
                      
                      data =res.json()

                      size=data['size'] 

                      sleep(1)
                      if not commitAdded:
                          commitItem={
                                      'hash':commit['sha'],
                                      'repo_id':repo_id,
                                      'auther':file_change['commit']['author']['name'],
                                      'auther_date':file_change['commit']['author']['date'],
                                      'committer':file_change['commit']['committer']['name'],
                                      'committer_date':file_change['commit']['committer']['date'],
                                      'msg':str(file_change['commit']['message']),
                                      'merge2':1,
                                      'num_lines_add':file_change['stats']['additions']  ,
                                      'num_lines_deleted':file_change['stats']['deletions'],
                                      'dmm_unit_size':size,

                                    }
                          
                          commitAdded=True
                    # ----------------------- Insert Commit just once -------------------#
                          try:
                           
                            insert_Commit(commitItem)
                          
                          except:
                            continue
                    # ------------------ Add File change Here ---------------------------# 
                    
                    

                    #----------------------- Open datesetFile Here ----------------#

                      f = open('docker-tools/tools/Dataset-github.json',"r")
                      datajson = json.load(f)
                      f.close()

                      #get the code_befoe and after
                      codeBefor,codeAfter,datajson=getCode( file['patch'],datajson)
                      
                     
                      change_file_item={
                        "file_change_id":file['sha'],
                        "hash":commit['sha'],
                        "filename":data['name'],
                        "old_path":"",
                        "new_path":file['raw_url'],
                        "diff":final_diffs,
                        "numlines_add":file['additions'],
                        "numlines_deleted":file['deletions'],
                        "change_type":file['status'],
                        "code_after":codeAfter,
                        "code_befor":codeBefor,
                        "nloc":size,
                        "programming_language":language,

                        }
                     

                      try :
                        insert_File_Change(change_file_item)
                       
                        with open('docker-tools/tools/githubChanges.json', 'w') as fp:
                           json.dump(datajson, fp)
                        fp.close()
                          #--------------Process File -------------#
                          
                      except:
                        continue  
                    
                else :
                  final_diffs=""
                  continue
             
  #-------------here we are going ti save reconrd and get commit info --------#

  except requests.exceptions.HTTPError as errh:
           print ("Http Error:",errh)
           numberOfRequest 
  except requests.exceptions.ConnectionError as errc:
           print ("Error Connecting:",errc)
  except requests.exceptions.Timeout as errt:
           print ("Timeout Error:",errt)
  except requests.exceptions.RequestException as err:
           print ("OOps: Something Else",err) 
  finally :
    return numberOfRequest  
        
#-----------------------------------------------------------------------------------#
#------------------ a Function to analyaze the dara that we got --------------------#
#-----------------------------------------------------------------------------------#

def start_analyzing():
      
  token=env("token")
  headers = {'Authorization': 'token ' + str(token)}

  tools= [  "smartcheck","solhint","securify","slither","osiris","mythril","maian","honeybadger" ]

  try:
    #---------------- get data ----------#
    data= get_unproccessed_Recoeds()
    #------loop throught Records  ----------#
    for item in data :
    #------get the file ----------#
      
      lag=item['programming_language']
      deownload_raw(item["new_path"],token,lag)
      for  index,tool in enumerate(tools) :
        
        
        if Analyze_Data_from_a_string(tool,lag,item["hash"],item['file_change_id']):
              break
        if index == len(tools)-1  :
         
              #------------- we need to insert not found
          Inser_tool_Result(tool,["Not Found"],item["hash"],item['file_change_id'],1)
        
      
      #---------------------- tools Section --------------------#

  except Exception as excpt:
    print(excpt)

    
#get_repos_within_a_period("2022")
#start_analyzing()






