import json
from tkinter import messagebox
import datetime


def write_to_register(data):
    with open('temp_login.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = []

    db.append(data)

    with open('temp_login.txt', 'r+', encoding='utf-8') as outfile:
        json.dump(db, outfile, indent=4)
        print("Data Received Successfully")

    return True


def write_to_logged(data):
    with open('logged_in.txt', 'w') as f:
        f.write(json.dumps(data, indent=4))
        print("Data Received Successfully")

    return True


def write_to_user(data, user):
    with open(user + '_login.txt') as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []
    db.append(data)
    with open(user + '_login.txt', 'r+', encoding='utf-8') as outfile:
        json.dump(db, outfile, indent=4)
        print("Data Received Successfully")
    return True


def check_register_exists(data):
    with open('temp_login.txt') as f:
        try:
            db = json.load(f)
            print("\nThis was db")
        except ValueError:
            db = []

    for x in range(len(db)):
        if (db[x]["Username:"]) == data["Username:"] \
                or data["Funds:"] == "" or data["Username:"] == "" or data["Password:"] == "" \
                or data["Account Type:"] == "":
            print("Duplicate found!")
            msg = "1) You either didn't fill all entries or... \n" \
                  "2) Your username/email already exists!"
            return True, msg

    print("No duplicates!")
    return False, None


def check_user_login(data, user):
    with open(user + '_login.txt') as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db)):
        if (db[x]["Username:"]) == data["Username:"] and (db[x]["Password:"]) == data["Password:"]:
            print("Login Successful!")
            return True, db[x], None
    print("Login Failed!")
    msg = "1) Your username/password is incorrect or... \n" \
          "2) You've selected the wrong login page"
    return False, None, msg


def check_blacklist(data, user):
    with open('blacklist.txt') as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db)):
        if (db[x]["Username:"]) == data["Username:"] \
                and (db[x]["Account Type:"]) == user:
            msg = "This account has been BlackListed."
            return True, msg
    print("Not BlackListed.")
    return False, None


def check_temp(data, user):
    with open('temp_login.txt') as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db)):

        if db[x]["Account Type:"] == user and db[x]["Username:"] == data["Username:"]:
            if (db[x]["Status:"]) == "Accepted":
                return False, db[x], None
            if (db[x]["Status:"]) == "Rejected":
                msg = "SuperUser rejected your application, reason:  \n " + db[x]['Reason:']
                return True, None, msg
            if (db[x]["Status:"]) == "Not Decided":
                return True, None, "Account Awaiting Approval"

    msg = "1) Your username/password is incorrect or... \n" \
          "2) You've selected the wrong login page"
    return True, None, msg


def get_list_of_projects():
    projectlist = []

    with open("projects_db.txt") as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []
    # Just iterating through the list of projects and finding each and every one.
    for x in range(len(db["Projects"])):
        projectlist.append(str(db["Projects"][x]["Project_Name:"]) + " " + str(db["Projects"][x]["Tags:"]))

    return projectlist


def get_sorted_tags(tags):
    projectlist = []

    with open("projects_db.txt") as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db["Projects"])):
        # Finding if there is a match between the provided list of tag arguments and tags within projects
        if set(tags) & set(db["Projects"][x]["Tags:"]) or (db["Projects"][x]["Developer:"] in tags) \
                or (db["Projects"][x]["Client:"] in tags):
            projectlist.append(
                str(db["Projects"][x]["Project_Name:"]) + " " + str(db["Projects"][x]["Tags:"]) + " " + str(
                    db["Projects"][x]["Completed:"]))

    return projectlist


def get_project_by_name(name):
    with open("projects_db.txt") as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db["Projects"])):
        if db["Projects"][x]["Project_Name:"] == name:
            project = db["Projects"][x]
            return project


