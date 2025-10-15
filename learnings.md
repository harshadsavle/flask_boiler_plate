# Things Needed while making an API

1. To connect to a mysql database running on a localhost through the python code -

```connection = mysql.connector.connect(
    host="localhost",      # Your MySQL host, usually 'localhost'
    user="root",           # Your MySQL username
    password="passwordSQL",  # Your MySQL password
    database="authentication"  # The database you want to use
)

cursor = connection.cursor(buffered=True)

```

- By default mysql allow root access using sudo and not using password, you need to change the mode so that it allows access using password. The code to do so is shown below -
  `sudo mysql`

  ```
  ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
  ```

  ```
    FLUSH PRIVILEGES;
    EXIT;
  ```

- To change mysql password for a root - `ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';`

2. Now we have connection to database, we just need to create a route that take fields required for signup in JSON format. Once we get them we will create a token out of username and password using a secret key for security purpose. Also to store them in database we take the help of mysql-connector.

```
    @app.route('/signup', methods=['POST'])
def signup():
    # Get JSON data from the request
    print("############")
    data = request.get_json()
    print(data)
    # Store username and password in variables
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    password = jwt.encode({"username": username, "password": password}, SECRET_KEY, algorithm="HS256")
    cursor.execute("INSERT INTO user_authentication (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    connection.commit()
    final = cursor.execute("SELECT * from user_authentication")
    print(final)


    # Print or return the variables to verify
    return f"Username: {username}, Password: {password}", 200

```

3. Now we need a similar login route. Check the code for that.

4. Once everything is ready, use postman to hit json requests. And make sure to put Content-Type as JSON in Headers at Postman, and write your data in **raw** column, not in body , in JSON format.
