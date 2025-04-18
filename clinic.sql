-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: clinic
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table appointments
--

DROP TABLE IF EXISTS appointments;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE appointments (
  appointment_id int NOT NULL AUTO_INCREMENT,
  patient_id int DEFAULT NULL,
  doctor_id int DEFAULT NULL,
  date date DEFAULT NULL,
  time time DEFAULT NULL,
  reason text,
  PRIMARY KEY (appointment_id),
  KEY patient_id (patient_id),
  KEY doctor_id (doctor_id),
  CONSTRAINT appointments_ibfk_1 FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
  CONSTRAINT appointments_ibfk_2 FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table appointments
--

LOCK TABLES appointments WRITE;
/*!40000 ALTER TABLE appointments DISABLE KEYS */;
/*!40000 ALTER TABLE appointments ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table doctors
--

DROP TABLE IF EXISTS doctors;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE doctors (
  doctor_id int NOT NULL AUTO_INCREMENT,
  name varchar(100) DEFAULT NULL,
  specialization varchar(100) DEFAULT NULL,
  phone varchar(15) DEFAULT NULL,
  PRIMARY KEY (doctor_id)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table doctors
--

LOCK TABLES doctors WRITE;
/*!40000 ALTER TABLE doctors DISABLE KEYS */;
INSERT INTO doctors VALUES (1,'Dr. Mandeep','Cardiology','2456147827'),(2,'Dr. Rakshita','Neumerology','2456137867'),(3,'Dr Roop','Pediatrics','6041122334'),(4,'Dr. Neha Sharma','Dermatology','6047788990'),(5,'Dr. Karan Singh','Orthopedics','6046655443'),(6,'','','');
/*!40000 ALTER TABLE doctors ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table nurses
--

DROP TABLE IF EXISTS nurses;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE nurses (
  nurse_id int NOT NULL AUTO_INCREMENT,
  name varchar(100) DEFAULT NULL,
  department varchar(100) DEFAULT NULL,
  shift varchar(50) DEFAULT NULL,
  phone varchar(15) DEFAULT NULL,
  PRIMARY KEY (nurse_id)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table nurses
--

LOCK TABLES nurses WRITE;
/*!40000 ALTER TABLE nurses DISABLE KEYS */;
INSERT INTO nurses VALUES (1,'Nurse Anjali Desai','Emergency','6042233445','Night'),(2,'Nurse Ritu Chauhan','ICU','6043344556','Morning'),(3,'Nurse Aakash Patel','General Ward','6044455667','Evening'),(4,'Nurse Simran Kaur','Pediatrics','6045566778','Night'),(5,'Nurse Mohit Nair','Surgery','6046677889','Morning');
/*!40000 ALTER TABLE nurses ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table patients
--

DROP TABLE IF EXISTS patients;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE patients (
  patient_id int NOT NULL AUTO_INCREMENT,
  name varchar(100) DEFAULT NULL,
  dob date DEFAULT NULL,
  gender enum('Male','Female','Other') DEFAULT NULL,
  contact varchar(15) DEFAULT NULL,
  address text,
  PRIMARY KEY (patient_id)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table patients
--

LOCK TABLES patients WRITE;
/*!40000 ALTER TABLE patients DISABLE KEYS */;
INSERT INTO patients VALUES (5,'devi','2025-08-05','Female','245678980','202 sweet'),(7,'tanvi','2005-09-07','Female','2345678910','909 White rock'),(8,'mandeep','2005-11-27','Female','2347988223','910 White rock'),(9,'chaitanya','2005-05-07','Female','2347988223','201 sweet'),(10,'pappu','2025-04-14','Male','0987654321','09 170 ave');
/*!40000 ALTER TABLE patients ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table prescriptions
--

DROP TABLE IF EXISTS prescriptions;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE prescriptions (
  prescription_id int NOT NULL AUTO_INCREMENT,
  appointment_id int DEFAULT NULL,
  diagnosis text,
  treatment text,
  notes text,
  PRIMARY KEY (prescription_id),
  KEY appointment_id (appointment_id),
  CONSTRAINT prescriptions_ibfk_1 FOREIGN KEY (appointment_id) REFERENCES appointments (appointment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table prescriptions
--

LOCK TABLES prescriptions WRITE;
/*!40000 ALTER TABLE prescriptions DISABLE KEYS */;
/*!40000 ALTER TABLE prescriptions ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table users
--

DROP TABLE IF EXISTS users;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE users (
  id int NOT NULL AUTO_INCREMENT,
  username varchar(50) DEFAULT NULL,
  password varchar(100) DEFAULT NULL,
  role enum('admin','doctor','nurse') DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table users
--

LOCK TABLES users WRITE;
/*!40000 ALTER TABLE users DISABLE KEYS */;
INSERT INTO users VALUES (1,'admin1','adminpass','admin'),(2,'drjones','docpass','doctor'),(3,'nurseamy','nursepass','nurse');
/*!40000 ALTER TABLE users ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-16 15:59:10