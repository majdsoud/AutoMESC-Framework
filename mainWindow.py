
from time import sleep
from tkinter import *
from tkinter.ttk import Progressbar
from WelcomFrame import WelcomFrame ,MenuFrame
from menus import MainMenu
from PIL import Image, ImageTk
from GitHub_repo_collecter import get_repos_within_a_period
from datetime import datetime
import customtkinter
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
from main import main_func
import threading 
from util import chech_main_Image
import logging    # first of all import the module


#----------------------------- Ctrate Our Log File --------------------------------#

logger=logging.getLogger('std.log') 
global progressPare
global top_level_window

#---------- Putting Window In the Center of the Screen ----------#
global window_height 
global window_width 

global screen_width 
global screen_height 

#----------------------------------------------------------------------------------#
#----------- a Function to start another Thread after the first thread dies -------#
#----------------------------------------------------------------------------------#
def check_if_alive(t, root ):
        if t.is_alive():

            root.after(200,lambda t=t, root=root: check_if_alive(t,root))

        elif  not t.is_alive():

           
           
           logger.info("Data base and Docker Thread is done")
           
           logger.info("Installing Tools now")

           sleep(30)

           f2 = threading.Thread( target=main_func, args=[logger])

           f2.start() 
           check_tools_thread_if_alive(f2) 
        

def check_tools_thread_if_alive(tools_thread):
        if tools_thread.is_alive():
            root.after(10000,lambda t=tools_thread: check_tools_thread_if_alive(t))
        elif not tools_thread.is_alive():
            logger.info("Done Working")

            #removing all childrens the fram Contains
            global top_level_window
            global progressPare
            """
            -------------------------------------------------------------------------------
                             Stop Progress Pare After Everything is Done 
            -------------------------------------------------------------------------------
            """
            
            progressPare.stop()
            progressPare.destroy()
            """
            -------------------------------------------------------------------------------
                             close Top Level Window and close after finishing 
            -------------------------------------------------------------------------------
            """
            for widget in top_level_window.winfo_children():
                widget.destroy()
                top_level_window.destroy()
           
           
            

#----------------------------------------------------------------------------#
#-----------------------------Splash Screen ---------------------------------#
#----------------------------------------------------------------------------#

splashScreen =  Tk()

#---------- Putting Window In the Center of the Screen ----------#

window_height = 500
window_width = 540

screen_width = splashScreen.winfo_screenwidth()
screen_height = splashScreen.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

splashScreen.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

splashScreen.resizable(False, False)

#--------------- Putting Image and Labels On Window ----------------#
img= ImageTk.PhotoImage(Image.open("imgs/icon-bug-15.jpg"))
background_label = Label(splashScreen,image=img)
background_label.place(x = 0,y = 0)
background_label2 = Label(splashScreen,text="Welcome to Automatic Ethereum Vulnerability AutoVuSolidity ..",font=("Helvetica",30))
background_label2.pack(pady=220)

splashScreen.overrideredirect(True)#Hide Title Par




#----------------------------------------------------------------------------#
#-----------------------------  Main Window ---------------------------------#
#----------------------------------------------------------------------------#
def mainWindow():

    #threading.Thread(target=my_function).start()
    splashScreen.destroy()
   
    global root
    root = customtkinter.CTk()

    #------------------ Create Our TitltBare ------------------------#
    root.title('Automatic Ethereum Vulnerability AutoVuSolidity')# secreen  Title

    root.iconbitmap("imgs\\bugIcon.ico")# secreen Icon

    #------------------- Configure Window View ----------------------#
    
    root.state('zoomed')

    # get the width and height of the machine
    ws = root.winfo_screenmmwidth()

    hs= root.winfo_screenheight()

    w=700

    h=400

    # calculate window height and width

    x = int(ws/2 -w/2)
    y= int(hs/2 -h/2)

    data = str(w)+"x"+str(h)+"+"+str(x)+"+"+str(y)
    root.geometry(data)

    # setting the width and height of the window
    root.configure(background="#1A1C1F")
    root.rowconfigure(0,weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=9)
    Main_menu = MainMenu(root)
    #------------ Menu Frame ----------------#
    menuFrame = MenuFrame(root)
    menuFrame.getFrame(root)

    
    
    #---------------------------------------------------------------------#
    # ------------------ Start Database Connectivity here ----------------#
    #---------------------------------------------------------------------#

    logger.info("Starting Checking Docker and Database Connection")
    #-------------------- Create Our Progress Pare ----------------------#
    """
    ----------------------------------------------------------------------
             Setting Up Hight and width of the Top level screen 
    ----------------------------------------------------------------------
    """
    global window_width
    global  window_height 
    window_width= 400
    window_height =250
    global  screen_width
    global screen_height


    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    global top_level_window
    top_level_window = Toplevel(root,background="#43423F")

   #------------------ Set Hight and Wisth----------------------#
    top_level_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    top_level_window.grab_set()
    top_level_window.overrideredirect(True)
    
    windowInfo =Label(top_level_window, text="Initializing App",width=400 ,height=3,fg="#ffffff",bg="#1C94D0",font=("Arial Bold", 12)).pack(anchor="ne")
    global progressPare
    #------------------ Start Progress Pare ----------------------#
    progressPare=Progressbar(top_level_window,orient=HORIZONTAL, length=300, mode='indeterminate')
    progressPare.pack(pady=30)
    progressPare.start(10)
    WlecomingLabel =Label(top_level_window, text="This Operation May Take a while, sit and relax until it finishes",fg="#ffffff",bg="#43423F").pack(pady=2)
    workinglabel =Label(top_level_window, text="In Progress ",fg="#ffffff",bg="#43423F").pack(pady=2)

    f1 = threading.Thread(target=chech_main_Image )
    f1.start() 
    logger.info("Docker Tools and Database are Connected and ready to go ")
    check_if_alive(f1 , root)
     

#--------- start Splash Screen ---------#
splashScreen.after(3000, mainWindow)


mainloop()