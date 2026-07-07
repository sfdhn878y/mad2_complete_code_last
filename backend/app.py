from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import create_access_token

app = Flask(__name__)

# allow requests from vue app
CORS(app)

# sqlite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from flask_jwt_extended import JWTManager

app.config["JWT_SECRET_KEY"] = "your-secret-key"   # Change this
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    # verified = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default="Active")



class treaking_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    slots = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="Open")
    duration = db.Column(db.String(50))

    # Assigned coordinator
    coordinator_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )
# open : users can book trek , upcomming : going 
    trek_state = db.Column(db.String(50), default="Upcoming") # uplcing : opne , ogiong : closed , completed: closed
    trek_status = db.Column(db.String(50), default="Open") # close
    
    # All bookings for this trek
    bookings = db.relationship(
        'booking',
        backref='trek',
        cascade='all, delete-orphan',
        lazy=True
    )

    # Coordinator assigned to this trek
    coordinator = db.relationship(
        'User',
        foreign_keys=[coordinator_id],
        backref='assigned_treks'
    )


class booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    treaking_table_id = db.Column(
        db.Integer,
        db.ForeignKey('treaking_table.id'),
        nullable=False
    )

    # Relationship to User
    user = db.relationship(
        'User',
        backref='bookings'
    )


class staff_profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
        , unique=True
    )
    # Additional fields for staff profile can be added here
    contact_number = db.Column(db.String(15))
    medication_certification = db.Column(db.String(100))
    experience = db.Column(db.String(200))
    user = db.relationship('User', backref=db.backref('staff_profile', uselist=False))


@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Trekking API"}), 200


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = 'user'


        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Username already exists"}), 400



        new_user = User(
            username=username,
            email=email,
            password=password,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
    return jsonify({"message": "User registration suffessly completed"}), 201

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            access_token = create_access_token(identity=user.id)
            return jsonify({
            "token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401


@app.route("/add_treks", methods=["POST"])
def add_treks():
    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        location = data.get("location")
        slots = data.get("slots")
        duration = data.get("duration")
        coordinator_id = data.get("coordinator_id")
        print(coordinator_id)

        new_trek = treaking_table(
            name=name,
            location=location,
            slots=slots,
            duration=duration,
            coordinator_id=coordinator_id
        )
        db.session.add(new_trek)
        db.session.commit()
    return jsonify({"message": "Trek added successfully"}), 201

# Get all staff
@app.route("/staff", methods=["GET"])
def get_staff():
    staff = User.query.filter_by(role="coordinator").all()

    data = []

    for s in staff:
        print(s)
        data.append({
            "id": s.id,
            "username": s.username,
            "email": s.email,
            "status": s.status
        })

    return jsonify(data), 200

@app.route("/staff/status", methods=["POST"])
def update_staff_status():
    data = request.get_json()

    staff = User.query.get(data["id"])

    if not staff:
        return jsonify({"error": "Staff not found"}), 404

    staff.status = data["status"]
    db.session.commit()

    return jsonify({"message": "Status updated successfully"})














@app.route('/all_coordinators', methods=['GET'])
def all_coordinators():
    coordinators = User.query.filter_by(role='coordinator').all()
    print(coordinators)
    return jsonify([{'id': user.id, 'username': user.username} for user in coordinators])


@app.route("/all_treks", methods=["GET"])
def all_treks():
    treks = treaking_table.query.all()

    return jsonify([{
        'id': trek.id,
        'name': trek.name,
        'location': trek.location,
        'slots': trek.slots,
        'trek_status': trek.trek_status,
        'trek_state': trek.trek_state,
        'duration': trek.duration,
        "coordinator_name": trek.coordinator.username if trek.coordinator else None
    } for trek in treks])


@app.route("/delete_trek/<int:trek_id>", methods=["DELETE"])
def delete_trek(trek_id):
    print('delte trek called')
    trek = treaking_table.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    db.session.delete(trek)
    db.session.commit()
    return jsonify({"message": "Trek deleted successfully"}), 200

@app.route("/add_staff", methods=["POST"])
def add_staff():    
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        role = 'coordinator'

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Username alresdfsdfsdfsdfdsfsady exists"}), 400
        new_user = User(
            username=username,
            email=email,
            password=password,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
    return jsonify({"message": "Staff added successfully"}), 201


@app.route("/all_staff", methods=["GET"])
def all_staff():
    staff_members = User.query.filter_by(role='coordinator').all()
    return jsonify([{
        'id': staff.id,
        'username': staff.username,
        'email': staff.email
    } for staff in staff_members])
@app.route("/all_users", methods=["GET"])
def all_users():
    users = User.query.filter_by(role='user').all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'status': user.status,
      
    } for user in users])


# staff dashbaord ----------------------------------
@app.route("/staff_profie/<int:user_id>", methods=["GET"])
def get_staff_profile(user_id):
    #user , staff_profile
    user = User.query.filter_by(id = user_id, role='coordinator').first()
    print(user)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'status': user.status,
        'contact_number': user.staff_profile.contact_number if user.staff_profile else None,
        'medication_certification': user.staff_profile.medication_certification if user.staff_profile else None,
        'experience': user.staff_profile.experience if user.staff_profile else None
    }) 


