from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token, JWTManager, jwt_required, get_jwt_identity,
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from functools import wraps
import json
from flask_caching import Cache
from sqlalchemy import text
from datetime import datetime, date, timedelta   # add timedelta
from flask_mail import Mail, Message
from celery import Celery
from celery.schedules import crontab
app = Flask(__name__)
from sqlalchemy import func
# allow requests from vue app
CORS(app)
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# sqlite database
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + os.path.join(basedir, "instance", "todos.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.config["JWT_SECRET_KEY"] = "your-secret-key"   # Change this
jwt = JWTManager(app)

# ---------------------------------------------------------------------------
# Redis cache setup (Flask-Caching)
# ---------------------------------------------------------------------------
# Uses Redis as the backend, running on localhost:6379.
# GET routes use @cache.cached(timeout=60) to store their response for 60s.
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_REDIS_DB"] = 0
app.config["CACHE_DEFAULT_TIMEOUT"] = 60   # default expiry in seconds

cache = Cache(app)

# ---------------------------------------------------------------------------
# Flask-Mail (for reminders, reports, export notifications)
# ---------------------------------------------------------------------------
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "tempmailshubham4@gmail.com"      # change this
app.config["MAIL_PASSWORD"] = "zjta adlj abdp tjrr" # NOT normal password
app.config["MAIL_DEFAULT_SENDER"] = "tempmailshubham4@gmail.com"

mail = Mail(app)
# After any create/update/delete we clear the whole cache so users never
# see stale data. cache.clear() is the simplest, beginner-friendly choice.
# ---------------------------------------------------------------------------
# Flask-Mail (for reminders, reports, export notifications)
# ---------------------------------------------------------------------------


def clear_cache():
    cache.clear()
from datetime import timedelta

# ---------------------------------------------------------------------------
# Celery + Redis (background jobs + daily schedule)
# ---------------------------------------------------------------------------
def make_celery(flask_app):
    celery_app = Celery(
        flask_app.import_name,
        broker="redis://localhost:6379/1",
        backend="redis://localhost:6379/1",
    )
    celery_app.conf.update(
        timezone="Asia/Kolkata",
        enable_utc=True,
        beat_schedule={
            "daily-trek-reminder": {
                "task": "send_trek_reminders",
                "schedule": timedelta(seconds=10)
            },
            "monthly-admin-report": {
                "task": "send_monthly_admin_report",
                "schedule": timedelta(seconds=10)
            },
        },
    )

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


celery = make_celery(app)
# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------
def hash_password(raw):
    return generate_password_hash(raw)


def verify_password(user, raw):
    """Check a password, transparently migrating legacy plaintext values."""
    stored = user.password or ""
    if not stored.startswith(("pbkdf2:", "scrypt:")):
        # legacy plaintext record: verify then upgrade to a hash
        if stored == raw:
            user.password = generate_password_hash(raw)
            db.session.commit()
            return True
        return False
    return check_password_hash(stored, raw)


def current_user():
    identity = get_jwt_identity()
    if identity is None:
        return None
    return User.query.get(int(identity))


def role_required(*roles):
    """Require a valid JWT and (optionally) one of the given roles."""
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated(*args, **kwargs):
            user = current_user()
            if not user:
                return jsonify({"error": "Unauthorized"}), 401
            if user.status == "Blacklisted":
                return jsonify({"error": "Your account has been blacklisted"}), 403
            if roles and user.role not in roles:
                return jsonify({"error": "Forbidden: insufficient permissions"}), 403
            return fn(*args, **kwargs)
        return decorated
    return wrapper

@celery.task(name="send_trek_reminders")
def send_trek_reminders():
    """Send email to users whose booked trek starts tomorrow."""
    tomorrow = date.today() + timedelta(days=1)

    treks = treaking_table.query.filter(
       
        treaking_table.trek_state == "upcoming"
    ).all()

    sent = 0
    for trek in treks:
        for b in active_bookings(trek):
            user = b.user
            msg = Message(
                subject=f"Reminder: {trek.name} starts tomorrow!",
                recipients=[user.email],
                body=(
                    f"Hi {user.full_name or user.username},\n\n"
                    f"Your trek \"{trek.name}\" at {trek.location} "
                    f"starts on {trek.start_date}.\n\n"
                    f"Difficulty: {trek.difficulty}\n"
                    f"Duration: {trek.duration}\n\n"
                    f"See you on the trail!\n"
                ),
            )
            mail.send(msg)
            sent += 1

    return f"Sent {sent} reminder(s)"






#-------------------__
# send month reprot 
@celery.task(name="send_monthly_admin_report")
def send_monthly_admin_report():
    """Email admins a monthly trekking activity report for the previous calendar month."""
    today = date.today()
    first_of_this_month = today.replace(day=1)
    last_month_end = first_of_this_month - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)
    month_label = last_month_start.strftime("%B %Y")  # e.g. "June 2026"

    # Treks conducted last month
    conducted = treaking_table.query.filter(
        treaking_table.trek_state == "completed",
        treaking_table.end_date >= last_month_start,
        treaking_table.end_date <= last_month_end,
    ).all()

    # Total participants on those treks
    participants = (
        booking.query
        .join(treaking_table, booking.treaking_table_id == treaking_table.id)
        .filter(
            booking.status.in_(["Completed", "Booked"]),
            treaking_table.trek_state == "completed",
            treaking_table.end_date >= last_month_start,
            treaking_table.end_date <= last_month_end,
        )
        .count()
    )

    # Top 5 popular treks by booking count
    popular = (
        db.session.query(
            treaking_table.name,
            func.count(booking.id).label("count"),
        )
        .join(booking, booking.treaking_table_id == treaking_table.id)
        .filter(
            treaking_table.trek_state == "completed",
            treaking_table.end_date >= last_month_start,
            treaking_table.end_date <= last_month_end,
            booking.status.in_(["Completed", "Booked"]),
        )
        .group_by(treaking_table.id)
        .order_by(func.count(booking.id).desc())
        .limit(5)
        .all()
    )

    # Build popular treks HTML list
    if popular:
        popular_html = "".join(
            f"<li>{name} — {count} participant(s)</li>"
            for name, count in popular
        )
    else:
        popular_html = "<li>No treks completed last month</li>"

    # Trek names list
    conducted_names = ", ".join(t.name for t in conducted) if conducted else "None"

    html_body = f"""
    <h2>Monthly Trekking Activity Report — {month_label}</h2>
    <p>Summary for <strong>{month_label}</strong>:</p>
    <ul>
        <li><strong>Treks conducted:</strong> {len(conducted)}</li>
        <li><strong>Total participants:</strong> {participants}</li>
        <li><strong>Treks:</strong> {conducted_names}</li>
    </ul>
    <h3>Popular treks</h3>
    <ul>{popular_html}</ul>
    <p>— Trekking Admin System</p>
    """

    admins = User.query.filter_by(role="admin").all()
    print(admins)
    if not admins:
        return "No admin users found"

    sent = 0
    for admin in admins:
        if not admin.email or admin.email == "admin":
            print('invalid admin email')
            continue  # skip invalid seed admin email
        msg = Message(
            subject=f"Monthly Trekking Report — {month_label}",
            recipients=[admin.email],
            html=html_body,
        )
        mail.send(msg)
        sent += 1

    return f"Monthly report sent to {sent} admin(s) for {month_label}"





# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # user | staff | admin

    # user  -> Active | Blacklisted
    # staff -> Pending | Approved | Blacklisted
    status = db.Column(db.String(20), default="Active")

    # shared profile fields (users + staff)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    address = db.Column(db.String(255))
    emergency_contact_name = db.Column(db.String(120))
    emergency_contact_number = db.Column(db.String(20))
    blood_group = db.Column(db.String(10))
    medical_conditions = db.Column(db.String(255))
    fitness_level = db.Column(db.String(50))
    profile_completed = db.Column(db.Boolean, default=False)


class treaking_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    difficulty = db.Column(db.String(20), default="Easy")  # Easy | Moderate | Hard
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    duration = db.Column(db.String(50))
    slots = db.Column(db.Integer, default=0)

    # trek_state: upcoming | ongoing | completed
    trek_state = db.Column(db.String(50), default="upcoming")
    # trek_status (booking status): Open | Closed
    trek_status = db.Column(db.String(50), default="Open")

    # staff-requested slot change awaiting admin approval
    pending_slots = db.Column(db.Integer, nullable=True)
    pending_approval = db.Column(db.Boolean, default=False)
    # staff-requested full edit (JSON of changed fields) awaiting admin approval
    pending_changes = db.Column(db.Text, nullable=True)

    coordinator_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    bookings = db.relationship(
        'booking',
        backref='trek',
        cascade='all, delete-orphan',
        lazy=True
    )

    coordinator = db.relationship(
        'User',
        foreign_keys=[coordinator_id],
        backref='assigned_treks'
    )


class booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    treaking_table_id = db.Column(db.Integer, db.ForeignKey('treaking_table.id'), nullable=False)
    status = db.Column(db.String(20), default="Booked")  # Booked | Completed | Cancelled
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='bookings')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def parse_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


def active_bookings(trek):
    return [b for b in trek.bookings if b.status == "Booked"]


def serialize_trek(trek):
    return {
        "id": trek.id,
        "name": trek.name,
        "location": trek.location,
        "difficulty": trek.difficulty,
        "start_date": trek.start_date.isoformat() if trek.start_date else None,
        "end_date": trek.end_date.isoformat() if trek.end_date else None,
        "duration": trek.duration,
        "slots": trek.slots,
        "trek_state": trek.trek_state,
        "trek_status": trek.trek_status,
        "pending_slots": trek.pending_slots,
        "pending_approval": trek.pending_approval,
        "pending_changes": json.loads(trek.pending_changes) if trek.pending_changes else None,
        "coordinator_id": trek.coordinator_id,
        "coordinator_name": trek.coordinator.username if trek.coordinator else None,
        "registered_count": len(active_bookings(trek)),
        "total_bookings": len(trek.bookings),
    }


def dates_overlap(start_a, end_a, start_b, end_b):
    if not (start_a and end_a and start_b and end_b):
        return False
    return start_a <= end_b and end_a >= start_b


def validate_trek_payload(name, start_date, end_date, coordinator_id, exclude_id=None):
    """Returns an error string or None."""
    if start_date and end_date and end_date <= start_date:
        return "End date must be after start date"

    # duplicate trek name
    dup_q = treaking_table.query.filter(treaking_table.name == name)
    if exclude_id:
        dup_q = dup_q.filter(treaking_table.id != exclude_id)
    if dup_q.first():
        return "A trek with this name already exists"

    # staff clash check
    if coordinator_id and start_date and end_date:
        others = treaking_table.query.filter(
            treaking_table.coordinator_id == coordinator_id
        )
        if exclude_id:
            others = others.filter(treaking_table.id != exclude_id)
        for other in others.all():
            if dates_overlap(start_date, end_date, other.start_date, other.end_date):
                return f"Assigned staff already leads '{other.name}' during these dates"
    return None


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Trekking API"}), 200


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(username=username, email=email, password=hash_password(password),
                    role="user", status="Active")
    db.session.add(new_user)
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "User registration successfully completed"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(user, password):
        return jsonify({"error": "Invalid credentials"}), 401

    if user.status == "Blacklisted":
        return jsonify({"error": "Your account has been blacklisted"}), 403

    if user.role == "staff" and user.status != "Approved":
        return jsonify({"error": "Your account is pending admin approval"}), 403

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        }
    }), 200


# ---------------------------------------------------------------------------
# Admin: stats
# ---------------------------------------------------------------------------
@app.route("/stats", methods=["GET"])
@cache.cached(timeout=60)  # cached for 60 seconds
@role_required("admin")
def stats():
    print("stats called")
   
    return jsonify({
        "total_treks": treaking_table.query.count(),
        "total_users": User.query.filter_by(role="user").count(),
        "total_staff": User.query.filter_by(role="staff").count(),
        "total_bookings": booking.query.count(),
    })


