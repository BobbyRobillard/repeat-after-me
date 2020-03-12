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
  username VARCHAR(50) NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  recording_key VARCHAR(10),
  play_mode_key VARCHAR(10)
);
-- #############################################################################
CREATE TABLE Profile (
  profile_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE
);
-- #############################################################################
CREATE TABLE Recording (
  recording_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  profile_id INT NOT NULL,
  activation_key_code VARCHAR(10) NOT NULL,
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
  x_position INT NOT NULL,
  y_position INT NOT NULL,
  is_press BOOLEAN NOT NULL,
  recording_id INT NOT NULL,
  FOREIGN KEY(recording_id) REFERENCES Recording(recording_id)
);
-- #############################################################################
CREATE TABLE Key_Event (
  event_id INT AUTO_INCREMENT PRIMARY KEY,
  delay_time INT DEFAULT 0,
  key_code VARCHAR(10) NOT NULL,
  is_press BOOLEAN NOT NULL,
  recording_id INT NOT NULL,
  FOREIGN KEY(recording_id) REFERENCES Recording(recording_id)
);
-- #############################################################################

-- INSERT DUMMY DATA

INSERT INTO User (username, first_name, last_name, password, email) VALUES (
  "test", "John", "Doe", "password123", "testing123@test.com"
);

INSERT INTO Profile (user_id, name) VALUES (1, "Elementor Essentials!");
INSERT INTO Profile (user_id, name) VALUES (1, "Modern Warfare");

UPDATE User SET current_profile_id = 1 WHERE user_id = 1;
UPDATE User SET recording_key = "A" WHERE user_id = 1;

INSERT INTO Recording (profile_id, activation_key_code, name) VALUES (1, "1", "MAGA");
INSERT INTO Recording (profile_id, activation_key_code, name) VALUES (1, "3", "BETTER MAGA");
-- #############################################################################
