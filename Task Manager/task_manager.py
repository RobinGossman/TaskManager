import os

from datetime import datetime


# below i defined functions for modularity

# reg user defined to write the new user details

def reg_user(newname, newpassword):
        with open('user.txt', 'a') as f:
                   f.write(newname+","+" "+newpassword+"\n")
                   
        f.close()
        
        
# add task defined to take in various variables of the task details and write it to the task.txt

def add_task(user_name, task_title, task_details, date_assign, task_due, task_prog):
        task=(user_name+","+" "+task_title+","+" "+task_details+","+" "+date_assign+","+" "+task_due+","+" "+task_prog)
        with open('tasks.txt','a') as a:
                a.write(f"{task}\n") 

        a.close()


# i defined view all to prinnt the tasks from eacg line in the txt file

def view_all():
        with open('tasks.txt', 'r+') as f:
            line=f.readlines()
            i=0
            for lines in line:
                    i=i+1
                    print(str(i)+"."+lines)
                    
        f.close()


# below is the code for the view mine function

def view_mine(username):
        usertask=[]
        i=0
        
        with open('tasks.txt')as ofile:
                lines = ofile.read().splitlines()
                
        for row, line in enumerate(lines):
                assigned_to, *rest = line.split(", ")
                if username == assigned_to:
                        task_dict={k: v for k,  v in zip(
                                ('number', 'row', 'assigned_to', 'title', 'description', 
                                 'due_date', 'date_assigned', 'completed'),
                                (i + 1, row, assigned_to, *rest))}
                        usertask.append(task_dict)
                        i+=1
                        
        ofile.close()
        
        task_number = int(input("Enter task number you would like edit:"))
        task = usertask[task_number -1]
        task_input = input(f"""Please Select 1 of the following options\n
 m - mark task as complete
 e - edit the task
-1 - for main menu:""")
        
        if task_input == "e":
                if task['completed']=='no':
                        e_input =input(f"""what would you like to edit:
u - username
d - due date\n""")                   

                        if e_input == "u":
                                       task['assigned_to'] = input("Please enter username:")
                        if e_input == "d":
                                       task['due_date'] = input("Enter new due date:")                                

        if task_input == "m": 
                task['completed']=input("Enter yes or no whether the task has been completed:")                       
                                       
        if task_input == "-1":
                user_menu()                        
                 
        row_app = [task['row'] for task in usertask]
        with open ('tasks.txt') as out_put, open('temp.txt', 'w') as te_mp:
                
                for row, line in enumerate (out_put):
                        if row in row_app:
                                row_app.remove(row)
                                print(', '.join(v for k, v in list(usertask.pop(0).items())[2:]), file=te_mp)                                              
                        else:
                                print(line.strip(), file=te_mp)
                                

# to create task overview files i created dictionaries and list from the task and user files
# i then did counts and various calculations to get percentages before writing to user and task overview
                                
def generate_reports():
# task_overview        
        usertask=[]
        i=0
        with open('tasks.txt')as ofile:
                lines = ofile.read().splitlines()
        for row, line in enumerate(lines):
                assigned_to, *rest = line.split(", ")
                task_dict={k: v for k,  v in zip(
                        ('number', 'row', 'assigned_to', 'title', 'description', 
                         'due_date', 'date_assigned', 'completed'),
                        (i + 1, row, assigned_to, *rest))}
                usertask.append(task_dict)
                i+=1        
       
        task_complete = 0
        task_uncomplete = 0
        task_overdue = 0
        for count in usertask:
                        task=count
                        if task['completed'] == 'Yes':
                                task_complete += 1               
                        elif task['completed'] == 'No':
                                task_uncomplete +=1
                        datetime_object = datetime.strptime(task['due_date'], '%d %B %Y')
                        if datetime_object < datetime.today() and 'No' == task['completed']: 
                                task_overdue += 1

        percentage_incomplete = (task_uncomplete * 100)/(len(usertask))
        percentage_overdue = (task_overdue * 100)/(len(usertask))

        with open('task_overview.txt', 'w', encoding='utf-8') as task_overview:
                task_overview.write(f"Total number of tasks generated using Task Manager: {len(usertask)}\n")
                task_overview.write(f"Number of completed tasks: {task_complete}\n")
                task_overview.write(f"Number of uncompleted tasks: {task_uncomplete}\n")
                task_overview.write(f"Number of uncompleted tasks that are overdue: {task_overdue:.0f}\n")
                task_overview.write(f"Percentage of uncompleted tasks: {percentage_incomplete:.0f}%\n")
                task_overview.write(f"Percentage of uncompleted overdue tasks: {percentage_overdue:.0f}%\n")
    
