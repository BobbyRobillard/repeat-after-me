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
-- #############################################################################
CREATE TABLE Profile (
  profile_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  name VARCHAR(50),
  FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE
);
-- #############################################################################
CREATE TABLE Recording (
  recording_id INT AUTO_INCREMENT PRIMARY KEY,
  profile_id INT NOT NULL,
  FOREIGN KEY(profile_id) REFERENCES Profile(profile_id)
);
-- #############################################################################
-- Add current profile foreign key to User table. This has to be done after
-- because the profile table isn't createrd when the User table is first created.
ALTER TABLE User ADD current_profile_id INT;
ALTER TABLE User ADD CONSTRAINT current_profile_id FOREIGN KEY(current_profile_id) REFERENCES Profile(profile_id);
-- #############################################################################
CREATE TABLE Mouse_Event (
  event_id INT AUTO_INCREMENT PRIMARY KEY,
  delay_time INT DEFAULT 0,
  x_position INT,
  y_position INT,
  is_press BOOLEAN,
  is_move BOOLEAN,
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

-- INSERT DUMMY DATA

INSERT INTO User (username, first_name, last_name, password, email) VALUES (
  "test", "John", "Doe", "password123", "testing123@test.com"
);

INSERT INTO Profile (user_id, name) VALUES (1, "Elementor Essentials!");

UPDATE User SET current_profile_id = 1 WHERE user_id = 1;
-- #############################################################################
