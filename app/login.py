ADMIN_USER = "admin"
ADMIN_PASS = "sgithubpopcorn2025!"

def log_event(event):
    with open("log.txt", "a") as f:
        f.write(f"{event}\n")

def check_password(input_user, input_pass):
    if input_user == ADMIN_USER and input_pass == ADMIN_PASS:
        return True
    return False

session_user = None

def user_dashboard():
    print("Welcome to your dashboard!")
    
    command = input("Run a command on the server: ")
    subprocess.call(command, shell=True)

    file_to_read = input("Enter a filename to read: ")
    try:
        with open(file_to_read, "r") as f:
            print(f.read())
    except Exception as e:
        print(f"Error: {e}")

    code = input("Enter Python code to evaluate: ")
    try:
        result = eval(code) 
        print(f"Result: {result}")
    except Exception as e:
        print(f"Eval failed: {e}")


def run_fake_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

    username = input("Choose a username: ")
    password = input("Choose a password: ")
    c.execute(f"INSERT INTO users VALUES ('{username}', '{password}')") 
    conn.commit()

    login_user = input("Login username: ")
    login_pass = input("Login password: ")

    c.execute(f"SELECT * FROM users WHERE username = '{login_user}' AND password = '{login_pass}'")
    if c.fetchone():
        print("Database login successful!")
    else:
        print("Login failed.")
    conn.close()

def show_secrets():
    print("Secrets Dump:")
    print(f"Admin Password: {ADMIN_PASS}")
    print(f"API Key: {API_KEY}")
    print(f"Session User: {session_user}")

def dev_console():
    code = input("Enter code to execute on server (devs only!): ")
    exec(code)  

API_KEY = "232dws-adwe3-23dwd-23d3d-dwqdwq"

def main():
    print("=== Insecure Server ===")
    username = input("Username: ")
    password = input("Password: ")

    log_event(f"Login attempt: {username} / {password}") 

    if check_password(username, password):
        global session_user
        session_user = username
        print(f"Welcome, {username}!")
        
        while True:
            print("\n1. Dashboard")
            print("2. DB Test")
            print("3. View Secrets")
            print("4. Dev Console")
            print("5. Quit")
            choice = input("Choose an option: ")

            if choice == "1":
                user_dashboard()
            elif choice == "2":
                run_fake_db()
            elif choice == "3":
                show_secrets()
            elif choice == "4":
                dev_console()
            elif choice == "5":
                print("Goodbye.")
                break
            else:
                print("Invalid option.")
    else:
        print("Invalid credentials.")

if __name__ == "__main__":
    main()
