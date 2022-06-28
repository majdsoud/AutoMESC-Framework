from cProfile import label
from pydoc import text
from time import sleep
from tkinter import *
from tkinter import ttk
import customtkinter
from numpy import pad
import util
from tkinter.scrolledtext import ScrolledText
import json
import webbrowser
import threading 
import dbInteraction
from PIL import Image, ImageTk
import re
from dbInteraction import update_user_profile,get_Profile
import matplotlib
import json
from os import getcwd

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)


def OpenUrl(aurl):
    print("somthing")
    webbrowser.open_new(aurl)

#----------------------Create Inner Frame for Tools ---------------#
def Create_Tool_Fram(fram, data,row,odd):

   


     url=data['githubLink']
     
     labelfram=Frame(fram,bg="#43423F",padx = 30,pady=10,width=300,height=400 )
     labelfram.rowconfigure(0,weight=1)
     labelfram.rowconfigure(1,weight=1)
     labelfram.rowconfigure(1,weight=1)
     labelfram.columnconfigure(0,weight=1)
    
     labelfram.grid_propagate(0)

     #button = customtkinter.CTkButton(labelfram, text="GitHub", command=lambda aurl=url:OpenUrl(aurl),width=120,height=50)
     #button.grid(row=2, column=0)
     HyperlinkLabel =Label(labelfram, text="GitHub",width=300 ,height=1,fg="#ffffff",bg="#303134",font=("Arial Bold", 9),cursor="hand2")
     HyperlinkLabel.bind("<Button-1>", lambda e: OpenUrl(url))
     HyperlinkLabel.grid(row=2, column=0)
     windowInfo =Label(labelfram, text=data['name'],width=300 ,height=1,fg="#ffffff",bg="#1C94D0",font=("Arial Bold", 10))
     infoLabel= Label(labelfram,text=data['info'],wraplength=500, justify=LEFT,padx = 30,pady=10,anchor="w",fg="white",bg="#303134",font=("Helvetica",11))
     windowInfo.grid(row=0, column=0,sticky="ew")
     infoLabel.grid(row=1, column=0,sticky="nsew")

    
     if odd :
        labelfram.grid(row=row, column=0,sticky="nsew")
     else:
         labelfram.grid(row=row, column=1,sticky="nsew")

    

#-------------------------------------------------------------------#
#--- Gloable Method for Removing any fram Item and its children ----#
#-------------------------------------------------------------------#
def remove_fram_Contents(frame):
         #removing all childrens the fram Contains
        for widget in frame.winfo_children():
            widget.destroy()
        frame.grid_forget()


