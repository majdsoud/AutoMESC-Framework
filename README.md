# About AutoVuSolidity 
- is a tool to continuously mine a comprehensive vulnerable and the corresponding patched smart contract code written in Solidity and Vyper from open source projects on GitHub and from CVE records. Next, AutoVuSolidity automatically cleans and organizes the vulnerabilities and their corresponding fixes at multiple levels of granularity. After that, it automatically scans and analyzes the collected vulnerabilities and their fixes using the available smart contracts analysis tools. In addition, it automatically notifies the tool owners if the tool fails to determine the type of vulnerability or detect it, on top of reporting the vulnerabilities to developers.
- For more information,email: majdsoud5@gmail.com 

 ## Technology used 
 - Python - tkinter
 - Docker
 - Sql server
 - solc-anlyzer

 
 ## Pre-request 
 -  [Tools for Visual Studio](https://visualstudio.microsoft.com/downloads/) at least 2015
 -  [Docker](https://www.docker.com/products/docker-desktop/) 
 -  [python 3](https://www.python.org/downloads/) and Above

 ## Tools Used 

 - [Smartcheck](https://github.com/smartdec/smartcheck)
 - [solhint](https://github.com/protofire/solhin)
 - [osiris](https://github.com/christoftorres/Osiris)
 - [securify](https://github.com/eth-sri/securify2)
 - [slither](https://github.com/crytic/slither)
 - [mythril](https://github.com/ConsenSys/mythril)
 - [maian](https://github.com/ivicanikolicsg/MAIAN)
 - [honeybadger](https://github.com/christoftorres/HoneyBadger)

 # Get started
 - create your own Github Access Token this [article will help you](https://catalyst.zoho.com/help/tutorials/githubbot/generate-access-token.html) 
 - create you Own [NVD API KEY](https://nvd.nist.gov/developers/request-an-api-key) 
 - activate python VE => & {path}/SolidityTool/myenv/Scripts/Activate.ps1
 - install packages => python -m pip install -U --force pip 
                       pip install -r /requirements.txt
 - creatr .env file with these variables 
    - token=(put you github Token here)
    - NVD_apk=(put you NVD key here)
     - emailPassword=(put [google app password](https://support.google.com/accounts/answer/185833) here)

    - your .env file will look like this

   ![](imgs/9.JPG)

    - and your data in you env file sould look like this

    ![](imgs/10.JPG)

 - run main window => python mainWindow.py

    ## Database Schema 
    - this app uses SQL Server as a Docker Image, all connections and creations of database and tables related to the following schema are maintained with the app itself.
![](imgs/3.JPG)

 # Screens 
 - ### Logs Window 
 Logs Window shows all installation logs for all docker tools, main SQL docker image, and connection to the database from where you can see if any error occurs while the configuration step 

 ![](imgs/1.JPG)


- ### Analyze Screen

  In this Screen You can Copy/Past your code and test it and get Errors in it as shown Below
  
 ![](imgs/12.jpg)

 - ### Tools 
 Small Explenation about each tool used in this App with GitGub-Repo
 
 ![](imgs/2.JPG)

 - ### Automation
  you can find it here and also export Your data as CSV format

  ![](imgs/4.jpg)    ![](imgs/7.png)  

  from here you will start your Automated Operation Of Collecting Github, CVES,and analyze them every 2 Hours, after launching the Background Process you will get a notification telling you that this is a scheduled process. 

![](imgs/4.png)

