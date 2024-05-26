# Library Management System

## Description

This project is a Library Management System built using Django. It allows library staff to manage the book collection, book issue and return books to customers, while customers can register on the site and use the library services.

## Functionality

### User Registration
1. Users can register on the site.
   - Mandatory fields: email, password, full name, personal_number, birth_date.
   - Employees are added via the admin panel.

### Authorization
2. Both employees and regular users can log in to the site.

### Management of Books
3. Librarians can add, delete, and update book data.
   - Data management is possible through the Django Admin interface and via API.
   - At least 1000 books are pre-populated in the system (randomly generated).

#### Book Details
- Title
- Author
- Genre
- Date of Publish
- Quantity of Stock

#### Models
- **Author**: A separate model connected to the book with the appropriate relationship.
- **Genre**: A separate model connected to the book with the appropriate relationship.

#### Admin Features
- Filtering and search functionality in the book list.
- Detailed view of each book with the following information:
  - How many times the book has been issued.
  - How many books are currently available.
  - How many books are currently issued.
- History of each book (who took the book, when it was taken, and when it was returned).

### User Side
4. Viewing and reserving books:
   - Users can view the list of books and detailed information.
     - The list of books has filtering, searching, and pagination.
   - Users can reserve a book for 1 day if it is in stock. If the book is not taken out, the reservation is automatically removed.
   - After returning the book, the librarian can mark in the database that the book has been returned by the specific user.

### Statistics
5. API for statistical data:
   - The most popular 10 books (most requested).
   - For each book, the number of times it was taken out of the library in the last year.
   - Top 100 books that were returned late most often.
   - Top 100 users who return books late most often.

### Libraries Used
6. The project uses the following libraries:
   - **Django**: The web framework used to build the project.
   - **Django Rest Framework (DRF)**: Used to build the RESTful API for the described functionality.

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/TikoTs/library_management_system_final.git
   cd library_management_system_final
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Populate the database with sample data:
   ```bash
   python manage.py generate_books
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the site at `http://127.0.0.1:8000`.

---

Feel free to contribute to this project by opening issues and submitting pull requests. Your feedback and contributions are highly appreciated!
