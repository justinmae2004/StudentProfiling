import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

# Initialize the main application window
root = tk.Tk()
root.title("Application Form")
root.minsize(300, 300)
root.configure(borderwidth=10, relief="groove", bd=10)

# Initialize the database (dictionary)
database = {}

# Function to clear entry fields
def clear_entry_fields():
    # Clear all entry fields for username and password in both login and registration forms.
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    if 'register_username_entry' in globals():
        register_username_entry.delete(0, tk.END)
    if 'register_password_entry' in globals():
        register_password_entry.delete(0, tk.END)
    if 'register_confirm_password_entry' in globals():
        register_confirm_password_entry.delete(0, tk.END)

# Function to validate login credentials
def validate_login():
    # Validate the login credentials entered by the user.
    username = username_entry.get()
    password = password_entry.get()
    if username in database and database[username]["password"] == password:
        messagebox.showinfo("Login Success", "You have successfully logged in.")
        dashboard(username)
        clear_entry_fields()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to display the register form
def show_register_form():
    #Display the registration form for new users to register.
    login_frame.pack_forget()
    global register_frame
    register_frame = tk.Frame(root, bg="#3C3B6E")
    register_frame.pack(fill="both", expand=True)

    # Create register form
    global register_username_entry, register_password_entry, register_confirm_password_entry
    register_username_label = tk.Label(register_frame, text="Username:", bg="#C3E7FD", fg="#4E6D7A", relief="solid")
    register_username_label.pack(fill='x', expand=True, padx=20)
    register_username_entry = tk.Entry(register_frame, bg="#C3E7FD", fg="#4E6D7A", bd=2)
    register_username_entry.pack(fill='both', expand=True, padx=20)
    
    register_password_label = tk.Label(register_frame, text="Password:", bg="#C3E7FD", fg="#4E6D7A", relief="solid")
    register_password_label.pack(fill='x', expand=True, padx=20)
    register_password_entry = tk.Entry(register_frame, show="*", bg="#C3E7FD", fg="#4E6D7A", bd=2)
    register_password_entry.pack(fill='both', expand=True, padx=20)
    
    register_confirm_password_label = tk.Label(register_frame, text="Confirm Password:", bg="#C3E7FD", fg="#4E6D7A", relief="solid")
    register_confirm_password_label.pack(fill='x', expand=True, padx=20)
    register_confirm_password_entry = tk.Entry(register_frame, show="*", bg="#C3E7FD", fg="#4E6D7A", bd=2)
    register_confirm_password_entry.pack(fill='both', expand=True, padx=20)

    register_profile_button = tk.Button(register_frame, text="Upload Profile Picture", command=upload_profile_picture, bg="#FFD700", fg="#3C3B6E")
    register_profile_button.pack(fill='x', expand=True, padx=50, pady=(0, 10))

    register_submit_button = tk.Button(register_frame, text="Submit", command=register_user, bg="#FFD700", fg="#3C3B6E")
    register_submit_button.pack(fill='x', expand=True, padx=50, pady=(0, 10))

# Function to upload profile picture
def upload_profile_picture():
    #Allow the user to upload a profile picture and display it in the registration form.
    filename = filedialog.askopenfilename(title="Choose your profile picture", filetypes=[("Image files", "*.jpg *.jpeg")])
    if filename:
        load = Image.open(filename)
        load = load.resize((100, 100))
        global profile_image
        profile_image = ImageTk.PhotoImage(load)
        
        profile_frame = tk.Frame(register_frame, bg="#C3E7FD", width=120, height=120)
        profile_frame.pack(pady=10)
        profile_frame.grid_propagate(False)
        profile_frame.columnconfigure(0, weight=1)
        profile_frame.rowconfigure(0, weight=1)

        profile_picture = tk.Label(profile_frame, image=profile_image, bg="#C3E7FD")
        profile_picture.image = profile_image
        profile_picture.grid(row=0, column=0, sticky="nsew")
        profile_picture.pack()

