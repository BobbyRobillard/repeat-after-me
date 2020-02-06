-- #############################################################################
-- Setup user to connect as
CREATE USER test IDENTIFIED BY 'testing123';
GRANT ALL PRIVILEGES ON *.* TO test;
FLUSH PRIVILEGES;
-- #############################################################################
-- Setup datbase to use
CREATE DATABASE test;
USE test;
-- #############################################################################
CREATE TABLE User (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50),
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  password VARCHAR(255),
  email VARCHAR(255)
);

INSERT INTO User (username, first_name, last_name, password, email) VALUES (
  "test", "John", "Doe", "password123", "test@testing.com"
);
-- #############################################################################
CREATE TABLE Profile (
  profile_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  name VARCHAR(50),
  UNIQUE (user_id),
  FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE
);
-- #############################################################################
CREATE TABLE Recording (
  recording_id INT AUTO_INCREMENT PRIMARY KEY,
  profile_id INT NOT NULL,
  FOREIGN KEY(profile_id) REFERENCES Profile(profile_id)
);
-- #############################################################################
-- Add current recording foreign key to Profile table. This has to be done after
-- because the recording table isn't createrd when the Profile table is first created.
ALTER TABLE Profile ADD current_recording_id INT;
ALTER TABLE Profile ADD CONSTRAINT current_recording_id FOREIGN KEY(current_recording_id) REFERENCES Recording(recording_id);
-- #############################################################################
CREATE TABLE Mouse_Event (
  event_id INT AUTO_INCREMENT PRIMARY KEY,
  delay_time INT DEFAULT 0,
  x_position INT,
  y_position INT,
  is_press BOOLEAN,
  recording_id INT,
  FOREIGN KEY(recording_id) REFERENCES Recording(recording_id)
);
-- #############################################################################
CREATE TABLE Key_Event (
  event_id INT AUTO_INCREMENT PRIMARY KEY,
  delay_time INT DEFAULT 0,
  button VARCHAR(20),
  is_press BOOLEAN,
  recording_id INT,
  FOREIGN KEY(recording_id) REFERENCES Recording(recording_id)
);
-- #############################################################################
