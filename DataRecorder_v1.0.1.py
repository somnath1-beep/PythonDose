import shelve as sh, re,os
import tkinter as tk
from tkinter import messagebox,simpledialog
#match pattern for password validation

def file_operation(file,u_keys=None,u_values=None,mode=None):#if you have to write pass keys and values list and file path
    # else for read pass file path and mode
    if mode=='r'or mode=='r+':
        if os.path.exists(file):
            fileobj=open(file,f'{mode}')
            keys=[]
            values=[]
            for file_line in fileobj.readlines():
                line_data=file_line.strip().split(':')
                keys.append(line_data[0])
                values.append(line_data[1])  
            fileobj.close()           
            return keys, values#return list of keys and values from file
        else:
            return 'Invalid Path!'
    elif mode=='a' or mode==None or mode=='w+':
        fileobj=open(file,f'{mode}')
        for i in range(0,len(u_keys)):
            fileobj.write(f'{u_keys[i]}:{u_values[i]}\n')
        fileobj.close()
        return 'success'#for writting completition


def filehandler(name,search=None,status='create'):#make folder and search path return file path and true /false
    if search==None and status=='create':# for new file, make folder and return path of file
        folder=os.path.join('c:\\','Datarecorder',f'info_{name}')
        os.makedirs(folder)
        file=os.path.join(folder,f'{name}.txt')
        return file
    elif search==None and status!='create': # for update or view . return file path
        file=os.path.join('c:\\','Datarecorder',f'info_{name}',f'{name}.txt')
        return file
    elif search=='searching':# for search any file associated with given name and return true /false if found or not
        file=os.path.join('c:\\','Datarecorder',f'info_{name}',f'{name}.txt')
        #folder=os.path.join('c:\\','Datarecorder',f'info_{name}')
        search_result=os.path.exists(file)  
        return search_result
    

password_pattern=re.compile(r'''\w+\d+[!@#$%^&*()_+{}":;\']+\w+\d+|\d+\w+[!@#$%^&*()_+{}":;\']+\w+\d+
                            \w+[!@#$%^&*()_+{}":;\']+\w+\d+|\w+\d+[!@#$%^&*()_+{}":;\']+\d+|
                            \w+\d+[!@#$%^&*()_+{}":;\']+\w+|[!@#$%^&*()_+{}":;\']+\w+\d+|[!@#$%^&*()_+{}":;\']+\d+\w+|
                            \d+[!@#$%^&*()_+{}":;\']+\w+\d+|[!@#$%^&*()_+{}":;\']+\w+\d+|\d+[!@#$%^&*()_+{}":;\']+\w+\d+|
                            \\d+\w+[!@#$%^&*()_+{}":;\']+\d+\w+''')# to valdiate password that contain at least one alphabet, one digit, and one special character.

#validate password function
def validate_password(password):
        if(len(password)<8):# for insufficient length
                verification_message="Password must be at least 8 character"
                return verification_message,0
                
        password_match=password_pattern.findall(password)
        if password_match!=[]:# if password validate successfully
                return  'Password Verified',1
        else:
            verification_message="Password must contain at least one alphabet, one digit, and one special character."
            return verification_message,0
        
        
#check if file exists and update or view information
def update_info(name,password):# to add or delete data from /in file
    filepath=filehandler(name,status='update')#return file path
    ret=file_operation(filepath,mode='r')#return keys and values from file in tuple
    if ret=='Invalid Path!':
        messagebox.showerror("File Search",f"{ret}")
        return
    filekeys=ret[0]# accessing list from tuple
    filevalues=ret[1] # accessing list from tuple 
    if filevalues[0]==password:#matching password
        modification_choice=simpledialog.askfloat(" File Modification",'''
                                                    1.Delete Data
                                                    2.Add Data''')
        if modification_choice==1:
            delete_key=information=simpledialog.askstring("Delete keys","Enter Keys to be deleted:",parent=root).split(",")#get list of keys to be deleted by user
            InvalidKeys=[]# for keys that not found in file given by user to delete
            for i in delete_key:
                if i in filekeys:
                    index=filekeys.index(i)
                    del filekeys[index]
                    del filevalues[index]
                else:
                    InvalidKeys.append(i)#appending  key not found
            file_operation(filepath,u_keys=filekeys,u_values=filevalues,mode='w+')
            messagebox.showinfo("Delete Keys","Deletion successful!")
            if InvalidKeys!=[]:# show key that not found 
                messagebox.showwarning("Delete Keys",f"Keys Not Found:{InvalidKeys}")
            return
        else:#adding data
            userkeys=simpledialog.askstring("Enter category","e.g., name,address,age",parent=root).split(",")
            uservalues=[]
            for i in range(0,len(userkeys)):
                info=simpledialog.askstring("Enter Your Details",f"Enter your {userkeys[i]}: ",parent=root)
                uservalues.append(info)# values appended give by user
            file_operation(filepath,u_keys=userkeys,u_values=uservalues,mode='a')
            messagebox.showinfo("File Modification","File Modified!")
            return
    else:
        messagebox.showerror("Password Verification","Wrong Password!")
        return        
    
