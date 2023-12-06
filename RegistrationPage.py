"""
    Zadanie zaliczeniowe z języka Python
    Imię i nazwisko ucznia: Bartłomiej Labenz
    Data wykonania zadania: 06.12.2023
    Treść zadania: Wypożyczalnia samochodów
    Opis funkcjonalności aplikacji: w pliku readme.md
"""

import flet as ft
from flet.security import encrypt, decrypt
from re import match
from key import KEY
import os

class RegistrationPage(ft.UserControl):
    def __init__(self):
        # Initializing the RegistrationPage attributes including text fields for user details
        super().__init__()
        self.nameField = ft.TextField(label="First name", width=400)
        self.lastNameField = ft.TextField(label="Last name", width=400)
        self.emailField = ft.TextField(label="Email", width=400)
        self.passwordField = ft.TextField(label="Password", width=400, password=True, can_reveal_password=True)
        
    def build(self):
        # Adding text fields and buttons to collect user details
        return ft.Container(
            ft.Row([
                    ft.Column([
                    self.nameField,
                    self.lastNameField,
                    self.emailField,
                    self.passwordField,
                    ft.ElevatedButton(text="Sign up", on_click=self.saveUserData, width=400, height=40),
                    ft.ElevatedButton(text="Back", icon=ft.icons.ARROW_BACK, on_click=lambda _: self.page.go('/'), width=400, height=40)
                ],alignment=ft.MainAxisAlignment.CENTER,),
            ],alignment=ft.MainAxisAlignment.CENTER,)
        )
    
    # Method to save user registration data
    def saveUserData(self, e):
    
        def checkEmail(email):
            # Function that check if the email is consistent with the pattern
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            return match(pattern, email) is not None
        
        # Check if the 'userdata' directory exists, if not, create it
        if "userdata" not in os.listdir("./assets"):
            os.mkdir("./assets/userdata")
        
        # Create 'userdata.txt' if it doesn't exist
        if os.path.exists("./assets/userdata/userdata.txt") == False:
            with open(f"./assets/userdata/userdata.txt", "x"):
                pass
            
            try:
                # Create default admin account
                with open("./assets/userdata/userdata.txt", "at") as f:
                    admin = encrypt("admin", KEY)
                    f.write(f"{admin},{admin},{admin},{admin}\n")
            except FileNotFoundError as e:
                print(f"File not found: {e}")
            except Exception as e:
                print(f"Error: {e}")
        
        # Retrieve user details from the text fields and remove spaces
        name, lastName, email, password = self.nameField.value.strip(), self.lastNameField.value.strip(), \
                                             self.emailField.value.strip(), self.passwordField.value.strip()
        name, lastName, email, password = (i.replace(" ","") for i in [name, lastName, email, password])
        
        # Validate if all fields are filled
        if name == "" or lastName == "" or email == "" or password == "":
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Fill all the data", color="white"), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return False
        
        elif checkEmail(email) == False:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Email is incorrect", color="white"), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return False
        
        # Encrypt user details for secure storage
        name, lastName, email, password = encrypt(name, KEY), encrypt(lastName, KEY), \
                                        encrypt(email, KEY), encrypt(password, KEY)
        
        try:
            # Read existing userdata and check if the email already exists
            with open("./assets/userdata/userdata.txt", "rt+") as f:
                userdata = [i.strip().split(",") for i in f]
                emails = [decrypt(userdata[i][0], KEY) for i in range(len(userdata))]
                if self.emailField.value.strip() in emails:
                    # Display an error message if the email already exists
                    self.page.snack_bar = ft.SnackBar(ft.Text(f"An account with this email already exists", color="white"), bgcolor="red")
                    self.page.snack_bar.open = True
                    self.page.update()
                    return False
                
            with open("./assets/userdata/userdata.txt", "at+") as f:
                # Save user data if the email is unique
                if f"{email}" not in userdata:
                    f.write(f"{email},{password},{name},{lastName}\n")
                    self.page.snack_bar = ft.SnackBar(ft.Text(f"The account has been successfully registered", color="white"), bgcolor="green")
                    self.page.snack_bar.open = True
                    self.page.update()
        except FileNotFoundError as e:
            print(f"File not found")
        except Exception as e:
            print(f"Error: {e}")
