import csv
import json
import requests
from ast import literal_eval


admin_username = raw_input("username : ")
admin_password = raw_input("password : ")

# def login():
#     print(":::::::::::::::Requires an grafana account with admin access:::::::::::::::")
#     admin_username = raw_input("username : ")
#     admin_password = raw_input("password : ")
#     return admin_username, admin_password

def create_urls():

    # admin_username, admin_password = login()
    grafana_url = 'localhost'

    admin_users_api_path = '/api/admin/users'
    orgs_api_path = '/api/orgs'


    users_url = 'http://'+admin_username+':'+admin_password+'@'+grafana_url+admin_users_api_path
    orgs_url = 'http://'+admin_username+':'+admin_password+'@'+grafana_url+orgs_api_path

    return users_url, orgs_url

def create_user_account():
    print("\n")
    print(":::::::::::::::To Create The Grafana Users:::::::::::::::")
    users_url, orgs_url = create_urls()
    print(orgs_url+"\n"+users_url)
    with open ('users.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            email = row['email']
            login = row['login']
            #password = row['password']
            password = row['first_name'][0] + row['last_name'][0] + row['mobile'][-5:]
            parameters = {"name":name,"email":email,"login":login,"password":password}
            headers = {"content-type": "application/json"}
            
            response = requests.request("POST", users_url, headers=headers, data=json.dumps(parameters))
            print(response.text)
            
def org_list():
    print("\n")
    print(":::::::::::::::To disply the ORGs list:::::::::::::::")
    users_url, orgs_url = create_urls()
    print(orgs_url+"\n"+users_url)
    headers = {"content-type": "application/json"}
    response = requests.request("GET",orgs_url,headers=headers)
    #print(response.text)
    return(response.text)

def assign_users():
    try:
        print("\n")
        print(":::::::::::::::Assign users to the Organization::::::::::::::")
        users_url, orgs_url = create_urls()
        print(orgs_url+"\n"+users_url)
        orgs = org_list()
        for key in literal_eval(orgs):
            print(str(key['id']) + " - " + key['name'])
        org_id = raw_input("Enter the orgId from the above list : ")
        assign_user_url = orgs_url+"/"+org_id+"/users"
        print(assign_user_url)
        with open ('users.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                loginOrEmail = row['login']
                role = raw_input("Enter the role (ex: Viewer/Editor) for " +loginOrEmail+ " : ")
                #password = row['password']
                #password = row['first_name'][0] + row['last_name'][0] + row['mobile'][-5:]
                parameters = {"loginOrEmail":loginOrEmail, "role":role}
                headers = {"content-type": "application/json"}

                response = requests.request("POST", assign_user_url, headers=headers, data=json.dumps(parameters))

                print(response.text)
    except TypeError as e:
        print(e)
        
create_user_account()

assign_users()


