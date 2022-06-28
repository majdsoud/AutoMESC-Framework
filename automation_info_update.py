from turtle import title
from GitHub_repo_collecter import get_repos_within_a_period,start_analyzing
from cves_collecter import Collect_Cves
import schedule
import time
import json
import logging
from plyer import notification
from util import  Send_email , get_Intervals

#----------------------------- Ctrate Our Log File --------------------------------#

logger=logging.getLogger('std.log') 

# make sure that the duration of start date and end date ia samll


def automate_repo_collecting():
    #----------------- Open data file ---------------#
    f = open('data.json')
    #------------------ load json -------------------#
    data = json.load(f)
    #---------------- get date Value ----------------#
    lastDateReacged = data["last_date_reached"]
    print(str(lastDateReacged) +" from Automation ")

    f.close()
    if __name__ =="__main__":
            notification.notify(
        title="Solidity Bug Tool BackGround Proccess ",
        message="Background Process Started to get Information, Please Wait some time to finish...",
        app_icon="imgs/bugIcon.ico",
        timeout=40,
    )
    get_repos_within_a_period(data['last_date_reached'])
   
    start_analyzing()
    Send_email()

    interval = get_Intervals()
    #-------------- Update the last date ---------------#
  
    data['last_date_reached']=int(interval)# Update Last Time
    print("From Automation : "+ str(data['last_date_reached']))
    
    #----------------------------Update Number of us -------------------------
    data['first_time_use']+=1
    
    with open("data.json", "w") as jsonFile:
        json.dump(data, jsonFile)
        jsonFile.close()


automate_repo_collecting()

#------------- Define Sechulare Time Autimation Range -----------#
schedule.every(2).hours.do(automate_repo_collecting)

#------------- Define Sechulare Time Autimation Range -----------#
schedule.every(24).hours.do(Collect_Cves)
#----------------------- Start Automation -----------------------#
while True:
    schedule.run_pending()
    time.sleep(1)