"""
    Zadanie zaliczeniowe z języka Python
    Imię i nazwisko ucznia: Bartłomiej Labenz
    Data wykonania zadania: 06.12.2023
    Treść zadania: Wypożyczalnia samochodów
    Opis funkcjonalności aplikacji: w pliku readme.md
"""

import flet as ft
from flet.security import decrypt
from key import KEY
import os

class LoginPage(ft.UserControl):
    def __init__(self):
        super().__init__()
        # Initializing the LoginPage attributes including email, password, and remember me checkbox
        self.email = ft.TextField(label="Email", width=400)
        self.password = ft.TextField(label="Password", width=400, password=True, can_reveal_password=True)
        self.remember = ft.Checkbox(label="Remember me")
        
    def build(self):
        # Building the UI layout for the login page including text fields and buttons
        return ft.Container(
            ft.Row([
                    ft.Column([
                    self.email,
                    self.password,
                    self.remember,
                    ft.Text(height=2),
                    ft.ElevatedButton(text="Sign in", on_click=self.getUserData, width=400, height=40),
                    ft.ElevatedButton(text="Sign up", on_click=lambda _: self.page.go("/registration"), width=400, height=40),
                ],alignment=ft.MainAxisAlignment.CENTER,),
            ],alignment=ft.MainAxisAlignment.CENTER,)
        )
        
    def getUserData(self, e):
        # Check if 'userdata' directory exists, then retrieve and validate user data from the form
        if "userdata" not in os.listdir("./assets"):
            os.mkdir("./assets/userdata")
        
        # Validate if email and password fields are not empty
        if self.email.value.strip() == "" or self.password.value.strip() == "":
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Fill all the data", color="white"), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
        else:
            # Retrieve email and password entered by the user
            emailStr, passwordStr = self.email.value.strip(), self.password.value.strip()
            try:
                # Open and read the 'userdata.txt' file to authenticate user credentials
                with open("./assets/userdata/userdata.txt", "rt+") as f:
                    for i in f:
                        user = i.strip().split(",")
                        # Decrypt user data and check if credentials match
                        if decrypt(user[0], KEY) == emailStr and decrypt(user[1], KEY) == passwordStr:
                            name, lastName, email = decrypt(user[-2], KEY), decrypt(user[-1], KEY), decrypt(user[0], KEY)
                            # If credentials match, set user's name, last name and email in the session or client storage
                            # based on the 'remember' checkbox
                            if self.remember.value == False:
                                self.page.client_storage.clear()
                                self.page.session.set("name", name)
                                self.page.session.set("lastName", lastName)
                                self.page.session.set("email", email)
                            else:
                                self.page.client_storage.set("name", name)
                                self.page.client_storage.set("lastName", lastName)
                                self.page.client_storage.set("email", email)
                            # Redirect to the store page after successful login
                            self.page.go("/store")
            except FileNotFoundError as e:
                print(f"File not found")
            except Exception as e:
                print(f"Error: {e}")