def get_unbidprojects_by_name(name):
    print(name)

    unbid_projects = []

    with open("projects_db.txt") as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db["Projects"])):
        if db["Projects"][x]["Client:"] == name and db["Projects"][x]["Developer:"] == "None" \
                and len(db["Projects"][x]["Bidders:"].values()) != 0:
            bidders = db["Projects"][x]["Bidders:"].items()
            print(bidders)
            bidders = db["Projects"][x]["Bidders:"]
            print(bidders)
            bid_tuple = sorted(bidders.items(), key=lambda x: x[1])
            print(bid_tuple)

            unbid_projects.append(str(db["Projects"][x]["Project_Name:"]) + " (" + str(bid_tuple[0][0]) + " $" +
                                  str(bid_tuple[0][1]) + ")")

    return unbid_projects


def get_delivered_by_user(name):
    delivered_projects = []

    with open("projects_db.txt") as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db["Projects"])):
        if db["Projects"][x]["Client:"] == name and db["Projects"][x]["Completed:"] == "Delivered" \
                and (db["Projects"][x]["OnTime:"] == "On time" or db["Projects"][x]["OnTime:"] == "Late") and \
                db["Projects"][x]["DevRating:"] == "None":
            delivered_projects.append(str(db["Projects"][x]["Project_Name:"]))

    return delivered_projects


