from audioop import add
import difflib,re
import sys
from bs4 import BeautifulSoup
import json
import logging 





def craet_diff(codeBefoe, codeafter ):
  
  
  codeBeforwoeds = codeBefoe.split(" ")
  codeafterewoeds = codeafter.split(" ")

  #------------------------------------------------------------------------------#
  #---------- carete Diff Html Report from the code before and after ------------#
  #------------------------------------------------------------------------------#
  defrencess = difflib.HtmlDiff().make_file(codeBeforwoeds , codeafterewoeds)

  #------------------------------------------------------------------------------#
  #---------- get body tag that contains all diff rows and columns --------------#
  #------------------------------------------------------------------------------#
  tbody = defrencess[defrencess.find("<tbody>")+len("<tbody>"):defrencess.find("</tbody>")]
  
  #------------------------------------------------------------------------------#
  #-------------- create list of items by spliting the lines  -------------------#
  #------------------------------------------------------------------------------#
  tbody_list = tbody.split("\n")

  #-----------------------------------------------------------------------------#
  #---------------------------- Open datesetFile Here --------------------------#
  #-----------------------------------------------------------------------------#
  f = open('docker-tools/tools/githubChanges.json',"r")
  datajson = json.load(f)
  f.close()


  #-------------------------------------------------------------------------------# 
  #---------------------------Loop Throw changes Rows-----------------------------# 
  #-------------------------------------------------------------------------------#
  for line in tbody_list[1:-1]:
       

        #-------------------------------------------------------------------------#
        #------------------------ Change code Case -------------------------------#
        #-------------------------------------------------------------------------#
        if "diff_chg"  in line: 
            print("---------------------------diff_add--------------------------" )
            keyChanged,replacedDiff= get_changed_word(line)
            

            
            if  keyChanged !=None:
                
                datajson[keyChanged["key"]]["C"]+=1
            if replacedDiff!=None :
                datajson["ReplaceDiff"][replacedDiff["fromkey"]][replacedDiff["tokey"]]+=1
            continue
        #-------------------------------------------------------------------------#
        #----------------------------- Add code Case -----------------------------#
        #-------------------------------------------------------------------------#
        
        datajson= get_delete_add_word(line,datajson)
        
            
           
            
         
        
                
  #----------------- Write as an Html just to check ----------#     
  difReport= open("difReposrt.html","w")
  difReport.write(defrencess)

  return datajson


"""
 -------------------------------------------------------------------------------------------
         Find changes in words and if there is any replacment for any keyword 
--------------------------------------------------------------------------------------------
"""
def get_changed_word(line):
        logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
        logging.FileHandler("changes.log"),
        logging.StreamHandler()
        ]   
        )
        logger = logging.getLogger("changes")
       
        replacedDiff =None
        keyChanged = None

        soup = BeautifulSoup(line,"html.parser")
        chg = soup.find_all("td",{"nowrap": "nowrap"})

        wordBefor = chg[0].text
        wordAfter = chg[1].text

        logger.info("(befor):=>  "+wordBefor +" -----  (after):=>  " +wordAfter)
          #------------------ Create Oue RegExpressuin ----------------#
        
        regEx='(break|require|if|case|catch|continue|do|switch|throw|this|while|final|assert|sizeof|return|abstract|typedef|static|reference|override|immutable|copyof|type|typedef|default|define|relocatable|sealed|mutable|macro|inline|apply|auto|supports|unchecked)'
        
        #----------------------- get keywords that starts or ends the line -------------------------#
        resultbefor = re.findall(regEx, wordBefor)
        resultafter = re.findall(regEx, wordAfter)
       
     
        #------------------------------ Upate data for changing Key --------------------------------#
        if len(resultbefor)!=0:
            keyChanged ={"key":resultbefor[0]}
        
        #------------------------------ Upate data for replacing Key --------------------------------#
        if len(resultbefor)!=0 and len(resultafter)!=0 :
            replacedDiff= { "fromkey":resultbefor[0] , "tokey":resultafter[0]}

        #------------------------------ Return the value to main Finction ---------------------------#
        

        return keyChanged,replacedDiff




"""
----------------------------------------------------------------------------------------------
                               get all added Deleted Code statistics
----------------------------------------------------------------------------------------------
"""
def get_delete_add_word(line ,  datajson):
    soup = BeautifulSoup(line,"html.parser")

    allRecord = soup.find_all("td",{"nowrap":"nowrap"})

    for td in allRecord :
        deleted = td.find_all("span",{"class": "diff_sub"})
        added = td.find_all("span",{"class": "diff_add"})
       
       
        if  len(deleted)!= 0 and len(added) !=0:
            print("********************************************************************" )
            print("---------------------------From Delete add -------------------------" )
            print("********************************************************************" )
            keyChanged,replacedDiff= get_changed_word(line)
           
        
            if replacedDiff!=None :
               
                if replacedDiff["fromkey"] != replacedDiff["tokey"]:
                    datajson["ReplaceDiff"][replacedDiff["fromkey"]][replacedDiff["tokey"]]+=1
            

        if len(deleted)>0:
             for item in deleted :
                
                key= Search_if_key_delete_added(item.text)
                if key!=None:
                    
                    datajson[key]['A']+=1
                    datajson[key]['T']+=1
                   
        if len(added)>0:
            for item in added :
               
                key= Search_if_key_delete_added(item.text)
                if key!=None:
                   
                    datajson[key]['D']+=1
                    datajson[key]['T']+=1

        if len(deleted)==0 and len(added)==0:
            
               
                key= Search_if_key_delete_added(td.text)
                if key!=None:
                    
                    datajson[key]['C']+=1
                    datajson[key]['T']+=1

    return datajson
    

