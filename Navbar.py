"""
    Zadanie zaliczeniowe z języka Python
    Imię i nazwisko ucznia: Bartłomiej Labenz
    Data wykonania zadania: 06.12.2023
    Treść zadania: Wypożyczalnia samochodów
    Opis funkcjonalności aplikacji: w pliku readme.md
"""

import flet as ft

def Navbar(page: ft.Page, admin):
    
    # Navigation bar creation function based on admin status
    def NavbarFunc(on_change_func):   
        
        # If not an admin, display navigation options for regular users
        if admin == False:
            return ft.NavigationBar(
                destinations=[
                    ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Home"),
                    ft.NavigationDestination(icon=ft.icons.COMMUTE, label="Car Rental"),
                ],
                on_change=on_change_func
            )
        else:
            # Display navigation options for admin users
            return ft.NavigationBar(
                destinations=[
                    ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Home"),
                    ft.NavigationDestination(icon=ft.icons.COMMUTE_OUTLINED, selected_icon=ft.icons.COMMUTE, label="Car Rental"),
                    ft.NavigationDestination(icon=ft.icons.ADD_BOX_OUTLINED, selected_icon=ft.icons.ADD_BOX, label="Add car"),
                    ft.NavigationDestination(icon=ft.icons.ADD, label="Admin manage"),
                ],
                on_change=on_change_func
            )
            
    def changeNavBar(e):
        # Function to handle navigation changes based on the selected index
        # If not an admin, handle navigation for regular users
        if admin == False:
            if NavBar.selected_index == 0:
                page.go("/")
            elif NavBar.selected_index == 1:
                page.go("/store")
        else:
            # Handle navigation for admin users
            if NavBar.selected_index == 0:
                page.go("/")
            elif NavBar.selected_index == 1:
                page.go("/store")
            elif NavBar.selected_index == 2:
                page.go("/addcar")
            elif NavBar.selected_index == 3:
                page.go("/adminmanage")

    # Create the navigation bar using the appropriate function based on admin status
    NavBar = NavbarFunc(changeNavBar)
    return NavBar