def write_to_project_db(data):
    with open('projects_db.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db['Projects'] = []

    db['Projects'].append(data)

    with open('projects_db.txt', 'r+', encoding='utf-8') as outfile:
        json.dump(db, outfile, indent=4)
        print("Data Received Successfully")

    return True


def check_duplicate_project(projectname):
    with open('projects_db.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db['Projects'] = []

    if len(db["Projects"]) > 0:
        for x in range(len(db["Projects"])):
            if (db["Projects"][x]["Project_Name:"]) == projectname:
                print("Duplicate found!")
                return True

    print("No duplicates!")
    return False


def sort_bidders_by_price(project_name):
    with open('projects_db.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db['Projects'] = []

    for x in range(len(db["Projects"])):
        if (db["Projects"][x]["Project_Name:"]) == project_name:
            bidders = db["Projects"][x]["Bidders:"]
            bid_tuple = sorted(bidders.items(), key=lambda x: x[1])
            return bid_tuple


def update_project_with_new_bidder(project_name, bidder_name, reason):
    with open('projects_db.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db['Projects'] = []

    with open('projects_db.txt', 'w') as f:
        for x in range(len(db["Projects"])):
            if (db["Projects"][x]["Project_Name:"]) == project_name:
                new_dev = {"Developer:": bidder_name}
                new_status = {"Completed:": "Working on"}
                db["Projects"][x].update(new_status)
                db["Projects"][x].update(new_dev)
                db["Projects"][x].update(reason)
                f.write(json.dumps(db, indent=4))
                print("Successfully edited!")
                return True


def get_list_of_bidders(project_name):
    with open("projects_db.txt") as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db["Projects"])):
        if db["Projects"][x]["Project_Name:"] == project_name:
            bidders = db["Projects"][x]["Bidders:"].items()
            print(bidders)
            bidders = db["Projects"][x]["Bidders:"]
            bid_tuple = sorted(bidders.items(), key=lambda x: x[1])
            return list(bid_tuple)


def send_funds_to_user(account, username, funds):
    with open(account + '_login.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = []

    with open(account + '_login.txt', 'w+', encoding='utf-8') as outfile:
        for x in range(len(db)):
            if db[x]["Username:"] == username:
                curr_fund = int(db[x]["Funds:"])
                new_funds = curr_fund + int(funds)
                data = {"Funds:": new_funds}
                db[x].update(data)
                print(db[x])
                json.dump(db, outfile, indent=4)
                print("Complete")


def subtract_from_funds(account, username, funds):
    with open(account + '_login.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = []

    with open(account + '_login.txt', 'w+', encoding='utf-8') as outfile:
        for x in range(len(db)):
            if db[x]["Username:"] == username:
                curr_fund = int(db[x]["Funds:"])
                new_funds = curr_fund - int(funds)
                data = {"Funds:": new_funds}
                db[x].update(data)
                print(db[x])
                json.dump(db, outfile, indent=4)


def give_rating_to_dev(project_name, rating):
    with open('projects_db.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db['Projects'] = []

    with open('projects_db.txt', 'w') as f:
        for x in range(len(db["Projects"])):
            if (db["Projects"][x]["Project_Name:"]) == project_name:
                DevRating = {"DevRating:": rating}
                db["Projects"][x].update(DevRating)
                f.write(json.dumps(db, indent=4))
                print("Successfully Rated!")
                return True


def user_history_rating(account, username):
    with open(account + '_login.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = []

    with open(account + '_login.txt', 'w+', encoding='utf-8') as f:
        for x in range(len(db)):
            if db[x]["Username:"] == username:
                ratings_given = db[x]["Ratings_Given:"]
                f.write(json.dumps(db, indent=4))
                return len(ratings_given), ratings_given


def user_history_received(account, username):
    with open(account + '_login.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = []

    with open(account + '_login.txt', 'w+', encoding='utf-8') as f:
        for x in range(len(db)):
            if db[x]["Username:"] == username:
                ratings_received = db[x]["Ratings_Received:"]
                f.write(json.dumps(db, indent=4))
                return len(ratings_received), ratings_received


def insert_into_ratings_given(account, username, rating):
    with open(account + '_login.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = []

    with open(account + '_login.txt', 'w+', encoding='utf-8') as f:
        for x in range(len(db)):
            if db[x]["Username:"] == username:
                db[x]["Ratings_Given:"].append(rating)
                db[x].update()
                f.write(json.dumps(db, indent=4))


def insert_into_ratings_received(account, username, rating):
    with open(account + '_login.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = []

    with open(account + '_login.txt', 'w+', encoding='utf-8') as f:
        for x in range(len(db)):
            if db[x]["Username:"] == username:
                db[x]["Ratings_Received:"].append(rating)
                db[x].update()
                f.write(json.dumps(db, indent=4))


def increment_warn_count(account, username):
    with open(account + '_login.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = []

    with open(account + '_login.txt', 'w+', encoding='utf-8') as f:
        for x in range(len(db)):
            if db[x]["Username:"] == username:
                db[x]["Warn_Count:"] += 1
                db[x].update()
                f.write(json.dumps(db, indent=4))


def increment_warn_count2(account, username):
    with open(account + '_login.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = []

    with open(account + '_login.txt', 'w+', encoding='utf-8') as f:
        for x in range(len(db)):
            if db[x]["Username:"] == username:
                db[x]["Warn_Count:"] += 1
                db[x]["Login_Warned:"] = "True"
                db[x].update()
                f.write(json.dumps(db, indent=4))


def get_user_total_warns(account, username):
    with open(account + '_login.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = []

    with open(account + '_login.txt', 'w+', encoding='utf-8') as f:
        for x in range(len(db)):
            if db[x]["Username:"] == username:
                f.write(json.dumps(db, indent=4))
                return db[x]["Warn_Count:"]


def update_project_stuff(data):
    with open('projects_db.txt') as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db["Projects"])):
        if (db["Projects"][x]["Project_Name:"] == data["Project_Name:"]):
            db["Projects"][x].update(data)

    with open('projects_db.txt', 'w', encoding='utf-8') as outfile:
        json.dump(db, outfile, indent=4)
        print("Client Rating updated Successfully")


def test_print_bidder():
    with open('projects_db.txt') as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db["Projects"])):
        if (db["Projects"][x]["Project_Name:"] == "Project_Three"):
            print(db["Projects"][x]["Bidders:"])


def update_bid_deadline(data, proj_name):
    with open('projects_db.txt') as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db["Projects"])):
        if (db["Projects"][x]["Project_Name:"] == proj_name):
            db["Projects"][x].update(data)

    with open('projects_db.txt', 'w', encoding='utf-8') as outfile:
        json.dump(db, outfile, indent=4)
        print("Bid deadline updated Successfully")


def update_bid_list(data, proj_name):
    with open('projects_db.txt') as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []
    print(proj_name)

    for x in range(len(db["Projects"])):
        if (db["Projects"][x]["Project_Name:"] == proj_name):
            db["Projects"][x]["Bidders:"].update(data)

    with open('projects_db.txt', 'w', encoding='utf-8') as outfile:
        json.dump(db, outfile, indent=4)
        print("Bidlist updated Successfully")


def get_list_of_projecterino():
    projectlist = []

    with open("projects_db.txt") as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []
    # Just iterating through the list of projects and finding each and every one.
    for x in range(len(db["Projects"])):
        try:
            projectlist.append(
                str(db["Projects"][x]["Project_Name:"]) + " " + str(db["Projects"][x]["Tags:"]) + " " + str(
                    db["Projects"][x]["Completed:"]))
        except KeyError:
            projectlist.append("")

    return projectlist


# Check superuser data with user input
def check_su_data(username, password):
    # Open the database
    with open('super_user.txt') as json_file:
        try:
            data = json.load(json_file)
        except ValueError:
            data['SuperUser'] = []
    # Matching the username and password, return boolean
    for p in data["SuperUser"]:
        if p["Username:"] == username and p["Password"] == password:
            return True
    return False


def submit_low_sysrate_reason(project, rating, reason):
    with open('projects_db.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db['Projects'] = []

    with open('projects_db.txt', 'w') as f:
        for x in range(len(db["Projects"])):
            if (db["Projects"][x]["Project_Name:"]) == project:
                sysRating = {"SystemRating:": rating}
                rateReason = {"Rate_Reason:": reason}
                db["Projects"][x].update(sysRating)
                db["Projects"][x].update(rateReason)
                f.write(json.dumps(db, indent=4))
                print("Successfully Rated!")
                return True


def write_to_mailbox(location, data):
    with open('mailbox') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = {}

    db[location].append(data)

    with open('mailbox', 'w+', encoding='utf-8') as outfile:
        json.dump(db, outfile, indent=4)
        print("Data Received Successfully")
    return True


def add_project_to_user(account, username, project_name):
    with open(account + '_login.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = {}

    for x in range(len(db)):
        if db[x]["Username:"] == username:
            db[x]["Projects:"].append(project_name)
            print(db[x]["Projects:"])
            with open(account + '_login.txt', 'w+', encoding='utf-8') as outfile:
                json.dump(db, outfile, indent=4)
                return


def update_client_rating(data):
    with open('projects_db.txt') as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db["Projects"])):
        if (db["Projects"][x]["Project_Name:"] == data["Project_Name:"]):
            if (db["Projects"][x]["ClientRating:"] == "None"):
                db["Projects"][x].update(data)
            else:
                messagebox.showerror("Error", "You rated already!")

    with open('projects_db.txt', 'w', encoding='utf-8') as outfile:
        json.dump(db, outfile, indent=4)
        print("Client Rating updated Successfully")


def update_project_delivery(data):
    with open('projects_db.txt') as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db["Projects"])):
        if (db["Projects"][x]["Project_Name:"] == data["Project_Name:"]):
            if (db["Projects"][x]["OnTime:"] == "None"):
                db["Projects"][x].update(data)
            else:
                messagebox.showerror("Error", "You delivered your project already!")

    with open('projects_db.txt', 'w', encoding='utf-8') as outfile:
        json.dump(db, outfile, indent=4)
        print("Project delivery updated Successfully")


# Delete data from the database(actually only used for mailbox)
# User input the main_type(issue type),input type(project name or username), input and text file name
def db_remover(main_type, target_type, target, text_file_name):
    with open(text_file_name) as json_file:
        try:
            db = json.load(json_file)
        except ValueError:
            print('Target not found!')
        # Indicate the remove item index
        i = 0
        # If not target, go to next item
        for words in db[main_type]:
            if words[target_type] != target:
                i += 1
            # Delete the target with their parents
            elif words[target_type] == target:
                del db[main_type][i]
                break

    open(text_file_name, 'w').write(
        json.dumps(db, indent=4)
    )


# Mailbox data getter with matching username
def get_mail_by_name(main_type, target_type, target):
    with open('mailbox') as json_file:
        db = json.load(json_file)

    for words in db[main_type]:
        if words[target_type] == target:
            mail = words
            return mail


# Change the mailbox status
def status_changer(main_type, target_type, target, result):
    with open('mailbox') as json_file:
        db = json.load(json_file)

    for words in db[main_type]:
        if words[target_type] == target:
            words['Status'] = result
            break

    open('mailbox', 'w').write(
        json.dumps(db, indent=4)
    )


# Send the money
def money_sender(target, money_send):
    with open('mailbox') as json_file:
        db = json.load(json_file)

    for words in db['Money']:
        if words['Projects'] == target:
            # Calculating the amount of money to be send to each user with 5% tax
            # Add to system money
            money_adder_su('SuperUser', 'test123', round(words['Money_holds'] * 0.05, 2), 'super_user.txt')
            words['Money_holds'] -= money_send
            client_money = round(words['Money_holds'] * 0.95, 2)
            dev_money = round(money_send * 0.95, 2)
            words['Client_received'] = client_money
            words['Developer_received'] = dev_money
            # Add to client and developer funds
            money_adder(words['Client'], client_money, 'client_login.txt')
            money_adder(words['Developer'], dev_money, 'developer_login.txt')
            break

    open('mailbox', 'w').write(
        json.dumps(db, indent=4)
    )


# Get project data by project name
def project_by_name(target):
    with open('mailbox') as json_file:
        db = json.load(json_file)

    for words in db['Money']:
        if words['Projects'] == target:
            return words
            break


# Change the reason attribute
def reason_changer(main_type, target, result):
    with open('mailbox') as json_file:
        db = json.load(json_file)

    for words in db[main_type]:
        if words['Username'] == target:
            words['Reason'] = result
            break

    open('mailbox', 'w').write(
        json.dumps(db, indent=4)
    )


def get_funds_of_user(account, name):
    with open(account + '_login.txt') as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db)):
        if (db[x]["Username:"]) == name:
            return db[x]["Funds:"]


def remove_projects_no_bids(username):
    removed = 0;
    with open("projects_db.txt") as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db["Projects"])):
        # Finding if there is a match between the provided list of tag arguments and tags within projects
        try:
            d1 = datetime.datetime.strptime((db["Projects"][x]["Bidding_Deadline:"]), "%m/%d/%Y").date()
            d2 = datetime.datetime.now()
            d2 = d2.date()

            if len(db["Projects"][x]["Bidders:"]) == 0:
                if d1 < d2 and db["Projects"][x]["Client:"] == username:
                    removed = removed + 1
                    del db["Projects"][x]
            db.update()
            open("projects_db.txt", 'w').write(json.dumps(db, indent=4))
        except KeyError:
            return 0

    return removed