# treks assigned to a coordinator with registered trekkers count
@app.route("/coordinator_treks/<int:user_id>", methods=["GET"])
def coordinator_treks(user_id):
    treks = treaking_table.query.filter_by(coordinator_id=user_id).all()
    return jsonify([{
        'id': trek.id,
        'name': trek.name,
        'location': trek.location,
        'slots': trek.slots,
        'duration': trek.duration,
        'trek_status': trek.trek_status,
        'trek_state': trek.trek_state,
        'trekkers_count': len(trek.bookings)
    } for trek in treks])


# registered users for a single trek
@app.route("/trek_participants/<int:trek_id>", methods=["GET"])
def trek_participants(trek_id):
    trek = treaking_table.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    return jsonify([{
        'booking_id': b.id,
        'user_id': b.user.id,
        'username': b.user.username,
        'email': b.user.email
    } for b in trek.bookings])


# update available slots (only assigned coordinator can update)
@app.route("/update_slots", methods=["POST"])
def update_slots():
    data = request.get_json()
    trek = treaking_table.query.get(data["trek_id"])
    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    if trek.coordinator_id != data.get("coordinator_id"):
        return jsonify({"error": "Not authorized for this trek"}), 403

    trek.slots = data["slots"]
    db.session.commit()
    return jsonify({"message": "Slots updated successfully"})


# update trek status Open / Closed
@app.route("/update_trek_status", methods=["POST"])
def update_trek_status():
    data = request.get_json()
    trek = treaking_table.query.get(data["trek_id"])
    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    if trek.coordinator_id != data.get("coordinator_id"):
        return jsonify({"error": "Not authorized for this trek"}), 403

    trek.trek_status = data["trek_status"]
    db.session.commit()
    return jsonify({"message": "Trek status updated successfully"})


# mark trek started / ongoing / completed
@app.route("/update_trek_state", methods=["POST"])
def update_trek_state():
    data = request.get_json()
    trek = treaking_table.query.get(data["trek_id"])
    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    if trek.coordinator_id != data.get("coordinator_id"):
        return jsonify({"error": "Not authorized for this trek"}), 403

    trek.trek_state = data["trek_state"]
    db.session.commit()
    return jsonify({"message": "Trek state updated successfully"})


# remove a participant from a trek (only assigned coordinator)
@app.route("/remove_participant", methods=["POST"])
def remove_participant():
    data = request.get_json()
    book = booking.query.get(data["booking_id"])
    if not book:
        return jsonify({"error": "Booking not found"}), 404

    if book.trek.coordinator_id != data.get("coordinator_id"):
        return jsonify({"error": "Not authorized for this trek"}), 403

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Participant removed successfully"})


# admin assigns a coordinator to a trek
@app.route("/assign_staff", methods=["POST"])
def assign_staff():
    data = request.get_json()
    trek = treaking_table.query.get(data["trek_id"])
    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    trek.coordinator_id = data["coordinator_id"]
    db.session.commit()
    return jsonify({"message": "Staff assigned successfully"})


# admin: all booking records with user and trek info
@app.route("/all_bookings", methods=["GET"])
def all_bookings():
    bookings = booking.query.all()
    return jsonify([{
        'id': b.id,
        'username': b.user.username,
        'email': b.user.email,
        'trek_name': b.trek.name,
        'trek_status': b.trek.trek_status,
        'trek_state': b.trek.trek_state
    } for b in bookings])


# admin: trekking statistics and reports
@app.route("/stats", methods=["GET"])
def stats():
    return jsonify({
        'total_users': User.query.filter_by(role='user').count(),
        'total_staff': User.query.filter_by(role='coordinator').count(),
        'total_treks': treaking_table.query.count(),
        'total_bookings': booking.query.count(),
        'open_treks': treaking_table.query.filter_by(trek_status='Open').count(),
        'closed_treks': treaking_table.query.filter_by(trek_status='Closed').count(),
        'completed_treks': treaking_table.query.filter_by(trek_state='completed').count()
    })


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
        if not User.query.filter_by(username="admin").first():
            new_user = User(username="admin", email="admin", password="admin", role="admin")
            db.session.add(new_user)
            db.session.commit()
    app.run(debug=True)