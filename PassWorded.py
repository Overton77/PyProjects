from tkinter import *
from tkinter import messagebox
import re
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]

    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    passwords = "".join(password_list)

    password_entry.insert(0, passwords)

    pyperclip.copy(passwords)
    #this will copy the password instantaneously when the function is called
    #by the button

# ---------------------------- SAVE PASSWORD ------------------------------- #

def is_valid_email(email):
    """Simple regex to validate the email """
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return re.match(email_regex, email)

def is_valid_website(website):
    """Validates the length of the website to be 4 or more characters"""
    return len(website) >= 4

def is_valid_password(password):
    """Validates the password length"""
    return len(password) >= 6

def find_password():
    website_search_term = website_input.get().strip().lower()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="Data File Not Found")
    else:
        website_found = [website for website in data if website_search_term in website.lower()]
        if website_found:
            website = website_found[0]
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website_search_term}")


def save_inputs():
    try:
        website = website_input.get().strip()
        password = password_input.get().strip()
        email = email_input.get().strip()
        new_data = {
            website: {
                "email": email,
                "password": password,
            }
        }

        if len(website) == 0 or len(password) == 0 or len(email) == 0:
            messagebox.showinfo(title="Oops", message="You left fields empty")
        else:

            if (
                is_valid_email(email)
                and is_valid_password(password)
                and is_valid_website(website)
                 ):
                try:
                    with open("data.json", "r") as data_file:
                        #Reading old data
                        data = json.load(data_file)
                        # updating old data with new data
                except FileNotFoundError:
                    with open('data.json', 'w') as data_file:
                        json.dump(new_data, data_file, indent=4)
                else:
                    # Updating old data with new_data
                    data.update(new_data)

                    with open("data.json", "w") as data_file:
                        json.dump(data, data_file, indent=4)

                finally:
                    website_entry.delete(0, END)
                    password_entry.delete(0, END)
                    email_entry.delete(0, END)
    except ValueError as v:
        print(v, "The details could not be accounted for correctly ")
    finally:
        print("Program ran no matter what")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(pady=20, padx=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_png = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_png) # this is the x and y positions of the image
canvas.grid(column=1, row=1)


website_label = Label(text="Website:", font=("Arial", 8))
website_label.grid(column=0, row=2)

website_input = StringVar()
website_entry = Entry(width=35, textvariable=website_input)
website_entry.grid(column=1, row=2, columnspan=2)
website_entry.focus()

email_label = Label(text="Email/Username", font=("Arial", 8))
email_label.grid(column=0, row=3)

email_input = StringVar()
email_entry = Entry(width=35, textvariable=email_input)
email_entry.grid(column=1, row=3, columnspan=2)

password_label = Label(text="Password", font=("Arial", 8))
password_label.grid(column=0, row=4)

password_input = StringVar()
password_entry = Entry(width=21, textvariable=password_input, show="*")
password_entry.grid(column=1, row=4, columnspan=1)

password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(column=3, row=4)

add_button = Button(text="Add", width=36, command=save_inputs)
add_button.grid(column=1, row=5, columnspan=2)

search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=2)





window.mainloop()


