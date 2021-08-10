#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 19:56:26 2021

@author: ashwin
"""

import tkinter as tk
import os
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
from tkinter import filedialog
from tkinter import messagebox
import random
from cryptography.fernet import Fernet
import shutil
from pathlib import Path

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.cwd =os.getcwd()
        self.Home_address = str(Path.home())
        print(self.Home_address)
        self.passwordfile = "password.txt"
        self.foldersfile = "folders.txt"
        self.Password_address = os.path.join(self.Home_address,self.passwordfile)
        self.Folders_address = os.path.join(self.Home_address,self.foldersfile)
        self.title('Locker-Encrypt')
        self.strspaced = ""
        self.stringedkey = ""
        self.strkey = ""
        self.str14 = ""
        self.renamed_folder = ""
        self.hide_button_image = PhotoImage(file = r"locks.png")
        self.hide_button_icon = self.hide_button_image.subsample(3, 3)
        self.restore_button_image = PhotoImage(file = r"unlocks.png")
        self.restore_button_icon = self.restore_button_image.subsample(3, 3)
        self.st = ttk.Style(self)
        self.st.configure('my.TButton',font=('Helvetica', 12),foreground='red',background='black',relief ='flat')
        self.st.map('my.TButton', background=[('active','red')])
        self.high_st = ttk.Style(self)
        self.high_st.configure('highlight.TButton',foreground='green',background='black',font=('Helvetica', 12))
        self.default = " \"Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30"
        self.notebook = ttk.Notebook(self)
        self.resizable(False,False)
        self.notebook.pack(fill=BOTH,expand=True)
        self.notebook.config(width=300,height=300)
        self.frame1 =ttk.Frame(self.notebook)
        self.frame2 =ttk.Frame(self.notebook)
        self.notebook.add(self.frame1,text='Add')
        self.notebook.add(self.frame2,text='Settings')
        self.bt1 = ttk.Button(self.frame1,text = 'Hide Folder', command = self.browseit, style = 'my.TButton',image = self.hide_button_icon, compound ="left")
        self.bt1.pack(fill=BOTH,expand=True)
        self.bt4 = ttk.Button(self.frame1,text = 'Restore Folders',command = self.getpass, style = 'highlight.TButton', image = self.restore_button_icon, compound = "left")
        self.bt4.pack(fill=BOTH,expand=True)
        self.bt2 = ttk.Button(self.frame2,text = 'Set Password',command = self.setpass, style = 'my.TButton')
        self.bt2.pack(fill=BOTH,expand=True)
        self.bt3 = ttk.Button(self.frame2,text = 'Change Password',command = self.changepass, style = 'my.TButton')
        self.bt3.pack(fill=BOTH,expand=True)
        self.frame3 = ttk.Frame(self.notebook)
        self.notebook.add(self.frame3,text='Folders')
        self.lb1 = Listbox(self.frame3,selectmode=MULTIPLE,width=100,height=20)
        self.lb1.pack(fill=BOTH,expand=True)
        
#Initial tests--------------------------------------------------------------------------        
        if(os.path.exists(self.Folders_address)==False):
            self.fcheck = open(self.Folders_address,"w")
            self.fcheck.close()
        if(os.path.exists(self.Password_address)==False):
            self.pfile = open(self.Password_address,"w")
            self.pfile.close()
        self.f = open(self.Folders_address,"r")
        self.filesize = os.path.getsize(self.Folders_address)
        print(self.filesize)
        print(self.st.theme_names())
        if(self.filesize == 0):
            self.f.close()
        else:    
            for x in self.f:
                self.lb1.insert(END,x.split(',')[1])
        self.f.close()
        
        self.lblist = []
        self.counter = 1 
        if os.stat(self.Password_address).st_size != 0:
            self.bt2.state(['disabled'])
#-----------------------------------------------------------------------------------------


#Get password from file-------------------------------------------------------------------     
    def getpass(self):
        self.passit = askstring('Password', 'Enter password:', show="*")
        f3 = open(self.Password_address,'r')
        self.passtext = f3.read()
        if(self.passit==self.passtext):
           self. restore()
        else:
            if(self.counter>1):
                messagebox.showerror("Password Error", "Incorrect Password!")
                self.counter = self.counter - 1
                self.getpass()
            else:
                messagebox.showerror("Password Error", "Try Again!!")
                return
#------------------------------------------------------------------------------------------

#Change password (If the password was already set once) -----------------------------------
    def changepass(self):
        if(self.bt2.instate(['active'])):
            messagebox.showerror("Password Error", "Set password first!")
        else:
            self.checkit = askstring('Password', 'Enter old password:', show="*")
            f3 = open(self.Password_address,'r')
            self.checktext = f3.read()
            if(self.checkit==self.checktext):
                self.newpass = askstring('New Password', 'Enter password:', show="*")
                f4 = open(self.Password_address,'w')
                f4.write(self.newpass)
                f4.close()
                messagebox.showinfo("Password Set", "Your new password has been set!")
            else:
                messagebox.showerror("Password Error", "Incorrect Password!")
                return
        
#-----------------------------------------------------------------------------------------
        
    
#Select a folder to hide------------------------------------------------------------------        
    
    def browseit(self):
        self.folder_selected = filedialog.askdirectory()
        if len(os.listdir(self.folder_selected) ) == 0:
            messagebox.showerror("Empty Folder", "You selected folder is empty, try again!")
            return
        if(self.folder_selected != ""):
            self.str1 = self.folder_selected[self.folder_selected.rindex("/")+1:]
            self.strspaced = self.str1
            self.str2 = self.folder_selected[:self.folder_selected.rindex("/")+1]
            self.str3 = "".join(random.choice('0123456789ABCDEF') for i in range(4))
            if(self.str1.find(" ")!=-1):
                self.str1 = self.str1.replace(" ","_")

            os.chdir(self.str2)
            self.encryptFile(self.str1,self.str2,self.folder_selected)
            self.strkey = str.encode(self.strkey)
            self.str4 = self.str2 + "," + self.str1 + ',' + self.str3 + ',' +self.strkey.decode('UTF-8')+'\n'
            f2 = open(self.Folders_address,'a')
            f2.write(self.str4)
            f2.close()
            print(os.getcwd());

            os.chdir(self.str2)
            print(os.getcwd(),self.str2,self.folder_selected,sep = "\n");
            os.system('ren '+self.str1+'.zip'+self.default+self.str3+'}\"  ')
            os.system('attrib +h +s'+self.default+self.str3+'}\"')
            self.lb1.insert(END,self.str1)
            os.chdir(self.cwd)

#-------------------------------------------------------------------------------------------


#Encrypt the zipped folder------------------------------------------------------------------
        
    def encryptFile(self,name,path,fileloc):
            if(os.path.isdir(fileloc)):
                shutil.make_archive(name,"zip",fileloc)
                shutil.rmtree(fileloc)
                key = Fernet.generate_key()
                self.strkey = key.decode('UTF-8')
                fernet = Fernet(key)
          
                # opening the original file to encrypt
                with open(name+'.zip', 'rb') as file:
                    original = file.read()
          
                # encrypting the file
                encrypted = fernet.encrypt(original)
          
                # opening the file in write mode and 
                # writing the encrypted data
                with open(name+'.zip', 'wb') as encrypted_file:
                    encrypted_file.write(encrypted)
#-------------------------------------------------------------------------------------------


#Decrypt the zipped folder------------------------------------------------------------------        
        
    def decryptFile(self,name,fileloc,key):
        fernet = Fernet(key)
        # opening the encrypted file
        with open(name+'.zip', 'rb') as enc_file:
            print(name+'.zip')
            encrypted = enc_file.read()
      
        # decrypting the file
        decrypted = fernet.decrypt(encrypted)
      
        # opening the file in write mode and
        # writing the decrypted data
        with open(name+'.zip', 'wb') as dec_file:
            dec_file.write(decrypted)
    
        shutil.unpack_archive(name+'.zip',fileloc,"zip")
        os.remove(name+'.zip')
#-------------------------------------------------------------------------------------------

#Iterate through each selection in the folders list ----------------------------------------
        
    def restore(self):
        for i in self.lb1.curselection():
            print(i,self.lb1.get(i))
            self.lblist.append(self.lb1.get(i))
            
        for i in self.lblist:
            self.getting(i)
            self.lb1.delete(self.lb1.get(0, tk.END).index(i))
            
        self.lblist = []
#-------------------------------------------------------------------------------------------


#Restore the unlocked folder back to its original location --------------------------------- 
            
    def revbrowseit(self,folder_name):
        f3 = open(self.Folders_address,"r")
        for x in f3:
            if(x.split(',')[1] == folder_name):
                self.str10 = x.split(',')[0]
                self.str11 = x.split(',')[1]
                self.str12 = x.split(',')[2]
                self.str13 = x.split(',')[3].rstrip('\n')
                self.str13 = str.encode(self.str13)
        os.chdir(self.str10)
        os.system('attrib -h -s'+self.default+self.str12+'}\"')
        os.system('ren '+self.default+self.str12+'}\" '+ self.str11+'.zip')
        
        print(self.str11,self.str10+self.str11+'/',self.str13)
        self.str14 = self.str10+self.str11+'/'
        print(self.str14)
        self.str14 = self.str14.replace("/","\\\\")
        print(self.str14)
        self.decryptFile(self.str11,self.str14,self.str13)
        f3.close()
        if(self.strspaced.find(" ")!=-1):
            self.renamed_folder = self.str11.replace("_"," ")
            os.system('ren '+self.str11+' \"'+self.renamed_folder+'\"')
        else:
            self.renamed_folder = self.str11
        messagebox.showinfo("Folder Restored", self.renamed_folder+' has been restored to '+self.str10)
        os.chdir(self.cwd)

#-------------------------------------------------------------------------------------------

#Once folder is restored, remove them from the hidden list(update folder list) -------------    
    def getting(self,folder_name):
        self.revbrowseit(folder_name)
        f3 = open(self.Folders_address,"r")
        lis1 = []
        for x in f3:
            if(x.split(',')[1] != folder_name):
                lis1.append(x)
        f3.close()
        print(lis1)
        f3 = open(self.Folders_address,"w")
        f3.close()
        f3 = open(self.Folders_address,"a")
        for i in lis1:
            f3.write(i)
        f3.close()
#-------------------------------------------------------------------------------------------        
  
#Set password (only for the first time)-----------------------------------------------------       
    def setpass(self):
        self.password = askstring('Password', 'Enter password:', show="*")
        f = open(self.Password_address, 'w')
        f.write(self.password)
        f.close()
        print(type(self.bt2))
        if os.stat(self.Password_address).st_size != 0:
            self.bt2.state(['disabled'])
        return

#-------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app = App()
    app.mainloop()