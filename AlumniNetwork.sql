-- Create database
CREATE DATABASE alumni_network;
USE alumni_network;

-- Alumni table
CREATE TABLE alumni (
    alumni_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    graduation_year INT,
    degree VARCHAR(100),
    phone VARCHAR(20),
    current_job VARCHAR(100),
    current_company VARCHAR(100),
    bio TEXT
);

-- Events table
CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    event_date DATETIME NOT NULL,
    location VARCHAR(255),
    organizer_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organizer_id) REFERENCES alumni(alumni_id)
);

-- Event registrations
CREATE TABLE event_registrations (
    registration_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    alumni_id INT NOT NULL,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (alumni_id) REFERENCES alumni(alumni_id),
    UNIQUE (event_id, alumni_id)
);

-- Connections table
CREATE TABLE connections (
    connection_id INT AUTO_INCREMENT PRIMARY KEY,
    alumni1_id INT NOT NULL,
    alumni2_id INT NOT NULL,
    connection_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
    FOREIGN KEY (alumni1_id) REFERENCES alumni(alumni_id),
    FOREIGN KEY (alumni2_id) REFERENCES alumni(alumni_id),
    CHECK (alumni1_id < alumni2_id)
);

-- News/Updates table
CREATE TABLE news (
    news_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    author_id INT,
    publish_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_published BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (author_id) REFERENCES alumni(alumni_id)
);

show tables;
select *from alumni;
select * from events;

