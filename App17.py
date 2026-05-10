# =========================================================
# AUTOSERVICE PRO - ULTIMATE PROFESSIONAL VERSION
# FULL FLASK WEBSITE
# =========================================================

# INSTALL THESE FIRST:
#
# pip install flask flask_sqlalchemy flask_mail
# pip install werkzeug requests
#
# =========================================================

from flask import Flask, render_template_string, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import requests
import random

# =========================================================
# APP CONFIG
# =========================================================

app = Flask(__name__)

app.secret_key = "anik_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///garage.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =========================================================
# EMAIL OTP CONFIG
# =========================================================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# PUT YOUR GMAIL
app.config['MAIL_USERNAME'] = 'YOUR_EMAIL@gmail.com'

# PUT GMAIL APP PASSWORD
app.config['MAIL_PASSWORD'] = 'YOUR_APP_PASSWORD'

mail = Mail(app)

# =========================================================
# SMS API
# =========================================================

FAST2SMS_API_KEY = "YOUR_FAST2SMS_API"

def send_sms(number, message):

    if FAST2SMS_API_KEY == "YOUR_FAST2SMS_API":
        return

    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "route": "v3",
        "sender_id": "TXTIND",
        "message": message,
        "language": "english",
        "flash": 0,
        "numbers": number
    }

    headers = {
        'authorization': FAST2SMS_API_KEY
    }

    try:
        requests.post(url, data=payload, headers=headers)
    except:
        pass

# =========================================================
# DATABASE MODELS
# =========================================================

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))

    password = db.Column(db.String(300))

    bike_type = db.Column(db.String(100))
    dream_bike = db.Column(db.String(100))
    favourite_gadget = db.Column(db.String(100))

