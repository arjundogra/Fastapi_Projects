# Library Management System

## Overview
The Library Management System is a web application built using FastAPI that allows users to manage books, members, and borrow records efficiently. This project provides a RESTful API for performing CRUD operations on books and members, as well as managing borrow transactions.

## Project Structure
```
Library_Management_System
├── src
│   ├── app.py                  # Entry point of the application
│   ├── database_connection.py   # Database connection management
│   ├── middleware.py            # Custom middleware implementation
│   ├── routes
│   │   ├── books.py            # Routes for book management
│   │   ├── members.py          # Routes for member management
│   │   └── borrowRecords.py     # Routes for borrow records management
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Library_Management_System
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```
   python src/app.py
   ```

2. The API will be available at `http://localhost:8080`.

## API Endpoints

### Books
- **GET /books**: Retrieve a list of all books.
- **POST /books**: Add a new book.
- **GET /books/{id}**: Retrieve a specific book by ID.
- **PUT /books/{id}**: Update a specific book by ID.
- **DELETE /books/{id}**: Delete a specific book by ID.

### Members
- **GET /members**: Retrieve a list of all members.
- **POST /members**: Add a new member.
- **GET /members/{id}**: Retrieve a specific member by ID.
- **PUT /members/{id}**: Update a specific member by ID.
- **DELETE /members/{id}**: Delete a specific member by ID.

### Borrow Records
- **GET /borrowRecords**: Retrieve a list of all borrow records.
- **POST /borrowRecords**: Record a new borrow transaction.
- **GET /borrowRecords/{id}**: Retrieve a specific borrow record by ID.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.