"""

-----------------------------------------------------------------------------------------------
                                  search for key in line
-----------------------------------------------------------------------------------------------
"""
def Search_if_key_delete_added(line):
     #------------------ Create Oue RegExpressuin ----------------#
        words= ["break", "assert","case","catch",
                "continue", "do","for",
                "if","return","switch",
                "synchronization", "throw","try","while"
                ]
        regEx='(?:[\s]|^)(break|case|catch|continue|do|switch|throw|while|try|final|if|for|assert|sizeof|return|abstract|typedef|static|reference|override|of|immutable|copyof|type|typedef|default|define|of|relocatable|sealed|mutable|macro|inline|apply|auto|supports|unchecked)(?=[\s]|$)'
        
        #----------------------- get keywords that starts or ends the line -------------------------#
        resultbefor = re.findall(regEx, line)
        
        if len(resultbefor)>0:
            return resultbefor[0]
        else:
            return None

"""
-----------------------------------------------------------------------------------------------
                                 Change JSON File Temporary 
-----------------------------------------------------------------------------------------------
"""
def Change_Diff_son(key,type,datajson):
  #-----------------------------------------------------------------------------#
  #---------------------------- Open datesetFile Here --------------------------#
  #-----------------------------------------------------------------------------#
  datajson[key][type]+=1


