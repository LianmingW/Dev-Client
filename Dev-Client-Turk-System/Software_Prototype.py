import json, time
import tkinter as tk
import tkinter.scrolledtext as tkst
import datetime
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from textfile_functions import *

LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 8)


class PrototypeApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.user_data = {
            "Account Type:": tk.StringVar(),
            "Username:": tk.StringVar(),
            "Password:": tk.StringVar(),
            "Email:": tk.StringVar(),
            "Address:": tk.StringVar(),
            "Telephone #:": tk.StringVar(),
            "Funds:": tk.StringVar()
        }

        tk.Tk.iconbitmap(self, default="amazon.ico")
        tk.Tk.wm_title(self, "Amazon Turk Project")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit System", command=quit)
        menubar.add_cascade(label="System", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        # Multiple frames to load different scenarios for our app
        self.frames = {}
        # Looping through pages/frames provided and instantiating them
        for F in (StartPage, SignUpPage, ClientLogin, DevLogin, SuperLogin, SuperUserPage):
            # Our starting page / initial screen
            frame = F(container, self)

            # Initializing the start frame to be the startpage
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        # Raises the frame input into the top of the frame
        # Essentially brings the frame into the application view
        frame = self.frames[cont]
        frame.tkraise()


# Our Starting Page, what we want to show upon application launch
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.form_labels = ["Username:", "Password:"]

        label = tk.Label(self, text="Starting Page", font=LARGE_FONT)
        label.place(relx=0.5, rely=0.02, anchor=CENTER)

        signup_button = ttk.Button(self, text="Sign Up",
                                   command=lambda: controller.show_frame(SignUpPage))
        signup_button.pack()
        signup_button.place(relx=1.0, y=0, anchor="ne")

        client_login_button = ttk.Button(self, text="Client Login",
                                         command=lambda: self.controller.show_frame(ClientLogin))
        client_login_button.pack(padx=20, pady=20)
        client_login_button.place(relx=0.7, rely=0.1, anchor=CENTER)
        # self.ClientLogin = ClientLogin(self, parent)
        # self.ClientLogin.printHello()

        dev_login_button = ttk.Button(self, text="Developer Login",
                                      command=lambda: controller.show_frame(DevLogin))
        dev_login_button.pack(padx=20, pady=20)
        dev_login_button.place(relx=0.3, rely=0.1, anchor=CENTER)

        super_login_button = ttk.Button(self, text="SuperUser Login",
                                        command=lambda: controller.show_frame(SuperLogin))
        super_login_button.pack(padx=20, pady=20)
        super_login_button.place(relx=0.5, rely=0.1, anchor=CENTER)

        placeHolder = StringVar(self, value="")
        self.searchBar = Entry(self, textvariable=placeHolder, width=40)
        self.searchBar.place(x=135, y=375, width=450)
        # Some buttons I declare as self if I need to perform actions with that button in another function
        self.searchButton = ttk.Button(self, text="Search", command=lambda: self.replace_listbox_projects())
        self.searchButton.place(x=35, y=370)

        self.listbox = Listbox(self, height=15, width=60, font=LARGE_FONT)
        self.listbox.pack()
        self.listbox.place(x=320, y=550, anchor=CENTER)

        self.listbox.bind("<Double-1>", lambda x: self.list_box_double_clicked())

        # Retrieves a list of all project names and tags associated with it
        projects_name_tags = get_list_of_projecterino()
        # Automatically populating the listbox with all projects in the projects db
        for x in range(len(projects_name_tags)):
            self.listbox.insert(END, projects_name_tags[x])

        # sort the list of clients from ascending projects
        client_most_projects, self.acctype = get_clients_with_most_projects("client")
        client_most_projects = sorted(client_most_projects, key=lambda x: (x[1]))

        placeHolder2 = StringVar(self, value="")
        self.searchBar2 = Entry(self, textvariable=placeHolder2, width=90)
        self.searchBar2.place(x=790, y=375, width=100)
        # Some buttons I declare as self if I need to perform actions with that button in another function
        self.searchButton2 = ttk.Button(self, text="Search", command=lambda: self.replace_listbox_users())
        self.searchButton2.place(x=705, y=370)

        self.listbox2 = Listbox(self, height=15, width=20, font=LARGE_FONT)
        self.listbox2.pack()
        self.listbox2.place(x=800, y=550, anchor=CENTER)
        length = len(client_most_projects)
        for x in range(length - 1, -1, -1):
            self.listbox2.insert(END, client_most_projects[x])

        self.listbox2.bind("<Double-1>", lambda x: self.list_box_double_clicked2())

        total_clients = get_total_acc_type("client")
        total_clients = total_clients + get_total_acc_type("developer")

        user_accounts = Label(self, text="Total Users:")
        user_accounts.place(x=30, y=30)

        totalCount = StringVar(self, value=total_clients)
        totalCountEntry = Entry(self, textvariable=totalCount)
        totalCountEntry.place(x=30, y=50)
        totalCountEntry.configure(state="readonly")

    # Function to be called upon a search is properly made in the searchbar
    # Repopulates the listbox with newly generated data
    def list_box_double_clicked(self):
        project_labels = ["Project_Name:", "Developer:", "Client:", "Completed:", "Cost:", "Tags:"]

        project_name = self.listbox.selection_get()
        # retrieving the project name. index = 0 as the name is found in the first index
        project_name = str(project_name.split()[0])
        myprojectinfo = get_project_by_name(project_name)

        # print(myprojectinfo)
        # Generating the size of the popup along with some configuration
        popup = tk.Tk()
        popup.geometry("600x600")
        popup.resizable(False, False)
        popup.wm_title(project_name)

        # Dynamically creating the labels/attributes found within a project and displaying them
        i = 25
        for words in project_labels:
            entryText = StringVar(popup, value="default")
            e = Entry(popup, textvariable=entryText)
            # print(words)
            # print(str(myprojectinfo[words]))
            label_values = str(myprojectinfo[words])
            entryText.set(label_values)
            e.configure(state="readonly")
            e.place(x=140, y=5 + i)

            lb = Label(popup, text=words)
            lb.place(x=30, y=5 + i)

            i += 30

        # Using ScrolledText from tkinter in order to provide a paragraph esque container for specifications
        # to be displayed
        specification_label = Label(popup, text="Specification:")
        specification_label.place(x=35, y=415)

        specification_text = tkst.ScrolledText(popup, wrap=tk.WORD, width=55, height=12)
        specification_text.place(x=140, y=360)
        specification_text.insert(tk.INSERT, str(myprojectinfo["Specification:"])[:10] + "... register for more info")
        specification_text.configure(state="disabled")
        # Button to leave/exit the popup page
        B1 = ttk.Button(popup, text="Exit", command=popup.destroy)
        B1.place(x=270, y=560)

        popup.mainloop()

    def list_box_double_clicked2(self):
        user_labels = ["Username:", "Interests:", "Email:", "Projects:"]

        username = self.listbox.selection_get()
        # retrieving the project name. index = 0 as the name is found in the first index
        username = str(username.split()[0])
        print(username)
        print(self.acctype)

        display_user_info = get_info_by_name(self.acctype, username)
        print(display_user_info)

        # print(myprojectinfo)
        # Generating the size of the popup along with some configuration
        popup = tk.Tk()
        popup.geometry("600x600")
        popup.resizable(False, False)
        popup.wm_title(username)

        i = 25
        for x in range(len(user_labels)):
            entryText = StringVar(popup, value="default")
            e = Entry(popup, width=50, textvariable=entryText)
            # print(words)
            # print(str(myprojectinfo[words]))
            label_values = str(display_user_info[x])
            entryText.set(label_values)
            e.configure(state="readonly")
            e.place(x=140, y=5 + i)

            lb = Label(popup, text=user_labels[x])
            lb.place(x=30, y=5 + i)

            i += 30

        popup.mainloop()

    def replace_listbox_users(self):
        search_tags = self.searchBar2.get()
        # If the user searches with nothing in the search bar
        # Brings back the entire DB of projects
        if len(search_tags) == 0:
            self.listbox2.delete(0, END)
            client_most_projects, self.acctype = get_clients_with_most_projects("client")
            client_most_projects = sorted(client_most_projects, key=lambda x: (x[1]))

            for x in range(len(client_most_projects), -1, -1):
                self.listbox2.insert(END, client_most_projects[x])

            self.listbox2.bind("<Double-1>", lambda x: self.list_box_double_clicked2())
        else:
            # removing the commas placed when searching via tags
            search_tags = search_tags.replace(",", " ")
            search_tags = search_tags.split()
            search_tags = search_tags[0]
            # finds the projects with tags related

            if search_tags == "":
                client_most_projects, self.acctype = get_clients_with_most_projects("client")
                client_most_projects = sorted(client_most_projects, key=lambda x: (x[1]))
            else:
                client_most_projects, self.acctype = get_clients_with_most_projects(search_tags)
                client_most_projects = sorted(client_most_projects, key=lambda x: (x[1]))

            # Clearing the contents of the listbox
            self.listbox2.delete(0, END)
            for x in range(len(client_most_projects) - 1, -1, -1):
                self.listbox2.insert(END, client_most_projects[x])

            self.listbox2.bind("<Double-1>", lambda x: self.list_box_double_clicked2())

    def replace_listbox_projects(self):
        search_tags = self.searchBar.get()
        # If the user searches with nothing in the search bar
        # Brings back the entire DB of projects
        if len(search_tags) == 0:
            print("Search tags is 0")
            self.listbox.delete(0, END)
            projects_name_tags = get_list_of_projecterino()
            print(projects_name_tags)
            for x in range(len(projects_name_tags)):
                self.listbox.insert(END, projects_name_tags[x])

            self.listbox.bind("<Double-1>", lambda x: self.list_box_double_clicked())
        else:
            # removing the commas placed when searching via tags
            search_tags = search_tags.replace(",", " ")
            search_tags = search_tags.split()
            # finds the projects with tags related
            find_sorted_projects = get_sorted_tags(search_tags)
            # Clearing the contents of the listbox
            self.listbox.delete(0, END)

            for x in range(len(find_sorted_projects)):
                self.listbox.insert(END, find_sorted_projects[x])

            self.listbox.bind("<Double-1>", lambda x: self.list_box_double_clicked())


class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="SignUp Page", font=LARGE_FONT)
        # label.place(relx = 0.5, rely = 0.02, anchor = CENTER)
        label.pack(pady=10, padx=10)

        viewhome_button = ttk.Button(self, text="View Home Page",
                                     command=lambda: controller.show_frame(StartPage))
        viewhome_button.place(relx=1.0, y=0, anchor="ne")

        self.form_labels = ["Username:", "Password:", "Funds:"]
        self.entry = {}
        self.data = {}
        self.mail = {}

        var = tk.StringVar()
        # initial value
        var.set('')
        type = ['Client', 'Developer']
        option = tk.OptionMenu(self, var, *type)
        option.place(x=318, y=105)
        acct_lb = Label(self, text="Account Type:")
        acct_lb.place(x=220, y=115)

        i = 25
        for words in self.form_labels:
            e = Entry(self)
            e.place(x=320, y=125 + i)
            self.entry[words] = e
            # print(self.entry[words].get())

            lb = Label(self, text=words)
            lb.place(x=220, y=125 + i)
            i += 25

        b = ttk.Button(self, text="Submit Registration Information", command=lambda: self.submit_info(var))
        b.place(x=250, y=250)

    def submit_info(self, var):

        account = var.get()

        self.data["Account Type:"] = account
        for name in self.form_labels:
            self.data[name] = str(self.entry[name].get())
        self.data["Status:"] = "Not Decided"
        self.data["Reason:"] = ""

        self.mail["Issue"] = "Apply"
        self.mail["Account"] = account
        self.mail["Username"] = str(self.entry["Username:"].get())
        self.mail["Password:"] = str(self.entry["Password:"].get())
        self.mail["Funds:"] = str(self.entry["Funds:"].get())
        self.mail["Status"] = "Not Decided"
        self.mail["Reason"] = ""

        dup, msg = check_register_exists(self.data)
        if dup == True:
            self.pop_up_msg(msg)
        bl, bl_msg = check_blacklist(self.data, self.data["Account Type:"])
        if bl == True:
            self.pop_up_msg(bl_msg)

        if dup == False and bl == False:
            write_to_register(self.data)
            write_to_mailbox("Apply", self.mail)
            self.pop_up_success("Account Successfully Created!\nAwaiting Approval")

    def pop_up_msg(self, msg):

        def leavemini():
            popup.destroy()

        popup = tk.Tk()
        popup.wm_title("Error!")
        label = ttk.Label(popup, text=msg, font=SMALL_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command=leavemini)
        B1.pack()

        popup.mainloop()

    def pop_up_success(self, msg):

        def leavemini():
            popup.destroy()
            self.controller.show_frame(StartPage)

        popup = tk.Tk()
        popup.wm_title("Success!")
        label = ttk.Label(popup, text=msg, font=SMALL_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command=leavemini)
        B1.pack()

        popup.mainloop()


class ClientLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Client Login Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        viewhome_button = ttk.Button(self, text="View Home Page",
                                     command=lambda: controller.show_frame(StartPage))
        viewhome_button.pack()
        viewhome_button.place(relx=1.0, y=0, anchor="ne")

        self.login_labels = ["Username:", "Password:"]
        self.user_info_labels = ["Account Type:", "Username:", "Password:", "Email:",
                                 "Address:", "Telephone #:", "Ratings_Received:"]
        self.entry = {}
        self.data = {}
        # Buttons + Labels for user login
        self.userLabel = ttk.Label(self, text="Username:")
        self.userLabel.place(x=30, y=50)
        self.passLabel = ttk.Label(self, text="Password:")
        self.passLabel.place(x=30, y=75)

        self.userEntry = ttk.Entry(self, textvariable=StringVar())
        self.userEntry.place(x=120, y=50)

        self.passEntry = ttk.Entry(self, show="*", textvariable=StringVar())
        self.passEntry.place(x=120, y=75)

        self.b = ttk.Button(self, text="Submit Login Credentials", command=lambda: self.submit_login_info())
        self.b.place(x=105, y=125)

    # Function to be called to pop up project viewer when doubleclick event occurs on listbox of projects
    def list_box_double_clicked(self):
        project_labels = ["Project_Name:", "Developer:", "Client:", "Completed:", "OnTime:", "Bidding_Deadline:",
                          "Delivery_Deadline:", "Cost:", "ClientRating:", "DevRating:", "Tags:"]

        project_name = self.listbox.selection_get()
        # retrieving the project name. index = 0 as the name is found in the first index
        project_name = str(project_name.split()[0])
        myprojectinfo = get_project_by_name(project_name)

        # print(myprojectinfo)
        # Generating the size of the popup along with some configuration
        popup = tk.Tk()
        popup.geometry("600x600")
        popup.resizable(False, False)
        popup.wm_title(project_name)

        # Dynamically creating the labels/attributes found within a project and displaying them
        i = 25
        for words in project_labels:
            entryText = StringVar(popup, value="default")
            e = Entry(popup, textvariable=entryText)
            # print(words)
            # print(str(myprojectinfo[words]))
            label_values = str(myprojectinfo[words])
            entryText.set(label_values)
            e.configure(state="readonly")
            e.place(x=140, y=5 + i)

            lb = Label(popup, text=words)
            lb.place(x=30, y=5 + i)

            i += 30

        # Using ScrolledText from tkinter in order to provide a paragraph esque container for specifications
        # to be displayed
        specification_label = Label(popup, text="Specification:")
        specification_label.place(x=35, y=415)

        specification_text = tkst.ScrolledText(popup, wrap=tk.WORD, width=55, height=12)
        specification_text.place(x=140, y=360)
        specification_text.insert(tk.INSERT, str(myprojectinfo["Specification:"]))
        specification_text.configure(state="disabled")
        # Button to leave/exit the popup page
        B1 = ttk.Button(popup, text="Exit", command=popup.destroy)
        B1.place(x=270, y=560)

        popup.mainloop()

    # Function called when creating project for a client
    def create_project(self):
        # Default labels that user has to fill.
        self.project_labels = ["Project_Name:", "Bidding_Deadline:", "Delivery_Deadline:",
                               "Cost:", "Tags:"]

        self.popup_proj_create = tk.Tk()
        self.popup_proj_create.geometry("600x600")
        self.popup_proj_create.resizable(False, False)
        # Generating the default labels and providing entries for them.
        i = 25
        for words in self.project_labels:
            entryText = StringVar(self.popup_proj_create, value="")
            submissionE = Entry(self.popup_proj_create, textvariable=entryText)
            submissionE.place(x=140, y=5 + i)
            self.entry[words] = submissionE

            self.submissionLB = Label(self.popup_proj_create, text=words)
            self.submissionLB.place(x=30, y=5 + i)

            i += 30
        # Creating the specifications entry box. Uses ScrolledText as well
        self.specification_label = Label(self.popup_proj_create, text="Specification:")
        self.specification_label.place(x=35, y=415)
        self.specification_entry = tkst.ScrolledText(self.popup_proj_create, wrap=tk.WORD, width=55, height=13)
        self.specification_entry.place(x=140, y=340)
        self.specification_entry.insert(tk.INSERT, "Enter Specifications Here")

        # Calls the submit project function found below
        submitButton = ttk.Button(self.popup_proj_create, text="Submit Info", command=lambda: self.submit_project())
        submitButton.place(x=220, y=560)
        # Leaves the create project window
        exitButton = ttk.Button(self.popup_proj_create, text="Exit", command=self.popup_proj_create.destroy)
        exitButton.place(x=310, y=560)

        self.popup_proj_create.mainloop()

    def rate_Projects(self):

        def pop_up_success():
            def leavemini():
                popup.destroy()

            popup = tk.Tk()
            msg = "\t\tSuccessfully Rated!  \t\t\t"
            popup.wm_title("Success!")
            label = ttk.Label(popup, text=msg, font=SMALL_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(popup, text="Okay", command=leavemini)
            B1.pack()

            popup.mainloop()

        def pop_up_fail():

            def leavemini():
                popup.destroy()

            popup = tk.Tk()
            msg = "Please enter a rating between 1 and 5"
            popup.wm_title("Error!")
            label = ttk.Label(popup, text=msg, font=SMALL_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(popup, text="Okay", command=leavemini)
            B1.pack()

            popup.mainloop()

        def pop_up_warning():

            def leavemini():
                popup.destroy()

            popup = tk.Tk()
            msg = "1) You have successfully rated the Client...\n" \
                  "2) However, you are also warned for irresponsible evaluations"
            popup.wm_title("Error!")
            label = ttk.Label(popup, text=msg, font=SMALL_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(popup, text="Okay", command=leavemini)
            B1.pack()

            popup.mainloop()

        def rate_selected_project():
            project_name = str(self.complete_proj_list.get(self.complete_proj_list.curselection()))
            developer_name = get_project_by_name(project_name)
            developer_name = developer_name["Developer:"]
            print(developer_name)
            devRating = int(ratingEntry.get())
            sysRating = int(rateSysEntry.get())
            curr_user = self.controller.user_data["Username:"]

            times_rated, ratings_given = user_history_rating("client", curr_user)
            ratings_given.append(devRating)
            average = (sum(ratings_given) / float(len(ratings_given)))

            # Accounting for negative and greater than 5 ratings
            if devRating <= 0 or devRating > 5:
                pop_up_fail()
            # If the user provided good rating for system but system finds user rating to be irresponsible
            # Warns user for irresponsible ratings to dev
            elif (times_rated >= 7 and (average > 4 or average < 2)) and sysRating >= 3:
                reason = "Good System"
                # Xfer funds to user automatically because good system
                project_details = get_project_by_name(project_name)
                cost = int(project_details["Cost:"])
                payment = int(cost / 2)

                send_funds_to_user("developer", developer_name, payment)
                subtract_from_funds("client", curr_user, payment)

                # not actually low rating just submit rating without a reason
                submit_low_sysrate_reason(project_name, sysRating, reason)
                give_rating_to_dev(project_name, devRating)
                insert_into_ratings_given("client", curr_user, devRating)
                insert_into_ratings_received("developer", developer_name, devRating)
                new_completed_projs = get_delivered_by_user(curr_user)
                self.complete_proj_list.delete(0, END)
                for x in range(0, len(new_completed_projs)):
                    self.complete_proj_list.insert(END, new_completed_projs[x])
                increment_warn_count("client", curr_user)
                pop_up_warning()
            # If the system rating is too low must provide reason
            elif sysRating <= 2:
                def pop_up_reason():
                    def leavemini():
                        popup.destroy()

                    popup = tk.Tk()
                    msg = "Please Enter Reason\nfor Low System Rating"
                    popup.wm_title("Reason!")
                    popup.geometry("250x100")
                    label = ttk.Label(popup, text=msg, font=SMALL_FONT)
                    label.pack(side="top", fill="x", pady=10)
                    B1 = ttk.Button(popup, text="Submit", command=leavemini)
                    B1.place(x=40, y=70)
                    reasonText = StringVar(popup, value="")
                    reasonEntry = Entry(popup, width=30, textvariable=reasonText)
                    reasonEntry.place(x=5, y=50)

                pop_up_reason()
                reason = "The system didn't meet specs"

                ##Give money to superuser

                # Xfer funds to super_user for evaluation
                project_details = get_project_by_name(project_name)
                cost = int(project_details["Cost:"])
                payment = int(cost / 2)

                give_money_to_su = {
                    "Issue": "Money",
                    "Projects": project_name,
                    "Client": curr_user,
                    "Developer": developer_name,
                    "Money_holds": payment,
                    "Rating": str(sysRating),
                    "Status": "Not Decided",
                    "Client_received": 0,
                    "Developer_received": 0
                }
                write_to_mailbox("Money", give_money_to_su)
                subtract_from_funds("client", curr_user, payment)

                submit_low_sysrate_reason(project_name, sysRating, reason)
                give_rating_to_dev(project_name, devRating)
                new_completed_projs = get_delivered_by_user(curr_user)
                insert_into_ratings_given("client", curr_user, devRating)
                insert_into_ratings_received("developer", developer_name, devRating)
                self.complete_proj_list.delete(0, END)
                for x in range(0, len(new_completed_projs)):
                    self.complete_proj_list.insert(END, new_completed_projs[x])
                pop_up_success()
            # System Rating is Fine and Client Rating is fine in this case
            else:
                # Nothing wrong -- give money to dev
                reason = "Good System"

                # Xfer funds to user automatically because good system
                project_details = get_project_by_name(project_name)
                cost = int(project_details["Cost:"])
                payment = int(cost / 2)

                send_funds_to_user("developer", developer_name, payment)
                subtract_from_funds("client", curr_user, payment)

                # not actually low rating just submit rating without a reason
                submit_low_sysrate_reason(project_name, sysRating, reason)
                give_rating_to_dev(project_name, devRating)
                insert_into_ratings_given("client", curr_user, devRating)
                insert_into_ratings_received("developer", developer_name, devRating)
                new_completed_projs = get_delivered_by_user(curr_user)
                self.complete_proj_list.delete(0, END)
                for x in range(0, len(new_completed_projs)):
                    self.complete_proj_list.insert(END, new_completed_projs[x])
                pop_up_success()

        popup = tk.Tk()
        popup.geometry("400x400")
        popup.wm_title("Select Bidders")
        popup.resizable(False, False)

        username = self.controller.user_data["Username:"]

        completed_projects = get_delivered_by_user(username)

        lbTitle = ttk.Label(popup, text="Rate Completed Projects")
        lbTitle.place(x=30, y=30)

        ratingText = StringVar(popup, value="")
        ratingEntry = Entry(popup, width=15, textvariable=ratingText)
        ratingEntry.place(x=30, y=300)

        devRate = ttk.Label(popup, text="Developer Rating:")
        devRate.place(x=30, y=270)

        sysRate = ttk.Label(popup, text="System Rating:")
        sysRate.place(x=150, y=270)

        rateDev = ttk.Button(popup, text="Submit Ratings:", command=lambda: rate_selected_project())
        rateDev.place(x=30, y=350)

        rateSysText = StringVar(popup, value="")
        rateSysEntry = Entry(popup, width=15, textvariable=rateSysText)
        rateSysEntry.place(x=150, y=300)

        self.complete_proj_list = Listbox(popup, height=10, width=30, font=LARGE_FONT)
        self.complete_proj_list.pack()
        self.complete_proj_list.place(x=185, y=145, anchor=CENTER)

        for x in range(0, len(completed_projects)):
            self.complete_proj_list.insert(END, completed_projects[x])

        exitButton = ttk.Button(popup, text="Exit", command=popup.destroy)
        exitButton.place(x=250, y=560)

        popup.mainloop()

    def submit_protest(self):
        username = self.controller.user_data["Username:"]
        account = self.controller.user_data["Account Type:"]
        reason = self.protest_entry.get(1.0, END)

        data = {"Username": username,
                "Account": account,
                "Issue": "Protest",
                "Reason": reason,
                "Status": "Not Decided"}

        write_to_mailbox("Protest", data)

        self.pop_up_success()

    def submit_appeal(self):
        username = self.controller.user_data["Username:"]
        account = self.controller.user_data["Account Type:"]
        reason = self.protest_entry.get(1.0, END)

        data = {"Username": username,
                "Account": account,
                "Issue": "Appeal",
                "Reason": reason,
                "Status": "Not Decided"}

        write_to_mailbox("Appeal", data)

        self.pop_up_success()

    def write_protests(self):

        popup = tk.Tk()
        popup.geometry("400x400")
        popup.wm_title("Create Protest")
        popup.resizable(False, False)

        self.protesting_label = Label(popup, text="Create Protest to Warnings\nOr Appeals for Blacklist")
        self.protesting_label.place(x=40, y=50)
        self.protest_entry = tkst.ScrolledText(popup, wrap=tk.WORD, width=30, height=10)
        self.protest_entry.place(x=40, y=90)
        self.protest_entry.insert(tk.INSERT, "Enter Protest Here")

        submit_protest = ttk.Button(popup, text="Submit Protest:", command=lambda: self.submit_protest())
        submit_protest.place(x=40, y=280)

        submit_appeal = ttk.Button(popup, text="Submit Appeal:", command=lambda: self.submit_appeal())
        submit_appeal.place(x=150, y=280)

    def add_funds(self):

        def submit_funds_to_account():
            funds_to_add = int(addfundsEntry.get())
            curr_funds = int(self.fundsText.get())

            send_funds_to_user("client", self.controller.user_data["Username:"], funds_to_add)

            self.fundsText.set(funds_to_add + curr_funds)
            messagebox.showinfo("Success!", "Funds added!")

        popup = tk.Tk()
        popup.geometry("400x400")
        popup.wm_title("Add/View Funds")
        popup.resizable(False, False)

        balance = Label(popup, text="Your Balance:", font=LARGE_FONT)
        balance.place(x=130, y=70)

        self.fundsText = StringVar(popup, value=get_funds_of_user("client", self.controller.user_data["Username:"]))
        fundsEntry = Entry(popup, width=15, textvariable=self.fundsText)
        fundsEntry.place(x=145, y=100)
        fundsEntry.configure(state="readonly")

        addfundsText = StringVar(popup, value="")
        addfundsEntry = Entry(popup, width=15, textvariable=addfundsText)
        addfundsEntry.place(x=180, y=315)

        submit_funds = ttk.Button(popup, text="Add Funds:", command=lambda: submit_funds_to_account())
        submit_funds.place(x=90, y=310)

        exit = ttk.Button(popup, text="Exit", command=lambda: popup.destroy())
        exit.place(x=300, y=360)

    def quit_system(self):
        def submit_quit_response():
            reason = (quit_text.get(1.0, END))

            infodata = {
                "Issue": "Quit",
                "Account": "Client",
                "Username": self.controller.user_data["Username:"],
                "Status": "Not Decided",
                "Reason": reason
            }

            write_to_mailbox("Quit", infodata)

            messagebox.showinfo("Success!", "Quit Response Received!")

        popup = tk.Tk()
        popup.geometry("400x400")
        popup.wm_title("Submit Quit Application")
        popup.resizable(False, False)

        balance = Label(popup, text="Username:", font=LARGE_FONT)
        balance.place(x=130, y=70)

        userText = StringVar(popup, value=(self.controller.user_data["Username:"]))
        userEntry = Entry(popup, width=15, textvariable=userText)
        userEntry.place(x=145, y=100)
        userEntry.configure(state="readonly")

        quit_text = tkst.ScrolledText(popup, wrap=tk.WORD, width=40, height=8)
        quit_text.place(x=30, y=130)
        quit_text.insert(tk.INSERT, "Enter your reason here")

        submit_resp = ttk.Button(popup, text="Submit Response", command=lambda: submit_quit_response())
        submit_resp.place(x=120, y=330)

        exit = ttk.Button(popup, text="Exit", command=lambda: popup.destroy())
        exit.place(x=300, y=360)

    def selectBidder(self):

        def pop_up_success():
            def leavemini():
                popup.destroy()

            popup = tk.Tk()
            msg = "\t\tBidder Chosen!  \t\t\t"
            popup.wm_title("Success!")
            label = ttk.Label(popup, text=msg, font=SMALL_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(popup, text="Okay", command=leavemini)
            B1.pack()

            popup.mainloop()

        def select_cheapest_bidder():
            project = (self.bidlistbox.get(self.bidlistbox.curselection()))
            project = project.split()
            project = project[0]

            curr_user = str((self.controller.user_data["Username:"]))
            # curr_proj = get_project_by_name(project)
            # new_proj = get_project_by_name(project)

            lowest_bid = sort_bidders_by_price(project)
            lowest_bidder_dev = (lowest_bid[0][0])
            lowest_price = str(lowest_bid[0][1])
            print(str(lowest_bidder_dev) + " <---- dev")
            print(str(lowest_price) + " <---- price")

            xfer_fund = (int(lowest_price) / 2)
            xfer_fund = int(xfer_fund)

            new_cost = int(lowest_price)
            new_cost = {"Cost:": new_cost}
            reason = {"Chosen_Reason:": "Cheapest Bidder"}
            reason.update(new_cost)

            update_project_with_new_bidder(project, lowest_bidder_dev, reason)
            send_funds_to_user("developer", lowest_bidder_dev, xfer_fund)
            subtract_from_funds("client", curr_user, xfer_fund)
            add_project_to_user("developer", lowest_bidder_dev, project)

            # Clearing listbox
            list_of_unbid_projs = get_unbidprojects_by_name(self.controller.user_data["Username:"])
            self.bidlistbox.delete(0, END)

            for x in range(len(list_of_unbid_projs)):
                self.bidlistbox.insert(END, list_of_unbid_projs[x])

            pop_up_success()

        def select_another_bidder():

            def submit_bidder(project):
                developerName = str(self.bidderslistbox.get(self.bidderslistbox.curselection()))
                developerName = developerName.split()
                price = int(developerName[1][1:-2])
                cost = int(price)
                price = (price / 2)
                developerName = developerName[0][2:-2]
                curr_user = self.controller.user_data["Username:"]
                print(curr_user)

                new_cost = {"Cost:": cost}

                reasonE = (str(reasonEntry.get()))
                reason = {"Chosen_Reason:": reasonE}
                reason.update(new_cost)

                print(str(developerName) + " <--- dev name")

                update_project_with_new_bidder(project, developerName, reason)
                send_funds_to_user("developer", developerName, price)
                subtract_from_funds("client", curr_user, price)
                add_project_to_user("developer", developerName, project)

                list_of_unbid_projs = get_unbidprojects_by_name(self.controller.user_data["Username:"])
                self.bidlistbox.delete(0, END)

                for x in range(len(list_of_unbid_projs)):
                    self.bidlistbox.insert(END, list_of_unbid_projs[x])

                popup.destroy()

                def pop_up_success():
                    def leavemini():
                        popup2.destroy()

                    popup2 = tk.Tk()
                    msg = "\t\tBidder Chosen!  \t\t\t"
                    popup2.wm_title("Success!")
                    label = ttk.Label(popup2, text=msg, font=SMALL_FONT)
                    label.pack(side="top", fill="x", pady=10)
                    B1 = ttk.Button(popup2, text="Okay", command=leavemini)
                    B1.pack()

                    popup2.mainloop()

                pop_up_success()

            popup = tk.Tk()
            popup.geometry("400x400")
            popup.wm_title("Select Bidders")
            popup.resizable(False, False)
            project = (self.bidlistbox.get(self.bidlistbox.curselection()))
            project = project.split()
            project = project[0]

            bidders = get_list_of_bidders(project)

            reasonText = StringVar(popup, value="")
            reasonEntry = Entry(popup, width=50, textvariable=reasonText)
            reasonEntry.place(x=30, y=300)

            reasonButton = ttk.Button(popup, text="Submit Reason:", command=lambda: submit_bidder(project))
            reasonButton.place(x=30, y=270)

            self.bidderslistbox = Listbox(popup, height=10, width=20, font=LARGE_FONT)
            self.bidderslistbox.pack()
            self.bidderslistbox.place(x=150, y=145, anchor=CENTER)

            for x in range(1, len(bidders)):
                self.bidderslistbox.insert(END, bidders[x])

        # Default labels that user has to fill.
        self.project_labels = ["Project_Name:", "Bidding_Deadline:", "Delivery_Deadline:",
                               "Cost:", "Tags:"]

        popup = tk.Tk()
        popup.geometry("600x600")
        popup.wm_title("Select Bidders")
        popup.resizable(False, False)

        self.bidlistbox = Listbox(popup, height=20, width=45, font=LARGE_FONT)
        self.bidlistbox.pack()
        self.bidlistbox.place(x=300, y=245, anchor=CENTER)

        lbTitle = ttk.Label(popup, text="Select Bidders From Projects")
        lbTitle.place(x=213, y=30)

        # get list of projects that currently have no bidder.
        list_of_unbid_projs = get_unbidprojects_by_name(self.controller.user_data["Username:"])

        for x in range(len(list_of_unbid_projs)):
            self.bidlistbox.insert(END, list_of_unbid_projs[x])

        # Calls the submit project function found below
        selectCheapest = ttk.Button(popup, text="Select Cheapest Bidder", command=lambda: select_cheapest_bidder())
        selectCheapest.place(x=80, y=450)

        selectAnotherBid = ttk.Button(popup, text="Select Another Bidder", command=lambda: select_another_bidder())
        selectAnotherBid.place(x=240, y=450)

        # Leaves the create project window
        exitButton = ttk.Button(popup, text="Exit", command=popup.destroy)
        exitButton.place(x=250, y=560)

        popup.mainloop()

    # Function that is called when user elects to submit project
    def submit_project(self):
        # Popup for any errors that will occur within the submission of project
        def pop_up_msg():
            def leavemini():
                popup.destroy()

            popup = tk.Tk()
            msg = "1) You either didn't fill all entries or... \n" \
                  "2) The project name already exists...\n" \
                  "3) You have insufficient funds for this project"
            popup.wm_title("Error!")
            label = ttk.Label(popup, text=msg, font=SMALL_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(popup, text="Okay", command=leavemini)
            B1.pack()

            popup.mainloop()

        def pop_up_success():
            def leavemini():
                self.popup_proj_create.destroy()
                popup.destroy()

            popup = tk.Tk()
            msg = "\t\tProject Created!  \t\t\t"
            popup.wm_title("Success!")
            label = ttk.Label(popup, text=msg, font=SMALL_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(popup, text="Okay", command=leavemini)
            B1.pack()
            popup.mainloop()

        # Declaring Data as a dictionary because I will need to use it as a dictionary type in order to
        # transform the entries retrieved as a dictionary
        data = {}
        for labels in self.project_labels:
            data[labels] = str(self.entry[labels].get())
            if self.entry[labels].get() == "":
                pop_up_msg()
                return
        # checks if the project name is a duplicate. We will not allow duplicate project name for our own purposes
        duplicate = check_duplicate_project(str(data["Project_Name:"]))
        # If duplicate then popup...
        if duplicate:
            pop_up_msg()
            return
        # Setting the other many attributes found within a project that isn't necessary/up to the client to decide/fill in
        data["Client:"] = self.controller.user_data["Username:"]
        data["Developer:"] = "None"
        data["Bidders:"] = {}
        data["Completed:"] = "Open"
        data["OnTime:"] = "None"
        data["ClientRating:"] = "None"
        data["DevRating:"] = "None"
        data["SystemRating:"] = "None"
        data["Tags:"] = data["Tags:"].replace(",", "")
        data["Tags:"] = data["Tags:"].split()
        data["Specification:"] = self.specification_entry.get(1.0, END)
        # print(self.specification_text.get(1.0, END))

        # Checking current user funds. User cannot submit a project cost that is more than their funds
        user_funds = int(self.controller.user_data["Funds:"])
        proj_cost = int(data["Cost:"])

        # Popup if project cost > funds
        # Else write it into the project db and it is now a valid project awaiting bidders.
        if (proj_cost > user_funds):
            pop_up_msg()
        else:
            add_project_to_user("client", self.controller.user_data["Username:"], data["Project_Name:"])
            write_to_project_db(data)
            pop_up_success()

    # Function to call when person submits login info on login page
    def submit_login_info(self):

        def pop_up_warning():
            def leavemini():
                popup.destroy()

            popup = tk.Tk()
            msg = "1)Successful login...\n" \
                  "2)However, You've been warned for receiving excessive poor ratings!"
            popup.wm_title("Warning!")
            label = ttk.Label(popup, text=msg, font=SMALL_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(popup, text="Okay", command=leavemini)
            B1.pack()
            popup.mainloop()

        infodata = {}
        infodata["Username:"] = self.userEntry.get()
        infodata["Password:"] = self.passEntry.get()
        check_login, client_info, msg = check_user_login(infodata, "client")
        bl, bl_msg = check_blacklist(infodata, "Client")
        if bl == True:
            print("bl")
            self.pop_up_fail(bl_msg)
        temp, temp_info, temp_msg = check_temp(infodata, "Client")
        write_to_logged(client_info)
        self.controller.user_data = client_info

        # does NOT exist in login db nor temp db
        if check_login == False and temp == True:
            self.pop_up_fail(temp_msg)

        # temp account, just accepted, requires more info
        elif check_login == False and temp == False:
            self.add_info(infodata)

        # exists in login db, not temp, and not blacklisted
        if check_login == True:
            self.controller.user_data = client_info
            # print(self.controller.user_data)
            self.create_labels()

            login_warned = client_info["Login_Warned:"]
            total_warned = get_user_total_warns("client", self.controller.user_data["Username:"])
            total_ratings, rating_list = user_history_received("client", self.controller.user_data["Username:"])

            if total_ratings >= 8 and (sum(rating_list) / float(len(rating_list))) <= 2 and login_warned == "False":
                increment_warn_count2("client", self.controller.user_data["Username:"])
                pop_up_warning()
            elif total_warned >= 2:
                add_to_blacklist(client_info)
                messagebox.showinfo("Warned!", "You've been blacklisted for having > 2 warnings!\n"
                                               "You can still write an appeal and access account\n"
                                               " for one last time")
            else:
                self.pop_up_success()

    def add_info(self, data):

        self.additional_labels = ["Address:", "Email:", "Interests:", "Telephone #:"]

        popup = tk.Tk()
        popup.geometry("600x600")
        popup.resizable(False, False)
        # Generating the default labels and providing entries for them.
        i = 25
        for words in self.additional_labels:
            entryText = StringVar(popup, value="")
            submissionE = Entry(popup, textvariable=entryText)
            submissionE.place(x=140, y=5 + i)
            self.entry[words] = submissionE

            self.submissionLB = Label(popup, text=words)
            self.submissionLB.place(x=30, y=5 + i)

            i += 30

        print(data)
        print("\n the crazy add_info data dont know what the fucks goin on lol")

        submitButton = ttk.Button(popup, text="Submit Info", command=lambda: self.submit_add_info(data, popup))
        submitButton.place(x=220, y=560)

        exitButton = ttk.Button(popup, text="Exit", command=popup.destroy)
        exitButton.place(x=310, y=560)

        popup.mainloop()

    def submit_add_info(self, data, popup):

        print(data)
        print("\n the passed on data in submit_add_info")

        db = {}

        db["Account Type:"] = "Client"
        db["Username:"] = data["Username:"]
        db["Password:"] = data["Password:"]
        db["Login_Warned:"] = "False"
        db["Funds:"] = get_funds_from_temp(data["Username:"])
        for labels in self.additional_labels:
            db[labels] = str(self.entry[labels].get())
            if self.entry[labels].get() == "":
                self.pop_up_fail("All entries must be filled")
                return
        db["Warn_Count:"] = 0
        db["Ratings_Received:"] = []
        db["Ratings_Given:"] = []
        db["Projects:"] = []

        db["Interests:"] = db["Interests:"].replace(",", "")
        db["Interests:"] = db["Interests:"].split()

        write_to_user(db, "client")
        popup.destroy()

    def pop_up_fail(self, msg):

        def leavemini():
            popup.destroy()

        popup = tk.Tk()
        popup.wm_title("Error!")
        label = ttk.Label(popup, text=msg, font=SMALL_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command=leavemini)
        B1.pack()

        popup.mainloop()

    def pop_up_fail(self, msg):

        def leavemini():
            popup.destroy()

        popup = tk.Tk()
        popup.wm_title("Error!")
        label = ttk.Label(popup, text=msg, font=SMALL_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command=leavemini)
        B1.pack()

        popup.mainloop()

    def pop_up_success(self):

        def leavemini():
            popup.destroy()

        popup = tk.Tk()
        msg = "\t\tSuccessful!  \t\t\t"
        popup.wm_title("Success!")
        label = ttk.Label(popup, text=msg, font=SMALL_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command=leavemini)
        B1.pack()

        write_to_logged(self.controller.user_data)

        popup.mainloop()

    # Function to be called upon login successful. Populates the client login page.
    def create_labels(self):

        def logout_user():

            messagebox.showinfo("Logging out", "You've been logged out!")

            for widget in self.winfo_children():
                widget.destroy()

            label = tk.Label(self, text="Client Login Page", font=LARGE_FONT)
            label.pack(pady=10, padx=10)

            viewhome_button = ttk.Button(self, text="View Home Page",
                                         command=lambda: self.controller.show_frame(StartPage))
            viewhome_button.pack()
            viewhome_button.place(relx=1.0, y=0, anchor="ne")

            self.login_labels = ["Username:", "Password:"]
            self.user_info_labels = ["Account Type:", "Username:", "Password:", "Email:",
                                     "Address:", "Telephone #:", "Ratings_Received:"]
            self.entry = {}
            self.data = {}
            # Buttons + Labels for user login
            self.userLabel = ttk.Label(self, text="Username:")
            self.userLabel.place(x=30, y=50)
            self.passLabel = ttk.Label(self, text="Password:")
            self.passLabel.place(x=30, y=75)

            self.userEntry = ttk.Entry(self, textvariable=StringVar())
            self.userEntry.place(x=120, y=50)

            self.passEntry = ttk.Entry(self, show="*", textvariable=StringVar())
            self.passEntry.place(x=120, y=75)

            self.b = ttk.Button(self, text="Submit Login Credentials", command=lambda: self.submit_login_info())
            self.b.place(x=105, y=125)


        with open('logged_in.txt') as f:
            db = json.load(f)

        logout_button = ttk.Button(self, text="Logout",
                                       command=lambda: logout_user())
        logout_button.pack()
        logout_button.place(x=10, y=15)

        self.controller.user_data = db

        # Drawing rectangles in the window in order to show a more geometric outline of our functions
        # Allows users to see a group of functions
        clientFunctions = Canvas(self)

        clientFunctions.create_rectangle(10, 10, 120, 650)
        clientFunctions.pack(fill=BOTH, expand=1)

        clientFunctions.create_rectangle(150, 60, 735, 650)
        clientFunctions.pack(fill=BOTH, expand=1)
        # Populating the right side of the page with the user info.
        i = 25
        for words in self.user_info_labels:
            entryText = StringVar(self, value="default")
            e = Entry(self, textvariable=entryText)
            # print(words)
            # print(str(self.controller.user_data[words]))
            label_values = str(self.controller.user_data[words])
            entryText.set(label_values)
            e.configure(state="readonly")
            e.place(x=860, y=120 + i)

            lb = Label(self, text=words)
            lb.place(x=760, y=120 + i)

            i += 25

        # Creating a project button
        createProjButton = ttk.Button(self, text="Create Project", command=lambda: self.create_project())
        createProjButton.place(x=22, y=190)

        # Selecting bidder in projects
        selectBidderButton = ttk.Button(self, text="Select Bidder", command=lambda: self.selectBidder())
        selectBidderButton.place(x=22, y=230)

        # Rating Completed Projects
        rateCompleted = ttk.Button(self, text="Rate Projects", command=lambda: self.rate_Projects())
        rateCompleted.place(x=22, y=270)

        # Create Protests for Warnings
        protestB = ttk.Button(self, text="Write Protest", command=lambda: self.write_protests())
        protestB.place(x=22, y=310)

        # Add funds to my account
        addFunds = ttk.Button(self, text="Add Funds", command=lambda: self.add_funds())
        addFunds.place(x=22, y=350)

        # Send request to quit system to Super
        quitSys = ttk.Button(self, text="Quit System", command=lambda: self.quit_system())
        quitSys.place(x=22, y=390)

        # default entry within the search bar function
        placeHolder = StringVar(self, value="")
        self.searchBar = Entry(self, textvariable=placeHolder, width=30)
        self.searchBar.place(x=228, y=70, width=508)
        # Some buttons I declare as self if I need to perform actions with that button in another function
        searchButton = ttk.Button(self, text="Search", command=lambda: self.replace_listbox_projects())
        searchButton.place(x=150, y=65)

        self.listbox = Listbox(self, height=31, width=60, font=LARGE_FONT)
        self.listbox.pack()
        self.listbox.place(x=435, y=400, anchor=CENTER)

        ##REMOVE PROJECTS THAT HAVE PASSED BIDDING DEADLINE AND NO BIDDERS
        total_expired_projects = remove_projects_no_bids(self.controller.user_data["Username:"])

        if total_expired_projects > 0:
            # Taking away funds from client... $10 for every expired project they have with no bidders
            subtract_from_funds("client", (self.controller.user_data["Username:"]), (total_expired_projects * 10))
            totalmsg = str(total_expired_projects * 10)
            messagebox.showinfo("Expired Projects!", "You have been fined $" + totalmsg + " for expired "
                                                                                          "projects with no bidders!")

        # Retrieves a list of all project names and tags associated with it
        projects_name_tags = get_list_of_projecterino()
        # Automatically populating the listbox with all projects in the projects db
        for x in range(len(projects_name_tags)):
            self.listbox.insert(END, projects_name_tags[x])

        # Action to make when user doubleclicks an index of the listbox
        self.listbox.bind("<Double-1>", lambda x: self.list_box_double_clicked())

    # Function to be called upon a search is properly made in the searchbar
    # Repopulates the listbox with newly generated data
    def replace_listbox_projects(self):
        search_tags = self.searchBar.get()
        # If the user searches with nothing in the search bar
        # Brings back the entire DB of projects
        if len(search_tags) == 0:
            print("Search tags is 0")
            self.listbox.delete(0, END)
            projects_name_tags = get_list_of_projecterino()
            print(projects_name_tags)
            for x in range(len(projects_name_tags)):
                self.listbox.insert(END, projects_name_tags[x])

            self.listbox.bind("<Double-1>", lambda x: self.list_box_double_clicked())
        else:
            # removing the commas placed when searching via tags
            search_tags = search_tags.replace(",", " ")
            search_tags = search_tags.split()
            # finds the projects with tags related
            find_sorted_projects = get_sorted_tags(search_tags)
            # Clearing the contents of the listbox
            self.listbox.delete(0, END)

            for x in range(len(find_sorted_projects)):
                self.listbox.insert(END, find_sorted_projects[x])

            self.listbox.bind("<Double-1>", lambda x: self.list_box_double_clicked())


class DevLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Developer Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        viewhome_button = ttk.Button(self, text="View Home Page",
                                     command=lambda: controller.show_frame(StartPage))
        viewhome_button.pack()
        viewhome_button.place(relx=1.0, y=0, anchor="ne")

        self.login_labels = ["Username:", "Password:"]
        self.user_info_labels = ["Account Type:", "Username:", "Password:", "Email:", "Address:", "Telephone #:",
                                 "Ratings_Received:"]
        self.entry = {}
        self.data = {}
        # Buttons + Labels for user login
        self.userLabel = ttk.Label(self, text="Username:")
        self.userLabel.place(x=30, y=50)
        self.passLabel = ttk.Label(self, text="Password:")
        self.passLabel.place(x=30, y=75)

        self.userEntry = ttk.Entry(self, textvariable=StringVar())
        self.userEntry.place(x=120, y=50)

        self.passEntry = ttk.Entry(self, show='*', textvariable=StringVar())
        self.passEntry.place(x=120, y=75)

        self.b = ttk.Button(self, text="Submit Login Credentials", command=lambda: self.submit_login_info())
        self.b.place(x=105, y=125)

    def submit_login_info(self):

        def pop_up_warning():
            def leavemini():
                popup.destroy()

            popup = tk.Tk()
            msg = "1)Successful login...\n" \
                  "2)However, You've been warned for receiving excessive poor ratings!"
            popup.wm_title("Warning!")
            label = ttk.Label(popup, text=msg, font=SMALL_FONT)
            label.pack(side="top", fill="x", pady=10)
            B1 = ttk.Button(popup, text="Okay", command=leavemini)
            B1.pack()
            popup.mainloop()

        infodata = {}
        infodata["Username:"] = self.userEntry.get()
        infodata["Password:"] = self.passEntry.get()

        check_login, dev_info, msg = check_user_login(infodata, "developer")
        bl, bl_msg = check_blacklist(infodata, "Developer")
        if bl == True:
            self.pop_up_fail(bl_msg)

        temp, temp_info, temp_msg = check_temp(infodata, "Developer")

        write_to_logged(dev_info)
        self.controller.user_data = dev_info

        # does NOT exist in login db or temp db
        if check_login == False and temp == True:
            self.pop_up_fail(msg)

        # temp account, just accepted, requires more info
        elif check_login == False and temp == False:
            self.add_info(infodata)

        # exists in login db, not temp, and not blacklisted
        if check_login == True:
            # print(self.controller.user_data)
            self.create_labels()
            self.controller.user_data = dev_info

            ##Checks warning counter when logging in to see if the user is now blacklisted.
            login_warned = dev_info["Login_Warned:"]
            total_warned = get_user_total_warns("developer", self.controller.user_data["Username:"])
            total_ratings, rating_list = user_history_received("developer", self.controller.user_data["Username:"])

            if total_ratings >= 8 and (sum(rating_list) / float(len(rating_list))) <= 2 and login_warned == "False":
                increment_warn_count2("developer", self.controller.user_data["Username:"])
                pop_up_warning()
            elif total_warned >= 2:
                add_to_blacklist(dev_info)
                messagebox.showinfo("Warned!", "You've been blacklisted for having > 2 warnings!\n"
                                               "You can still write an appeal and access account\n"
                                               " for one last time")
            else:
                self.pop_up_success()

    def add_info(self, data):

        self.additional_labels = ["Address:", "Email:", "Interests:", "Telephone #:"]

        popup = tk.Tk()
        popup.geometry("600x600")
        popup.resizable(False, False)
        # Generating the default labels and providing entries for them.
        i = 25
        for words in self.additional_labels:
            entryText = StringVar(popup, value="")
            submissionE = Entry(popup, textvariable=entryText)
            submissionE.place(x=140, y=5 + i)
            self.entry[words] = submissionE

            self.submissionLB = Label(popup, text=words)
            self.submissionLB.place(x=30, y=5 + i)

            i += 30


        submitButton = ttk.Button(popup, text="Submit Info", command=lambda: self.submit_add_info(data, popup))
        submitButton.place(x=220, y=560)

        exitButton = ttk.Button(popup, text="Exit", command=popup.destroy)
        exitButton.place(x=310, y=560)

        popup.mainloop()

    def submit_add_info(self, data, popup):

        db = {}

        db["Account Type:"] = "Developer"
        db["Username:"] = data["Username:"]
        db["Password:"] = data["Password:"]
        db["Login_Warned:"] = "False"
        db["Funds:"] = get_funds_from_temp(data["Username:"])
        for labels in self.additional_labels:
            db[labels] = str(self.entry[labels].get())
            if self.entry[labels].get() == "":
                self.pop_up_fail("All entries must be filled")
                return
        db["Warn_Count:"] = 0
        db["Ratings_Received:"] = []
        db["Ratings_Given:"] = []
        db["Projects:"] = []

        db["Interests:"] = db["Interests:"].replace(",", "")
        db["Interests:"] = db["Interests:"].split()

        write_to_user(db, "developer")
        popup.destroy()

    def pop_up_fail(self, msg):

        def leavemini():
            popup.destroy()

        popup = tk.Tk()
        popup.wm_title("Error!")
        label = ttk.Label(popup, text=msg, font=SMALL_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command=leavemini)
        B1.pack()

        popup.mainloop()

    def pop_up_success(self):

        def leavemini():
            popup.destroy()

        popup = tk.Tk()
        msg = "\t\tLogin Successful!  \t\t\t"
        popup.wm_title("Success!")
        label = ttk.Label(popup, text=msg, font=SMALL_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command=leavemini)
        B1.pack()

        write_to_logged(self.controller.user_data)

        popup.mainloop()

    def create_labels(self):

        def logout_user():

            messagebox.showinfo("Logging out", "You've been logged out!")

            for widget in self.winfo_children():
                widget.destroy()

            label = tk.Label(self, text="DeveloperPage", font=LARGE_FONT)
            label.pack(pady=10, padx=10)

            viewhome_button = ttk.Button(self, text="View Home Page",
                                         command=lambda: self.controller.show_frame(StartPage))
            viewhome_button.pack()
            viewhome_button.place(relx=1.0, y=0, anchor="ne")

            self.login_labels = ["Username:", "Password:"]
            self.user_info_labels = ["Account Type:", "Username:", "Password:", "Email:",
                                     "Address:", "Telephone #:", "Ratings_Received:"]
            self.entry = {}
            self.data = {}
            # Buttons + Labels for user login
            self.userLabel = ttk.Label(self, text="Username:")
            self.userLabel.place(x=30, y=50)
            self.passLabel = ttk.Label(self, text="Password:")
            self.passLabel.place(x=30, y=75)

            self.userEntry = ttk.Entry(self, textvariable=StringVar())
            self.userEntry.place(x=120, y=50)

            self.passEntry = ttk.Entry(self, show="*", textvariable=StringVar())
            self.passEntry.place(x=120, y=75)

            self.b = ttk.Button(self, text="Submit Login Credentials", command=lambda: self.submit_login_info())
            self.b.place(x=105, y=125)


        with open('logged_in.txt') as f:
            db = json.load(f)


        logout_button = ttk.Button(self, text="Logout",
                                       command=lambda: logout_user())

        logout_button.pack()
        logout_button.place(x=10, y=15)


        self.controller.user_data = db


        # Rectangle things
        clientFunctions = Canvas(self)
        clientFunctions.create_rectangle(10, 10, 120, 650)
        clientFunctions.pack(fill=BOTH, expand=1)
        clientFunctions.create_rectangle(150, 60, 735, 650)
        clientFunctions.pack(fill=BOTH, expand=1)

        # Information stuff
        i = 25
        for words in self.user_info_labels:
            entryText = StringVar(self, value="default")
            e = Entry(self, textvariable=entryText)
            label_values = str(self.controller.user_data[words])
            entryText.set(label_values)
            e.configure(state="readonly")
            e.place(x=860, y=120 + i)
            lb = Label(self, text=words)
            lb.place(x=760, y=120 + i)
            i += 25

        # Listbox
        self.listbox = Listbox(self, height=31, width=60, font=LARGE_FONT)
        self.listbox.pack()
        self.listbox.place(x=435, y=400, anchor=CENTER)

        # Populate tis betch
        projects_name_tags = get_list_of_projecterino()
        for x in range(len(projects_name_tags)):
            self.listbox.insert(END, projects_name_tags[x])

        self.listbox.bind("<Double-1>", lambda x: self.list_box_double_clicked())

        # Create Protests for Warnings
        protestB = ttk.Button(self, text="Write Protest", command=lambda: self.write_protests())
        protestB.place(x=22, y=70)

    def write_protests(self):
        popup = tk.Tk()
        popup.geometry("400x400")
        popup.wm_title("Create Protest")
        popup.resizable(False, False)

        self.protesting_label = Label(popup, text="Create Protest to Warnings\nOr Appeals for Blacklist")
        self.protesting_label.place(x=40, y=50)
        self.protest_entry = tkst.ScrolledText(popup, wrap=tk.WORD, width=30, height=10)
        self.protest_entry.place(x=40, y=90)
        self.protest_entry.insert(tk.INSERT, "Enter Protest Here")

        if self.controller.user_data["Warn_Count:"] > 0:
            submit_protest = ttk.Button(popup, text="Submit Protest:", command=lambda: self.submit_protest())
            submit_protest.place(x=40, y=280)
        infodata = {}
        infodata["Username:"] = self.controller.user_data["Username:"]
        check_bl, msg = check_blacklist(infodata, "Developer")
        if check_bl == True:
            submit_appeal = ttk.Button(popup, text="Submit Appeal:", command=lambda: self.submit_appeal())
            submit_appeal.place(x=150, y=280)

    def submit_appeal(self):
        username = self.controller.user_data["Username:"]
        account = self.controller.user_data["Account Type:"]
        reason = self.protest_entry.get(1.0, END)

        data = {"Username": username,
                "Account": account,
                "Issue": "Appeal",
                "Reason": reason,
                "Status": "Not Decided"}

        write_to_mailbox("Appeal", data)

        self.pop_up_success()

    def submit_protest(self):
        username = self.controller.user_data["Username:"]
        account = self.controller.user_data["Account Type:"]
        reason = self.protest_entry.get(1.0, END)

        data = {"Username": username,
                "Account": account,
                "Issue": "Protest",
                "Reason": reason,
                "Status": "Not Decided"}

        write_to_mailbox("Protest", data)

        self.pop_up_success()

    def list_box_double_clicked(self):
        project_labels = ["Project_Name:", "Developer:", "Client:", "Completed:", "OnTime:", "Bidding_Deadline:",
                          "Delivery_Deadline:", "Cost:", "ClientRating:", "DevRating:", "Tags:"]

        project_name = self.listbox.selection_get()
        # retrieving the project name. index = 0 as the name is found in the first index
        project_name = str(project_name.split()[0])
        myprojectinfo = get_project_by_name(project_name)

        popup = tk.Tk()
        popup.geometry("600x600")
        popup.resizable(False, False)
        popup.wm_title(project_name)

        # Display stuff in popup window
        i = 25
        for words in project_labels:
            entryText = StringVar(popup, value="default")
            e = Entry(popup, textvariable=entryText)
            print(myprojectinfo[words])
            label_values = str(myprojectinfo[words])
            entryText.set(label_values)
            e.configure(state="readonly")
            e.place(x=140, y=5 + i)
            lb = Label(popup, text=words)
            lb.place(x=30, y=5 + i)
            i += 30
        specification_label = Label(popup, text="Specification:")
        specification_label.place(x=35, y=415)

        specification_text = tkst.ScrolledText(popup, wrap=tk.WORD, width=55, height=12)
        specification_text.place(x=140, y=360)
        specification_text.insert(tk.INSERT, str(myprojectinfo["Specification:"]))
        specification_text.configure(state="disabled")

        B1 = ttk.Button(popup, text="Exit", command=popup.destroy)
        B1.place(x=270, y=560)

        if str(myprojectinfo["Completed:"]) == "Delivered" and str(myprojectinfo["Developer:"]) == \
                self.controller.user_data["Username:"] and myprojectinfo["DevRating:"] != "None":
            # Allow Developer to rate Client
            self.rate_button = ttk.Button(popup, text="Rate Client",
                                          command=lambda: self.submit_rating(project_name, popup))
            self.rate_button.place(x=350, y=28)
            self.rate_entry = Entry(popup)
            self.rate_entry.place(x=450, y=30)
        elif str(myprojectinfo["Completed:"]) == "Working on" and str(myprojectinfo["Developer:"]) == \
                self.controller.user_data["Username:"]:
            # Deliver on time
            self.deliver_ontime_button = ttk.Button(popup, text="Deliver On Time",
                                                    command=lambda: self.ontime_delivery(project_name, popup))
            self.deliver_ontime_button.place(x=350, y=60)

            # Deliver late
            self.deliver_late_button = ttk.Button(popup, text="Deliver Late",
                                                  command=lambda: self.late_delivery(project_name, popup))
            self.deliver_late_button.place(x=350, y=90)

            # Delivery Project on specific date
            self.deliver_project_button = ttk.Button(popup, text="Deliver Project",
                                                     command=lambda: self.deliver_project(project_name, popup))
            self.deliver_project_button.place(x=350, y=90 + 30)

            v = StringVar(popup, value='DD/MM/YYYY')
            self.deliver_project_entry = Entry(popup, textvariable=v)
            self.deliver_project_entry.place(x=450, y=90 + 30)
        elif str(myprojectinfo["Completed:"]) == "Open" and str(myprojectinfo["Developer:"]) == "None":
            # Allow Developer to bid
            self.bid_button = ttk.Button(popup, text="Bid", command=lambda: self.submit_bid(project_name))
            self.bid_button.place(x=350, y=30)
            v = StringVar(popup, value='Enter bid price')
            self.bid_entry = Entry(popup, textvariable=v)
            self.bid_entry.place(x=450, y=30)

            v = StringVar(popup, value='DD/MM/YYYY')
            self.promised_time_entry = Entry(popup, textvariable=v)
            self.promised_time_entry.place(x=450, y=60)

    def submit_rating(self, proj_name, popup):
        infodata = {}
        infodata["ClientRating:"] = self.rate_entry.get()
        infodata["Project_Name:"] = proj_name
        infodata["Completed:"] = "Completed"
        if (int(self.rate_entry.get()) < 1 or int(self.rate_entry.get()) > 5):
            messagebox.showerror("Error!", "Rate range 1-5 only please!")
        else:
            check_none = update_client_rating(infodata)
            myprojectinfo = get_project_by_name(proj_name)

            insert_into_ratings_given("developer", self.controller.user_data["Username:"], infodata["ClientRating:"])
            insert_into_ratings_received("client", myprojectinfo["Client:"], infodata["ClientRating:"])

            # update the entry box too
            entryText = StringVar(popup, value="default")
            e = Entry(popup, textvariable=entryText)
            label_values = str(myprojectinfo["ClientRating:"])
            entryText.set(label_values)
            e.configure(state="readonly")
            e.place(x=140, y=5 + 25 + (8 * 30))

            if int(self.rate_entry.get()) <= 2 and check_none != False:
                def pop_up_reason():
                    def leavemini():
                        popup.destroy()

                    popup = tk.Tk()
                    msg = "Please Enter Reason\nfor Low System Rating"
                    popup.wm_title("Reason!")
                    popup.geometry("250x100")
                    label = ttk.Label(popup, text=msg, font=SMALL_FONT)
                    label.pack(side="top", fill="x", pady=10)
                    B1 = ttk.Button(popup, text="Submit", command=leavemini)
                    B1.place(x=40, y=70)
                    ratingText = StringVar(popup, value="")
                    ratingEntry = Entry(popup, width=30, textvariable=ratingText)
                    ratingEntry.place(x=5, y=50)

                pop_up_reason()

    def deliver_project(self, project_name, popup):
        infodata = {}
        myprojectinfo = get_project_by_name(project_name)
        # bidding deadline
        bidding_deadline = str(myprojectinfo["Delivery_Deadline:"])
        # promised deadline
        delivery_date = str(self.deliver_project_entry.get())
        if (delivery_date <= bidding_deadline):
            self.ontime_delivery(project_name, popup)
        else:
            self.late_delivery(project_name, popup)

    def late_delivery(self, project_name, popup):
        infodata = {}
        infodata["OnTime:"] = "Late"
        infodata["Project_Name:"] = project_name
        infodata["Completed:"] = "Delivered"
        update_project_delivery(infodata)
        # update on time entry box
        myprojectinfo = get_project_by_name(project_name)
        entryText = StringVar(popup, value="default")
        e = Entry(popup, textvariable=entryText)
        label_values = str(myprojectinfo["OnTime:"])
        entryText.set(label_values)
        e.configure(state="readonly")
        e.place(x=140, y=5 + 25 + (4 * 30))
        # update completed entry box
        entryText2 = StringVar(popup, value="default")
        e2 = Entry(popup, textvariable=entryText2)
        label_values = str(myprojectinfo["Completed:"])
        entryText2.set(label_values)
        e2.configure(state="readonly")
        e2.place(x=140, y=5 + 25 + (3 * 30))
        # front money + fee goes to client
        my_bid = get_my_bid(project_name, self.controller.user_data["Username:"])
        front_money = my_bid / 2
        fee = front_money * 0.05
        money_to_client = front_money + fee
        client_name = get_my_client(project_name)
        print(client_name)
        send_funds_to_user("client", client_name, money_to_client)
        subtract_from_funds("developer", self.controller.user_data["Username:"], money_to_client)

    def ontime_delivery(self, project_name, popup):
        infodata = {}
        infodata["OnTime:"] = "On time"
        infodata["Project_Name:"] = project_name
        infodata["Completed:"] = "Delivered"
        update_project_delivery(infodata)
        # update on time entry box
        myprojectinfo = get_project_by_name(project_name)
        entryText = StringVar(popup, value="default")
        e = Entry(popup, textvariable=entryText)
        label_values = str(myprojectinfo["OnTime:"])
        entryText.set(label_values)
        e.configure(state="readonly")
        e.place(x=140, y=5 + 25 + (4 * 30))
        # update completed entry box
        entryText2 = StringVar(popup, value="default")
        e2 = Entry(popup, textvariable=entryText2)
        label_values = str(myprojectinfo["Completed:"])
        entryText2.set(label_values)
        e2.configure(state="readonly")
        e2.place(x=140, y=5 + 25 + (3 * 30))

    def submit_bid(self, proj_name):
        if (int(self.bid_entry.get()) < 1):
            messagebox.showerror("O.O", "O.O staph trollin pls!")
        else:
            infodata = {self.controller.user_data["Username:"]: self.bid_entry.get()}
            update_bid_list(infodata, proj_name)

            infodata2 = {}
            infodata2["Bidding_Deadline:"] = self.promised_time_entry.get()
            print(infodata2["Bidding_Deadline:"])
            update_bid_deadline(infodata2, proj_name)


class SuperLogin(tk.Frame):
    # Initialize the page
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Create login page label
        label = tk.Label(self, text="SuperUser Login Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        # Create button for user to get back to homepage
        viewhome_button = ttk.Button(self, text="View Home Page",
                                     command=lambda: controller.show_frame(StartPage))
        viewhome_button.pack()
        viewhome_button.place(relx=1.0, y=0, anchor="ne")

        # Create entry for user to input username and password
        self.entry = {}
        self.data = {}
        self.userLabel = ttk.Label(self, text="Username:")
        self.userLabel.place(x=30, y=50)
        self.passLabel = ttk.Label(self, text="Password:")
        self.passLabel.place(x=30, y=75)

        self.userEntry = ttk.Entry(self, textvariable=StringVar())
        self.userEntry.place(x=120, y=50)

        self.passEntry = ttk.Entry(self, show="*", textvariable=StringVar())
        self.passEntry.place(x=120, y=75)
        # Create login button for user to submit their login credentials
        self.b = ttk.Button(self, text="Submit Login Credentials", command=lambda: self.submit_info())
        self.b.place(x=105, y=125)

        # Popup success when username and password matched

    def login_sucess(self):
        messagebox.showinfo("Login Successfully!", "Welcome back, Super User")
        self.controller.show_frame(SuperUserPage)

        # Submit the information, called when user pressed the login button

    def submit_info(self):
        # Check if the input is empty
        if self.userEntry.get == '' or self.passEntry.get() == '':
            messagebox.showerror("Error", 'Invalid Input!')
        else:
            # Get user input
            username = self.userEntry.get()
            password = self.passEntry.get()
            # Call the check function, act as a boolean value
            check = check_su_data(username, password)
            # Yes, popup success page, empty the entry box
            if check:
                self.login_sucess()
                self.userEntry.delete(0, END)
                self.passEntry.delete(0, END)
            # Print error when don't
            else:
                self.userEntry.delete(0, END)
                self.passEntry.delete(0, END)
                messagebox.showerror("Login Failed", "Your username or password is wrong! Try again")


class SuperUserPage(tk.Frame):
    # Initialize the page
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Create the listbox to show the mailbox items with scrollbar
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.listbox = Listbox(self, height=35, width=95, font=LARGE_FONT, yscrollcommand=self.scrollbar.set)
        self.controller = controller
        # Show total money system have earned by checking the Superuser data
        self.system_money = get_system_money()
        self.sys_money = tk.Label(self, text='System Revenue: ' + str(self.system_money), font=SMALL_FONT)
        self.sys_money.place(x=40, y=150)
        # Homepage label
        label = tk.Label(self, text="SuperUser Homepage", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        # Mailbox label
        label2 = tk.Label(self, text="Mailbox", font=LARGE_FONT)
        label2.place(x=40, y=180)
        # Log out button
        Log_out_button = ttk.Button(self, text="Log out",
                                    command=self.logout)
        Log_out_button.place(relx=1.0, y=0, anchor="ne")
        # Button for remove the mailbox item
        delete_button = ttk.Button(self, text='Remove', command=self.remove_item)
        delete_button.place(x=200, y=180)
        # Button for refresh the mailbox item
        refresh_button = ttk.Button(self, text='Refresh', command=self.refresh_listbox)
        refresh_button.place(x=120, y=180)
        # Create searchbar for searching the mailbox data
        placeHolder = StringVar(self, value="")
        self.searchBar = Entry(self, textvariable=placeHolder, width=30)
        self.searchBar.place(x=250, y=80, width=550)
        # Some buttons I declare as self if I need to perform actions with that button in another function
        searchButton = ttk.Button(self, text="Search", command=self.search)
        searchButton.place(x=168, y=75)
        # Bind listbox when user double click the item, and popup window for each type of items
        self.listbox.bind('<Double-1>', self.doubleclick)
        # Mail item initializer, for the popup window
        self.mail = ['Appeal', 'Apply', 'Money', 'Protest', 'Quit']
        self.mail_items = ['Issue', 'Account', 'Username', 'Status']
        self.money_items = ['Issue', 'Projects', 'Client', 'Developer', 'Money_holds', 'Rating']
        self.apply_items = ['Issue', "Account", "Username", "Password:", "Funds:", 'Status']
        self.after_money_done = ['Issue', 'Projects', 'Client', 'Developer', 'Rating', 'Client_received',
                                 'Developer_received']
        # Populate the listbox with mail items
        self.create_listbox()
        self.listbox_populate()
        # Search listbox function

    def search(self):
        # Check when input is empty
        if self.searchBar.get() == '':
            messagebox.showerror("Error", "Invalid Input!")
        else:
            # Empty the listbox
            self.listbox.delete(0, END)
            # Getting the data
            data = search_mail_data(self.searchBar.get())
            # Using the data got and populate hte listbox
            for x in range(len(data)):
                # When issue about money, as only money problem involve project
                if data[x]['Issue'] == 'Money':
                    self.listbox.insert(END, 'Issue:  ' + data[x]['Issue'] + ' ,  Project:  ' + data[x][
                        'Projects'] + ' ,  Client:  ' + data[x][
                                            'Client'] + ' ,  Developer  ' + data[x]['Developer'])
                    if data[x]['Status'] != 'Not Decided':
                        self.listbox.itemconfig(END, {'fg': 'gray'})
                # When about all other issues
                else:
                    self.listbox.insert(END, 'Issue:  ' + data[x]['Issue'] + ' ,  Account_type:  ' + data[x][
                        'Account'] + ' ,  Username:  ' + data[x]['Username'])
                    if data[x]['Status'] != 'Not Decided':
                        self.listbox.itemconfig(END, {'fg': 'gray'})

    # Refresh listbox function
    def refresh_listbox(self):
        # Empty the listbox
        self.listbox.delete(0, END)
        # Refresh the system earning
        self.system_money = get_system_money()
        self.sys_money = tk.Label(self, text='System Revenue: ' + str(self.system_money), font=SMALL_FONT)
        self.sys_money.place(x=40, y=150)
        # Populate the listbox with all data in the mailbox database
        self.listbox_populate()

    # Populate the listbox with all the data in the mailbox database
    def listbox_populate(self):
        with open('mailbox') as json_file:
            data = json.load(json_file)

        for words in self.mail:
            for names in data[words]:
                if names['Issue'] == 'Money':
                    self.listbox.insert(END, 'Issue:  ' + names['Issue'] + ' ,  Project:  ' + names[
                        'Projects'] + ' ,  Client:  ' + names[
                                            'Client'] + ' ,  Developer  ' + names['Developer'])
                    if names['Status'] != 'Not Decided':
                        self.listbox.itemconfig(END, {'fg': 'gray'})
                else:
                    self.listbox.insert(END, 'Issue:  ' + names['Issue'] + ' ,  Account_type:  ' + names[
                        'Account'] + ' ,  Username:  ' + names['Username'])
                    if names['Status'] != 'Not Decided':
                        self.listbox.itemconfig(END, {'fg': 'gray'})

    # Log out function
    def logout(self):
        # Popup window to ask user if they want to log out
        result = messagebox.askquestion("Confirmation", "Are you sure you want to log out?")
        if result == 'yes':
            self.controller.show_frame(StartPage)
        # If not, don't do anything
        else:
            pass

    # Remove the listbox items
    def remove_item(self):
        # Get the index of what user is selecting
        index = self.listbox.curselection()
        # Get the mail item's data in the index
        selection = self.listbox.selection_get()
        main_type = selection.split()[1]
        project_name = selection.split()[4]
        username = selection.split()[7]
        # Delete from the database
        # Using project name as identifier when issue is about money
        if main_type == 'Money':
            db_remover(main_type, 'Projects', project_name, 'mailbox')
        # Using username otherwise
        else:
            db_remover(main_type, 'Username', username, 'mailbox')
        # Delete from the listbox
        self.listbox.delete(index)

    # The core of the whole page, showing information when double clicked the corresponding mail items
    def doubleclick(self, event):
        # Accept button pressed
        def accept():
            # Deal with all different scenarios
            if main_type == 'Apply':
                # Get the reason from the reason entry box and insert them temp user database lastly popup window to
                # indicate the action has be done
                reason = reason_text.get(1.0, END)
                reason_changer(main_type, username, reason)
                temp_data_changer(username, reason, 'Accepted')
                messagebox.showinfo("Success! ", 'Application accepted')
                # Decrement the warning
            elif main_type == 'Appeal' and account_type == 'Client':
                messagebox.showinfo("Success! ", 'Appeal accepted')
                warning_minus(username, 'client_login.txt')
            elif main_type == 'Appeal' and account_type == 'Developer':
                messagebox.showinfo("Success! ", 'Appeal accepted')
                warning_minus(username, 'developer_login.txt')
                # Delete user from databse
            elif main_type == 'Quit' and account_type == 'Client':
                messagebox.showinfo("Success! ", 'Quit accepted')
                remove_user(username, 'client_login.txt')
            elif main_type == 'Quit' and account_type == 'Developer':
                messagebox.showinfo("Success! ", 'Quit accepted')
                remove_user(username, 'developer_login.txt')
                # Remove user from blacklist and decrement their warning counter
            elif main_type == 'Protest' and account_type == 'Client':
                remove_user(username, 'blacklist.txt')
                warning_minus(username, 'client_login.txt')
                messagebox.showinfo("Success! ", 'Protest accepted')
            elif main_type == 'Protest' and account_type == 'Developer':
                remove_user(username, 'blacklist.txt')
                warning_minus(username, 'developer_login.txt')
                messagebox.showinfo("Success! ", 'Protest accepted')
            # Storing action for history
            status_changer(main_type, 'Username', username, 'Accepted')
            # Makes the items gray to indicate viewed
            self.listbox.itemconfig(item, {'fg': 'gray'})
            popup.destroy()

        # Decline button pressed
        def decline():
            # If it's application, change the data in temp user database
            if main_type == 'Apply':
                reason = reason_text.get(1.0, END)
                reason_changer(main_type, username, reason)
                temp_data_changer(username, reason, 'Rejected')
                messagebox.showinfo("Success! ", 'Application rejected')
            # Stroing history
            status_changer(main_type, 'Username', username, 'Rejected')
            self.listbox.itemconfig(item, {'fg': 'gray'})
            messagebox.showinfo("Success! ", 'Request rejected')
            popup.destroy()

        # Send money function
        def send_money():
            # Check for empty input
            if m_send.get() == '':
                messagebox.showerror("Error", 'Invalid input!')
            else:
                # Rounding the input to 2 digit after decimal as its about money
                amount = round(float(m_send.get()), 2)
                # Check if the input is negative, greater than max or 0
                holding_left = money_data['Money_holds']
                if holding_left < amount or holding_left == 0 or amount < 0:
                    messagebox.showerror("Error", 'Invalid input!')
                # Send the money, change the status for storing history
                else:
                    money_sender(project_name, amount)
                    status_changer(main_type, 'Projects', project_name, 'Sent')
                    messagebox.showinfo("Success! ", 'Money Sent!')
                    self.listbox.itemconfig(item, {'fg': 'gray'})
                    popup.destroy()

        # Create labels for popup window
        def create_labels(labels, data):
            # Reading the data from the database and use for loop to generate label line by line
            i = 25
            for words in labels:
                entryText = StringVar(popup, value="default")
                e = Entry(popup, textvariable=entryText)
                label_values = str(data[words])
                entryText.set(label_values)
                e.configure(state="readonly")
                e.place(x=140, y=5 + i)
                lb = Label(popup, text=words)
                lb.place(x=30, y=5 + i)

                i += 30

        # Those are popup window creators
        # When issue is not about money and application
        def mail():
            # Create labels
            create_labels(self.mail_items, mail_data)
            # Using ScrolledText from tkinter in order to provide a paragraph container for specifications
            # to be displayed
            reason_label = Label(popup, text="Reason:")
            reason_label.place(x=30, y=150)
            reason_text = tkst.ScrolledText(popup, wrap=tk.WORD, width=50, height=12)
            reason_text.place(x=30, y=180)
            reason_text.insert(tk.INSERT, str(mail_data['Reason']))
            reason_text.configure(state="disabled")
            # Accept and decline button
            B1 = ttk.Button(popup, text="Accept", command=accept)
            B1.place(x=85, y=360)
            B2 = ttk.Button(popup, text="Decline", command=decline)
            B2.place(x=230, y=360)
            # If action has be done, destroy the button so user can no longer access them
            if mail_data['Status'] != 'Not Decided':
                B1.destroy()
                B2.destroy()

        # When issue is regarding the money
        def money():
            if money_data['Status'] == 'Not Decided':
                create_labels(self.money_items, money_data)
                m_label = Label(popup, text='Send Amount')
                m_label.place(x=30, y=215)

                B1 = ttk.Button(popup, text="Send", command=send_money)
                B1.place(x=85, y=260)
                B2 = ttk.Button(popup, text="Cancel", command=popup.destroy)
                B2.place(x=230, y=260)
            elif money_data['Status'] != 'Not Decided':
                m_send.destroy()
                create_labels(self.after_money_done, money_data)

        # When issue about temp user application
        def apply():
            create_labels(self.apply_items, mail_data)
            reason_label = Label(popup, text="Reason:")
            reason_label.place(x=30, y=210)
            reason_text.insert(tk.INSERT, str(mail_data['Reason']))

            B1 = ttk.Button(popup, text="Accept", command=accept)
            B1.place(x=85, y=420)
            B2 = ttk.Button(popup, text="Decline", command=decline)
            B2.place(x=230, y=420)
            if mail_data['Status'] != 'Not Decided':
                B1.destroy()
                B2.destroy()
                reason_text.configure(state="disabled")

        # Get the current selection information so can decide for popup different windows
        item = self.listbox.curselection()
        selection = self.listbox.selection_get()
        main_type = selection.split()[1]
        project_name = selection.split()[4]
        account_type = selection.split()[4]
        username = selection.split()[7]

        # Create popup window
        popup = tk.Tk()

        if main_type == 'Apply':
            # Get the actual data by going to database (as listbox only store basic inforamtion for viewing purpose)
            mail_data = get_mail_by_name(main_type, 'Username', username)
            reason_text = tkst.ScrolledText(popup, wrap=tk.WORD, width=50, height=12)
            reason_text.place(x=30, y=240)
            popup.geometry("400x470")
            apply()

        elif main_type == 'Money':
            money_data = project_by_name(project_name)
            popup.geometry("400x300")
            # Money sending entry
            m_send = Entry(popup, textvariable=int)
            m_send.place(x=140, y=215)
            money()
        else:
            mail_data = get_mail_by_name(main_type, 'Username', username)
            popup.geometry("400x400")
            mail()

        popup.resizable(False, False)
        # Popup title
        popup.wm_title(main_type)
        # Window popup
        popup.mainloop()

        # Make the listbox appear

    def create_listbox(self):

        self.listbox.pack()
        self.listbox.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)


app = PrototypeApp()
app.geometry("1024x768")

# app.resizable(False,False)
app.mainloop()
