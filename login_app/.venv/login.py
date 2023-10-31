# Grace Padgett
# check if password meets requirements and 
# validate login credentials in database dump file

# to connect to postgres database
import psycopg2

from flask import Flask

app = Flask(__name__)

@app.route("/validate/<x>") #password as route parameter
def validatePassword(x): #define function to validate password requirements
    # set flags to false
    flag_len = 0
    flag_alpha = 0
    flag_num = 0
    flag_upper = 0
    flag_lower = 0
    
    # flag if too long/short
    if len(x) < 8 or len(x) > 20: 
        flag_len = 1 

    # using any() to check for any occurrence of a number
    num = any(chr.isdigit() for chr in x) 
    if num != True: # flag if no numbers
        flag_num = 1

    # using any() to check for any occurrence of a letter
    alpha = any(chr.isalpha() for chr in x) 
    if alpha != True: # flag if no letters
        flag_alpha = 1
    
    # flag if only uppercase
    if x.isupper(): 
        flag_upper = 1
    
    # flag if only lowercase
    if x.islower(): 
        flag_lower = 1

    # check for any flags 
    flagTotal = flag_len + flag_alpha + flag_num + flag_upper + flag_lower

    print(flagTotal)

    # return true if passes validation
    if flagTotal > 0:
        return("False")
    else:
        return("True")


@app.route("/login/<x>/<y>") # username and password as params
def login(x, y): # define login function with login arguments

    conn = psycopg2.connect(host="dpg-cirfrcp8g3n42okl5gj0-a.oregon-postgres.render.com", 
                    port="5432", 
                    user="inew2374250fall23_user", 
                    password="VeqKMiDIcOWKEAT3SmjF8ZJM5UemCw8O", 
                    database="inew2374250fall23", 
                    options="-c search_path=msg_app")
    
    cur = conn.cursor() 
    
    # get login info from users table
    cur.execute(
        "SELECT email, password FROM msg_app.user")
    
    data = cur.fetchall()
    
    # set bool to false
    loggedIn = "False"
    
    # loop through users to find matching email then test if password matches
    # sets bool to true if login credentials correct
    for row in data: # read each line in users table
        if (row[0]) == x:
            if (row[1]) == y:
                message = ("You are signed in.")
                loggedIn = "True"
                break
            else:
                message = ("Password incorrect.")
                break
        else:
            message = ("Email not found.")

    # display message for testing purposes
    print(message)
    
    # commit the changes 
    conn.commit() 
    
    # close the cursor and connection 
    cur.close() 
    conn.close() 

    # return true/false
    return(loggedIn)

'''
# was used for testing purposes, please ignore

# data from frontend will need to be fetched
# temporarily input for testing purposes
print("Insert email")
username = input()

print("Insert password")
password = input()

# run validatePassword function
# true if passes validation
passesValidation = validatePassword(password)

# run login function with login parameters
# returns true if login successful
success = login(username, password)

print(passesValidation)
print(success)

# send return data to frontend (TBD how)
'''
