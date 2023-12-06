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

class AdminManagePage(ft.UserControl):
    def __init__(self):
        super().__init__()
        # Initializing the AdminManagePage attributes
        self.emailField = ft.TextField(label="Email", width=400)
        self.add = ft.ElevatedButton(icon=ft.icons.ADD, text="Add admin", width=400, on_click=self.addAdmin)
        self.remove = ft.ElevatedButton(icon=ft.icons.REMOVE, text="Remove admin", width=400, on_click=self.removeAdmin)
        self.listViewAdmins = ft.ListView(expand=1,height=100, width=100, auto_scroll=True)
        self.getUsers()
        
    def build(self):
        # Building the UI layout for the admin manage page including text fields and buttons
        return ft.Column([
            ft.Row([
                ft.Column([
                    self.emailField,
                    ft.Text(height=2),
                    self.add,
                    self.remove,
                ], alignment=ft.MainAxisAlignment.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text(height=50),
            ft.Row([
                self.listViewAdmins,
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER, height=500)

        
    def getUsers(self):
        self.listViewAdmins.controls.clear()
        
        # Check if 'userdata' directory exists, if not create it
        if "userdata" not in os.listdir("./assets"):
            os.mkdir("./assets/userdata")
        
        if os.path.exists("./assets/userdata/userdata.txt") == False:
            with open(f"./assets/userdata/userdata.txt", "x") as f:
                pass
            
            # Create default admin account
            with open("./assets/userdata/userdata.txt", "at") as f:
                admin = encrypt("admin", KEY)
                f.write(f"{admin},{admin},{admin},{admin}\n")
        
        
        if os.path.exists("./assets/userdata/admin.txt") == False:
            with open(f"./assets/userdata/admin.txt", "x"):
                pass
            
            try:
                # Grant admin to default admin account
                with open("./assets/userdata/admin.txt", "at") as f:
                    admin = encrypt("admin", KEY)
                    f.write(f"{admin}\n")
            except FileNotFoundError as e:
                print(f"File not found: {e}")
            except Exception as e:
                print(f"Error: {e}")
            
        try:
            # Read existing userdata and check if the email already exists
            with open("./assets/userdata/admin.txt", "rt+") as f:
                emails = [decrypt(i, KEY) for i in f]
                [self.listViewAdmins.controls.append(ft.Text(i)) for i in emails]
                   
        except FileNotFoundError as e:
                print(f"File not found: {e}")
        except Exception as e:
            print(f"Error: {e}")


    def addAdmin(self, e):
        emailvalue = self.emailField.value.strip()
        
        def checkEmail(email):
            # Function that check if the email is consistent with the pattern
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            return match(pattern, email) is not None
        
        # Check if email field is empty or is not matching pattern
        if emailvalue == "" or checkEmail(emailvalue) == False:
            return False
        else:
            
            try:
                with open("./assets/userdata/admin.txt", "rt+") as f:
                    admins = [decrypt(i, KEY) for i in f]
                    if emailvalue in admins:
                        return False
            except FileNotFoundError as e:
                print(f"File not found: {e}")
            except Exception as e:
                print(f"Error: {e}")
            
            try:
                with open("./assets/userdata/admin.txt", "at+") as f:
                    # Find user data and grant admin status
                    email = encrypt(emailvalue, KEY)
                    f.write(f"{email}\n")
            except FileNotFoundError as e:
                print(f"File not found: {e}")
            except Exception as e:
                print(f"Error: {e}")
            self.getUsers()
            self.update()
                
    def removeAdmin(self, e):
        emailvalue = self.emailField.value.strip()
        admins = []
        
        # Check if email field is not empty
        if emailvalue == "":
            return False
        else:
            try:
                with open("./assets/userdata/admin.txt", "rt+") as f:
                    admins = [decrypt(i, KEY) for i in f]
                    if emailvalue in admins:
                        # If email in admins remove
                        admins.remove(emailvalue)
                    else:
                        return False
            except FileNotFoundError as e:
                print(f"File not found: {e}")
            except Exception as e:
                print(f"Error: {e}")
                
            try:
                with open("./assets/userdata/admin.txt", "wt+") as f:
                    # Save file without removed email
                    [f.write(encrypt(i, KEY) + "\n") for i in admins]
            except FileNotFoundError as e:
                print(f"File not found: {e}")
            except Exception as e:
                print(f"Error: {e}")
    
            self.getUsers()
            self.update()