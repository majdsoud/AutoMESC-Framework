
from ast import Import
from asyncio.windows_events import NULL
import re
import math
from select import select
from time import sleep
import requests
from util import Check_repo_Lang
from dbInteraction import get_commit_for_cv, Insert_CVE,Insert_Nodes,insert_Refrences
import environ


env = environ.Env()
environ.Env.read_env()

githubToken = env("token")

apk= env("NVD_apk")
"""
a function to create a structured Object from Nodes json
"""
def nods_formater(node):
    pass
#-------------------------------------------------------------------------------------#
#---------------------- Collects all Cve's for smart contracts -----------------------#
#-------------------- compare it with our database to find commits  ------------------#
#----------------------- related to it and then save it localy -----------------------#
#-------------------------------------------------------------------------------------#

def Collect_Cves():

    res=None

    # formate the URL
    apk= env("NVD_apk")
    token=env("token") 
 
    url ="https://services.nvd.nist.gov/rest/json/cves/1.0/?resultsPerPage=100&startIndex=2&keyword=smart+contract&apiKey={}".format(apk)
  
    res = requests.get(url)
    data= res.json()

    totalResults= data["totalResults"]

    resultsPerPage=data["resultsPerPage"]

    numberOfRounds= math.ceil(totalResults/resultsPerPage) +1  
    
   
    for round in range(totalResults-1,0,-1):
     
        url ="https://services.nvd.nist.gov/rest/json/cves/1.0/?keyword=smart+contract&resultsPerPage=20&startIndex={}&apiKey={}".format(round,apk)
        sleep(1)
        res = requests.get(url)
        sleep(3)
        try:
            data= res.json()
        
        #-----------------------------------------------------------------------------------------#
        #--------for each cve item we need to get full detaols about the cve byt its id-----------#
        #-----------------------------------------------------------------------------------------#

            for item in  data["result"]["CVE_Items"]:
                
                cveurl ="https://services.nvd.nist.gov/rest/json/cve/1.0/{}".format(item["cve"]["CVE_data_meta"]["ID"])
                print(str(item["cve"]["CVE_data_meta"]["ID"])+"-------"+str(round))
                #print(cveurl)
                
                try :
                    res = requests.get(cveurl)
                    sleep(1)
                    cvedata = res.json()
                
                    githubCommit_CHEKER= "https://github\.com(?:/[^/]+)*/commit/[0-9a-f]{40}"
                    githubCommit = 'github\.com\/(.+?)\/'



                    #------------------------ we need to loop throw items ----------------------------#

                    cveIems= cvedata['result']["CVE_Items"]
                    #----------------- define values we need to save later if its a gitgub commit -----------#
                    severity=None
                    obtain_all_privilege=NULL
                    obtain_user_privilege=NULL
                    user_interacrion_required=NULL
                    vectorString=NULL
                    accessVector=NULL
                    accessComplexity=NULL
                    authentication=NULL
                    confidentialityImpact=NULL
                    baseScore:NULL
                    vectorString_cve3=NULL
                    attackVector=NULL
                    privilegesRequired=NULL
                    userInteraction=NULL
                    scope=NULL
                    baseScore=NULL
                    confidentialityImpact=NULL
                    integrityImpact=NULL
                    cvss3_base_score=NULL
                    baseSeverity=NULL
                    impactScore=NULL
                    acInsufInfo=NULL
                    references=""
                    
                    #------------------ check in case the json file dose not have it --------------#
                    if cveIems[0]["impact"] :
                        #------------------ check in case the json file dose not have it --------------#
                        if cveIems[0]["impact"]['baseMetricV2']:
                                try:
                                    #------------------ check in case the json file dose not have it --------------#
                                    if cveIems[0]["impact"]['baseMetricV2']['acInsufInfo']:
                                        acInsufInfo=cveIems[0]["impact"]['baseMetricV2']['acInsufInfo']
                                except:
                                    pass

                                severity=cveIems[0]["impact"]['baseMetricV2']['severity']
                                obtain_all_privilege=cveIems[0]["impact"]['baseMetricV2']['obtainAllPrivilege']
                                obtain_user_privilege=cveIems[0]["impact"]['baseMetricV2']['obtainUserPrivilege']
                                user_interacrion_required=cveIems[0]["impact"]['baseMetricV2']['userInteractionRequired']

                                #------------------ check in case the json file dose not have it --------------#
                                if cveIems[0]["impact"]['baseMetricV2']['cvssV2'] :
                                    vectorString=cveIems[0]["impact"]['baseMetricV2']['cvssV2']['vectorString']
                                    accessVector=cveIems[0]["impact"]['baseMetricV2']['cvssV2']['accessVector']
                                    accessComplexity=cveIems[0]["impact"]['baseMetricV2']['cvssV2']['accessComplexity']
                                    authentication=cveIems[0]["impact"]['baseMetricV2']['cvssV2']['authentication']
                                    confidentialityImpact=cveIems[0]["impact"]['baseMetricV2']['cvssV2']['confidentialityImpact']
                                    baseScore=cveIems[0]["impact"]['baseMetricV2']['cvssV2']['baseScore']

                                #------------------ check in case the json file dose not have it --------------#
                                if cveIems[0]["impact"]['baseMetricV3'] :
                                    impactScore =cveIems[0]["impact"]['baseMetricV3']['impactScore']
                                
                                    if cveIems[0]["impact"]['baseMetricV3']['cvssV3']:
                                        vectorString_cve3=cveIems[0]["impact"]['baseMetricV3']['cvssV3']['vectorString']
                                        attackVector=cveIems[0]["impact"]['baseMetricV3']['cvssV3']['attackVector']
                                        privilegesRequired=cveIems[0]["impact"]['baseMetricV3']['cvssV3']['privilegesRequired']
                                        userInteraction=cveIems[0]["impact"]['baseMetricV3']['cvssV3']['userInteraction']
                                        scope=cveIems[0]["impact"]['baseMetricV3']['cvssV3']['scope']
                                        confidentialityImpact=cveIems[0]["impact"]['baseMetricV3']['cvssV3']['confidentialityImpact']
                                        integrityImpact=cveIems[0]["impact"]['baseMetricV3']['cvssV3']['integrityImpact']
                                        cvss3_base_score=cveIems[0]["impact"]['baseMetricV3']['cvssV3']['baseScore']
                                        baseSeverity=cveIems[0]["impact"]['baseMetricV3']['cvssV3']['baseSeverity']

                    nodes=cveIems[0]["configurations"]['nodes']
                
                    #------------------ The Complete Object we are going to save --------------#
                    CVE={
                            "CVE_ID": cveIems[0]['cve']['CVE_data_meta']['ID'],
                            "published_date":cveIems[0]['publishedDate'] , 
                            "last_Modified_Date":cveIems[0]['lastModifiedDate'],
                            "discription":cveIems[0]['cve']['description']['description_data'][0]['value'],
                            "severity":severity,
                            "obtain_all_privilege":int(obtain_all_privilege),
                            "obtain_user_privilege":int(obtain_user_privilege),
                            "user_interacrion_required":int(user_interacrion_required),
                            "cvss2_vector_string":vectorString,
                            "cvss2_access_vector":accessVector,
                            "cvss2_access_complixity":accessComplexity,
                            "cvss2_authentication":authentication,
                            "cvss2_confidentiality_impact":confidentialityImpact,
                            "cvss2_base_score":baseScore,
                            "cvss3_vectore_string":vectorString_cve3,
                            "cvss3_attack_vector":attackVector,
                            "cvss3_privileges_required":privilegesRequired,
                            "cvss3_user_interaction":userInteraction,
                            "cvss3_scope":scope,
                            "cvss3_confidentiality_impact":confidentialityImpact,
                            "cvss3_integrity_impact":integrityImpact,
                            "cvss3_base_score":cvss3_base_score,
                            "cvss3_base_severity":baseSeverity,
                            "impact_score":impactScore,
                            "ac_insuf_info":acInsufInfo,
            
                            }
                   
                    
                    #------------------ rest of CVE Obect data --------------#
                    problem_type_data=None
                    problem_json=""
                    problem_type_data= cveIems[0]["cve"]["problemtype"]["problemtype_data"]

                    #------------------ formate a string from problem type data --------------#
                    try:
                        problem_type_data= cveIems[0]["cve"]["problemtype"]["problemtype_data"]
                        for pro in problem_type_data:
                            for item in pro["description"]:
                                problem_json+=item['value'] +"\n"


                    except:
                        pass

                    #------------------------- Loop through urls in the dic -------------------------------#
                    reference_data= cveIems[0]["cve"]["references"]["reference_data"]
                    reference_data_filterted=[]
                    #------------------ get the refrence url and make sure its github commit --------------#

                    #----------- a cheker to make sure that this CVE contains a gitgub refrence -----------#
                    insert = False
                    for url in reference_data:
                        
                            result= re.search(githubCommit,url["url"])

                            if result !=None :
                                insert=True
                            #print(result)
                        #------------------------------- Create Refrencrs -----------------------------#
                                references+= url["url"]+"\n"
                                #print(url["url"]+"--------------------************-------------------")
                        #------------------ split url to get commit number rebo and owner --------------#
                                urlparts=url["url"].split("/")
                                if result != None :
                                    commit_result = re.findall(githubCommit_CHEKER,url["url"])
                                    print("----------------commit_result ---------------")
                                    print(commit_result,urlparts[6],len(commit_result))
                                    print("----------------End commit_result ---------------")

                                if len(commit_result) :
                                        hash=urlparts[6]
                                else:
                                        hash=""
                                
                                owner=urlparts[3]
                                repo=urlparts[4]
                               
                                # print(startDate=os.environ.get("last_date_for_repo_search"))
                                headers = {'Authorization': 'token ' +githubToken}
                                
                                #res = requests.get(url, headers=headers)
                                res=requests.get("https://api.github.com/repos/{}/{}".format(owner,repo),headers=headers)
                                datalang={}
                                try:
                                    datalang=res.json()
                                    print(datalang)
                                    val= {
                                   
                                    "language":datalang['language']
                                    }
                                except:
                                    print("********************************************************")
                                    print("********************************************************")
                                    print("Exception")
                                    print("********************************************************")
                                    print("********************************************************")
                                hash=hash
                                val= {
                                    "owner":urlparts[3],
                                    "repo":urlparts[4],
                                    "hash":hash,
                                    "url": url["url"],
                                    "language":datalang['language']
                                   
                                }
                                reference_data_filterted.append(val)
                                print("********************************************************")
                                print("********************************************************")
                                print(reference_data_filterted)
                                print("********************************************************")
                                print("********************************************************")
                               #print(CVE['owner'],CVE['repo'],hash)

                    #------------- we need a select statment to get any commit with these thress values -----#
                               #print (url["url"])
                               #insert=Check_repo_Lang(owner,repo)
                               #insert=get_commit_for_cv(hash, repo, owner)
                                
                    #--------------------- after making sure that this is the record we need -----------------#
                    #------------------ we change the value of the cheker to true for insertion --------------#
                                    #insert=True
            
                    #------------  -------------#
                    #CVE["refrence_json"]=references
                    CVE['problemtype_json']=problem_json
                    
                
                    
                    if insert:
                        try:
                            Insert_CVE(CVE)

                            try:
                                 Insert_Nodes(nodes,CVE['CVE_ID'])
                            except:
                                print("exprion")

                            try:
                                print(reference_data_filterted)
                               
                        #---------------------------- Inser Refrences here -------------------#
                                if len(reference_data_filterted) :
                                     insert_Refrences(reference_data_filterted,CVE['CVE_ID'] )
                            #print(reference_data_filterted)
                            except:
                                print("Error in inserting Refrence ....")
                        except:
                            pass
 
                except :
                    pass       
        except:
            continue

#Collect_Cves()