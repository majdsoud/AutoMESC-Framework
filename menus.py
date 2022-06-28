from tkinter import *
from asyncio.windows_events import NULL
from dbInteraction import Create_csv
import os, time, sys, subprocess
from WelcomFrame import UserProfile
import platform

class MainMenu :
    
    menu=None #Main Menu
    master=None# Tkinter Container Reference
    file_menu = None# File Menu
    Setting_Menu =None #Settings Menu

    def open_Notification_of_Automation(self):
        global window_width
        global  window_height 
        window_width= 400
        window_height =250
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()


        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        global top_level_window
        top_level_window = Toplevel(self.master,background="#43423F")

    #------------------ Set Hight and Wisth----------------------#
        top_level_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        top_level_window.grab_set()
        top_level_window.overrideredirect(True)

        windowInfo =Label(top_level_window, text="Automation Operation Has Started",width=400 ,height=3,fg="#ffffff",bg="#1C94D0",font=("Arial Bold", 12)).pack(anchor="ne")
        WlecomingLabel =Label(top_level_window, text="This Operation May Take a while",fg="#ffffff",bg="#43423F").pack(pady=2)
        WlecomingLabel2 =Label(top_level_window, text=" Keep The Terminal (cmd) working,don't close it plz",fg="#ffffff",bg="#43423F").pack(pady=2)
        NoteLabel =Label(top_level_window, text="Closing the Terminal will close the Operation",fg="red",bg="#43423F").pack(pady=2)
        NoteLabel2 =Label(top_level_window, text=" wait till it is done working",fg="red",bg="#43423F").pack(pady=2)
        closeButton= Button(top_level_window,text="Close", command=top_level_window.destroy,fg="#ffffff",bg="#1C94D0",font=("Arial Bold", 12)).pack(pady=3)


    def Start_Automation(self):
        print('main begin')
        
        #----------------------- Start Automatoon Process In the Background --------------------------------------#
        

        if platform.system() == 'Windows':
            #start /min python automation_info_update.py -u &
            #command = ["start \min ",os.path.abspath(os.curdir) ,"\\automation_info_update.py","-u &"]
            command = "start /min python automation_info_update.py -u &"
            #print(command)
            print("In Windows................")
            #p = subprocess.Popen(command, stderr=PIPE, stdout=PIPE, shell=True)
            p= subprocess.Popen(command,shell=True,stdout=subprocess.PIPE, close_fds=True)
            #self.Setting_Menu.entryconfig("name of the command", state='di')
            print(p)
        
        else:
           # print("In Others ................")
            subprocess.Popen([' nohup python', os.path.realpath(' automation_info_update.py -u &'), '0'], close_fds=True)
        print('main end')
        self.open_Notification_of_Automation()

    # Menu Quit Command
    def exit_Progeam(self):
        self.master.quit()
   
   #Menu export Command 
    def export_csv(self):
        Create_csv()

    # Open Profile window 
    def OpenWindow(self):
        profile = UserProfile(self.master)
        profile.Open_User_Profile_Window()


   #Initialize Menu Object Class
    def __init__(self,root): 
        self.menu = Menu(root)
        self.master= root
        root.config(menu=self.menu)
        self.Submenus()

    # create a menu item 
    def Submenus(self):
        #-------------------------- File Menu ----=-----------------#
        self.file_menu =Menu(self.menu)# Instantiate menu Object
        self.menu.add_cascade(label="File", menu=self.file_menu) # add the menu to the main menu
        self.file_menu.add_command(label="Set User Profile", command=self.OpenWindow) # create submenu and add action to it
        self.file_menu.add_command(label="Exit", command=self.exit_Progeam) # create submenu and add action to it
       
       #------------------------- Settings Menu -----------------------#
        self.Setting_Menu= Menu(self.menu)# Instantiate menu Object
        self.menu.add_cascade(label="Settings", menu=self.Setting_Menu)# add the menu to the main menu
        self.Setting_Menu.add_command(label="Start Automation", command=self.Start_Automation)# create submenu and add action to it
        self.Setting_Menu.add_command(label="Export CSV", command=self.export_csv)# Export all tables as CSV

       