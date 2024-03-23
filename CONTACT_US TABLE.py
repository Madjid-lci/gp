#!C:\Users\Madjid\AppData\Local\Programs\Python\Python312\python.exe

import cgi
import mysql.connector

print("Content-type: text/html")
print()  # Blank line required

try:
# Connect to MySQL database
    connection = mysql.connector.connect(
        user='root',
        password='madjidlachichi',
        host='localhost',
        database='GRP1'
    )
    cursor = connection.cursor()

    # Retrieve form data
    form = cgi.FieldStorage()
    first_name = form.getvalue('First_Name')
    last_name = form.getvalue('Last_Name')
    email = form.getvalue('Email')
    mobile = form.getvalue('Mobile')
    message = form.getvalue('Message')

    # Check if email already exists
    cursor.execute("SELECT * FROM CONTACT_US WHERE Email = %s", (email,))
    if cursor.fetchone():
        raise ValueError("Email already exists")  # Raise exception if email already exists

    # Insert form data into the database
    cursor.execute("INSERT INTO CONTACT_US (First_Name, Last_Name, Email, Mobile, Message) VALUES (%s, %s, %s, %s, %s)",
                   (first_name, last_name, email, mobile, message))
    connection.commit()

    # Close database connection
    cursor.close()
    connection.close()

    # Display success message and redirect to index.html
    print("<h1>Data saved successfully!</h1>")
    print("<meta http-equiv='refresh' content='2;url=home.html'>")  # Redirect to home.html after 2 seconds

except mysql.connector.Error as e:
    print("<h1>Error submitting your message.</h1>")
    print("<p>Please try again later.</p>")
    print("<p>Error details: {}</p>".format(e))

except ValueError:
    print("<h1>Error submitting your message.</h1>")
    print("<p>The email address already exists. Please use a different email address.</p>")
    print("<meta http-equiv='refresh' content='2;url=index.html'>")