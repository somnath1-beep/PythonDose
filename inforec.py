import shelve as sh, re,os

def validate_password():
    password_pattern=re.compile(r'''\w+\d+[!@#$%^&*()_+{}":;\']+\w+\d+|\d+\w+[!@#$%^&*()_+{}":;\']+\w+\d+
                            \w+[!@#$%^&*()_+{}":;\']+\w+\d+|\w+\d+[!@#$%^&*()_+{}":;\']+\d+|
                            \w+\d+[!@#$%^&*()_+{}":;\']+\w+|[!@#$%^&*()_+{}":;\']+\w+\d+|[!@#$%^&*()_+{}":;\']+\d+\w+|
                            \d+[!@#$%^&*()_+{}":;\']+\w+\d+|[!@#$%^&*()_+{}":;\']+\w+\d+|\d+[!@#$%^&*()_+{}":;\']+\w+\d+|
                            \\d+\w+[!@#$%^&*()_+{}":;\']+\d+\w+''')
    print(''' Password must be at least 8 characters long and 
            contain at least one uppercase letter, one lowercase letter, one digit, and one special character.''')
 
    for i in range(3):    
        password=input("Enter your password: ")
        if(len(password)<8):
            print("Password must be at least 8 characters long.")
            continue
            
        password_match=password_pattern.findall(password)
        if password_match!=[]:
            print("Password saved successfully !")
            return password
        else:
            print("Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
            continue
    return None
    

def update_info(name):
    fileobj=sh.open(f'{name}.db', 'w')
    password=input("Enter your password to update your information: ")
    if password==fileobj['password']:
        print("Password verified. You can now update your information.")
        information=input ("Enter what you want to update e.g., age, address, etc.: ").split(',')
        catogory=list(information)
        rec=[]
        for i in range(len(catogory)):
            catogory[i]=input(f"Enter your new {catogory[i]}: ")
            rec.append(catogory[i])
        
        for i in range (len(catogory)):
            fileobj[catogory[i]]=rec[i]
        print(f"Your information has been updated in {name}.db file.")
    else:
        print("Incorrect password. You cannot update your information.")
    fileobj.close()
def view_info(name):
    fileobj=sh.open(f'{name}.db')
    password=input("Enter your password to view your information: ")
    if password==fileobj['password']:
        print(f"Hello {name}, your information is as follows:")
        for key in fileobj.keys():
            if key != 'password':
                print(f"{key}: {fileobj[key]}")
    else:
        print("Incorrect password. You cannot view your information.")
    fileobj.close()
def new_info(name):
    fileobj=sh.open(f'{name}.db')
    print("Create a password for your file.")
    password=validate_password()
    if password is None:
        print("Failed to create a valid password. Exiting.")
        fileobj.close()
        os.remove(f'{name}.db')  # Remove the file if password creation failed
        return
    else:
        fileobj['password']=password
        print("Password saved successfully!")
    
    information=input ("Enter what you want to add e.g., age, address, etc.: ").split(',')
    catogory=list(information)
    rec=[]
    for i in range(len(catogory)):
        catogory[i]=input(f"Enter your {catogory[i]}: ")
        rec.append(catogory[i])
    print(f"Hello {name}, your information has been recorded.")
        
        
    for i in range (len(catogory)):
        fileobj[catogory[i]]=rec[i]
    print(f"Your information has been saved in {name}.db file.")

    print("Do you want to see your information? press 1 for yes and 0 for no")
    see_info=int(input())
    if see_info==1:
        for i in range(len(catogory)):
            print(f"{catogory[i]}: {fileobj[catogory[i]]}")
    fileobj.close()
      
        


Name=input("Enter your file name: ")
name=Name.lower()
if(os.path.exists(f'{name}.db')):
    print(f'''Hello {name}, file already exists. 
          Do you want to update your file or view it?
          press 1 for update and 0 for view''')
    choice=int(input())
    if choice==1:
        os.system('cls' if os.name == 'nt' else 'clear')
        update_info(name)
    elif choice==0:
        os.system('cls' if os.name == 'nt' else 'clear')
        view_info(name)

else:
    print (f"Hello {name}, file does not exist. Do you want to create a new file? press 1 for yes and 0 for no")
    choice=int(input())
    if choice==1:
        os.system('cls' if os.name == 'nt' else 'clear')
        new_info(name)
    else:
        print("Thank you for using our service. Goodbye!")
    

