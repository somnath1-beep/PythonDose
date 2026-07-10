import shelve as sh, re,os
import tkinter as tk
from tkinter import messagebox,simpledialog 
import base64 # to convert binary data to scramble object 
#match pattern for password validation
#to decode Base64 structure into bytes then string
def text_manipulate(scramble_obj):
    #Decode the Base64 structure back to standard bytes
    decoded_key_bytes = base64.b64decode(scramble_obj)
    # decode bytes to original string
    final_key = decoded_key_bytes.decode('utf-8')
    return final_key
def file_operation(file,u_keys=None,u_values=None,mode=None):#if you have to write pass keys and values list and file path
    # else for read pass file path and mode
    if mode=='r'or mode=='r+':
        if os.path.exists(file):
            fileobj=open(file,f'{mode}')
            keys=[]
            values=[]
            for file_line in fileobj.readlines():
                line_data=file_line.strip().split(':')
                scramble_key=line_data[0].strip('"').lstrip('b')# scramble obj contain "b'X2luZm9fcGFzc3dvcmQ='" like format
                # that's why i stripped " from both side and then b other "b'X2luZm9fcGFzc3dvcmQ='" can't be decoded by utf-8 sceme
                scramble_value=line_data[1].strip('"').lstrip('b')
                final_key=text_manipulate(scramble_key)
                final_value=text_manipulate(scramble_value)
                keys.append(final_key)
                values.append(final_value)
            fileobj.close()           
            return keys, values#return list of keys and values from file
        else:
            return 'Invalid Path!'
    elif mode=='a' or mode==None or mode=='w+':# binary mode 
        fileobj=open(file,f'{mode}')
        for i in range(0,len(u_keys)):
            binary_u_keys=u_keys[i].encode("utf-8")#encoding in binary
            binary_u_values=u_values[i].encode("utf-8")
            scramble_binary_u_keys=base64.b64encode(binary_u_keys)#encoding in scramble obj
            scramble_binary_u_values=base64.b64encode(binary_u_values)
            fileobj.write(f'{scramble_binary_u_keys}:{scramble_binary_u_values}\n')
        fileobj.close()
        return 'success'#for writting completition


def filehandler(name,search=None,status='create'):#make folder and search path return file path and true /false
    if search==None and status=='create':# for new file, make folder and return path of file
        folder=os.path.join('c:\\','MyRecords',f'info_{name}')
        file=os.path.join(folder,f'{name}.txt')# .dat -> generic data
        if os.path.exists(folder):
            return file
        else:
            os.makedirs(folder)
            return file
    elif search==None and status!='create': # for update or view . return file path
        file=os.path.join('c:\\','MyRecords',f'info_{name}',f'{name}.txt')
        return file
    elif search=='searching':# for search any file associated with given name and return true /false if found or not
        file=os.path.join('c:\\','MyRecords',f'info_{name}',f'{name}.txt')
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
        modification_choice=simpledialog.askinteger(" File Modification",'''
                                                    1.Delete Data     
                                                    2.Add Data          ''',parent=root)
        if modification_choice==1:
            try:
                delete_key=information=simpledialog.askstring("Delete keys","Enter Keys to be deleted:              ",parent=root).split(",")#get list of keys to be deleted by user
            except:
                return
            InvalidKeys=[]# for keys that not found in file given by user to delete
            delflag=0
            
            for i in delete_key:
                if i in filekeys:
                    delflag=1
                    key_frequency=filekeys.count(i)
                    for j in range(key_frequency):
                        index=filekeys.index(i)
                        del filekeys[index]
                        del filevalues[index]
                else:
                    InvalidKeys.append(i)#appending  key not found
            file_operation(filepath,u_keys=filekeys,u_values=filevalues,mode='w+')
            if delflag==1:
                messagebox.showinfo("Delete Keys"," Valid Key Deleted successfull!")
            if InvalidKeys!=[]:# show key that not found 
                messagebox.showwarning("Delete Keys",f"Keys Not Found:{InvalidKeys}")                           
            
        elif modification_choice==2:#adding data
            messagebox.showinfo("Enter category","Don't use ':' with category or as a category",parent=root)
            flag=0
            while True:
                try:
                    userkeys=simpledialog.askstring("Enter category","e.g., name,address,age:               ",parent=root).split(",")
                except:
                    return
                for i in  userkeys:
                    if ':' in i:
                        messagebox.showwarning("Enter category","Don't use':' anywhere!",parent=root)
                        flag=1
                        break
                if flag==0:
                    if userkeys==[''] :
                        messagebox.showwarning("Enter category","Invalid category",parent=root)
                        continue
                    uservalues=[]
                    for i in range(0,len(userkeys)):
                        info=simpledialog.askstring("Enter Your Details",f"Enter your {userkeys[i]}:                ",parent=root)
                        if info == None:
                            return
                        elif ':'in info:
                            messagebox.showwarning("Enter category","Don't use':' anywhere!",parent=root)
                            info=simpledialog.askstring("Enter Your Details",f"Enter your {userkeys[i]}:                ",parent=root)
                            
                        uservalues.append(info)# values appended given by user
                    file_operation(filepath,u_keys=userkeys,u_values=uservalues,mode='a')
                    messagebox.showinfo("File Modification","File Modified!")
                    return
                elif flag==1:
                    flag=0
                    continue
        elif modification_choice==None:# user cancel
                return
        else:#if user give invalid choice 
            messagebox.showwarning("File Modification","Invalid Choice!")
            del filepath
            del ret
            del filekeys
            del filevalues
            update_info(name,password)
    else:
        messagebox.showerror("Password Verification","Wrong Password!")
        return      
    
