from app import app, db
from models import User

with app.app_context():
    def revoke_attendance_by_email(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            print("User not found")
            return

        user.can_mark_attendance = False
        db.session.commit()
        print(f"Permission revoked for {user.name}")

    revoke_attendance_by_email("aulia.meilinda@gdajogja.sch.id")
