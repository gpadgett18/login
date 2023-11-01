# Grace Padgett
# check if password meets requirements and 
# validate login credentials in database dump file

# to connect to postgres database


import psycopg2

from waitress import serve

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)



@app.route("/validate", methods=["GET", "POST"]) 
def validate(): #define function to validate password requirements
    
    if request.method == "POST":

        # get data from frontend
        data = request.get_json()
        password = data["password"]
    
        # set flags to false
        flag_len = 0
        flag_alpha = 0
        flag_num = 0
        flag_upper = 0
        flag_lower = 0
        
        # flag if too long/short
        if len(password) < 8 or len(password) > 20: 
            flag_len = 1 

        # using any() to check for any occurrence of a number
        num = any(chr.isdigit() for chr in password) 
        if num != True: # flag if no numbers
            flag_num = 1

        # using any() to check for any occurrence of a letter
        alpha = any(chr.isalpha() for chr in password) 
        if alpha != True: # flag if no letters
            flag_alpha = 1
        
        # flag if only uppercase
        if password.isupper(): 
            flag_upper = 1
        
        # flag if only lowercase
        if password.islower(): 
            flag_lower = 1

        # check for any flags 
        flagTotal = flag_len + flag_alpha + flag_num + flag_upper + flag_lower

        flagTotal.headers.add('Access-Control-Allow-Origin', '*')

        # return false if any flags present
        # true if passes validation
        return jsonify(flagTotal)
    
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"]) # login route checks login credentials
def login(): # define login function
    if request.method == "POST":
        
        # get data from frontend
        data = request.get_json()
        
        # connect to database
        try: 
            conn = psycopg2.connect(host="dpg-cirfrcp8g3n42okl5gj0-a.oregon-postgres.render.com", 
                        port="5432", 
                        user="inew2374250fall23_user", 
                        password="VeqKMiDIcOWKEAT3SmjF8ZJM5UemCw8O", 
                        database="inew2374250fall23", 
                        options="-c search_path=msg_app")
        except:
            return("Could not connect to the database.")
        
        # query stored in a variable to clean up code and make easy changes
        LOGIN_CREDENTIALS = (
            "SELECT email, password FROM msg_app.user \
            WHERE email LIKE (%s) AND password LIKE (%s)"
        )

        # store data in variables
        email = data["email"]
        password = data["password"]
        
        # create cursor 
        cur = conn.cursor() 

        # get login info from users table
        cur.execute(LOGIN_CREDENTIALS, (email, password))

        # store data from cursor into variable
        login_exists = cur.fetchall()
        
        # commit the changes 
        conn.commit() 
        
        # close the cursor and connection 
        cur.close() 
        conn.close() 

        login_exists.headers.add('Access-Control-Allow-Origin', '*')

        # return true if login credentials found
        return {
            'response' : login_exists
        }

    return render_template('index.html')

if __name__ == "__main__":
    serve(app, debug=True, port=5000)