def view_info(name,password):# display your saved information in the file
    filepath=filehandler(name,status='view')
    ret=file_operation(filepath,mode='r')#return keys and values or Invalid Path!
    if ret=='Invalid Path!':
        messagebox.showerror("File Search",f"{ret}")
        return
    filekeys=ret[0]#list of keys
    filevalues=ret[1] #list of values  
    if filevalues[0]==password:
        widget=root.winfo_children()
        if len(widget)==8:
            output.delete("1.0",tk.END)
        else:
            output_widget()
        for i in range(1,len(filekeys)):
            output.insert(tk.END,f"{filekeys[i]}:{filevalues[i]}\n")# displaying output in window
    
    else:
        messagebox.showerror("Password Verification","Wrong Password!")
        return
    return

def new_info(name,password):# create a new file and save your information in it
    filepath=filehandler(name)
    file_operation(filepath,u_keys=['_info_password'],u_values=[password],mode='w+')
    messagebox.showinfo("Enter category","Don't use ':' with category or as a category",parent=root)
    flag=0
    while True:
        try:
            userkeys=simpledialog.askstring("Enter category","e.g., name,address,age:               ",parent=root).split(",")
        except:
            os.remove(filepath)
            return
        for i in  userkeys:
            if ':' in i:
                messagebox.showwarning("Enter category","Don't use':' anywhere!",parent=root)
                flag=1
                break
        if flag==0:
            if userkeys==[''] :
                messagebox.showwarning("Enter category","Invalid category",parent=root)
                continue
            uservalues=[]
            for i in range(0,len(userkeys)):
                info=simpledialog.askstring("Enter Your Details",f"Enter your {userkeys[i]}:                ",parent=root)
                if info == None:
                    return
                elif ':'in info:
                    messagebox.showwarning("Enter category","Don't use':' anywhere!",parent=root)
                    info=simpledialog.askstring("Enter Your Details",f"Enter your {userkeys[i]}:                ",parent=root)
                    
                uservalues.append(info)# values appended given by user
            file_operation(filepath,u_keys=userkeys,u_values=uservalues,mode='a')
            messagebox.showinfo("File Modification","File Created successfully!")
            return
        elif flag==1:
            flag=0
            continue

def backend(Name=None, password=None):
    name=Name.lower()
    password_result=validate_password(password)#rreturn tupple with message and 1/0 1-> success
    if password_result[1]==0:# 0 means password doesn't meet criteria
        messagebox.showinfo("Password Verification",password_result[0])
        return
    root.lift()# bring main tkinter window automatically on top of desktop
    root.focus_force()# bring any popup window wiating for input from keyboard in focus
    option=simpledialog.askinteger("Select OPtion",''' 
1.Create File
2.Update File 
3.View File 
4.Delete File            ''',parent=root)
    if option==1: 
        if(filehandler(name,'searching')):
            while True:
                replace=simpledialog.askinteger("Create File","""File Already Exist!
                                                Do you want to Replace file
                                                Enter 1 for yes 0 for no                """,parent=root)
                if replace==1:
                    file=filehandler(name,status='update')
                    os.remove(file) 
                    new_info(name,password)#replace existed file
                    return
                elif replace==0 or replace==None:
                    return
                else:
                    messagebox.showwarning("Create File","Invalid Choice!")
                    continue
        new_info(name,password)# create a new file if file not existed already
        
    elif option==2:
        if filehandler(name,'searching'):
            update_info(name,password)
        else: 
            messagebox.showerror("Create File","File not found!")
            return
    elif  option==3 :
        if filehandler(name,'searching'):
            view_info(name,password)
        else: 
            messagebox.showerror("Create File","File not found!")
            return
    elif option==4 and filehandler(name,search='searching'):
        filepath=filehandler(name,status='view')
        ret=file_operation(filepath,mode='r')#return keys and values or Invalid Path!  
        if ret[1][0]==password:
            os.remove(filepath)
            messagebox.showinfo('Delete File','File Deleted Successfully!')
            return
        else:
            messagebox.showerror("Password Verification","Wrong Password!")
            return
        
    elif filehandler(name,search='searching')==False:
        messagebox.showerror("delete File","File not Found")
        backend(name,password)
    elif option==None:
        return
    else:
        messagebox.showerror("Select OPtion","Invalid Choice!")
        backend(name,password)       
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
    #if user not inputed any onr field then no operation will perfomed
    if name==''or password=='':
        return
    backend(name,password)

def output_widget():
    global output
    outputlbl=tk.Label(root,text="Output:")
    outputlbl.pack(pady=10)
    output=tk.Text(root, width=50, height=100,bg='cyan',fg='black')
    output.pack(pady=10)
    return

def main_interface():
    clean_widget()
    name_widget()
    password_widget()
    send_btn(getinfo,"ok")
    send_btn(main_interface,"Refresh")
root=tk.Tk()
root.title("Information Recorder")
root.geometry("500x500")
main_interface()
root.mainloop()