# user_overview

        userpass = []
        i = 0
        with open('user.txt')as user_info:
                lines = user_info.read().splitlines()
                
        for row, line in enumerate(lines):
                users, *rest = line.split(", ")
                user_dict={k: v for k,  v in zip(
                        ('number', 'row', 'users', 'passwords'),
                        (i + 1, row, users, *rest))}
                userpass.append(task_dict)
                i+=1

        total_user=len(userpass)
        total_task=len(usertask)

        user_dets=input("Enter a username to write details to user overview:")
        userTasks = 0
        usertasks_overdue = 0
        for i in usertask:
                task=i
                if user_dets == task['assigned_to']:
                        userTasks += 1
                datetime_object = datetime.strptime(task['due_date'], '%d %B %Y')
                if user_dets == task['assigned_to'] and datetime_object < datetime.today() and 'No' == task['completed']: 
                        usertasks_overdue += 1

        usertask=[]
        task_num=0
        file = open ('tasks.txt', 'r+')
        lines = file.readlines()
        user_complete = 0
        user_incomplete = 0
        for i in lines:
            task = i.replace(" ","")
            task = i.replace("\n", "")
            task = i.split(",")
            task_num +=1
            usertask.append(task_num)
            if user_dets in task[0] and 'Yes' in task[5]:
                    user_complete += 1               
            if user_dets in task[0] and "No" in task[5]:
                    user_incomplete += 1

        
        total_percent = userTasks/(len(usertask))*100
        total_overdue = (usertasks_overdue/userTasks)*100
        total_complete = (user_complete/userTasks)*100
        total_incomplete =(user_incomplete/userTasks)*100
               
        
        with open('user_overview.txt', 'w', encoding='utf-8') as user_overview:
                user_overview.write(f"The total number of users register with Task Manager: {len(userpass)}\n")
                user_overview.write(f"The total number of tasks that have been generated with the Task Manager: {total_task}\n")
                user_overview.write(f"The total number of task assigned to {user_dets}: {userTasks}\n")
                user_overview.write(f"The percentage of tasks assigned to {user_dets}: {total_percent:.0f}%\n")
                user_overview.write(f"Percentage of completed tasks assigned to {user_dets}: {total_complete:.0f}%\n")
                user_overview.write(f"Percentage of uncompleted tasks assigned to {user_dets}: {total_incomplete:.0f}%\n")
                user_overview.write(f"Percentage of uncompleted tasks that are over due assigned to {user_dets}:{total_overdue:.0f}%\n")
                print("Task_overview.txt and user_overview.txt have been generated.\n")         
                
# defined statistics to print the 2 files 

def statistics():
        print("THE STATISTICS FROM TASK OVERVIEW ARE AS FOLLOWS: \n")
        
        with open('task_overview.txt', 'r+') as f:
            line=f.readlines()
            i=0
            for lines in line:
                    i=i+1
                    print(str(i)+"."+lines)

        print("THE STATISTICS FROM USER OVERVIEW ARE AS FOLLOWS: \n")
        
        with open('user_overview.txt', 'r+') as f:
            line=f.readlines()
            i=0
            for lines in line:
                    i=i+1
                    print(str(i)+"."+lines)

# i then created the menu option and made sure that the username admin had the more advanced menu
                
def user_menu():
        if username == "admin":
                print("Please select one of the following options\n")
                print("r - register user")
                print("a - add task")
                print("va - view all tasks")
                print("vm - view my tasks")
                print("gr - generate reports")
                print("st - statistics")
                print("e - exit")
        else:
                print("Please select one of the following options\n")
                print("a - add task")
                print("va - view all tasks")
                print("vm - view my tasks")
                print("e - exit")
        
       


# i started the program by focusing on getting the program to be accessed using a username and password
# using the data from the users.txt file

# below i created 2 lists so that i could focus on seperating the password from the username and store them in seperate lists

username_list=[]
password_list=[]

# i usedn the with open function to open users.txt for reading and stored it in a variable called ufile
# i then used a for loop with a indexed variable called space to replace space with no space
# and then replacing a new line with no space
# i then split the indexed variable using the comma between the passwords and usernames
# i then used indexing and stored the password which was 1 and the usernames which was and stored them in new variables
# i then appended both lists


with open('user.txt', 'r+') as ufile:
        for space in ufile:
                space=space.replace(" ","")
                space=space.replace("\n","")
                space=space.split(",")
                user=space[0]
                pass_word=space[-1]
                username_list.append(user)
                password_list.append(pass_word)

# below i created 2 inputs for users to put in name and password                

username=input("Enter your username:")
password=input("Enter your password:")

# below i created 2 variables below for login and stored a value of 0 in both

i = 0
login = 0

