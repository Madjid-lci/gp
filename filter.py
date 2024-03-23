#!C:\Users\Madjid\AppData\Local\Programs\Python\Python312\python.exe

import cgi

# Define gym data globally
power_zone_data_with_membership = {
    "Joining fee (one-off fee)": 30,
    "Super-off peak (10 am - 12 pm & 2 pm - 4 pm)": 13,
    "Off-peak (12 - 2 pm & 8 - 11 pm)": 19,
    "Anytime": 24,
    "Swimming pool (with gym m.)": 12.5,
    "Classes (with gym m.)": 0,
    "Massage therapy (with gym m.)": 25,
    "Physiotherapy (with gym m.)": 25
}

power_zone_data_without_membership = {
    "Joining fee (one-off fee)": 30,
    "Super-off peak (10 am - 12 pm & 2 pm - 4 pm)": 13,
    "Off-peak (12 - 2 pm & 8 - 11 pm)": 19,
    "Anytime": 24,
    "Swimming pool (without gym m.)": 20,
    "Classes (without gym m.)": 20,
    "Massage therapy (without gym m.)": 30,
    "Physiotherapy (without gym m.)": 30,
}

uGym_data_with_membership = {
    "Joining fee (one-off fee)": 10,
    "Super-off peak (10 am - 12 pm & 2 pm - 4 pm)": 16,
    "Off-peak (12 - 2 pm & 8 - 11 pm)": 21,
    "Anytime": 30,
    "Swimming pool (with gym m.)": 15,
    "Classes (with gym m.)": 10,
    "Massage therapy (with gym m.)": 25,
    "Physiotherapy (with gym m.)": 20
}

uGym_data_without_membership = {
    "Joining fee (one-off fee)": 10,
    "Super-off peak (10 am - 12 pm & 2 pm - 4 pm)": 16,
    "Off-peak (12 - 2 pm & 8 - 11 pm)": 21,
    "Anytime": 30,
    "Swimming pool (without gym m.)": 25,
    "Classes (without gym m.)": 20,
    "Massage therapy (without gym m.)": 30,
    "Physiotherapy (without gym m.)": 25
}

def calculate_price(user_data, gym_data):
    price = 0
    price += gym_data.get("Joining fee (one-off fee)", 0)  # Add joining fee only once
    

    if user_data["trainer_type"] == "super_off_peak":
        key = "Super-off peak (10 am - 12 pm & 2 pm - 4 pm)" if user_data["subscribe"] == "yes" else 0
        price += gym_data.get(key, 0)
    elif user_data["trainer_type"] == "off_peak":
        key = "Off-peak (12 - 2 pm & 8 - 11 pm)" if user_data["subscribe"] == "yes" else 0
        price += gym_data.get(key, 0)
    elif user_data["trainer_type"] == "anytime":
        key = "Anytime" if user_data["subscribe"] == "yes" else 0
        price += gym_data.get(key, 0)

    if user_data["add_swimming_pool"] == "yes":
        key = "Swimming pool (with gym m.)" if user_data["subscribe"] == "yes" else "Swimming pool (without gym m.)"
        price += gym_data.get(key, 0)
    if user_data["add_classes"] == "yes":
        key = "Classes (with gym m.)" if user_data["subscribe"] == "yes" else "Classes (without gym m.)"
        price += gym_data.get(key, 0)
    if user_data["Massage_Therapy"] == "yes":
        key = "Massage therapy (with gym m.)" if user_data["subscribe"] == "yes" else "Massage therapy (without gym m.)"
        price += gym_data.get(key, 0)
    if user_data["Physiotherapy"] == "yes":
        key = "Physiotherapy (with gym m.)" if user_data["subscribe"] == "yes" else "Physiotherapy (without gym m.)"
        price += gym_data.get(key, 0)
        
    return price

def calculate_price_with_discount(user_data, gym_data):
    price = calculate_price(user_data, gym_data)  # Get base price first
    
    age = int(user_data.get("age", 0))
    if age <= 25:
        discount_percent = 20
    elif age >= 66:
        discount_percent = 15
    else:
        discount_percent = 0

    price = price - (price * discount_percent) / 100

    return price

# Process form data
form = cgi.FieldStorage()

# Get user data from the form
user_data = {
    "trainer_type": form.getvalue("trainer_type"),
    "add_swimming_pool": form.getvalue("add_swimming_pool"),
    "add_classes": form.getvalue("add_classes"),
    "Massage_Therapy": form.getvalue("Massage_Therapy"),
    "Physiotherapy": form.getvalue("Physiotherapy"),
    "age": form.getvalue("age"),  # Include user's age
    "subscribe": form.getvalue("subscribe")  
}

# Determine gym data based on the selected gym
if user_data["subscribe"] == "yes":
    gym_data = power_zone_data_with_membership
else:
    gym_data = power_zone_data_without_membership

# Calculate the total price for Power Zone
price_power_zone = calculate_price_with_discount(user_data, gym_data)

# Determine gym data based on the selected gym for uGym
if user_data["subscribe"] == "yes":
    gym_data = uGym_data_with_membership
else:
    gym_data = uGym_data_without_membership

# Calculate the total price for uGym
price_uGym = calculate_price_with_discount(user_data, gym_data)

# Determine which gym is the best based on price
best_gym = "Power Zone" if price_power_zone < price_uGym else "uGym"

# HTML response with CSS included
print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>Gym Suggestion</title>")
print("<style>")
print("""
/* Define your CSS styles here */
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
}
.container {
    max-width: 600px;
    margin: 20px auto;
    margin-top:6%;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
    color:#000000 ;
}

p {
    margin: 10px 0;
}
""")
print("</style>")
print("</head>")
print("<body>")
print("<div class='container'>")
print("<center><h2>Best Gym Suggestion</h2></center>")
print("<br>")
print("<p>The best gym for you based on your preferences is: {}</p>".format(best_gym))
print("<br>")
print("<p>The price for Power Zone is: £{:.2f}</p>".format(price_power_zone))
print("<br>")
print("<p>The price for uGym is: £{:.2f}</p>".format(price_uGym))
print("<br>")
print("<p> If you want to know more about the GYM follow this link: ")
# Depending on the gym, link to the respective page
if best_gym == "Power Zone":
    print("<a href='power_zone.html'>{}</a>".format(best_gym))
else:
    print("<a href='u_gym.html'>{}</a>".format(best_gym))
print("</p>")
print("</div>")
print("</body>")
print("</html>")