#------------------------------------------------------------------------------#
#--------------------- User Profile TopLevel Window -- ------------------------#
#------------------------------------------------------------------------------#
class UserProfile:
    """ 
    --------------------------------------------------------------------------------
                                 variables Section
    --------------------------------------------------------------------------------
    """
    root=None #master tkinter container
    usernameText= None #text to enter the user name
    EmailText= None #text to enter the user email
    SubmitButton=None #save info button
    SendNotification =None #send email to user or not
   
    ErroeLabel =None

    """ 
    --------------------------------------------------------------------------------
                                 Constructore 
    --------------------------------------------------------------------------------
    """
    def __init__(self,root ):
        self.root =root

         # Variable to change the value of notification
          #--------------get User Info Here --------------#
        
         
    """ 
    --------------------------------------------------------------------------------
                                 Save Data to Database 
    --------------------------------------------------------------------------------
    """
    def saveUserProfile(self):
    
       #----------------------get Text from Entries -------------------------#
       email =self.EmailText.get()
       name =self.usernameText.get()
       sendNotification=self.var.get()
       

       #------------------ Check  if Fields are not Empty ---------------------#
       if email =="" or name == "":
            self.ErroeLabel["text"] ="Cannot save Empty Values"

       #--------------------------- validate Email -----------------------------#
       elif re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            self.ErroeLabel["text"] =""
            update_user_profile(email,name,sendNotification)
            #------save data to database ----------#
            
       else:
           #------------ Upadte the Error label with the validation -------------#   
            self.ErroeLabel["text"] ="The Email you Entred is not a valid email "

    """ 
    --------------------------------------------------------------------------------
                                 Close the window
    --------------------------------------------------------------------------------
    """
     
    def CancelUserProfile(self):
       
        self.top_level_window.destroy()


    """ 
    --------------------------------------------------------------------------------
                                 Open Window 
    --------------------------------------------------------------------------------
    """

    def Open_User_Profile_Window(self ):

        #---------------- get user info here --------------------#
        profile = get_Profile()

        if profile!=-1 :
            username , email, notify,id= profile
        else :
            username =""
            email=""
            notify=False
            id=0

        #---------------------- Our Window ------------------------#
        self.top_level_window = Toplevel(self.root, background="#43423F")

        #--------------- Row/Column Configuration -----------------#
        self.top_level_window.rowconfigure(0,weight=1 )
        self.top_level_window.rowconfigure(1,weight=1)
        self.top_level_window.rowconfigure(2,weight=1)
        self.top_level_window.rowconfigure(3,weight=1)
        self.top_level_window.rowconfigure(4,weight=1)
        self.top_level_window.rowconfigure(5,weight=1)
        self.top_level_window.rowconfigure(6,weight=1)
        self.top_level_window.columnconfigure(0,weight=1)
        self.top_level_window.columnconfigure(1,weight=3)

        #------------------ Set Hight and Width---------------------#
        window_width= 400
        window_height =350
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.top_level_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.top_level_window.overrideredirect(True)
        self.top_level_window.grab_set()

        #-------------------------- Buttons -------------------------#
        self.SubmitButton = customtkinter.CTkButton(master=self.top_level_window,  width=130,  height=36,text="Save",command=self.saveUserProfile)#CTkButton(self.top_level_window, "Save User Info",width=100,  height=32, command=self.saveUserProfile)
        self.CancelButton=customtkinter.CTkButton(master=self.top_level_window,  width=130,  height=36,text="Cancel",command=self.CancelUserProfile)
       
       #----------------------------- Labels ------------------------#
        self.ErroeLabel= Label(self.top_level_window, text="",fg="red",bg="#43423F")
        userLabel = Label(self.top_level_window, text="User Name :",fg="#ffffff",bg="#43423F" )
        emailLabel = Label(self.top_level_window, text="Email :",fg="#ffffff",bg="#43423F")
        windowInfo =Label(self.top_level_window, text="User profile",width=400 ,height=3,fg="#ffffff",bg="#1C94D0")
       
       #------------------------ CheckButton ------------------------#
 
        self.var= IntVar()
        self.SendNotification=Checkbutton(
                                            self.top_level_window,
                                            text="Send notifications",
                                            variable=self.var,
                                            onvalue=1,
                                            offvalue=0,
                                            selectcolor="#43423F",
                                            fg="#ffffff",
                                            bg="#43423F",
                                            
                                        )
        self.var.set(int(notify))
        self.SendNotification.var  =self.var 
       
        
        #-------------------------  Entries  ------------------------#
        self.EmailText=Entry(self.top_level_window, width=45)
        self.EmailText.insert(END,email)
        self.usernameText=Entry(self.top_level_window,width=45)
        self.usernameText.insert(END,username)
        #----------------------- Packing -----------------------------#
        windowInfo.grid(row=0,column=0 ,columnspan=2,sticky="ew")
        # user name
        userLabel.grid(row=1, column=0,pady=3)
        self.usernameText.grid(row=1,column=1,pady=3)
        # email
        self.EmailText.grid(row=2,column=1,pady=3)
        emailLabel.grid(row=2, column=0,pady=3)
        #checkButtons
        self.SendNotification.grid(row=3, column=0,columnspan=2,pady=3)
        #error text columnspan=2
        self.ErroeLabel.grid(row=4, column=1,columnspan=2,pady=3)
        #buttons
        self.SubmitButton.grid(row=5, column=0,columnspan=2,pady=2,padx=0)
        self.CancelButton.grid(row=6, column=0,columnspan=2,pady=1,padx=0)
        
#------------------------------------------------------------------------------#
#------------------------------- Chart Class ----------------------------------#
#------------------------------------------------------------------------------#