# ---------------------------------------------------------------------------
# Admin: treks
# ---------------------------------------------------------------------------
@app.route("/all_treks", methods=["GET"])
@role_required("admin")
@cache.cached(timeout=60)  # cached for 60 seconds
def all_treks():
    treks = treaking_table.query.all()
    return jsonify([serialize_trek(t) for t in treks])


@app.route("/admin/trek_details/<int:trek_id>", methods=["GET"])
@role_required("admin")
def trek_details(trek_id):
    trek = treaking_table.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    data = serialize_trek(trek)
    data["participants"] = [{
        "booking_id": b.id,
        "user_id": b.user.id,
        "username": b.user.username,
        "email": b.user.email,
        "status": b.status,
        "booked_at": b.booked_at.isoformat() if b.booked_at else None,
    } for b in trek.bookings]
    return jsonify(data)


@app.route("/add_treks", methods=["POST"])
@role_required("admin")
def add_treks():
    data = request.get_json()
    name = data.get("name")
    location = data.get("location")
    difficulty = data.get("difficulty", "Easy")
    duration = data.get("duration")
    slots = data.get("slots") or 0
    coordinator_id = data.get("coordinator_id") or None
    start_date = parse_date(data.get("start_date"))
    end_date = parse_date(data.get("end_date"))

    error = validate_trek_payload(name, start_date, end_date, coordinator_id)
    if error:
        return jsonify({"error": error}), 400

    new_trek = treaking_table(
        name=name,
        location=location,
        difficulty=difficulty,
        start_date=start_date,
        end_date=end_date,
        duration=duration,
        slots=slots,
        coordinator_id=coordinator_id,
        trek_state="upcoming",
        trek_status="Open",
    )
    db.session.add(new_trek)
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Trek added successfully"}), 201


@app.route("/admin/edit_trek/<int:trek_id>", methods=["PUT"])
@role_required("admin")
def edit_trek(trek_id):
    trek = treaking_table.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    data = request.get_json()
    name = data.get("name", trek.name)
    start_date = parse_date(data.get("start_date")) or trek.start_date
    end_date = parse_date(data.get("end_date")) or trek.end_date
    coordinator_id = data.get("coordinator_id") if data.get("coordinator_id") else None

    error = validate_trek_payload(name, start_date, end_date, coordinator_id, exclude_id=trek_id)
    if error:
        return jsonify({"error": error}), 400

    trek.name = name
    trek.location = data.get("location", trek.location)
    trek.difficulty = data.get("difficulty", trek.difficulty)
    trek.start_date = start_date
    trek.end_date = end_date
    trek.duration = data.get("duration", trek.duration)
    if data.get("slots") is not None:
        trek.slots = data.get("slots")
    trek.coordinator_id = coordinator_id
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Trek updated successfully"})


@app.route("/delete_trek/<int:trek_id>", methods=["DELETE"])
@role_required("admin")
def delete_trek(trek_id):
    trek = treaking_table.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    db.session.delete(trek)
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Trek deleted successfully"}), 200


@app.route("/admin/toggle_booking/<int:trek_id>", methods=["POST"])
@role_required("admin")
def toggle_booking(trek_id):
    trek = treaking_table.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    trek.trek_status = "Closed" if trek.trek_status == "Open" else "Open"
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Booking status updated", "trek_status": trek.trek_status})


@app.route("/admin/approve_change/<int:trek_id>", methods=["POST"])
@role_required("admin")
def approve_change(trek_id):
    trek = treaking_table.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404

    if trek.pending_slots is not None:
        trek.slots = trek.pending_slots

    if trek.pending_changes:
        changes = json.loads(trek.pending_changes)
        if "name" in changes:
            trek.name = changes["name"]
        if "location" in changes:
            trek.location = changes["location"]
        if "difficulty" in changes:
            trek.difficulty = changes["difficulty"]
        if "duration" in changes:
            trek.duration = changes["duration"]
        if changes.get("start_date"):
            trek.start_date = parse_date(changes["start_date"])
        if changes.get("end_date"):
            trek.end_date = parse_date(changes["end_date"])
        if changes.get("slots") is not None:
            trek.slots = changes["slots"]

    trek.pending_slots = None
    trek.pending_changes = None
    trek.pending_approval = False
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Change approved"})