# i then created a while loop stating i which is 0 was greater then the username_list
# i then used conditionals within the loop so that if the username and password was equal to the list of username and passwords
# login becomes 1 and they would get access
# i then created an indented if statement within the previous if statement
# if user equals to admin they would get a different list of options from the other users

while i < len(username_list):
        if username == str(username_list[i]) and password==str(password_list[i]):
                login=1
# below if username and password was incorrect it would loop until they entered the correct username and password
        i+=1        
        if i==len(username_list) and login == 0:
                print("Your Username or password is incorrect please try again")
                username=input("Enter your username:")
                password=input("Enter your password:")
                i=0

 
# to loop the menu i used a while loop with if elif else conditionals

user_menu()
user_select = 0
while True:
        user_select= input("Select an option:").lower()
        
        if user_select == "r":
                check_username=[]
                check_file = open ('user.txt', 'r')
                check=check_file.readlines
                for space in check_file:
                        space=space.replace(" ","")
                        space=space.replace("\n","")
                        space=space.split(",")
                        user=space[0]
                        check_username.append(user)
                        
                newname=input("Enter a username:").lower()        
                reg = 0
                i = 0
                while i == 0 and reg == 0:
                        if newname in check_username :
                                print("The username already exists, please try again.")
                                newname=input("Enter a username:").lower()
                                i = 0
                        else:
                                reg = 1
                                
                newpassword=input("Enter a password:")
                confirm_pass=input("Please re_enter password:")
                while confirm_pass != newpassword:
                        print("The passwords you have entered do not match, please try again.")
                        newpassword=input("Enter a password:")
                        confirm_pass=input("Please re_enter password:")
                
                reg_user(newname, newpassword)
                print("Username and Password Registered Successfully")
                user_menu()
            

# below if user wants to add a task i used various input statements to get details about the task they are adding
# then i used with open to open tasks.txt before writing all the details in the txt. file same way the previous tasks were written

        elif user_select == "a":
            check_name = []    
            with open('user.txt', 'r+') as check_user:
                for check in check_user:
                        check=check.replace(" ","")
                        check=check.replace("\n","")
                        check=check.split(",")
                        user=check[0]
                        check_name.append(user)
            
            user_name=input("Enter the username for task assignment:").lower()
            for i in check_name:
                    if user_name in check_name:
                            task_title=input("Enter the title of the task:")
                            task_details=input("Enter a description of the task:")
                            date_assign=input("Enter the date the task was assigned:")
                            task_due=input("Enter a due date:")
                            task_prog=input("Has the task been completed yes or no?:")
                            
                    if user_name != check_name:
                            user_name=input("The username you have entered does not exist, try again:").lower()                     
                   
            add_task(user_name, task_title, task_details, date_assign, task_due, task_prog)
            
            print("Task assigned successfully")
            
            user_menu()
                
 
# to view all tasks i created a empty string called contents
# i then used with open tasks.txt for reading before using a for loop to store txt files data in the empty string

        elif user_select == "va":
            view_all()
            user_menu()
# to view my task option
# i created a empty list to store tasks numbers called usertask
# i then stored 0 in a variable called task_num
# i then opened the txt file tasks before using the readlines function and storing it in a variable called lines
# i then used a for loop with a indexed varible called i before using the replace function to replace space with no space and then a new line with no space
# i then used the split function on the comma 
# i then appended the list of task numbers
# before using a conditional to print the specific users task

        elif user_select == "vm":
                usertask=[]
                task_num=0
                file = open ('tasks.txt', 'r+')
                lines = file.readlines()
                for i in lines:
                    task = i.replace(" ","")
                    task = i.replace("\n", "")
                    task = i.split(",")
                    task_num +=1
                    usertask.append(task_num)
                    if username == task[0]:
                                    sentence = (f"""
                                             Task Number     : {task_num}
                                             Task assigned to: {task[0]}
                                             Task title      : {task[1]}
                                             Task descrition : {task[2]}
                                             Due Date        : {task[3]}
                                             Date Assigned   : {task[4]}
                                             Completed       : {task[5]}\n""")
                                    print(sentence) 
                file.close()
                view_mine(username)
                os.remove('tasks.txt')
                os.rename('temp.txt', 'tasks.txt')
                
# menu option gr i use generate reports function

        elif user_select == "gr":
                generate_reports()
                user_menu()

# for statistics i used input to make sure user has alreadt generated the files before using conditions to select which menu option user should get

        elif user_select == "st":
                call=input("Please enter yes or no, whether you've generated Task and User Overview files for viewing:").lower()
                if call == "no":
                        generate_reports()
                        
                else:   
                        statistics()           

                user_menu()
                
# below i used a print statement to exit out of program        
   
        elif user_select == "e": 
            print("You've selected exit, Thank you.")
            break

        else:
                user_menu()




          
    