class Charts():
    """ 
    --------------------------------------------------------------------------------
                                 variables Section
    --------------------------------------------------------------------------------
    """

    """ 
    -----------------------------------------------------------------------------------
                                    constructor
    ------------------------------------------------------------------------------------
    """
    def __init__(self,root, Title, Opertation="", column=1,row=-1):
        self.Title=Title
        self.root=root
        self.Opertation= Opertation
        self.column= column
        self.row= row

    """ 
    -----------------------------------------------------------------------------------
                                 Create The Figure Diagram
    ------------------------------------------------------------------------------------
    """    
    def creat_figure(self, type="C"):
        
        f = open('githubChanges.json',"r")
        datajson = json.load(f)
        f.close()
        datajson.pop("ReplaceDiff",None)
        #----------------------- Convert data to Percentege --------------------------#
        Total = 0
        data={}
       

        for key,item  in datajson.items():
            if  item["C"] != 0:
                data[key] =float("{:.2f}".format( (item[type] / item["T"])*100))
            else :
                data[key] =0
        
        # prepare data
        data =  datajson
        
        languages = data.keys()
        popularity = data.values()  
        # create a figure
        
        figure = Figure(figsize=(16, 4), dpi=80)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure,  self.root)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, self.root)

        # create axes
        axes = figure.add_subplot()

        # create the barchart
        axes.bar(languages, popularity)
        axes.set_title('Top Errors in Code')
        axes.set_ylabel('Popularity')

        figure_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

       
#------------------------------------------------------------------------------#
#--------------------- Progress Par to Wait the result ------------------------#
#------------------------------------------------------------------------------#