@app.route("/admin/reject_change/<int:trek_id>", methods=["POST"])
@role_required("admin")
def reject_change(trek_id):
    trek = treaking_table.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    trek.pending_slots = None
    trek.pending_changes = None
    trek.pending_approval = False
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Change rejected"})


@app.route("/assign_staff", methods=["POST"])
@role_required("admin")
def assign_staff():
    data = request.get_json()
    trek = treaking_table.query.get(data["trek_id"])
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    trek.coordinator_id = data.get("coordinator_id") or None
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Staff assigned successfully"})


@app.route("/view_participants/<int:trek_id>", methods=["GET"])
@role_required("admin", "staff")
def view_participants(trek_id):
    trek = treaking_table.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    user = current_user()
    if user.role == "staff" and trek.coordinator_id != user.id:
        return jsonify({"error": "Not authorized for this trek"}), 403
    return jsonify({
        "trek_name": trek.name,
        "participants": [{
            "booking_id": b.id,
            "user_id": b.user.id,
            "username": b.user.username,
            "email": b.user.email,
            "phone": b.user.phone,
            "full_name": b.user.full_name,
            "status": b.status,
        } for b in trek.bookings]
    })


# ---------------------------------------------------------------------------
# Admin: staff management
# ---------------------------------------------------------------------------
@app.route("/all_staff", methods=["GET"])
@role_required("admin")
@cache.cached(timeout=60)  # cached for 60 seconds
def all_staff():
    staff_members = User.query.filter_by(role="staff").all()
    return jsonify([{
        "id": s.id,
        "username": s.username,
        "email": s.email,
        "status": s.status,
    } for s in staff_members])


# dropdown of staff for assignment (kept for backward compatibility)
@app.route("/all_coordinators", methods=["GET"])
@role_required("admin")
def all_coordinators():
    coordinators = User.query.filter_by(role="staff").all()
    return jsonify([{"id": u.id, "username": u.username} for u in coordinators])


@app.route("/add_staff", methods=["POST"])
@role_required("admin")
def add_staff():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(username=username, email=email, password=hash_password(password),
                    role="staff", status="Approved")
    db.session.add(new_user)
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Staff added successfully"}), 201


@app.route("/staff/status", methods=["POST"])
@role_required("admin")
def update_staff_status():
    data = request.get_json()
    staff = User.query.get(data["id"])
    if not staff:
        return jsonify({"error": "Staff not found"}), 404
    staff.status = data["status"]
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Status updated successfully"})


@app.route("/staff/remove/<int:staff_id>", methods=["DELETE"])
@role_required("admin")
def remove_staff(staff_id):
    staff = User.query.filter_by(id=staff_id, role="staff").first()
    if not staff:
        return jsonify({"error": "Staff not found"}), 404
    # unassign from treks first
    for trek in staff.assigned_treks:
        trek.coordinator_id = None
    db.session.delete(staff)
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Staff removed successfully"})


@app.route("/staff_profile/<int:user_id>", methods=["GET"])
@role_required("admin")
def staff_profile(user_id):
    user = User.query.filter_by(id=user_id, role="staff").first()
    if not user:
        return jsonify({"error": "Staff not found"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "full_name": user.full_name,
        "status": user.status,
        "managed_treks": [{
            "id": t.id,
            "name": t.name,
            "location": t.location,
            "start_date": t.start_date.isoformat() if t.start_date else None,
            "total_bookings": len(t.bookings),
        } for t in user.assigned_treks],
    })


# ---------------------------------------------------------------------------
# Admin: user management
# ---------------------------------------------------------------------------
@app.route("/all_users", methods=["GET"])
@role_required("admin")
@cache.cached(timeout=60)  # cached for 60 seconds
def all_users():
    
    users = User.query.filter_by(role="user").all()
    return jsonify([{
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "status": u.status,
        "total_treks": len(u.bookings),
    } for u in users])