def add_to_blacklist(data_dict):
    with open('blacklist.txt') as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = {}

    db.append(data_dict)

    with open('blacklist.txt', 'w+', encoding='utf-8') as outfile:
        json.dump(db, outfile, indent=4)
        print("Data Received Successfully")
    return True


def get_clients_with_most_projects(account):
    client_list = []
    projects_total = []

    with open(account + "_login.txt") as f:
        try:
            db = json.load(f)
        except:
            pass

    if account == "client":
        for x in range(len(db)):
            client_list.append(db[x]["Username:"])
            projects_total.append(len(db[x]["Projects:"]))

        return list(zip(client_list, projects_total)), "client"

    else:
        for x in range(len(db)):
            client_list.append(db[x]["Username:"])
            projects_total.append(int(db[x]["Funds:"]))

        return list(zip(client_list, projects_total)), "developer"


def get_total_acc_type(account):
    with open(account + "_login.txt") as f:
        try:
            db = json.load(f)
        except:
            pass

    return len(db)


# Searching the mailbox
def search_mail_data(target):
    with open('mailbox') as json_file:
        db = json.load(json_file)
    mail_get = []
    mail = ['Appeal', 'Apply', 'Money', 'Protest', 'Quit']
    for words in mail:
        # Got all the data and check specific fields to see if they match the input
        if words == 'Money':
            for x in range(len(db['Money'])):
                if db['Money'][x]['Projects'] == target or \
                        db['Money'][x]['Client'] == target or \
                        db['Money'][x]['Developer'] == target or \
                        db['Money'][x]['Issue'] == target:
                    mail_get.append(db['Money'][x])
        elif words == 'Apply':
            for x in range(len(db['Apply'])):
                if db['Apply'][x]['Username'] == target or \
                        db['Apply'][x]['Account'] == target or \
                        db['Apply'][x]['Issue'] == target:
                    mail_get.append(db['Apply'][x])
        else:
            for x in range(len(db[words])):
                if db[words][x]['Username'] == target or \
                        db[words][x]['Account'] == target or \
                        db[words][x]['Issue'] == target:
                    mail_get.append(db[words][x])

    return mail_get