'''
craet_diff("""
 pragma solidity 0.4.18; import "./MultiSigWallet.sol";     contract MultiSigWalletWithDailyLimit is MultiSigWallet {        /*     event DailyLimitChange(uint dailyLimit);        /*      uint public dailyLimit;      uint public lastDay;      uint public spentToday;      function executeTransaction(uint transactionId)          public         ownerExists(msg.sender)         confirmed(transactionId, msg.sender)          notExecuted(transactionId)      {         Transaction storage txn = transactions[transactionId];         bool _confirmed = isConfirmed(transactionId);         if (_confirmed || txn.data.length == 0 && isUnderLimit(txn.value)) {              txn.executed = true;             if (!_confirmed)                  spentToday += txn.value;              if (txn.destination.call.value(txn.value)(txn.data))                  Execution(transactionId);              else {                  ExecutionFailure(transactionId);                  txn.executed = false;                 if (!_confirmed)                      spentToday -= txn.value;              }          } 
""","""

 pragma solidity 0.4.18;     contract MultiSigWallet {      uint constant public MAX_OWNER_COUNT = 50;      event Confirmation(address indexed sender, uint indexed transactionId);     event Revocation(address indexed sender, uint indexed transactionId);     event Submission(uint indexed transactionId);     event Execution(uint indexed transactionId);     event ExecutionFailure(uint indexed transactionId);     event Deposit(address indexed sender, uint value);     event OwnerAddition(address indexed owner);     event OwnerRemoval(address indexed owner);     event RequirementChange(uint required);      mapping (uint => Transaction) public transactions;     mapping (uint => mapping (address => bool)) public confirmations;     mapping (address => bool) public isOwner;     address[] public owners;     uint public required;     uint public transactionCount;      struct Transaction {         address destination;         uint value;         bytes data;         bool executed;     }      modifier onlyWallet() {         require(msg.sender != address(this));         _;     }      modifier ownerDoesNotExist(address owner) {         require(isOwner[owner]);         _;     }      modifier ownerExists(address owner) {         require(!isOwner[owner]);         _;     }      modifier transactionExists(uint transactionId) {         require(transactions[transactionId].destination == 0);         _;     }      modifier confirmed(uint transactionId, address owner) {         require(!confirmations[transactionId][owner]);         _;     }      modifier notConfirmed(uint transactionId, address owner) {         require(confirmations[transactionId][owner]);         _;     }      modifier notExecuted(uint transactionId) {         require(transactions[transactionId].executed);         _;     }      modifier notNull(address _address) {         require(_address == 0);         _;     }      modifier validRequirement(uint ownerCount, uint _required) {         require(ownerCount > MAX_OWNER_COUNT             || _required > ownerCount             || _required == 0             || ownerCount == 0);         _;     }      function()         payable     {         if (msg.value > 0)             Deposit(msg.sender, msg.value);     }      /*     function MultiSigWallet(address[] _owners, uint _required)         public         validRequirement(_owners.length, _required)     {         for (uint i=0; i<_owners.length; i++) {             require(isOwner[_owners[i]] || _owners[i] == 0);             isOwner[_owners[i]] = true;         }         owners = _owners;         required = _required;     }      function addOwner(address owner)         public         onlyWallet         ownerDoesNotExist(owner)         notNull(owner)         validRequirement(owners.length + 1, required)     {         isOwner[owner] = true;         owners.push(owner);         OwnerAddition(owner);     }      function removeOwner(address owner)         public         onlyWallet         ownerExists(owner)     {         isOwner[owner] = false;         for (uint i=0; i<owners.length - 1; i++)             if (owners[i] == owner) {                 owners[i] = owners[owners.length - 1];                 break;             }         owners.length -= 1;         if (required > owners.length)             changeRequirement(owners.length);         OwnerRemoval(owner);     }      function replaceOwner(address owner, address newOwner)         public         onlyWallet         ownerExists(owner)         ownerDoesNotExist(newOwner)     {         for (uint i=0; i<owners.length; i++)             if (owners[i] == owner) {                 owners[i] = newOwner;                 break;             }         isOwner[owner] = false;         isOwner[newOwner] = true;         OwnerRemoval(owner);         OwnerAddition(newOwner);     }      function changeRequirement(uint _required)         public         onlyWallet         validRequirement(owners.length, _required)     {         required = _required;         RequirementChange(_required);     }      function submitTransaction(address destination, uint value, bytes data)         public         returns (uint transactionId)     {         transactionId = addTransaction(destination, value, data);         confirmTransaction(transactionId);     }      function confirmTransaction(uint transactionId)         public         ownerExists(msg.sender)         transactionExists(transactionId)         notConfirmed(transactionId, msg.sender)     {         confirmations[transactionId][msg.sender] = true;         Confirmation(msg.sender, transactionId);         executeTransaction(transactionId);     }      function revokeConfirmation(uint transactionId)         public         ownerExists(msg.sender)         confirmed(transactionId, msg.sender)         notExecuted(transactionId)     {         confirmations[transactionId][msg.sender] = false;         Revocation(msg.sender, transactionId);     }      function executeTransaction(uint transactionId)         public         notExecuted(transactionId)     {         if (isConfirmed(transactionId)) {             Transaction txn = transactions[transactionId];             txn.executed = true;             if (txn.destination.call.value(txn.value)(txn.data))                 Execution(transactionId);             else {                 ExecutionFailure(transactionId);                 txn.executed = false;             }         }     }      function isConfirmed(uint transactionId)         public         constant         returns (bool)     {         uint count = 0;         for (uint i=0; i<owners.length; i++) {             if (confirmations[transactionId][owners[i]])                 count += 1;             if (count == required)                 return true;         }     }        /*     function addTransaction(address destination, uint value, bytes data)         internal         notNull(destination)         returns (uint transactionId)     {         transactionId = transactionCount;         transactions[transactionId] = Transaction({             destination: destination,             value: value,             data: data,             executed: false         });         transactionCount += 1;         Submission(transactionId);     }        /*     function getConfirmationCount(uint transactionId)         public         constant         returns (uint count)     {         for (uint i=0; i<owners.length; i++)             if (confirmations[transactionId][owners[i]])                 count += 1;     }      function getTransactionCount(bool pending, bool executed)         public         constant         returns (uint count)     {         for (uint i=0; i<transactionCount; i++)             if (   pending && !transactions[i].executed                 || executed && transactions[i].executed)                 count += 1;     }      function getOwners()         public         constant         returns (address[])     {         return owners;     }      function getConfirmations(uint transactionId)         public         constant         returns (address[] _confirmations)     {         address[] memory confirmationsTemp = new address[](owners.length);         uint count = 0;         uint i;         for (i=0; i<owners.length; i++)             if (confirmations[transactionId][owners[i]]) {                 confirmationsTemp[count] = owners[i];                 count += 1;             }         _confirmations = new address[](count);         for (i=0; i<count; i++)             _confirmations[i] = confirmationsTemp[i];     }      function getTransactionIds(uint from, uint to, bool pending, bool executed)         public         constant         returns (uint[] _transactionIds)     {         uint[] memory transactionIdsTemp = new uint[](transactionCount);         uint count = 0;         uint i;         for (i=0; i<transactionCount; i++)             if (   pending && !transactions[i].executed                 || executed && transactions[i].executed)             {                 transactionIdsTemp[count] = i;                 count += 1;             }         _transactionIds = new uint[](to - from);         for (i=from; i<to; i++)             _transactionIds[i - from] = transactionIdsTemp[i];     } }   contract MultiSigWalletWithDailyLimit is MultiSigWallet {      event DailyLimitChange(uint dailyLimit);       uint public dailyLimit;      uint public lastDay;      uint public spentToday;      function executeTransaction(uint transactionId)          public          notExecuted(transactionId)      {         Transaction txn = transactions[transactionId];         bool confirmed = isConfirmed(transactionId);         if (confirmed || txn.data.length == 0 && isUnderLimit(txn.value)) {              txn.executed = true;             if (!confirmed)                  spentToday += txn.value;              if (txn.destination.call.value(txn.value)(txn.data))                  Execution(transactionId);              else {                  ExecutionFailure(transactionId);                  txn.executed = false;                 if (!confirmed)                      spentToday -= txn.value;              }          } 
""")
'''