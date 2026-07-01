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

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
        if not User.query.filter_by(username="admin").first():
            new_user = User(username="admin", email="admin", password="admin", role="admin")
            db.session.add(new_user)
            db.session.commit()
    app.run(debug=True)