@app.route("/user/status", methods=["POST"])
@role_required("admin")
def update_user_status():
    data = request.get_json()
    user = User.query.get(data["id"])
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.status = data["status"]
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Status updated successfully"})


@app.route("/admin/user_profile/<int:user_id>", methods=["GET"])
@role_required("admin")
def admin_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role,
        "status": user.status,
        "verified": user.status != "Blacklisted",
    })


# ---------------------------------------------------------------------------
# Admin: bookings
# ---------------------------------------------------------------------------
@app.route("/all_bookings", methods=["GET"])
@role_required("admin")
@cache.cached(timeout=60)  # cached for 60 seconds
def all_bookings():
    bookings = booking.query.all()
    return jsonify([{
        "id": b.id,
        "username": b.user.username,
        "user_id": b.user.id,
        "trek_name": b.trek.name,
        "trek_id": b.trek.id,
        "location": b.trek.location,
        "difficulty": b.trek.difficulty,
        "trek_state": b.trek.trek_state,
        "booking_status": b.status,
        "trek_status": b.trek.trek_status,
        "booked_at": b.booked_at.isoformat() if b.booked_at else None,
    } for b in bookings])


# ---------------------------------------------------------------------------
# Staff dashboard
# ---------------------------------------------------------------------------
def progress_percent(trek):
    if trek.trek_state == "completed":
        return 100
    if trek.trek_state == "ongoing":
        return 50
    return 0


@app.route("/staff/overview/<int:user_id>", methods=["GET"])
@role_required("staff")
def staff_overview(user_id):
    if current_user().id != user_id:
        return jsonify({"error": "You can only view your own dashboard"}), 403
    user = User.query.filter_by(id=user_id, role="staff").first()
    if not user:
        return jsonify({"error": "Staff not found"}), 404

    treks = user.assigned_treks
    trek_list = []
    for t in treks:
        data = serialize_trek(t)
        data["progress"] = progress_percent(t)
        trek_list.append(data)

    completed = [t for t in treks if t.trek_state == "completed"]
    current = [t for t in treks if t.trek_state != "completed"]
    registered = sum(len(active_bookings(t)) for t in treks)
    open_bookings = sum(1 for t in treks if t.trek_status == "Open")

    return jsonify({
        "staff": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "profile_completed": user.profile_completed,
        },
        "stats": {
            "total_conducted": len(completed),
            "current_assigned": len(current),
            "registered_trekkers": registered,
            "open_bookings": open_bookings,
        },
        "treks": trek_list,
    })


@app.route("/staff/trek/<int:trek_id>", methods=["GET"])
@role_required("staff")
def staff_trek(trek_id):
    trek = treaking_table.query.get(trek_id)
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    if trek.coordinator_id != current_user().id:
        return jsonify({"error": "Not authorized for this trek"}), 403
    data = serialize_trek(trek)
    data["progress"] = progress_percent(trek)
    data["available_slots"] = trek.slots - len(active_bookings(trek))
    return jsonify(data)


@app.route("/staff/request_slot_change", methods=["POST"])
@role_required("staff")
def request_slot_change():
    data = request.get_json()
    trek = treaking_table.query.get(data["trek_id"])
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    if trek.coordinator_id != current_user().id:
        return jsonify({"error": "Not authorized for this trek"}), 403
    if trek.pending_approval:
        return jsonify({"error": "A change is already pending approval"}), 400

    new_slots = int(data["slots"])
    booked = len(active_bookings(trek))
    if new_slots < booked:
        return jsonify({"error": f"Slots cannot be less than current bookings ({booked})"}), 400

    trek.pending_slots = new_slots
    trek.pending_approval = True
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Slot change requested, awaiting admin approval"})


@app.route("/staff/toggle_booking", methods=["POST"])
@role_required("staff")
def staff_toggle_booking():
    data = request.get_json()
    trek = treaking_table.query.get(data["trek_id"])
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    if trek.coordinator_id != current_user().id:
        return jsonify({"error": "Not authorized for this trek"}), 403
    trek.trek_status = "Closed" if trek.trek_status == "Open" else "Open"
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Booking status updated", "trek_status": trek.trek_status})


