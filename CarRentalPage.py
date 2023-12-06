"""
    Zadanie zaliczeniowe z języka Python
    Imię i nazwisko ucznia: Bartłomiej Labenz
    Data wykonania zadania: 06.12.2023
    Treść zadania: Wypożyczalnia samochodów
    Opis funkcjonalności aplikacji: w pliku readme.md
"""

import flet as ft
from flet.security import encrypt, decrypt
import os
from Car import Car
from key import KEY
import datetime as dt

class CarRentalPage(ft.UserControl):
    def __init__(self, name, lastName, email, admin=False):
        super().__init__()
        # Initializing the Car Rental Page attributes
        self.name = name
        self.lastName = lastName
        self.email = email
        self.admin = admin
        self.carlist = []
        self.carlistColumn = ft.Row(wrap=True, width=self.width, vertical_alignment=ft.MainAxisAlignment.CENTER)
        self.getCars()
        self.checkAdmin()

    def build(self):
        # Building the user interface for the Car Rental Page
        header = ft.Row([
            ft.Text(),
            ft.Text("Car Rental", size=30, font_family="Arial"),
            ft.IconButton(icon=ft.icons.REFRESH, bgcolor="blue", on_click=self.__updatePageCars)
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
        user = ft.Row([ft.Text(f"{self.name} {self.lastName}", size=30, font_family="Arial")], alignment=ft.MainAxisAlignment.CENTER)
        return ft.Column([
                ft.Text(width=100),
                header,
                user,
                self.carlistColumn,
            ])

    # Temporary method to check the admin account
    def checkAdmin(self):
        # Check if 'userdata' directory exists, if not create it
        if "userdata" not in os.listdir("./assets"):
            os.mkdir("./assets/userdata")
        
        if os.path.exists("./assets/userdata/admin.txt") == False:
            with open(f"./assets/userdata/admin.txt", "x"):
                pass
            
            # Add admin to default admin account
            with open("./assets/userdata/admin.txt", "at") as f:
                admin = encrypt("admin", KEY)
                f.write(f"{admin}\n")
        
        try:
            with open("./assets/userdata/admin.txt", "rt") as f:
                for i in f:
                    email = decrypt(i, KEY)
                    if self.email == email:
                        self.admin = True
                        self.updateCars()      
                        break
        except FileNotFoundError as e:
                print(f"File not found: {e}")
        except Exception as e:
            print(f"Error: {e}")
            

    
    # Method to update the car list and UI
    def __updatePageCars(self, e=""):
        self.carlist.clear()
        self.carlistColumn.controls.clear()
        self.getCars()
        self.update()
        
    # Method to update the car list without UI
    def updateCars(self):    
        self.carlist.clear()
        self.carlistColumn.controls.clear()
        self.getCars()
    
    # Method to retrieve car data and create Car instances
    def getCars(self):
        if "assets" not in os.listdir():
            os.mkdir("assets")
        
        if "cars" not in os.listdir("./assets"):
            os.mkdir("./assets/cars")

        # Get car data from files and create Car instances for display
        for i, v in enumerate(os.listdir("./assets/cars")):
            try:
                with open(f"./assets/cars/{v}/data.txt", "rt+") as f:
                    cardata = [v.strip().split(": ")[::][1] for v in f]
                    registration = cardata[-2]
                    if registration not in self.carlist:
                        self.carlist.insert(i, registration)
                        self.carlistColumn.controls.insert(i, Car(cardata[0], cardata[1], cardata[2], cardata[3], cardata[4], cardata[5], self.rent, self.visibility))
            except FileNotFoundError as e:
                print(f"File not found")
            except Exception as e:
                print(f"Error: {e}")
            
    # Method to control the visibility of cars based on visibility status   
    def visibility(self, car):
        if self.admin == False:
            if car.available == True and self.admin == False:
                car.visibility = True
            elif car.available == False and car.lastPerson == self.name + " " + self.lastName and self.admin == False:
                car.visibility = True
            elif car.available == False and self.admin == False:
                car.visibility = False
            elif self.admin == True:
                car.visibility = "admin" 
    
    # Method to handle car renting      
    def rent(self, car):
        if self.name == "" or self.lastName == "" or self.name == None or self.lastName == None:
            return False
        nameLastname = self.name + " " + self.lastName
        for carinlist in self.carlistColumn.controls:
            historydata = []
            try:
                with open(f"./assets/cars/{car.brand}-{car.model}-{car.registration}/history.txt", "rt+") as f:
                    [historydata.append(i.strip().split(" ")) for i in f]
            except FileNotFoundError as e:
                print(f"File not found")
            except Exception as e:
                print(f"Error: {e}")
            if car == carinlist:
                if carinlist.available == True:
                    # If car is avaiable
                    if historydata != []:
                        if len(historydata[-1][-1]) < 12:
                            self.page.snack_bar = ft.SnackBar(ft.Text(f"Car is already rented, refresh the page", color="white"), bgcolor="red")
                            self.page.snack_bar.open = True
                            self.page.update()
                            return False
                        
                    carinlist.lastPerson = nameLastname
                    
                    carinlist.available = False if carinlist.available == True else True
                    brand, model, registration = carinlist.brand, carinlist.model, carinlist.registration
                    try:
                        with open(f"./assets/cars/{brand}-{model}-{registration}/data.txt", "rt+") as f:
                            cardata = dict([tuple(i.strip().split(": ")) for i in f])
                            cardata["available"] = carinlist.available
                    except FileNotFoundError as e:
                        print(f"File not found")
                    except Exception as e:
                        print(f"Error: {e}")
                        
                    try:
                        with open(f"./assets/cars/{brand}-{model}-{registration}/data.txt", "wt+") as f:
                            [f.write(f"{k}: {v}\n" )for k, v in cardata.items()]
                    except FileNotFoundError as e:
                        print(f"File not found")
                    except Exception as e:
                        print(f"Error: {e}")
                        
                    try:
                        if cardata["available"] == False:
                            with open(f"./assets/cars/{brand}-{model}-{registration}/history.txt", "at+") as f:
                                f.write(f"{self.name} {self.lastName} {dt.datetime.strftime(dt.datetime.now(), '%m-%d-%Y')}\n")
                    except FileNotFoundError as e:
                        print(f"File not found")
                    except Exception as e:
                        print(f"Error: {e}")
                        
                    self.carlistColumn.controls.remove(car)
                    self.carlist.remove(registration)
                        
                elif carinlist.available == False and carinlist.lastPerson == nameLastname:
                    # If car is unavaiable and lastPerson is equal to username
                    if historydata != []:
                        if len(historydata[-1][-1]) > 12:
                            self.page.snack_bar = ft.SnackBar(ft.Text(f"Car is already returned, refresh the page", color="white"), bgcolor="red")
                            self.page.snack_bar.open = True
                            self.page.update()
                            return False
                    # Method to handle car returning
                    self.returnCar(car)
                    self.update()
                    
        self.getCars()
        super().update()
    
    # Method to handle car returning
    def returnCar(self, car):
        mileageField = ft.TextField(label="Current mileage")
        error = ft.Text(color="red")
        
        def accept(e):
            if mileageField.value ==  "" or (mileageField.value).isdigit() == False:
                error.value = "Incorrect data"
                self.update()
            elif int(mileageField.value) < int(car.mileage):
                error.value = "Enter current mileage"
                self.update()
            else:
                try:
                    backModal.open = False
                    giveBack(car)
                    self.update()
                finally:
                    self.carlistColumn.controls.pop()
                    
        # Function to handle car returning
        def giveBack(car):
            nameLastname = self.name + " " + self.lastName
            for carinlist in self.carlistColumn.controls:
                if car == carinlist:
                    if carinlist.available == False and carinlist.lastPerson == nameLastname:
                        carinlist.lastPerson = ""
                        carinlist.available = False if carinlist.available == True else True
                        brand, model, registration = carinlist.brand, carinlist.model, carinlist.registration
                        
                        try:
                            with open(f"./assets/cars/{brand}-{model}-{registration}/data.txt", "rt+") as f:
                                cardata = dict([tuple(i.strip().split(": ")) for i in f])
                                cardata["available"] = carinlist.available
                                cardata["mileage"] = int(mileageField.value)
                        except FileNotFoundError as e:
                            print(f"File not found")
                        except Exception as e:
                            print(f"Error: {e}")
                            
                        try:
                            with open(f"./assets/cars/{brand}-{model}-{registration}/data.txt", "wt+") as f:
                                [f.write(f"{k}: {v}\n" )for k, v in cardata.items()]
                        except FileNotFoundError as e:
                            print(f"File not found")
                        except Exception as e:
                            print(f"Error: {e}")
                        
                        historydata = []
                        try:
                            with open(f"./assets/cars/{brand}-{model}-{registration}/history.txt", "rt+") as f:
                                [historydata.append(i.strip().split(" ")) for i in f]
                        except FileNotFoundError as e:
                            print(f"File not found")
                        except Exception as e:
                            print(f"Error: {e}")
                        if historydata != []:
                            if historydata[-1][0] == self.name and historydata[-1][1] == self.lastName and len(historydata[-1][-1]) < 12:
                                historydata[-1][-1] = historydata[-1][-1] + "/" + dt.datetime.strftime(dt.datetime.now(), '%m-%d-%Y')
                                try:
                                    with open(f"./assets/cars/{brand}-{model}-{registration}/history.txt", "wt+") as f:
                                        [f.write(f"{historydata[i][0]} {historydata[i][1]} {historydata[i][2]}\n") for i in range(len(historydata))]
                                except FileNotFoundError as e:
                                    print(f"File not found")
                                except Exception as e:
                                    print(f"Error: {e}")
                        self.carlistColumn.controls.remove(car)
                        self.carlist.remove(registration)
            self.getCars()
            self.update()
                    
        # Dialog for confirming the return of a rented car            
        backModal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text(value=f"{car.brand} {car.model} {car.registration}"),
            actions=[
                mileageField,
                error,
                ft.TextButton("Confirm", on_click=accept),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
            
        self.carlistColumn.controls.append(backModal)
        backModal.open = True
        self.update()