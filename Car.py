"""
    Zadanie zaliczeniowe z języka Python
    Imię i nazwisko ucznia: Bartłomiej Labenz
    Data wykonania zadania: 06.12.2023
    Treść zadania: Wypożyczalnia samochodów
    Opis funkcjonalności aplikacji: w pliku readme.md
"""

import flet as ft
import os
from shutil import rmtree

class Car(ft.UserControl):
    def __init__(self, brand, model, carYear, mileage, registration, available, rent, visibility):
        # Initializing Car attributes
        super().__init__()
        self.brand = brand
        self.model = model
        self.carYear = carYear
        self.mileage = mileage
        self.registration = registration
        self.available = True if available == "True" else False
        self.lastPerson = self.getLastPerson()
        self.img = self.checkImg()
        self.bcolor = "green" if self.available else "red"
        self.rent = rent
        self.visibility = visibility
        self.getvisibility()
        # Dialog for displaying car history
        self.historyDialog = ft.AlertDialog(
                                modal=True,
                                actions_alignment=ft.MainAxisAlignment.CENTER,
                            )


    def build(self):
        # Building the UI for displaying car details based on visibility settings
        if self.visibility == True:
            # UI if car avaiable
            return ft.Container(
                content=ft.Column([
                        ft.Row([
                            ft.Image(src=self.img, height=100)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.Text(value=self.brand + " " + self.model, size=30)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.Text(value=self.registration, size=30)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.Text(value=self.lastPerson, color=ft.colors.BLACK, size=30, weight=ft.FontWeight.BOLD)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.Text(value=str("Available" if self.available else "Unavailable"), color=ft.colors.BLACK, size=30, weight=ft.FontWeight.BOLD)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.ElevatedButton(text=("Rent" if self.available else "Return"), icon=ft.icons.ADD, bgcolor=ft.colors.BLACK, scale=1.2, width=150 ,on_click=self.rentClicked),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=300,
                height=450,
                bgcolor=self.bcolor,
                border_radius=ft.border_radius.all(5),
            )
        elif self.visibility == False:
            # UI if car unavaiable
            return ft.Container(
                content=ft.Column([
                        ft.Row([
                            ft.Image(src=self.img, height=100)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.Text(value=self.brand + " " + self.model, size=30)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.Text(value=self.registration, size=30)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.Text(value=self.lastPerson, color=ft.colors.BLACK, size=30, weight=ft.FontWeight.BOLD)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.Text(value=str("Available" if self.available else "Unavailable"), color=ft.colors.BLACK, size=30, weight=ft.FontWeight.BOLD)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=300,
                height=450,
                bgcolor=self.bcolor,
                border_radius=ft.border_radius.all(5),
            )
        else:
            # UI if admin
            return ft.Container(
                content=ft.Column([
                        self.historyDialog,
                        ft.Row([
                            ft.Image(src=self.img, height=100)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.Text(value=self.brand + " " + self.model, size=30)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.Text(value=self.registration, size=30)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.Text(value=self.lastPerson, color=ft.colors.BLACK, size=30, weight=ft.FontWeight.BOLD)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.Text(value=str("Available" if self.available else "Unavailable"), color=ft.colors.BLACK, size=30, weight=ft.FontWeight.BOLD)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row([
                            ft.Text(),
                            ft.ElevatedButton(text="History", icon=ft.icons.LIST, bgcolor=ft.colors.BLACK, scale=1.2, width=150 ,on_click=self.checkHistory),
                            ft.IconButton(icon=ft.icons.REMOVE, bgcolor=ft.colors.BLACK, on_click=self.deleteCar, icon_color=ft.colors.BLUE_200)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=300,
                height=450,
                bgcolor=self.bcolor,
                border_radius=ft.border_radius.all(5),
            )
    
    # Handler for rent button click
    def rentClicked(self, e):
        self.rent(self)
    
    # Function for visibility status
    def getvisibility(self):
        self.visibility(self)
    
    # Check and retrieve the car's image path
    def checkImg(self):
        if os.path.exists(f"./assets/cars/{self.brand}-{self.model}-{self.registration}/img.png"):
            return f"./assets/cars/{self.brand}-{self.model}-{self.registration}/img.png"
        elif os.path.exists(f"./assets/cars/{self.brand}-{self.model}-{self.registration}/img.jpg"):
            return f"./assets/cars/{self.brand}-{self.model}-{self.registration}/img.jpg"
        else:
            return "./assets/img/carMiss.png"
    
    # Retrieve the last person who interacted with the car
    def getLastPerson(self):
        if os.path.exists(f"./assets/cars/{self.brand}-{self.model}-{self.registration}/history.txt") == False:
            with open(f"./assets/cars/{self.brand}-{self.model}-{self.registration}/history.txt", "x"):
                pass
        historydata = []
        try:
            with open(f"./assets/cars/{self.brand}-{self.model}-{self.registration}/history.txt", "rt+") as f:
                [historydata.append(i.strip().split(" ")) for i in f]
        except FileNotFoundError:
            print("File not Found")
        except Exception as e:
            print(f"Error: {e}")
                
        if historydata != []:
            if len(historydata[-1][-1]) < 12:
                return historydata[-1][0] + " " + historydata[-1][1]
            else:
                return ""
        else:
            return ""
     
    # Display car history in an alert dialog   
    def checkHistory(self, e):
        def accept(e):
            self.historyDialog.open = False
            self.update()
        
        
        self.historyDialog.actions = [(ft.TextButton("Close", on_click=accept))]
        self.historyDialog.title = ft.Text(value=f"History: {self.brand} {self.model} {self.registration}")
        self.historyDialog.on_dismiss = accept
        
        try:
            with open(f"./assets/cars/{self.brand}-{self.model}-{self.registration}/history.txt", "rt") as f:
                historyData = [i.strip().split(" ") for i in f]
                self.historyDialog.content = ft.ListView(width=self.page.width - 400, height=self.page.height)
                for i in range(len(historyData) - 1, -1, -1):
                    self.historyDialog.content.controls.append(ft.Text(f"User: {historyData[i][0]} {historyData[i][1]}", size=30, weight="bold"))
                    self.historyDialog.content.controls.append(ft.Text(f"Date of borrowing and returning: from {historyData[i][2].replace('/', ' to ')}", color="blue", size=25))
                    self.historyDialog.content.controls.append(ft.Text())
                
        except FileNotFoundError:
            print("File not Found")
        except Exception as e:
            print(f"Error: {e}")


        self.historyDialog.open = True
        self.update()
    
    # Delete car directory and display a notification 
    def deleteCar(self, e):
        if os.path.exists("./assets/cars"):
            if os.path.exists(f"./assets/cars/{self.brand}-{self.model}-{self.registration}"):
                rmtree(f"./assets/cars/{self.brand}-{self.model}-{self.registration}")
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Removed: {self.brand} {self.model} {self.registration}", color="white"), bgcolor="red", duration=800)
                self.page.snack_bar.open = True
                self.page.update()