CREATE DATABASE library_system;
USE library_system;

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `role` ENUM('user', 'admin') NOT NULL DEFAULT 'user',
  `current_borrowed_count` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `books` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `author` varchar(100) NOT NULL,
  `copy_number` varchar(50) NOT NULL DEFAULT '1',
  `is_available` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `borrow_and_return_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `book_id` int NOT NULL,
  `borrow_date` timestamp DEFAULT CURRENT_TIMESTAMP,
  `return_date` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  FOREIGN KEY (`book_id`) REFERENCES `books` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `books` (`title`, `author`, `copy_number`, `is_available`) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'The Great Gatsby-1', 1),
('To Kill a Mockingbird', 'Harper Lee', 'To Kill a Mockingbird-1', 1),
('1984', 'George Orwell', '1984-1', 1),
('Pride and Prejudice', 'Jane Austen', 'Pride and Prejudice-1', 1),
('The Catcher in the Rye', 'J.D. Salinger', 'The Catcher in the Rye-1', 1),
('The Hobbit', 'J.R.R. Tolkien', 'The Hobbit-1', 1),
('The Lord of the Rings', 'J.R.R. Tolkien', 'The Lord of the Rings-1', 1),
('The Da Vinci Code', 'Dan Brown', 'The Da Vinci Code-1', 1),
('The Great Gatsby', 'F. Scott Fitzgerald', 'The Great Gatsby-2', 1),
('To Kill a Mockingbird', 'Harper Lee', 'To Kill a Mockingbird-2', 1),
('1984', 'George Orwell', '1984-2', 1),
('Pride and Prejudice', 'Jane Austen', 'Pride and Prejudice-2', 1),
('The Catcher in the Rye', 'J.D. Salinger', 'The Catcher in the Rye-2', 1),
('The Hobbit', 'J.R.R. Tolkien', 'The Hobbit-2', 1),
('The Lord of the Rings', 'J.R.R. Tolkien', 'The Lord of the Rings-2', 1),
('The Da Vinci Code', 'Dan Brown', 'The Da Vinci Code-2', 1);