#-------------------------------------------------------#
#--------------------- Maian Paser ---------------------#
#-------------------------------------------------------#


import logging
from operator import le    # first of all import the module
from dbInteraction import Inser_tool_Result
import re
#logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger=logging.getLogger('std.log')

class MaianPaser():
    def __init__(self,outPut):
        self.output = outPut

    def Decode(self):
        lines = self.output.splitlines()
        output=[]
        for line in lines:
             if 'Locking vulnerability found!' in line:
                  print("Locking vulnerability found!")
                  output.append('is_lock_vulnerable : '+"True")  
             if 'The contract is prodigal' in line:
                  print("The contract is prodigal")
                  output.append('is_prodigal_vulnerable :'+"True")
             if 'Confirmed ! The contract is suicidal' in line:
                 output.append('s_suicidal_vulnerable :'+"True")
                 print("Confirmed ! The contract is suicidal")
              

        return output , len(output)
             
#-------------------------------------------------------#
#-------------------- Osiris Paser ---------------------#
#-------------------------------------------------------#
class OsirisPaser():
    def __init__(self,outPut):
        self.output = outPut

    def Decode(self):
         values=[]
         lines = self.output.splitlines()
         for line in lines:
            values.append(line +" "+"  \n")
            logger.error( line +"\n")
         return values

#-------------------------------------------------------#
#-------------------- Slither Paser --------------------#
#-------------------------------------------------------#
class SlitherPaser():
    def __init__(self,outPut):
        self.output = outPut

    def Decode(self):
         values=[]
         lines = self.output.splitlines()
         for line in lines:
            values.append(line +" "+"  \n")
            logger.error( line +"\n")
         return values


#-------------------------------------------------------#
#-------------------- Slither Paser --------------------#
#-------------------------------------------------------#
class conkasPaser():
    def __init__(self,outPut):
        self.output = outPut

    def Decode(self):
         values=[]
         lines = self.output.splitlines()
         for line in lines:
            values.append(line +" "+"  \n")
            logger.error( line +"\n")
         return values
#-------------------------------------------------------#
#----------------- Smartcheck Paser --------------------#
#-------------------------------------------------------#
class SmartcheckPaser():
    def __init__(self,outPut):
        self.output = outPut

    def extract_result_line(self, line):
        index_split = line.index(":")
        key = line[:index_split]
        value = line[index_split + 1:].strip()
        if value.isdigit():
            value = int(value)
        return line

    def Decode(self):
         values=[]
         lines = self.output.splitlines()

         for line in lines:

                try:  
                    finalline=self.extract_result_line(line)   
                    values.append( finalline+"  \n")
                except Exception as e:
                    continue

         return values,len(values)

    #--------------------------------------------------#
    #------------get Proplems Count -------------------#
    #--------------------------------------------------#
   

class SolhintPaser():
     
    def __init__(self,outPut):
        self.output = outPut

    def Decode(self):
         values=[]
        
         lines = self.output.splitlines()
         for line in lines:
                if ":" in line:
                    self.output = line.split(':')
                    if len(self.output) != 4:
                        continue
                    (file, line, column, end_error) = self.output
                    if ']' not in end_error:
                        continue
                    message = end_error[1:end_error.index('[') - 1]
                    level = end_error[end_error.index('[') + 1: end_error.index('/')]
                    type = end_error[end_error.index('/') + 1: len(end_error) - 1]
                    
                    values.append(' line :'+ line+
                     ' column :'+ column+ ' message : '+
                      message+ ' level :'+ level+'\n type :'+
                       type +"\n")

         return values,len(values)
             

#-------------------------------------------------------#
#------------------- mythril Paser ---------------------#
#-------------------------------------------------------#
class mythrilPaser():
    def __init__(self,outPut):
        self.output = outPut

    def Decode(self):
         values=[]
         lines = self.output.splitlines()
         for line in lines:
            values.append(line +" "+"  \n")
            logger.error( line +"\n")
         return values

#-------------------------------------------------------#
#----------------- honeybadger Paser -------------------#
#-------------------------------------------------------#
class honeybadgerPaser():
    def __init__(self,outPut):
        self.output = outPut

    def Decode(self):
         values=[]
         lines = self.output.splitlines()
         for line in lines:
            values.append(line +" "+"  \n")
            logger.error( line +"\n")
         return values
        
