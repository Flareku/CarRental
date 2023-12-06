# Car Rental Application
#### Autor: Bartłomiej Labenz

**Email and password for the default administrator created is admin admin**

This Car Rental Application provides a comprehensive platform for users to interact with a car rental service. The system caters to both regular users and administrators, offering functionalities for renting cars, managing rentals, and facilitating administrative tasks.

## Overview

### Pages

- **Login Page**: Allows users to log in with their email and password.
- **Registration Page**: Facilitates user registration by collecting user details like name, last name, email, and password.
- **Car Rental Page**: Displays available cars for rental, along with functionalities to rent or return cars. Administrators have additional management options.
- **Add Car Page**: Admin-exclusive page for adding new cars to the rental service.
- **Admin Manage Page**: Specific page for admin users to handle admin users.

### Features

- **Navigation Bar (`Navbar`)**: Dynamically adjusts based on user roles (admin or regular user).
  - For regular users: Provides options for "Home" and "Car Rental."
  - For admin users: Includes additional functionalities like "Add Car" and "Admin Manage" along with regular options.
- **User Authentication and Storage**: Utilizes session and client storage to manage user login details, ensuring a seamless login experience and persistence between sessions.
- **Responsive UI**: Offers an intuitive and responsive user interface for easy interaction.

## More accurate description

### Car Rental Page (CarRentalPage)

- **Initialization and Attributes:** Manages user details (name, last name, email), admin status, and car instances.
- **Check Admin Functionality:** Verifies user admin status and updates the page layout accordingly.
- **Car Management:** Handles car availability, rental, and returning functionalities.
- **Car Display:** Retrieves and displays car details for user interaction.

### Add Car Page (AddCarPage)

- **Initialization and User Interface:** Sets up text fields for car details and space for image selection.
- **UI Construction (build()):** Constructs UI elements - text fields, buttons, and file selection space.
- **Snackbar (snackBar()):** Displays validation messages.
- **Adding a Car (addCar()):** Validates and saves car data, creates directories, and stores image files.
- **Handling Image Selection (pickImgResult()):** Updates UI with selected image.

### Admin Management Page (AdminManagePage)

- **Initialization and UI Setup:** Initializes UI elements like text fields, admin list, and buttons.
- **UI Construction (build()):** Constructs UI layout for admin management.
- **Retrieving Admins (getUsers()):** Fetches existing admins' emails and displays them.
- **Adding Admins (addAdmin()):** Validates and adds admin emails to the admin list.
- **Removing Admins (removeAdmin()):** Removes specified admin emails and updates the admin list.

### Car Class

- **Initialization and Attributes:** Sets up attributes for car instances.
- **Building UI (build()):** Constructs UI to display car details.
- **Handling Rent Button (rentClicked()):** Manages renting or returning a car.
- **Visibility Management (getvisibility()):** Controls car visibility.
- **Image Path Retrieval (checkImg()):** Retrieves the car's image path.
- **Retrieving Last Interaction (getLastPerson()):** Fetches the last interaction details.
- **History Display (checkHistory()):** Shows car history in an alert dialog.
- **Deleting Car Data (deleteCar()):** Removes car data and directory.

### Login Page Class (LoginPage)

- **Initialization and Attributes:** Sets up email, password, and remember me checkbox.
- **UI Layout (build()):** Constructs UI layout for the login page.
- **Authenticate User (getUserData()):** Validates credentials and manages session/client storage.

### Registration Page Class (RegistrationPage)

- **Initialization and Attributes:** Collects user details for registration.
- **UI Layout (build()):** Constructs UI layout for user registration.
- **Save User Registration Data (saveUserData()):** Validates and securely stores user registration data.

### Navbar Function (Navbar)

- **Navbar Functionality:** Creates dynamic navigation bars based on user roles.
- **Nested Function (NavbarFunc()):** Constructs navigation bar options for different user roles.
- **Handling Navigation (changeNavBar()):** Manages navigation based on user selection.

## Installation and Usage

- Clone the repository.
- Install dependencies using `pip install -r requirements.txt`.
- Run the application with `python main.py`.
