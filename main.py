"""
    Zadanie zaliczeniowe z języka Python
    Imię i nazwisko ucznia: Bartłomiej Labenz
    Data wykonania zadania: 06.12.2023
    Treść zadania: Wypożyczalnia samochodów
    Opis funkcjonalności aplikacji: w pliku readme.md
"""

import flet as ft
from CarRentalPage import CarRentalPage
from AddCarPage import AddCarPage
from LoginPage import LoginPage
from RegistrationPage import RegistrationPage
from AdminManagePage import AdminManagePage
from Navbar import Navbar

def main(page: ft.Page):
    # Setting up the initial page configurations
    page.title = "Car Rental"
    page.theme_mode = ft.ThemeMode.DARK;
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


    # Helper functions to get user's name, last name and email from session or client storage
    def getName():
        return page.session.get("name") if page.client_storage.get("name") == None else page.client_storage.get("name")
        
    def getLastName():
        return page.session.get("lastName") if page.client_storage.get("lastName") == None else page.client_storage.get("lastName")
    
    def getEmail():
        return page.session.get("email") if page.client_storage.get("email") == None else page.client_storage.get("email")

    # Function to handle different views for routing
    def views_handler(page):
        CarRental = CarRentalPage(getName(), getLastName(), getEmail())
        NavBar = Navbar(page, CarRental.admin)
        
        # Change navbar depending on the page
        if page.route == "/":
            NavBar.selected_index = 0
        elif page.route == "/store":
            NavBar.selected_index = 1
        elif page.route == "/addcar":
            NavBar.selected_index = 2 
        elif page.route == "/adminmanage":
            NavBar.selected_index = 3
        # Define different views based on routes
        return {
            '/':ft.View(
                route='/',
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    LoginPage()
                ]
            ),
            '/registration':ft.View(
                route='/registration',
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    RegistrationPage()
                ]
            ),
            '/store':ft.View(
                route='/store',
                scroll=ft.ScrollMode.ADAPTIVE,
                controls=[
                    CarRental,
                    NavBar,
                ],
            ),
            '/addcar':ft.View(
                route='/addcar',
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    AddCarPage(),
                    NavBar    
                ],
            ),
            '/adminmanage':ft.View(
                route='/adminmanage',
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    AdminManagePage(),
                    NavBar    
                ],
            ),
        }
    
    # Function to handle route changes
    def route_change(route):
        page.views.clear()
        page.views.append(
        views_handler(page)[page.route],
        )
        
        # Clear client storage on the login page route
        if page.route == "/":
            page.client_storage.clear()

    # Set the route change handler
    page.on_route_change = route_change
    
    # Navigate the user to different routes based on conditions
    if page.client_storage.get("name") != None and page.client_storage.get("lastName") != None:
        page.go('/store')
    else:
        page.go('/')
               
if __name__ == "__main__":
    ft.app(main, assets_dir="assets")