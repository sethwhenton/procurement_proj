# Procurement Benefits Project

## Introduction
Welcome to the Procurement Benefits project README! This project is aimed at developing a web application using Django for managing procurement benefits, including items, users, departments, budgets, and more. It provides interfaces for both administrators and users to manage and utilize procurement resources effectively for my company.

## Setup Instructions
To get started with this project locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd procurement_benefits
   ```

2. **Set Up Virtual Environment:**
   ```bash
   # Install virtualenv if not already installed
   pip install virtualenv
   
   # Create a virtual environment
   virtualenv venv
   
   # Activate the virtual environment
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application:**
   Open a web browser and go to `http://localhost:8000` to view the application.

## Project Overview
The Procurement Benefits project uses Django framework to build a comprehensive web application with the following features:

- **Admin Interface:** Allows administrators to manage items, users, departments, budgets, and settings.
- **User Interface:** Provides functionalities for users to view items, manage their profiles, and interact with procurement features.

### Key Features
- **Items:** CRUD operations for managing procurement items.
- **Users:** Management of user profiles and permissions.
- **Departments:** Creation and management of organizational departments.
- **Budgets:** Allocation and management of budget resources.
- **Settings:** Configuration options for application behavior.

## New Updates
- Implement shopping cart functionality for users to select and manage items.✅
- Work on the view all items selected by staff in a particular department✅
- Work on the table to view all items from all departments combined as well as the total cost of items selected.✅

## Future Plans
- Work on some extra few features for accessibility and convenience.
- Improve user interface and user experience based on feedback and testing.(might need some help)
  


---

Feel free to customize each section further with specific details about your project, dependencies, setup specifics, and future goals. This README serves as a guide for new developers joining the project and as a reference for maintaining and evolving the application.
