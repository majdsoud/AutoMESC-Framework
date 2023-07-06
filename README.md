# AutoMESC: Automatic Framework for Mining and Classifying Ethereum Smart Contract Vulnerabilities and Their Fixes
Majd Soud, Ilham Qasse, Grischa Liebel, Mohammad Hamdaqa

Due to the risks associated with vulnerabilities in smart contracts, their security has gained significant attention in recent years. We present an automated method for mining and classifying Ethereum smart contract vulnerabilities and corresponding fixes from GitHub and from Common Vulnerabilities and Exposures (CVE) records in the National Vulnerability Database that is implemented in a fully automated framework, AutoMESC, that classifies and, using seven of the most well-known smart contract security tools, labels the collected vulnerabilities based on vulnerability types. Furthermore, AutoMESC collects metadata that can be used for smart contract security research, such as vulnerability detection, classification, severity prediction, and automated repair.  
 

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
     - emailPassword=(put [google password](https://support.google.com/accounts/answer/185833) here)

    - your .env file will look like this

   ![](imgs/9.JPG)

    - and your data in you env file sould look like this

    ![](imgs/10.JPG)

 - run main window => python mainWindow.py

    ## Database Schema 
    - AutoMESC uses SQL Server as a Docker Image, all connections and creations of database and tables related to the following schema are maintained with AutoMESC itself.
![](imgs/3.JPG)

 

   