# Adding the money to the system db
def money_adder_su(main_type, target, amount, text_file_name):
    with open(text_file_name) as json_file:
        db = json.load(json_file)
    for words in db[main_type]:
        if words['Username:'] == target:
            words['Funds:'] += amount
            break
    open(text_file_name, 'w').write(
        json.dumps(db, indent=4)
    )


# General money adder
def money_adder(username, amount, textfile_name):
    with open(textfile_name) as json_file:
        db = json.load(json_file)
    for x in range(len(db)):
        if db[x]["Username:"] == username:
            db[x]['Funds:'] += round(amount, 2)
            break

    open(textfile_name, 'w').write(
        json.dumps(db, indent=4)
    )


# Decrement the warning counter by one
def warning_minus(username, textfile_name):
    with open(textfile_name) as json_file:
        db = json.load(json_file)
    for x in range(len(db)):
        if db[x]['Username:'] == username:
            # Check if greater than 0
            if db[x]['Warn_Count:'] > 0:
                db[x]['Warn_Count:'] -= 1
                break
    open(textfile_name, 'w').write(
        json.dumps(db, indent=4)
    )


# Change the reason and status in temp database
def temp_data_changer(username, reason, result):
    with open('temp_login.txt') as json_file:
        db = json.load(json_file)
    for x in range(len(db)):
        if db[x]['Username:'] == username:
            db[x]['Status:'] = result
            db[x]['Reason:'] = reason
            break
    open('temp_login.txt', 'w').write(
        json.dumps(db, indent=4)
    )