@app.route("/staff/update_state", methods=["POST"])
@role_required("staff")
def staff_update_state():
    data = request.get_json()
    trek = treaking_table.query.get(data["trek_id"])
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    if trek.coordinator_id != current_user().id:
        return jsonify({"error": "Not authorized for this trek"}), 403

    new_state = data["trek_state"]
    if new_state == "ongoing" and trek.trek_state != "upcoming":
        return jsonify({"error": "Only an upcoming trek can be marked ongoing"}), 400
    if new_state == "completed" and trek.trek_status != "Closed":
        return jsonify({"error": "Close booking before marking the trek completed"}), 400

    trek.trek_state = new_state
    if new_state == "completed":
        for b in trek.bookings:
            if b.status == "Booked":
                b.status = "Completed"
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Trek state updated"})


@app.route("/staff/edit_trek", methods=["POST"])
@role_required("staff")
def staff_edit_trek():
    data = request.get_json()
    trek = treaking_table.query.get(data["trek_id"])
    if not trek:
        return jsonify({"error": "Trek not found"}), 404
    if trek.coordinator_id != current_user().id:
        return jsonify({"error": "Not authorized for this trek"}), 403
    if trek.pending_approval:
        return jsonify({"error": "A change is already pending approval"}), 400

    booked = len(active_bookings(trek))
    changes = {
        "name": data.get("name", trek.name),
        "location": data.get("location", trek.location),
        "duration": data.get("duration", trek.duration),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
    }
    if data.get("slots") is not None:
        if int(data["slots"]) < booked:
            return jsonify({"error": f"Slots cannot be less than current bookings ({booked})"}), 400
        changes["slots"] = int(data["slots"])

    trek.pending_changes = json.dumps(changes)
    trek.pending_approval = True
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Edit submitted, awaiting admin approval"})


# ---------------------------------------------------------------------------
# Profile (shared by staff + users)
# ---------------------------------------------------------------------------
@app.route("/profile/<int:user_id>", methods=["GET"])
@role_required("user", "staff")
def get_profile(user_id):
    if current_user().id != user_id:
        return jsonify({"error": "You can only view your own profile"}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "status": user.status,
        "profile_completed": user.profile_completed,
        "full_name": user.full_name,
        "phone": user.phone,
        "age": user.age,
        "gender": user.gender,
        "address": user.address,
        "emergency_contact_name": user.emergency_contact_name,
        "emergency_contact_number": user.emergency_contact_number,
        "blood_group": user.blood_group,
        "medical_conditions": user.medical_conditions,
        "fitness_level": user.fitness_level,
    })


@app.route("/profile/<int:user_id>", methods=["POST"])
@role_required("user", "staff")
def save_profile(user_id):
    if current_user().id != user_id:
        return jsonify({"error": "You can only edit your own profile"}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    user.full_name = data.get("full_name", user.full_name)
    user.phone = data.get("phone", user.phone)
    user.age = data.get("age", user.age)
    user.gender = data.get("gender", user.gender)
    user.address = data.get("address", user.address)
    user.emergency_contact_name = data.get("emergency_contact_name", user.emergency_contact_name)
    user.emergency_contact_number = data.get("emergency_contact_number", user.emergency_contact_number)
    user.blood_group = data.get("blood_group", user.blood_group)
    user.medical_conditions = data.get("medical_conditions", user.medical_conditions)
    user.fitness_level = data.get("fitness_level", user.fitness_level)
    user.profile_completed = True
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Profile saved successfully"})


# ---------------------------------------------------------------------------
# User dashboard
# ---------------------------------------------------------------------------
def serialize_booking(b):
    return {
        "booking_id": b.id,
        "status": b.status,
        "booked_at": b.booked_at.isoformat() if b.booked_at else None,
        "trek_id": b.trek.id,
        "name": b.trek.name,
        "location": b.trek.location,
        "difficulty": b.trek.difficulty,
        "duration": b.trek.duration,
        "trek_status": b.trek.trek_status,
        "trek_state": b.trek.trek_state,
        "coordinator_name": b.trek.coordinator.username if b.trek.coordinator else None,
    }


@app.route("/user/overview/<int:user_id>", methods=["GET"])
@role_required("user")
def user_overview(user_id):
    if current_user().id != user_id:
        return jsonify({"error": "You can only view your own dashboard"}), 403
    user = User.query.filter_by(id=user_id, role="user").first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    booked = [serialize_booking(b) for b in user.bookings if b.status == "Booked"]
    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "profile_completed": user.profile_completed,
        },
        "booked_treks": booked,
    })