# Function to register a new user
def register_user():
    #Register a new user with a username and password, and optionally a profile picture.
    username = register_username_entry.get()
    password = register_password_entry.get()
    confirm_password = register_confirm_password_entry.get()

    if username.strip() != "" and password.strip() != "" and confirm_password.strip() != "":
        if password == confirm_password:
            if username not in database:
                database[username] = {"password": password}
                if 'profile_image' in globals():
                    database[username]["profile_image"] = profile_image
                print(f"User registered successfully: {username}", database[username])
                register_frame.pack_forget()
                login_frame.pack(fill='both', expand=True)
                clear_entry_fields()
                messagebox.showinfo("Registration Success", "You have successfully registered.")
            else:
                messagebox.showerror("Registration Failed", "Username already exists")
        else:
            messagebox.showerror("Registration Failed", "Passwords do not match")
    else:
        messagebox.showerror("Registration Failed", "Please fill out all fields")

# Function to display the dashboard
def dashboard(username):
    #Display the dashboard for the logged-in user, showing their profile picture and a welcome message.
    login_frame.pack_forget()
    global dashboard_frame
    dashboard_frame = tk.Frame(root, bg="#3C3B6E")
    dashboard_frame.pack(fill='both', expand=True)

    if username in database and "profile_image" in database[username]:
        profile_frame = tk.Frame(dashboard_frame, bg="#C3E7FD", width=120, height=120)
        profile_frame.pack(pady=10)
        profile_frame.grid_propagate(False)
        profile_frame.columnconfigure(0, weight=1)
        profile_frame.rowconfigure(0, weight=1)

        profile_picture = tk.Label(profile_frame, image=database[username]["profile_image"], bg="#C3E7FD")
        profile_picture.image = database[username]["profile_image"]
        profile_picture.grid(row=0, column=0, sticky="nsew")
        profile_picture.pack()

    welcome_label = tk.Label(dashboard_frame, text="Welcome, " + username, bg="#C3E7FD", fg="#4E6D7A")
    welcome_label.pack(padx=20, pady=10)

    logout_button = tk.Button(dashboard_frame, text="Logout", command=logout, bg="#FFD700", fg="#3C3B6E")
    logout_button.pack(pady=10)

# Function to log out
def logout():
    #Log out the current user and return to the login screen.
    dashboard_frame.pack_forget()
    login_frame.pack(fill='both', expand=True)
    clear_entry_fields()

# Creating the login frame
login_frame = tk.Frame(root, bg="#3C3B6E")
login_frame.pack(fill='both', expand=True)

# Username label and entry field
username_label = tk.Label(login_frame, text="Username", bg="#C3E7FD", fg="#4E6D7A", relief="solid")
username_label.pack(fill='x', expand=True, padx=20)
username_entry = tk.Entry(login_frame, bg="#C3E7FD", fg="#4E6D7A", bd=2)
username_entry.pack(fill='both', expand=True, padx=20)

# Password label and entry field
password_label = tk.Label(login_frame, text="Password", bg="#C3E7FD", fg="#4E6D7A", relief="solid")
password_label.pack(fill='x', expand=True, padx=20)
password_entry = tk.Entry(login_frame, show="*", bg="#C3E7FD", fg="#4E6D7A", bd=2)
password_entry.pack(fill='both', expand=True, padx=20)

# Login and Register buttons
login_button = tk.Button(login_frame, text="Login", command=validate_login, bg="#FFD700", fg="#3C3B6E")
login_button.pack(fill='x', expand=True, padx=50, pady=(10, 5))
register_button = tk.Button(login_frame, text="Register", command=show_register_form, bg="#FFD700", fg="#3C3B6E")
register_button.pack(fill='x', expand=True, padx=50, pady=(0, 10))

# Start the main loop
root.mainloop()