# Get system money
def get_system_money():
    with open('super_user.txt') as json_file:
        db = json.load(json_file)
    return db['SuperUser'][0]['Funds:']


# For blacklist remove, as it data structure is different from the mailbox
def remove_user(username, textfile_name):
    with open(textfile_name)as json_file:
        db = json.load(json_file)
    for x in range(len(db)):
        if db[x]['Username:'] == username:
            del db[x]
            break
    open(textfile_name, 'w').write(
        json.dumps(db, indent=4)
    )


def get_my_bid(project_name, bidder_name):
    my_bid = -1
    with open("projects_db.txt") as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db["Projects"])):
        if project_name == db["Projects"][x]["Project_Name:"] == project_name and bidder_name == db["Projects"][x][
            "Developer:"]:
            my_bid = db["Projects"][x]["Bidders:"][bidder_name]
            return int(my_bid)


def get_my_client(project_name):
    client_name = "?"
    with open("projects_db.txt") as f:
        try:
            db = json.load(f)
        except ValueError:
            db = []

    for x in range(len(db["Projects"])):
        if project_name == db["Projects"][x]["Project_Name:"] == project_name:
            client_name = db["Projects"][x]["Client:"]
            return client_name


def get_funds_from_temp(username):
    with open("temp_login.txt") as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = []

    for x in range(len(db)):
        if db[x]["Username:"] == username:
            return int(db[x]["Funds:"])


def get_info_by_name(accounttype, name):
    info = []

    with open(accounttype + "_login.txt") as f:
        try:
            db = json.load(f)
        # if the file is empty the ValueError will be thrown
        except ValueError:
            db = []

    for x in range(len(db)):
        if db[x]["Username:"] == name:
            info.append(db[x]["Username:"])
            info.append(db[x]["Interests:"])
            info.append(db[x]["Email:"])
            info.append(db[x]["Projects:"])
            return info