class Booking(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    customer = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    garage = db.Column(db.String(100))

    vehicle = db.Column(db.String(100))
    problem = db.Column(db.String(300))
    address = db.Column(db.String(300))

    status = db.Column(db.String(100))

class Review(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    customer = db.Column(db.String(100))
    garage = db.Column(db.String(100))

    rating = db.Column(db.String(10))
    review = db.Column(db.String(500))

with app.app_context():
    db.create_all()

# =========================================================
# GARAGES
# =========================================================

garages = [

{
    "name":"Urban Bike Garage",
    "location":"Salt Lake, Kolkata",
    "service":"Bike Service",
    "phone":"+91 9876543210",
    "rating":"4.9",
    "image":"https://images.unsplash.com/photo-1558981806-ec527fa84c39?q=80&w=1200",
    "map":"https://maps.google.com/maps?q=kolkata&t=&z=13&ie=UTF8&iwloc=&output=embed"
},

{
    "name":"Turbo Car Care",
    "location":"Howrah",
    "service":"Car Service",
    "phone":"+91 8012345678",
    "rating":"4.8",
    "image":"https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?q=80&w=1200",
    "map":"https://maps.google.com/maps?q=howrah&t=&z=13&ie=UTF8&iwloc=&output=embed"
},

{
    "name":"Moto Accessories Hub",
    "location":"Kolkata",
    "service":"Accessories",
    "phone":"+91 9988776655",
    "rating":"4.7",
    "image":"https://images.unsplash.com/photo-1580310614729-ccd69652491d?q=80&w=1200",
    "map":"https://maps.google.com/maps?q=kolkata&t=&z=13&ie=UTF8&iwloc=&output=embed"
},

{
    "name":"Emergency Auto Rescue",
    "location":"Burdwan",
    "service":"Emergency Repair",
    "phone":"+91 9090909090",
    "rating":"5.0",
    "image":"https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?q=80&w=1200",
    "map":"https://maps.google.com/maps?q=burdwan&t=&z=13&ie=UTF8&iwloc=&output=embed"
}

]

garages = garages * 5

# =========================================================
# LOGIN
# =========================================================

@app.route("/", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session["user"] = user.name
            session["email"] = user.email
            session["phone"] = user.phone

            return redirect("/home")

        else:

            message = "Invalid Login"

    return render_template_string("""

<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1">

<title>AutoService Pro</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">

<style>

body{
background:linear-gradient(135deg,#0f172a,#2563eb);
height:100vh;
display:flex;
justify-content:center;
align-items:center;
font-family:'Poppins',sans-serif;
}

.login-box{
background:rgba(255,255,255,0.12);
backdrop-filter:blur(15px);
padding:40px;
border-radius:25px;
color:white;
width:100%;
max-width:420px;
box-shadow:0 0 30px rgba(0,0,0,0.3);
}

</style>

</head>

<body>

<div class="login-box">

<h1 class="text-center">AutoService Pro</h1>

<p class="text-center">Professional Vehicle Services</p>

<form method="POST">

<input type="email" name="email"
class="form-control mt-3"
placeholder="Email" required>

<input type="password" name="password"
class="form-control mt-3"
placeholder="Password" required>

<button class="btn btn-dark w-100 mt-4">
Login
</button>

</form>

<p class="text-danger text-center mt-3">
{{message}}
</p>

<p class="text-center mt-3">

New User?

<a href="/signup" class="text-white">
Create Account
</a>

</p>

</div>

</body>

</html>

""", message=message)

# =========================================================
# SIGNUP
# =========================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    message = ""

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        password = generate_password_hash(
            request.form["password"]
        )

        bike_type = request.form["bike_type"]
        dream_bike = request.form["dream_bike"]
        favourite_gadget = request.form["favourite_gadget"]

        existing = User.query.filter_by(email=email).first()

        if existing:

            message = "Email Already Exists"

        else:

            user = User(

                name=name,
                email=email,
                phone=phone,
                password=password,

                bike_type=bike_type,
                dream_bike=dream_bike,
                favourite_gadget=favourite_gadget
            )

            db.session.add(user)
            db.session.commit()

            # SMS

            send_sms(
                phone,
                "Welcome to AutoService Pro"
            )

            return redirect("/")

    return render_template_string("""

<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

body{
background:#f1f5f9;
padding:20px;
font-family:Poppins;
}

.box{
background:white;
padding:40px;
border-radius:25px;
max-width:650px;
margin:auto;
}

</style>

</head>

<body>

<div class="box">

<h1>Create Account</h1>

<form method="POST">

<input type="text" name="name"
class="form-control mt-3"
placeholder="Full Name" required>

<input type="email" name="email"
class="form-control mt-3"
placeholder="Email" required>

<input type="text" name="phone"
class="form-control mt-3"
placeholder="Phone Number" required>

<input type="password" name="password"
class="form-control mt-3"
placeholder="Password" required>

<select name="bike_type"
class="form-control mt-3">

<option>Sports Bike</option>
<option>Adventure Bike</option>
<option>Cruiser Bike</option>
<option>Electric Bike</option>

</select>

<input type="text" name="dream_bike"
class="form-control mt-3"
placeholder="Dream Bike">

<input type="text" name="favourite_gadget"
class="form-control mt-3"
placeholder="Favourite Gadget">

<button class="btn btn-primary w-100 mt-4">
Create Account
</button>

</form>

<p class="text-danger mt-3">
{{message}}
</p>

</div>

</body>

</html>

""", message=message)

# =========================================================
# HOME
# =========================================================

@app.route("/home")
def home():

    if "user" not in session:
        return redirect("/")

    category = request.args.get("category", "")
    search = request.args.get("search", "")

    filtered = garages

    if category:

        filtered = [

            g for g in filtered

            if g["service"].lower() == category.lower()
        ]

    if search:

        filtered = [

            g for g in filtered

            if search.lower() in g["name"].lower()
        ]

    return render_template_string("""

<html>

<head>

<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>

<style>

body{
background:#f1f5f9;
font-family:Poppins;
}

.hero{
background:linear-gradient(to right,#0f172a,#2563eb);
color:white;
padding:80px 20px;
text-align:center;
}

.card{
border:none;
border-radius:25px;
overflow:hidden;
box-shadow:0 0 15px rgba(0,0,0,0.1);
transition:0.3s;
}

.card:hover{
transform:translateY(-5px);
}

.dark{
background:black;
color:white;
}

</style>

<script>

function darkMode(){
document.body.classList.toggle("dark");
}

</script>

</head>

<body>

<nav class="navbar navbar-expand-lg bg-white shadow-sm p-3">

<div class="container-fluid">

<a class="navbar-brand fw-bold">
AutoService Pro
</a>

<div>

<a href="/profile"
class="btn btn-outline-primary">
Profile
</a>

<a href="/admin"
class="btn btn-dark">
Admin
</a>

<button onclick="darkMode()"
class="btn btn-secondary">
Dark Mode
</button>

<a href="/customer-care"
class="btn btn-primary">
Customer Care
</a>

<a href="/logout"
class="btn btn-danger">
Logout
</a>

</div>

</div>

</nav>

<div class="hero">

<h1>Find Best Garage Near You</h1>

<p>Bike • Car • Emergency • Accessories</p>

<lottie-player
src="https://assets2.lottiefiles.com/packages/lf20_qp1q7mct.json"
background="transparent"
speed="1"
style="width:300px;height:300px;margin:auto;"
loop autoplay>

</lottie-player>

<form method="GET">

<input type="text"
name="search"
class="form-control mt-4"
placeholder="Search Garage...">

</form>

</div>

<div class="container mt-4">

<div class="row g-3">

<div class="col-md-3">
<a href="/home?category=Bike Service"
class="btn btn-outline-dark w-100">
Bike Service
</a>
</div>

<div class="col-md-3">
<a href="/home?category=Car Service"
class="btn btn-outline-dark w-100">
Car Service
</a>
</div>

<div class="col-md-3">
<a href="/home?category=Accessories"
class="btn btn-outline-dark w-100">
Accessories
</a>
</div>

<div class="col-md-3">
<a href="/home?category=Emergency Repair"
class="btn btn-outline-dark w-100">
Emergency Repair
</a>
</div>

</div>

<div class="row mt-4">

{% for garage in garages %}

<div class="col-md-4 mb-4">

<div class="card">

<img src="{{garage.image}}"
style="height:220px;object-fit:cover;">

<div class="p-3">

<h4>{{garage.name}}</h4>

<p>📍 {{garage.location}}</p>

<p>🔧 {{garage.service}}</p>

<p>⭐ {{garage.rating}}</p>

<p>📞 {{garage.phone}}</p>

<iframe
src="{{garage.map}}"
width="100%"
height="200"
style="border:0;border-radius:15px;">
</iframe>

<div class="d-flex gap-2 mt-3">

<a href="/book/{{garage.name}}"
class="btn btn-primary w-100">
Book Now
</a>

<a href="tel:{{garage.phone}}"
class="btn btn-danger w-100">
Emergency
</a>

</div>

<a href="/review/{{garage.name}}"
class="btn btn-success w-100 mt-2">
Reviews
</a>

</div>

</div>

</div>

{% endfor %}

</div>

</div>

</body>

</html>

""", garages=filtered)

# =========================================================
# PROFILE PAGE
# =========================================================

@app.route("/profile")
def profile():

    if "user" not in session:
        return redirect("/")

    bookings = Booking.query.filter_by(
        customer=session["user"]
    ).all()

    return render_template_string("""

<html>

<head>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

</head>

<body class="bg-light">

<div class="container mt-5">

<div class="card p-4 rounded-4">

<h1>{{user}}</h1>

<p>Email: {{email}}</p>

<p>Phone: {{phone}}</p>

<h3 class="mt-4">
My Bookings
</h3>

{% for b in bookings %}

<div class="border rounded p-3 mt-3">

<h5>{{b.garage}}</h5>

<p>{{b.vehicle}}</p>

<p>Status:
<b>{{b.status}}</b>
</p>

</div>

{% endfor %}

</div>

</div>

</body>

</html>

""",

user=session["user"],
email=session["email"],
phone=session["phone"],
bookings=bookings
)

# =========================================================
# BOOKING
# =========================================================

@app.route("/book/<garage_name>", methods=["GET", "POST"])
def book(garage_name):

    if request.method == "POST":

        vehicle = request.form["vehicle"]
        problem = request.form["problem"]
        address = request.form["address"]

        booking = Booking(

            customer=session["user"],
            phone=session["phone"],

            garage=garage_name,

            vehicle=vehicle,
            problem=problem,
            address=address,

            status="Pending"
        )

        db.session.add(booking)
        db.session.commit()

        send_sms(
            session["phone"],
            f"Booking Confirmed for {garage_name}"
        )

        return redirect("/profile")

    return render_template_string("""

<html>

<head>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

</head>

<body class="bg-light">

<div class="container mt-5">

<div class="card p-4 rounded-4">

<h1>Book {{garage}}</h1>

<form method="POST">

<input type="text"
name="vehicle"
class="form-control mt-3"
placeholder="Vehicle Name" required>

<input type="text"
name="problem"
class="form-control mt-3"
placeholder="Problem" required>

<input type="text"
name="address"
class="form-control mt-3"
placeholder="Pickup Address" required>

<button class="btn btn-primary w-100 mt-4">
Confirm Booking
</button>

</form>

</div>

</div>

</body>

</html>

""", garage=garage_name)

# =========================================================
# REVIEWS
# =========================================================

@app.route("/review/<garage_name>", methods=["GET", "POST"])
def review(garage_name):

    if request.method == "POST":

        r = Review(

            customer=session["user"],
            garage=garage_name,

            rating=request.form["rating"],
            review=request.form["review"]
        )

        db.session.add(r)
        db.session.commit()

    reviews = Review.query.filter_by(
        garage=garage_name
    ).all()

    return render_template_string("""

<html>

<head>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

</head>

<body class="bg-light">

<div class="container mt-5">

<div class="card p-4 rounded-4">

<h1>{{garage}}</h1>

<form method="POST">

<select name="rating"
class="form-control">

<option>⭐ 1</option>
<option>⭐ 2</option>
<option>⭐ 3</option>
<option>⭐ 4</option>
<option>⭐ 5</option>

</select>

<textarea
name="review"
class="form-control mt-3"
placeholder="Write Review"
required></textarea>

<button class="btn btn-success w-100 mt-3">
Submit Review
</button>

</form>

<hr>

{% for r in reviews %}

<div class="border rounded p-3 mt-3">

<h5>{{r.customer}}</h5>

<p>{{r.rating}}</p>

<p>{{r.review}}</p>

</div>

{% endfor %}

</div>

</div>

</body>

</html>

""",

garage=garage_name,
reviews=reviews
)

# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin():

    bookings = Booking.query.all()
    users = User.query.all()
    reviews = Review.query.all()

    return render_template_string("""

<html>

<head>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

</head>

<body class="bg-light">

<div class="container mt-5">

<h1>Admin Dashboard</h1>

<h3 class="mt-5">Users</h3>

{% for u in users %}

<div class="border rounded p-3 mt-2">
{{u.name}} - {{u.email}}
</div>

{% endfor %}

<h3 class="mt-5">Bookings</h3>

{% for b in bookings %}

<div class="border rounded p-3 mt-2">

<h5>{{b.customer}}</h5>

<p>{{b.garage}}</p>

<p>Status:
<b>{{b.status}}</b>
</p>

</div>

{% endfor %}

<h3 class="mt-5">Reviews</h3>

{% for r in reviews %}

<div class="border rounded p-3 mt-2">

<h5>{{r.customer}}</h5>

<p>{{r.review}}</p>

</div>

{% endfor %}

</div>

</body>

</html>

""",

bookings=bookings,
users=users,
reviews=reviews
)

# =========================================================
# CUSTOMER CARE
# =========================================================

@app.route("/customer-care")
def customer_care():

    return """

<html>

<head>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

</head>

<body class="bg-light">

<div class="container mt-5">

<div class="card p-5 rounded-4 text-center">

<h1>Customer Care</h1>

<p>📞 +91 8101200478</p>

<p>📧 support@autoservicepro.com</p>

<p>🕒 24x7 Support</p>

</div>

</div>

</body>

</html>

"""

# =========================================================
# AI CHATBOT
# =========================================================

@app.route("/chatbot")
def chatbot():

    return jsonify({
        "message":"Hello! AutoService AI Assistant Ready."
    })

# =========================================================
# PUSH NOTIFICATION DEMO
# =========================================================

@app.route("/notification")
def notification():

    return jsonify({
        "notification":"Your mechanic is on the way."
    })

# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5002,
        debug=True
    )