@app.route("/user/bookings/<int:user_id>", methods=["GET"])
@role_required("user")
def user_bookings(user_id):
    if current_user().id != user_id:
        return jsonify({"error": "You can only view your own bookings"}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify([serialize_booking(b) for b in user.bookings])


@app.route("/user/treks/<int:user_id>", methods=["GET"])
@role_required("user")
@cache.cached(timeout=60)  # cached per user (URL includes user_id)
def user_treks(user_id):
    if current_user().id != user_id:
        return jsonify({"error": "You can only view your own treks"}), 403
    booked_ids = {
        b.treaking_table_id
        for b in booking.query.filter_by(user_id=user_id, status="Booked").all()
    }
    treks = treaking_table.query.all()
    result = []
    for t in treks:
        data = serialize_trek(t)
        data["available_slots"] = t.slots - len(active_bookings(t))
        data["already_booked"] = t.id in booked_ids
        result.append(data)
    return jsonify(result)


@app.route("/book_trek", methods=["POST"])
@role_required("user")
def book_trek():
    data = request.get_json()
    user = current_user()
    trek = treaking_table.query.get(data.get("trek_id"))
    if not user or not trek:
        return jsonify({"error": "User or trek not found"}), 404
    if user.status == "Blacklisted":
        return jsonify({"error": "Blacklisted users cannot book treks"}), 403
    if trek.trek_status != "Open":
        return jsonify({"error": "Booking is closed for this trek"}), 400
    if trek.trek_state != "upcoming":
        return jsonify({"error": "This trek is no longer upcoming"}), 400

    already = booking.query.filter_by(
        user_id=user.id, treaking_table_id=trek.id, status="Booked"
    ).first()
    if already:
        return jsonify({"error": "You have already booked this trek"}), 400

    if trek.slots - len(active_bookings(trek)) <= 0:
        return jsonify({"error": "No slots available"}), 400

    db.session.add(booking(user_id=user.id, treaking_table_id=trek.id, status="Booked"))
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Trek booked successfully"}), 201


@app.route("/cancel_booking", methods=["POST"])
@role_required("user")
def cancel_booking():
    data = request.get_json()
    book = booking.query.get(data.get("booking_id"))
    if not book:
        return jsonify({"error": "Booking not found"}), 404
    if book.user_id != current_user().id:
        return jsonify({"error": "Not authorized"}), 403
    if book.status != "Booked":
        return jsonify({"error": "Only active bookings can be cancelled"}), 400
    book.status = "Cancelled"
    db.session.commit()
    clear_cache()   # remove old cached data
    return jsonify({"message": "Booking cancelled successfully"})


@app.route("/view_coordinator_profile/<int:user_id>", methods=["GET"])
@role_required()
def view_coordinator_profile(user_id):
    user = User.query.filter_by(id=user_id, role="staff").first()
    if not user:
        return jsonify({"error": "Coordinator not found"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "full_name": user.full_name,
    })


def run_migrations():
    """Lightweight SQLite migration: add columns introduced after first run."""
    existing = [row[1] for row in db.session.execute(text("PRAGMA table_info(treaking_table)"))]
    if "pending_changes" not in existing:
        db.session.execute(text("ALTER TABLE treaking_table ADD COLUMN pending_changes TEXT"))
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        run_migrations()
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", email="admin@gmail.com", password=hash_password("admin"),
                         role="admin", status="Active")
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)