def view_info(name,password):# display your saved information in the file
    filepath=filehandler(name,status='view')
    ret=file_operation(filepath,mode='r')#return keys and values or Invalid Path!
    if ret=='Invalid Path!':
        messagebox.showerror("File Search",f"{ret}")
        return
    filekeys=ret[0]
    filevalues=ret[1]    
    if filevalues[0]==password:
        out=output_widget()
        for i in range(1,len(filekeys)):
            out.insert(tk.END,f"{filekeys[i]}:{filevalues[i]}\n")# displaying output in window
    
    else:
        messagebox.showerror("Password Verification","Wrong Password!")
        return
    return

def new_info(name,password):# create a new file and save your information in it
    filepath=filehandler(name)
    fileobj=open(filepath,'w')
    fileobj.write(f'_file_password:{password}\n')
    fileobj.close()
    userkeys=simpledialog.askstring("Enter category","e.g., name,address,age",parent=root).split(",")
    uservalues=[]
    for i in range(0,len(userkeys)):
        info=simpledialog.askstring("Enter Your Details",f"Enter your {userkeys[i]}: ",parent=root)
        uservalues.append(info)# values appended give by user
    file_operation(filepath,u_keys=userkeys,u_values=uservalues,mode='a')
    messagebox.showinfo("Create","File Created Successfully!")
    return

def backend(Name=None, password=None):
    name=Name.lower()
    
    password_result=validate_password(password)#rreturn tupple with message and 1/0 1-> success
    if password_result[1]==0:
         messagebox.showinfo("Password Verification",password_result[0])
         return
    option=int(simpledialog.askfloat("Select OPtion",''' 
1.for new file
2.for update file 
3.for view info''',parent=root))
    if option==1:
         if(filehandler(name,'searching')):
              replace=simpledialog.askfloat("File Searching","""File Already Exist!
                                            Do you want to Replace file
                                            Enter 1 for yes 0 for no
                                            """)
              if replace==1:
                   os.remove(f'{name}') 
                   new_info(name,password)
              else:
                   return  
         new_info(name,password)
         
    elif option==2:
         if filehandler(name,'searching'):
            update_info(name,password)
         else: 
            messagebox.showerror("File Searching","File not found!")
            return
    elif  option==3 :
         if filehandler(name,'searching'):
             view_info(name,password)
         else: 
            messagebox.showerror("File Searching","File not found!")
            return
        
    
def name_widget():
    global name_entry
    namelbl=tk.Label(root,text="Enter your Name:")
    namelbl.pack(pady=10)
    name_entry=tk.Entry(root,width=40,bg="cyan",fg="black")
    name_entry.pack(pady=10)

def password_widget():
    global  password_entry
    passwordlbl=tk.Label(root,text="Password:")
    passwordlbl.pack(pady=10)
    password_entry=tk.Entry(root,width=40, show="*", bg='cyan')
    password_entry.pack(pady=10)

def clean_widget():
    for widget in root.winfo_children():
        widget.destroy()


def send_btn(function, head):
    global submit_button
    submit_btn=tk.Button(root,text=head, command=function)
    submit_btn.pack(pady=10)

def getinfo():
    global name, password
    name=name_entry.get()
    password=password_entry.get()
    backend(name,password)
    name_entry.delete(0,tk.END)
    password_entry.delete(0,tk.END)

   
    

def password_validate_widget():
    clean_widget()
    name_widget()
    password_widget()
def output_widget():
    global output
    outputlbl=tk.Label(root,text="Output:")
    outputlbl.pack(pady=10)
    output=tk.Text(root, width=50, height=100,bg='cyan',fg='black')
    output.pack(pady=10)
    return output


def main_interface():
    clean_widget()
    name_widget()
    password_widget()
    send_btn(getinfo,"ok")
    send_btn(main_interface,"clear screeen")
root=tk.Tk()
root.title("Information Recorder")
root.geometry("500x500")
main_interface()
root.mainloop()

    

#create / make name and password global 
