CREATE DATABASE IF NOT EXISTS attendance;
CREATE TABLE IF NOT EXISTS attendance.student_data(
    position INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    class VARCHAR(10) NOT NULL,
    roll INT NOT NULL,
    PRIMARY KEY (position, class, roll)
);
