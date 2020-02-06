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
-- Add current recording foreign key to Profiles table. This has to be done after
-- because the recording table isn't createrd when the Profiles table is first created.
ALTER TABLE Profiles ADD current_recording_id INT;
ALTER TABLE Profiles ADD CONSTRAINT current_recording_id FOREIGN KEY(current_recording_id) REFERENCES Recording(recording_id);
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
