import argparse
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Base, User

# Database setup
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def register_user(role, first_name, last_name, password):
    hashed_password = generate_password_hash(password)
    user = User(role=role, first_name=first_name, last_name=last_name, password_hash=hashed_password)
    session.add(user)
    session.commit()
    print("Registration successful!")

def login_user(first_name, last_name, password):
    user = session.query(User).filter(User.first_name.ilike(first_name), User.last_name.ilike(last_name)).first()
    if user and check_password_hash(user.password_hash, password):
        print("Login successful!")
    else:
        print("Invalid credentials.")

def main():
    parser = argparse.ArgumentParser(description="User Registration and Login")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Register command
    register_parser = subparsers.add_parser("register", help="Register a new user")
    register_parser.add_argument("role", choices=["doctor", "patient"], help="Role of the user")
    register_parser.add_argument("first_name", help="First name of the user")
    register_parser.add_argument("last_name", help="Last name of the user")
    register_parser.add_argument("password", help="Password for the user")

    # Login command
    login_parser = subparsers.add_parser("login", help="Login for existing users")
    login_parser.add_argument("first_name", help="First name of the user")
    login_parser.add_argument("last_name", help="Last name of the user")
    login_parser.add_argument("password", help="Password for the user")

    args = parser.parse_args()

    if args.command == "register":
        register_user(args.role, args.first_name, args.last_name, args.password)
    elif args.command == "login":
        login_user(args.first_name, args.last_name, args.password)

if __name__ == "__main__":
    main()