class CustmizeProgressPar:

    """ 
    --------------------------------------------------------------------------------
                                 variables Section
    --------------------------------------------------------------------------------
    """

   
    root=NONE
    OperationList=[dbInteraction.get_commits_errors_totals,
                    dbInteraction.get_totals,
                    dbInteraction.get_number_of_buges_and_fixes]
    fram=None
    TextLabel=""
    Opertation=0

    """ 
    -----------------------------------------------------------------------------------
                                    constructor
    ------------------------------------------------------------------------------------
    """
    def __init__(self,root, TextLabel, Opertation, column=1,row=-1):

        self.root = root
        self.TextLabel=TextLabel
        self.Currentopertation= self.OperationList[Opertation]
        self.Opertation=Opertation
        self.data=[]
        self.columns=[]
        self.Headings=[]
        self.progressPare = NONE
        self.InfoLabel=NONE
        self.column= column
        self.row = row
       
        
    """ 
    ------------------------------------------------------------------------------------
                                     Thread Checking
    ------------------------------------------------------------------------------------
    """
    def check_thread_Alive(self,thread):
        #check if the Thread is alive
        if thread.is_alive():
            #Keeps Progress Bar wait some seconds until finish
            self.root.after(3000,lambda t=thread: self.check_thread_Alive(thread))
        else:
            # if not remove Progress Bar
            self.progressPare.stop()
            self.progressPare.destroy()
            self.Formate_Table()
            self.iInfoLabel.destroy()

    """ 
    ------------------------------------------------------------------------------------
                                         start Thread
    ------------------------------------------------------------------------------------
    """
    def start_Thread(self,columnspan=0):

        
            #-------------------- start the thread here -----------------#
            thred = threading.Thread(target=self.Create_Totals_Table)
            thred.start()
            

            self.fram = LabelFrame(self.root,text=self.TextLabel ,padx=10,pady=20,borderwidth=0,bg="#43423F",fg="white" ,font=("Helvetica bold",15))
            if self.row !=-1:
                if columnspan >0:
                    self.fram.grid(row=self.row,column=self.column,sticky="nsew",columnspan=columnspan)
                else :
                    self.fram.grid(row=self.row,column=self.column,sticky="nsew")
            else :
                if columnspan >0:
                     self.fram.grid(row=self.Opertation,column=self.column,sticky="nsew",columnspan=columnspan)
                else :
                    self.fram.grid(row=self.Opertation,column=self.column,sticky="nsew")

            #------------------ Start Progress Pare ----------------------#
            self.progressPare=ttk.Progressbar(self.fram,orient=HORIZONTAL, length=300, mode='indeterminate')
            self.iInfoLabel= ttk.Label(self.fram, text=" Gathering Information ..",background="#43423F",foreground="white")
            self.progressPare.pack()
            self.iInfoLabel.pack()
            self.progressPare.start(10)
        
            #----------------------- start checking the thred -----------#
            self.check_thread_Alive(thred)



    """ 
    ---------------------------------------------------------------------------------------
                                    get data from Thread
    ---------------------------------------------------------------------------------------
    """
    def Create_Totals_Table(self):
        self.data,self.columns,self.Headings = self.Currentopertation()
       

    """ 
    --------------------------------------------------------------------------------------
                                      Formate Table
    --------------------------------------------------------------------------------------
    """
    def Formate_Table(self ):

       
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=2, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading",background='#ffffff',foreground="black", font=('Calibri', 12,'bold')) # Modify the font of the headings
        style.configure("Treeview.Heading", font=('Calibri', 13,'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
    
        # ------- Create Table View Instance -------#
        my_tree = ttk.Treeview(self.fram,style="mystyle.Treeview", height=10)
        my_tree['columns']=self.columns

        my_tree.tag_configure('odd', background='#FFFFFF',foreground="#282726")
        my_tree.tag_configure('even', background='#9ECAFF',foreground="#282726")

        # ------------ Format Columns ---------------#
        my_tree.column("#0",width=40,minwidth=25)
        for column in  self.columns :
            my_tree.column(column,anchor="w",minwidth=170)

        # -----------  Columns Headings ---------------#
        my_tree.heading("#0",text="",anchor=W)

        #------ Loop Throw 2 List in the same time ----#
        zip_object = zip(self.Headings, self.columns)
        for Heading,column in zip_object:
            my_tree.heading(column,text=Heading,anchor=W)

        # -----------  Columns INSERT ---------------#
        for index,value in enumerate(self.data):
            if index%2 ==0:
                my_tree.insert(parent='',index='end',iid=index,text=str(index +1),values=([value[col] for col in self.columns]),tags = ('even',))
            else:
                 my_tree.insert(parent='',index='end',iid=index,text=str(index+1),values=([value[col] for col in self.columns]),tags = ('odd',))

        my_tree.pack(pady=20,anchor=W)





#------------------------------------------------------------------#
#------------------------- AboutFrame -----------------------------#
#------------------------------------------------------------------#

class AboutFrame:
    fram=None
    root=None
    Welcomlabel=None

    #Initialize Welcome Frame Object Class
    def __init__(self,root):
        self.fram = LabelFrame(root,text="AutoVuSolidity",padx=50,pady=50,borderwidth=1,bg="#43423F",fg="white" ,font=("Helvetica bold",15))
        self.root = root


    def getFrame(self,root):
        self.fram.grid(row=0,column=1,sticky="new")
         #-------------- Create Frame Contents Here --------------#
        self.fram.rowconfigure(0,weight=1)
        self.fram.rowconfigure(1,weight=1)
       
        self.fram.columnconfigure(0,weight=1)

        self.Welcomlabel= Label(self.fram,bg='#43423F', text='''AutoVuSolidity is a tool to continuously mine a comprehensive vulnerable and the corresponding patched smart contract code written in Solidity and Vyper from open source projects on GitHub and from CVE records. Next, AutoVuSolidity automatically cleans and organizes the vulnerabilities and their corresponding fixes at multiple levels of granularity. After that, it automatically scans and analyzes the collected vulnerabilities and their fixes using the available smart contracts analysis tools.
             In addition, it automatically notifies the tool owners if the tool fails to determine the type of vulnerability or detect it, on top of reporting the vulnerabilities to developers. ''',
             fg='#ffffff', pady=2, padx=10,justify=CENTER, font=10,wraplength=700 )

        self.Welcomlabel2= Label(self.fram,bg='#43423F', text='''For more information, email: majdsoud5@gmail.com ''',fg='#ffffff', pady=10, padx=10,justify=CENTER, font=10 )
        self.Welcomlabel.grid(row=0,column= 0, ipady=50,sticky="nsew")
        self.Welcomlabel2.grid(row=1,column= 0, ipady=50,sticky="nsew")
        
  
     # remove Fram from the window
    def Forget_Fram(self):
       remove_fram_Contents(self.fram)
#-------------------------------------------------------------------#
#------------------------- Welcome Class ---------------------------#
#-------------------------------------------------------------------#

class WelcomFrame :

    fram=None
    root=None
    working= True
    #Initialize Welcome Frame Object Class
    def __init__(self,root):
        self.fram = Frame(root,bg="#43423F", bd=10,padx=2,pady=10)
        self.root = root
        
    #----------------- function to Update Logs In Logs Fram -------------------------------#
    def write_logs(self):
        #------------- Delete prevoiuse Text ------------#
        self.text.delete("1.0", "end")
        #----------------------------- Ctrate Our Log File --------------------------------#
        text=""
        try:
            #------------- open Log File ------------#
            with open("std.log") as f:
            #------------- read File Lines------------#
                lines = f.readlines()
            #------------Loop Through lines-----------#
            for line in lines:
                #---------check if the pulling and configuration are done ------#
                if "Done Working" in line:
                    self.working= False
                #------------insert line to text-----------#
                self.text.insert(END,line)
                self.text.see("end")
            #------------Update Text View After all-----------#
            self.text.update()
        except: 
            pass
        #-------------- Recall Function after 5 sec ------------#
        #------------ if any thread is still working -----------#
        if self.working :
            self.fram.after(3000,self.write_logs)
            
        

    def getFrame(self,root):

        self.fram.grid(row=0,column=1,sticky="nsew")
        #-------------- Configure Rows and Columns --------------#
        self.fram.rowconfigure(0,weight=1)
        self.fram.rowconfigure(1,weight=1)
        self.fram.rowconfigure(2,weight=12)
        self.fram.columnconfigure(0,weight=1)
        self.fram.columnconfigure(1,weight=9)

        #----------------- Create Logo Images ------------------#
        self.img= ImageTk.PhotoImage(Image.open("imgs/SolidityAutoLogo.png"))
        self.background_label = Label(self.fram,image=self.img,bg="#43423E")
        self.background_label.grid(row=1,column=1,columnspan=10, padx=10,pady=10,sticky="n")
        
        #-------------- Create Frame Contents Here --------------#
        self.text = Text(self.fram) 
        self.text.grid(row=2,column=1,columnspan=10, padx=10,pady=10,ipady=50,sticky="nsew")
        self.text.insert(INSERT,"Configuration Procedures Started please wait until everything is set up correctly.if this is the first time using our App then it will take several minutes until everything is installed so set down and relate Until all processes completes")

        self.scrolbar= Scrollbar(self.fram , command=self.text.yview )
        self.scrolbar.grid(row=2, column=0,sticky="nse")
        self.text.config(yscrollcommand=self.scrolbar.set)

        #------------------ Start Recursions  -------------------#
        self.write_logs()

  
        
    def format_log(string1):
        return string1

    def Forget_Fram(self):
        remove_fram_Contents(self.fram)
#-------------------------------------------------------------------#
#------------------------- Welcome Class ---------------------------#
#-------------------------------------------------------------------#
class statisticsFrame : 

    GithubTotals = None
    def __init__(self,root):
        self.fram = Frame(root, bd=10,padx=10,pady=10,bg="#43423F") 

        """
        --------------------------------------------------------------
                    Start The Operation Of Gathering data
        --------------------------------------------------------------
        """
        self.GithubTotals = CustmizeProgressPar(self.fram,"Top 10 GitHub Repos with the highest Errors Detected By tools",0)
        self.ToolsErrorsTotal = CustmizeProgressPar(self.fram,"Top 10 GitHub Repos with the highest Files-Changing Rates",1)
        self.TotalFixesBuges =CustmizeProgressPar(self.fram,"Total/AVERAGE # of Bugs with Fixes and without Fixes",2,2,0)

    def getFrame(self,root):

         self.fram.grid(row=0,column=1,sticky="nsew")

         #------------------ Start Thread -------------------#
        
         self.GithubTotals.start_Thread()
         self.ToolsErrorsTotal.start_Thread(2)
         self.TotalFixesBuges.start_Thread()

    # remove Fram from the window
    def Forget_Fram(self):
        remove_fram_Contents(self.fram)
#-------------------------------------------------------------------#
#------------------------- Welcome Class ---------------------------#
#-------------------------------------------------------------------#
class ToolsFrame :
    
    fram=None
    #Initialize Welcome Frame Object Class
    def __init__(self,root):
        self.fram = Frame(root, bd=10,padx=10,pady=10,bg="#43423F")
     

    def getFrame(self,root):
        self.fram.grid(row=0,column=1,sticky="nsew")
        #------- copy past Fram Configurations
        f = open('docker-tools/tools/tools.json')
        data = json.load(f)
        f.close()
        
        #-------------- Create Frame Contents Here --------------#
        self.fram.rowconfigure(0,weight=1)
        self.fram.rowconfigure(1,weight=1)
        self.fram.rowconfigure(2,weight=1)
        self.fram.rowconfigure(3,weight=1)
        self.fram.rowconfigure(4,weight=1)
        self.fram.rowconfigure(5,weight=1)
        self.fram.rowconfigure(6,weight=1)
        self.fram.columnconfigure(0,weight=1)
        self.fram.columnconfigure(1,weight=1)
        
        index=0
        twis=0
        row=0
        for item in data :
            if twis==2:
                twis=0
                row= row+1

            if index%2==0:
                odd= False
            else:
                odd= True
         
            Create_Tool_Fram(self.fram,item,row,odd) 
            twis+=1
            index+=1
            
    # remove Fram from the window
    def Forget_Fram(self):
       remove_fram_Contents(self.fram)

#-------------------------------------------------------------------#
#------------------------- Analyz Class ---------------------------#
#-------------------------------------------------------------------#
class AnalyzFrame :
    
    fram=None
    MessageEntry=None
    CodeEntry=None
    #Initialize Welcome Frame Object Class
    def __init__(self,root):
        self.fram = Frame(root, bd=10,padx=2,pady=10)
        

    def getFrame(self,root):
        self.fram.grid(row=0,column=1,sticky="nsew")
       
        #-------------- Create Frame Contents Here --------------#
        self.fram.rowconfigure(0,weight=10)
        self.fram.rowconfigure(1,weight=1)
       
        self.fram.columnconfigure(0,weight=1)

        #------- copy past Fram Configurations
        CopyPast_Fram = LabelFrame(self.fram,text="Analyze A copy of the code:",height=10)
        CopyPast_Fram.rowconfigure(0,weight=10)
        CopyPast_Fram.rowconfigure(1,weight=5)
        CopyPast_Fram.rowconfigure(2,weight=5)
        CopyPast_Fram.rowconfigure(3,weight=5)
        CopyPast_Fram.rowconfigure(4,weight=1)
        CopyPast_Fram.columnconfigure(0,weight=1)
     

        Result_Fram = LabelFrame(self.fram,text="Analyzing Result :" ,height=2)
        Result_Fram.rowconfigure(0,weight=1)
        Result_Fram.columnconfigure(0,weight=1)

        #------- copy past Fram Main Tools Buttons
        self.CodeEntry = ScrolledText(CopyPast_Fram)
        self.MessageEntry = Label(CopyPast_Fram, text="")
        self.ErrorMrssage = Label(CopyPast_Fram, text="")
        self.MessageEntry.config(font=("Arial Bold", 15))#smartcheck
        

        #------- Result Fram Text-----------------#
        self.ResultEntry = ScrolledText(Result_Fram,height = 8,pady = 10, padx = 10 )
        #-------copy past Fram Analyze Buton solhint_image_check
        self.anlyzeButton = customtkinter.CTkButton(master=CopyPast_Fram,  width=100,  height=32,text="Analyze", command=self.Start_Analyze_image_check)#tkinter.Button(self.fram,text="Analyze")

              #------------------------ CheckButton ------------------------#
 
        self.var= BooleanVar()
        self.IsVyber=Checkbutton(
                                            CopyPast_Fram,
                                            text="Is Vyber",
                                            variable=self.var,
                                            onvalue=True,
                                            offvalue=False,
                                            
                                        )
       
        #-----packing CopyPast_Fram Items ----------#
        self.CodeEntry.grid(row=0,column= 0,columnspan=10, padx=10,pady=10,ipady=50,sticky="nsew")
        self.MessageEntry.grid(row=1, column=0,columnspan=10, padx=10,pady=10)
        self.ErrorMrssage.grid(row=2,column= 0, padx=10,pady=10)
        self.IsVyber.grid(row=3,column= 0, padx=10,pady=10,sticky="nsew")
        self.anlyzeButton.grid(row=4,column= 0, padx=10,pady=10)
       

        #--------------------pack Frames-------------------------#
        CopyPast_Fram.grid(row=0,column=0,sticky="nsew")

        #------------------- Result Packing ----------------------#
        self.ResultEntry.grid(row=0,column= 0,columnspan=10, padx=10,pady=10,ipady=50,sticky="nw")

        #---------------------------------------------------------#
        Result_Fram.grid(row=1,column=0)
       

    """
    -------------------------------------------
        analyzeing past code by tools 
    -------------------------------------------
    """
    def Start_Analyze_image_check(self):
        tools= [  "smartcheck","solhint","securify","slither","osiris","mythril","maian","honeybadger" ]
        #----------------------- get Values ------------------------#
        isVyber =self.var.get()
        cur_inp = self.CodeEntry.get("1.0", END)

        #--------- Check If there is any Code in the text -----------#
        if len(cur_inp) <= 1 or cur_inp==" " or cur_inp=="" or cur_inp==None:
            print("Hello" + str(len(cur_inp)))
            self.ErrorMrssage.config(text=" No Code To Analyze !!") 
            return
        else:
            print("Not Hallo"+ str(len(cur_inp)))
            self.ErrorMrssage.config(text="") 
        #--------------- Exit From The Function -------------------#
            

        #------- Check The File Type if its Vyper Or Solidity -------#
        if isVyber:

            # ------ Write in Vyber File and then process it --------#
            lag="Vyper"
             #------------------- get the directory where we are going to save it -------------#
            directory = getcwd()
            filename = directory + '/docker-tools/contracts/anlyizing.vyp'
            print("Vyper")
            
            
        else:

            # ------ Write in Solidity File and then process it ------#
            lag="Solidity"
            directory = getcwd()
            filename = directory + '/docker-tools/contracts/anlyizing.sol'
            print("Solidity")

         #------------------------- Open the File and Wite it -----------------#
        with open(filename, "w", encoding="utf-8") as f:
            f.write(cur_inp)
        
        f.close()

        for  index,tool in enumerate(tools) :
            print(tool)
            value,errorscount= util.Analyze_Data_from_a_string(tool,lag,None,None)
            print(value ,"value",errorscount,"errorscount")
            if value !=[] and errorscount!=0:
                print(value,"==============Analyze_Data_from_a_string===============")
                break
            if index == len(tools)-1  :
                value,errorscount  ="None",0
             
            #------------- we need to insert not found
           
            
        
        print(cur_inp)
        print(isVyber)
        
        self.ResultEntry.insert(END, value)
        
 
    # remove Fram from the window
    def Forget_Fram(self):
       remove_fram_Contents(self.fram)




#-------------------------------------------------------------------#
#------------------------- Welcome Class ---------------------------#
#-------------------------------------------------------------------#
class MenuFrame :
    #Class Varibles
    fram=None
    Tool_fram=None
    welcomfram=None
    anlyz_fram=None
    About_Fram=None
    infoFram=None
    github_datasetfram=None
    statics_fram=None
    root=None

    #Initialize Welcome Frame Object Class
    def __init__(self,root):
        self.Tool_fram=ToolsFrame(root)#Create an Instance from Tool_Fram class
        self.welcomfram=WelcomFrame(root)#Create an Instance from WelcomFrame class
        self.anlyz_fram=AnalyzFrame(root)#Create an Instance from anlyz_fram class
        self.About_Fram=AboutFrame(root)#Create an Instance from About class
        self.github_datasetfram=WelcomFrame(root)#Create an Instance from github_datasetfram class
        self.statics_fram=statisticsFrame(root)#Create an Instance from statics_fram class

        self.root=root
        self.fram = Frame(root, bg="#43423F", bd=2)#Create Main Fram
        
     

    def getFrame(self,root):
        self.Menu_Buttons()#Create Menu Butons 
        self.fram.grid(row=0,column=0,sticky="nsew")
        self.welcomfram.getFrame(root)
        
    
    #------------ Open Analyze Frame ------#
    def open_anlysz(self):
        self.Close_frames()
        self.anlyz_fram.getFrame(self.root)

    #------------ Open Tools Frame ---------#
    def open_Tools(self):
        self.Close_frames()
        self.Tool_fram.getFrame(self.root)

    #---------- Open Welcome Frame ----------#
    def open_Welcome(self):
        self.Close_frames()
        self.welcomfram.getFrame(self.root)

     #---------- Open Github dataset Frame ----------#
    def open_Github_dataset_fram(self):
        self.Close_frames()
        self.welcomfram.getFrame(self.root)

     #---------- Open Welcome Frame ----------#
    def open_statics_fram(self):
        self.Close_frames()
        self.statics_fram.getFrame(self.root)

    #---------- Open Welcome Frame ----------#
    def open_About_fram(self):
        self.Close_frames()
        self.About_Fram.getFrame(self.root)
    #-----------------------------------------#
    def open_Welcom_fram(self):
        self.Close_frames()
        self.welcomfram.getFrame(self.root)
    #----------- Close All Frames -----------#
    def Close_frames(self):
        self.About_Fram.Forget_Fram()
        self.anlyz_fram.Forget_Fram()
        self.statics_fram.Forget_Fram()
        self.Tool_fram.Forget_Fram()
        self.github_datasetfram.Forget_Fram()
        self.welcomfram.Forget_Fram()


    #----------- define Butons and Its Actions -----------#
    def Menu_Buttons(self):
         #---But all MenuButtons here

        self.fram.rowconfigure(0,weight=1)
        self.fram.rowconfigure(1,weight=1)
        self.fram.rowconfigure(2,weight=1)
        self.fram.rowconfigure(3,weight=1)
        self.fram.rowconfigure(4,weight=1)
        self.fram.rowconfigure(7,weight=15)
        self.fram.grid_columnconfigure(0, weight=1)

        analyze_btn = customtkinter.CTkButton(master=self.fram,  width=250,  height=60,text="Analyze", command=self.open_anlysz)#tkinter.Button(self.fram,text="Analyze")
        statistics_btn = customtkinter.CTkButton(master=self.fram, width=250,  height=60,text="Statistics", command=self.open_statics_fram)#tkinter.Button(self.fram,text="Statistics")
        #GithubSet_btn = customtkinter.CTkButton(master=self.fram, width=250,  height=60,text="Github Dataset", command=self.open_Github_dataset_fram)#tkinter.Button(self.fram,text="Github Sets")
        tools_btn = customtkinter.CTkButton(master=self.fram, width=250,  height=60,text="Tools", command=self.open_Tools)#tkinter.Button(self.fram,text="Tools")
        about_btn = customtkinter.CTkButton(master=self.fram,width=250,  height=60, text="About", command=self.open_About_fram)#tkinter.Button(self.fram,text="About")
        Info_btn = customtkinter.CTkButton(master=self.fram,width=250,  height=60, text="App Process Info", command=self.open_Welcom_fram)#tkinter.Button(self.fram,text="About")
        analyze_btn.grid(row=0,column=0, pady=1)
        statistics_btn.grid(row=1,column=0, pady=1)
        #GithubSet_btn.grid(row=2,column=0, pady=1)
        tools_btn.grid(row=2,column=0, pady=1)
        about_btn.grid(row=3,column=0, pady=1)
        Info_btn.grid(row=4,column=0, pady=1)





