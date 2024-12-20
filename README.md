Online Library Management System
Backend introduction：
1. Flask Framework:
Flask is a lightweight web application framework that allows developers to quickly build websites and web services using the Python language. In this program, Flask is used to define routes (i.e., URL rules), handle user requests, and return responses.
2. MySQL Database:
MySQL is a relational database management system that stores and manages data. In this program, the MySQL database is used to store user information, book information, and borrowing records.
3. Database Connection:
The program uses the mysql.connector library to connect to the MySQL database, execute SQL queries, and process the results. This is the bridge between Python and MySQL databases.
4. Password Security:
Use the generate_password_hash and check_password_hash functions in the werkzeug.security module to securely handle user passwords. Passwords are encrypted (hashed) for security before being stored in the database.
5. Regular Expressions (re module):
Regular expressions are used for text pattern matching. In this program, it is used to extract numbers from the copy number of a book in order to generate a unique copy number when a new book is added.
6. Date and Time Processing:
Use the 'datetime' module to handle dates and times, such as calculating the borrowing period and overdue days for books.
7. Session:
Flask's 'session' object is used to store user session information on the server side, such as user ID and username. This allows the program to recognize and maintain the user's presence while the user is browsing the website.
8. Stencil Rendering:
Flask uses the 'render_template' function to pass dynamic data to the HTML template and generate the final HTML page. A template is a special type of file that contains markup that is used to populate dynamic content.
9. Form Data Processing:
Through the 'request.form' object, Flask can access the form data submitted by the user via a POST request.
10. Redirects and Message Prompts:
Use the 'redirect' function to direct the user to another page after they have completed the action, and the 'flash' function to display a message prompt for the result of the action.
11. Error Handling:
The program includes handling of database operation errors, using a 'try-except' block to catch exceptions, and rolling back database transactions in the event of an error to maintain data consistency.
12. Routing and View Functions:
The @app.route decorator in Flask defines the route, which is the mapping between the URL path and the corresponding handler (view). The view function is responsible for handling a specific request and returning a response.
13. User Authentication:
The program implements user registration and login functions, including checking the existence of user names, password verification, etc.
14. Admin Features:
The program offers admin-specific features, such as adding and removing users, adding and removing books, and viewing a list of all users and books.

Introduction to the database:
The database is named `library_system` and contains three main tables: `users`, `books`, and `borrow_and_return_logs`. Below is a detailed explanation of the structure and function of each table:

1. `users` Table
This table stores user information in the library system.

- `id`: Primary key, auto-incrementing integer, uniquely identifies each user.
- `username`: String, the user's login name, must be unique.
- `password`: String, the user's password.
- `full_name`: String, the user's full name, can be null.
- `email`: String, the user's email address, must be provided.
- `role`: Enum, can be 'user' or 'admin', defaults to 'user', indicating the user's role.
- `current_borrowed_count`: Integer, indicates the number of books currently borrowed by the user, defaults to 0.

2. `books` Table
This table stores information about the books in the library.

- `id`: Primary key, auto-incrementing integer, uniquely identifies each book.
- `title`: String, the title of the book.
- `author`: String, the author of the book.
- `copy_number`: String, indicates the copy number of the book, for example, 'The Great Gatsby-1' means the first copy of "The Great Gatsby".
- `is_available`: Boolean, indicates whether the book is available for borrowing, 1 means available, 0 means not available.

3. `borrow_and_return_logs` Table
This table records the borrowing and returning logs of users.

- `id`: Primary key, auto-incrementing integer, uniquely identifies each borrowing record.
- `user_id`: Foreign key, references `id` in the `users` table, indicates the user who borrowed the book.
- `book_id`: Foreign key, references `id` in the `books` table, indicates the book that was borrowed.
- `borrow_date`: Timestamp, defaults to the current timestamp, records the time when the book was borrowed.
- `return_date`: Timestamp, defaults to the current timestamp, records the time when the book was returned.

Data Insertion
Finally, the SQL insert statement you provided adds records for 20 books to the `books` table, including two copies each of "The Great Gatsby," "To Kill a Mockingbird," "1984," "Pride and Prejudice," "The Catcher in the Rye," "The Hobbit," "The Lord of the Rings," and "The Da Vinci Code." The `is_available` field for each book is set to 1, indicating that these books are currently available for borrowing.

This database structure provides basic data storage functions for a library system, including user management, book management, and tracking of borrowing records.

Through this project, we have accomplished:
1. Website construction: We built a website using Flask where users can register an account, log in, and perform borrowing and returning operations.
2. Database management: We designed a database to store user and book information, as well as track which books have been borrowed and which are still on the shelves.
3. User permissions: We set up different user roles, such as regular users and administrators, each with different permissions.
4. Automated testing: We wrote some automated tests using Selenium to ensure the website's functionality is working properly.
5. Beautify the interface: We used HTML and CSS to make the website interface more user-friendly and aesthetically pleasing.
6. Testing and optimization: We tested the website to ensure it can function properly even under extreme conditions, such as when a user borrows a large number of books.
7. Performance and security: We focused on the operational performance and security of our website, ensuring it is both fast and secure.

