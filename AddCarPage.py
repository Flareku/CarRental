"""
    Zadanie zaliczeniowe z języka Python
    Imię i nazwisko ucznia: Bartłomiej Labenz
    Data wykonania zadania: 06.12.2023
    Treść zadania: Wypożyczalnia samochodów
    Opis funkcjonalności aplikacji: w pliku readme.md
"""

import flet as ft
import os
import shutil
from re import match
from datetime import datetime

#
class AddCarPage(ft.UserControl):
    # Initializing fields and variables
    def __init__(self):
        super().__init__()
        self.brandField = ft.TextField(label="Brand", width=400)
        self.modelField = ft.TextField(label="Model", width=400)
        self.carYearField = ft.TextField(label="Car year", width=400)
        self.mileageField = ft.TextField(label="Mileage", width=400)
        self.registrationField = ft.TextField(label="Registration", width=400)
        self.selectedFile = ft.Text()
        self.filePath = ""
        self.fileName = ""
    
    # Building the UI layout for adding a car
    def build(self):
        pick_files_dialog = ft.FilePicker(on_result=self.pickImgResult)
        return ft.Container(ft.Row([
                ft.Column([
                    self.brandField,
                    self.modelField,
                    self.carYearField,
                    self.mileageField,
                    self.registrationField,
                    ft.Row([
                        ft.ElevatedButton(
                        "Add photo",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: pick_files_dialog.pick_files(dialog_title="Pick car photo", file_type=ft.FilePickerFileType.IMAGE, allowed_extensions=["png", "jpg"]),
                        ),
                        self.selectedFile,
                        pick_files_dialog
                    ], height=50),
                    ft.ElevatedButton("Add car", on_click=self.addCar, width=400),
                ],alignment=ft.MainAxisAlignment.CENTER),
            ],alignment=ft.MainAxisAlignment.CENTER),)
        
    # Showing a snackbar notification
    def snackBar(self, message, color):
        self.page.snack_bar = ft.SnackBar(ft.Text(message, color="white"), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()
    
    # Function to add a new car
    def addCar(self, e):
        def checkRegistration(registration):
            # Function that check if the registration is consistent with the pattern
            pattern = r'^[A-Z0-9]{2,}[A-Z0-9]{4,}$'
            return match(pattern, registration) is not None
        
        
        brand, model, carYear, mileage, registration = self.brandField.value.strip(), self.modelField.value.strip(), self.carYearField.value.strip(), \
                                                        self.mileageField.value.strip(), self.registrationField.value.strip()
        
        data = {
            "brand": brand,
            "model": model,
            "carYear": carYear,
            "mileage": mileage,
            "registration": registration,
            "available": True
        }
        
        # Validating input data
        if brand == "" or model == "" or carYear == "" or mileage ==  "" or registration == "":
            self.snackBar("Fill all the data", "red")
            return False
        
        elif carYear.isdigit() == False:
            self.snackBar("Car year must be a number", "red")
            return False
        
        elif mileage.isdigit() == False:
            self.snackBar("Mileage must be a number", "red")
            return False
        
        elif int(carYear) > datetime.now().year or int(carYear) < 1886:
            self.snackBar("Incorrect car year", "red")
            return False
        
        elif checkRegistration(registration) == False:
            self.snackBar("Incorrect registration", "red")
            return False
        
        # Checking if the car already exists
        elif os.path.exists(f"./assets/cars/{brand}-{model}-{registration}"):
            self.snackBar("This car already exist", "red")
            return False
        
        # Checking if a vehicle with the same registration exists
        for i in os.listdir("./assets/cars"):
            if registration in i:
                self.snackBar("A vehicle with such registration already exists", "red")
                return False
        
        # Creating directory for the new car
        os.mkdir(f"./assets/cars/{brand}-{model}-{registration}")
        
        if self.filePath != "" and self.fileName != "":
            if "png" in self.fileName:
                shutil.copy(self.filePath, f"./assets/cars/{brand}-{model}-{registration}/img.png")
            elif "jpg" in self.fileName:
                shutil.copy(self.filePath, f"./assets/cars/{brand}-{model}-{registration}/img.jpg")
            
        try:
            # Creating necessary text files for car data
            with open(f"./assets/cars/{brand}-{model}-{registration}/history.txt", "x"):
                pass

            with open(f"./assets/cars/{brand}-{model}-{registration}/data.txt", "wt+") as f:
                [f.write(f"{k}: {v}\n" )for k, v in data.items()]
                self.snackBar("Added successfully", "green")
                self.update()
                
        except FileNotFoundError as e:
            print(f"File not found")
        except Exception as e:
            print(f"Error: {e}")
            
    def pickImgResult(self, e: ft.FilePickerResultEvent):
        # Handling the result of picking an image file
        if e.files != []:
            self.selectedFile.value = e.files[0].name
            self.filePath = e.files[0].path
            self.fileName = e.files[0].name
            self.selectedFile.update()
