-- database creation

CREATE DATABASE IF NOT EXISTS genebank CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE genebank;

-- species table

CREATE TABLE Species (
	species_id INT AUTO_INCREMENT PRIMARY KEY,
	`name` VARCHAR(255) NOT NULL,
    family VARCHAR(255),
    common_name VARCHAR(255),
    `description` TEXT
);

-- samples table 

CREATE TABLE Samples (
	sample_id INT AUTO_INCREMENT PRIMARY KEY,
    species_id INT NOT NULL,
    accession_code VARCHAR(50) UNIQUE NOT NULL,
    collection_date DATE,
    origin VARCHAR(255),
    storage_location VARCHAR(255),
    notes TEXT,
    FOREIGN KEY (species_id) REFERENCES Species(species_id) ON DELETE CASCADE
);
    

-- genetic traits table 

CREATE TABLE Genetic_Traits (
	trait_id INT AUTO_INCREMENT PRIMARY KEY,
    sample_id INT NOT NULL,
    trait_name VARCHAR(255),
    `description` TEXT,
    FOREIGN KEY (sample_id) REFERENCES Samples(sample_id) ON DELETE CASCADE
);

-- Improvement Goals table

CREATE TABLE Improvement_Goals (
	goals_id INT AUTO_INCREMENT PRIMARY KEY,
    species_id INT NOT NULL,
    goal_name VARCHAR(255),
    `description` TEXT,
    FOREIGN KEY (species_id) REFERENCES Species(species_id) ON DELETE CASCADE
);

-- Storage Condition Table

CREATE TABLE Storage_Conditions (
	storage_id INT AUTO_INCREMENT PRIMARY KEY,
    sample_id INT NOT NULL,
    temperature VARCHAR(50),
    humidity VARCHAR(50),
    duration_years INT,
    notes TEXT,
    FOREIGN KEY (sample_id) REFERENCES Samples(sample_id) ON DELETE CASCADE
);

-- Table for users to login

CREATE TABLE Users (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);
-- Add some values
-- Species

INSERT INTO Species (`name`, family, common_name, `description`) VALUES
('Triticum aestivum', 'Poaceae', 'Σιτάρι', 'Σημαντικό δημητριακό'),
('Zea mays', 'Poaceae', 'Καλαμπόκι', 'Καλλιεργείται παγκοσμίως'),
('Solanum lycopersicum', 'Solanaceae', 'Τομάτα', 'Καλλιεργούμενο λαχανικό');

-- Samples 

INSERT INTO Samples (species_id, accession_code, collection_date, origin, storage_location, notes) VALUES
(1, 'TA-2023-01', '2023-05-10', 'Θεσσαλία', 'Ψυγείο Α1', 'Υψηλή αντοχή σε ξηρασία'),
(2, 'ZM-2022-15', '2022-08-12', 'Μακεδονία', 'Ψυγείο Β2', 'Καλή απόδοση σε χαμηλή θερμοκρασία'),
(3, 'SL-2023-05', '2023-04-20', 'Κρήτη', 'Ψυγείο Α3', 'Γευστική ποικιλία');

-- Genetic Traits

INSERT INTO Genetic_Traits (sample_id, trait_name, `description`) VALUES
(1, 'Drought tolerance', 'Αντοχή σε ξηρασία'),
(2, 'Cold tolerance', 'Αντοχή σε χαμηλές θερμοκρασίες'),
(3, 'Taste quality', 'Βελτιωμένη γεύση');

-- Improvement Goals

INSERT INTO Improvement_Goals (species_id, goal_name, `description`) VALUES
(1, 'Yield increase', 'Αύξηση παραγωγής'),
(2, 'Pest resistance', 'Αντοχή σε παράσιτα'),
(3, 'Shelf life', 'Μεγαλύτερη διάρκεια αποθήκευσης');

-- Storage Condition

INSERT INTO Storage_Conditions (sample_id, temperature, humidity, duration_years, notes) VALUES
(1, '-20°C', '50%', 10, 'Μακροχρόνια αποθήκευση'),
(2, '-18°C', '55%', 8, 'Κρυοσυντήρηση'),
(3, '-15°C', '60%', 5, 'Προσωρινή αποθήκευση');


