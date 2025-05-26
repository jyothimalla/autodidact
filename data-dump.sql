-- MySQL dump 10.13  Distrib 9.3.0, for macos14.7 (x86_64)
--
-- Host: localhost    Database: autodidact_db
-- ------------------------------------------------------
-- Server version	9.3.0

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
-- Table structure for table `fmc_admin`
--

DROP TABLE IF EXISTS `fmc_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fmc_admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `level` int NOT NULL,
  `question_type` varchar(255) NOT NULL,
  `question` varchar(1000) NOT NULL,
  `answer` varchar(255) NOT NULL,
  `explanation` varchar(1000) NOT NULL,
  `image` varchar(500) DEFAULT NULL,
  `is_exam_ready` tinyint(1) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_fmc_admin_id` (`id`),
  CONSTRAINT `fmc_admin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fmc_admin`
--

LOCK TABLES `fmc_admin` WRITE;
/*!40000 ALTER TABLE `fmc_admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `fmc_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fmc_paper_sets`
--

DROP TABLE IF EXISTS `fmc_paper_sets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fmc_paper_sets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `paper_id` varchar(255) DEFAULT NULL,
  `user_id` int NOT NULL,
  `level` int DEFAULT NULL,
  `show_answers` tinyint(1) DEFAULT NULL,
  `questions_json` json DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `paper_id` (`paper_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `fmc_paper_sets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fmc_paper_sets`
--

LOCK TABLES `fmc_paper_sets` WRITE;
/*!40000 ALTER TABLE `fmc_paper_sets` DISABLE KEYS */;
/*!40000 ALTER TABLE `fmc_paper_sets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fmc_question_attempts`
--

DROP TABLE IF EXISTS `fmc_question_attempts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fmc_question_attempts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `level` int NOT NULL,
  `score` int NOT NULL,
  `questions` text NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_fmc_question_attempts_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fmc_question_attempts`
--

LOCK TABLES `fmc_question_attempts` WRITE;
/*!40000 ALTER TABLE `fmc_question_attempts` DISABLE KEYS */;
/*!40000 ALTER TABLE `fmc_question_attempts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fmc_question_bank`
--

DROP TABLE IF EXISTS `fmc_question_bank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fmc_question_bank` (
  `id` int NOT NULL AUTO_INCREMENT,
  `level` int NOT NULL,
  `question_type` varchar(255) NOT NULL,
  `question` varchar(1000) NOT NULL,
  `answer` varchar(255) NOT NULL,
  `explanation` varchar(1000) NOT NULL,
  `image` varchar(500) DEFAULT NULL,
  `is_exam_ready` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_fmc_question_bank_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fmc_question_bank`
--

LOCK TABLES `fmc_question_bank` WRITE;
/*!40000 ALTER TABLE `fmc_question_bank` DISABLE KEYS */;
/*!40000 ALTER TABLE `fmc_question_bank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fmc_question_save`
--

DROP TABLE IF EXISTS `fmc_question_save`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fmc_question_save` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `level` int DEFAULT NULL,
  `paper_id` varchar(255) DEFAULT NULL,
  `question_type` varchar(255) DEFAULT NULL,
  `question` varchar(1000) DEFAULT NULL,
  `answer` varchar(255) DEFAULT NULL,
  `explanation` varchar(1000) DEFAULT NULL,
  `image` varchar(500) DEFAULT NULL,
  `is_exam_ready` tinyint(1) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `fmc_question_save_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fmc_question_save`
--

LOCK TABLES `fmc_question_save` WRITE;
/*!40000 ALTER TABLE `fmc_question_save` DISABLE KEYS */;
INSERT INTO `fmc_question_save` VALUES (1,1,0,'paper_20250521_225742_c304','fmc','Molly has $69. After spending $17, how much is left?','52','$69 - $17 = $52',NULL,0,'2025-05-21 21:57:43','2025-05-21 21:57:43'),(2,1,0,'paper_20250521_225742_c304','fmc','Landon has 8 apples.\nMadelyn took 6/8 of them.\nHow many did Madelyn take?','6','6/8 of 8 = 6',NULL,0,'2025-05-21 21:57:43','2025-05-21 21:57:43'),(3,1,0,'paper_20250521_225742_c304','fmc','Sofia has a rope of 21 cm. Charles has a rope of 6 cm. How long are they together?','27','21 cm + 6 cm = 27 cm',NULL,0,'2025-05-21 21:57:43','2025-05-21 21:57:43'),(4,1,0,'paper_20250521_225742_c304','fmc','How many odd numbers are there between 30 and 68 ?','19','There are 19 [\'even\', \'odd\'] numbers between 30 and 68.',NULL,0,'2025-05-21 21:57:43','2025-05-21 21:57:43'),(5,1,0,'paper_20250521_225742_c304','fmc','Sabrina has a meeting at 9:52. \nIt lasts 7 hours and 0 minutes. \n What time does it end? (Give your answer in HH:MM format)','16:52','Start: 9:52, Duration: 7h 0m, End: 16:52',NULL,0,'2025-05-21 21:57:43','2025-05-21 21:57:43'),(6,1,0,'paper_20250521_225742_c304','fmc','Lennon has a rope of 20 cm. Chase has a rope of 1 cm. How long are they together?','21','20 cm + 1 cm = 21 cm',NULL,0,'2025-05-21 21:57:43','2025-05-21 21:57:43'),(7,1,0,'paper_20250521_225742_c304','fmc','Jeremiah has 3 boxes of Beading Kits, each with 3 items. \n How many in total?','9','3 × 3 = 9',NULL,0,'2025-05-21 21:57:43','2025-05-21 21:57:43'),(8,1,0,'paper_20250521_225742_c304','fmc','Koa has a secret code: 9793. What is the code?','9793','The code is 9793.',NULL,0,'2025-05-21 21:57:43','2025-05-21 21:57:43'),(9,1,0,'paper_20250521_225742_c304','fmc','Mckenzie has $46. After spending $39, how much is left?','7','$46 - $39 = $7',NULL,0,'2025-05-21 21:57:43','2025-05-21 21:57:43'),(10,1,0,'paper_20250521_225742_c304','fmc','Autumn had 6 Gardening Kits. \n Thomas gave Autumn 2 more. \n How many does Autumn have now?','8','6 + 2 = 8',NULL,0,'2025-05-21 21:57:43','2025-05-21 21:57:43'),(11,1,0,'paper_20250521_225809_1cbe','fmc','A pet home has 4 parrots, 4 cats, and 4 dogs.\nHow many legs can the owner see?','40','2×4 + 4×4 + 4×4 = 40',NULL,0,'2025-05-21 21:58:10','2025-05-21 21:58:10'),(12,1,0,'paper_20250521_225809_1cbe','fmc','Benjamin has a secret code. What is the code?','8410','The code is a random number between 1000 and 9999.',NULL,0,'2025-05-21 21:58:10','2025-05-21 21:58:10'),(13,1,0,'paper_20250521_225809_1cbe','fmc','Zane the cat and her 2 kittens each eat 4 cat treats every day.\nHow many treats altogether do they eat in one day?','12','3 × 4 = 12',NULL,0,'2025-05-21 21:58:10','2025-05-21 21:58:10'),(14,1,0,'paper_20250521_225809_1cbe','fmc','Rocco ate four-fifths of a chocolate bar. 24g was left. How much did Rocco eat?','96g','1/5 = 24, so 5/5 = 120, 4/5 = 96',NULL,0,'2025-05-21 21:58:10','2025-05-21 21:58:10'),(15,1,0,'paper_20250521_225809_1cbe','fmc','Peyton has a secret code. What is the code?','7042','The code is a random number between 1000 and 9999.',NULL,0,'2025-05-21 21:58:10','2025-05-21 21:58:10'),(16,1,0,'paper_20250521_225809_1cbe','fmc','What is the smallest number of coins which will make 8p?','4','Use 4 × 2p and 0 × 1p coins → Total: 4 coins',NULL,0,'2025-05-21 21:58:10','2025-05-21 21:58:10'),(17,1,0,'paper_20250521_225809_1cbe','fmc','Alina has a secret code. What is the code?','2155','The code is a random number between 1000 and 9999.',NULL,0,'2025-05-21 21:58:10','2025-05-21 21:58:10'),(18,1,0,'paper_20250521_225809_1cbe','fmc','Aubrielle has a meeting at 3:00. \nIt lasts 2 hours and 53 minutes. \n What time does it end? (Give your answer in HH:MM format)','5:53','Start: 3:00, Duration: 2h 53m, End: 5:53',NULL,0,'2025-05-21 21:58:10','2025-05-21 21:58:10'),(19,1,0,'paper_20250521_225809_1cbe','fmc','Savannah has a meeting at 9:18. \nIt lasts 2 hours and 52 minutes. \n What time does it end? (Give your answer in HH:MM format)','12:10','Start: 9:18, Duration: 2h 52m, End: 12:10',NULL,0,'2025-05-21 21:58:10','2025-05-21 21:58:10'),(20,1,0,'paper_20250521_225809_1cbe','fmc','Kaden has a meeting at 11:11. \nIt lasts 9 hours and 21 minutes. \n What time does it end? (Give your answer in HH:MM format)','20:32','Start: 11:11, Duration: 9h 21m, End: 20:32',NULL,0,'2025-05-21 21:58:10','2025-05-21 21:58:10'),(21,1,0,'paper_20250522_080812_b099','fmc','Koa has 4 boxes of Kites, each with 2 items. \n How many in total?','8','4 × 2 = 8',NULL,0,'2025-05-22 07:08:12','2025-05-22 07:08:12'),(22,1,0,'paper_20250522_080812_b099','fmc','Sienna had 14 Shells. \nSienna gave away 9. \n How many are left?','5','14 - 9 = 5',NULL,0,'2025-05-22 07:08:12','2025-05-22 07:08:12'),(23,1,0,'paper_20250522_080812_b099','fmc','Ariana had 13 Flowers. \nAriana gave away 11. \n How many are left?','2','13 - 11 = 2',NULL,0,'2025-05-22 07:08:12','2025-05-22 07:08:12'),(24,1,0,'paper_20250522_080812_b099','fmc','How many odd numbers are there between 38 and 70 ?','16','There are 16 [\'even\', \'odd\'] numbers between 38 and 70.',NULL,0,'2025-05-22 07:08:12','2025-05-22 07:08:12'),(25,1,0,'paper_20250522_080812_b099','fmc','Wyatt has a rope of 46 cm. Sebastian has a rope of 9 cm. How long are they together?','55','46 cm + 9 cm = 55 cm',NULL,0,'2025-05-22 07:08:12','2025-05-22 07:08:12'),(26,1,0,'paper_20250522_080812_b099','fmc','Evan has a secret code. What is the code?','7676','The code is a random number between 1000 and 9999.',NULL,0,'2025-05-22 07:08:12','2025-05-22 07:08:12'),(27,1,0,'paper_20250522_080812_b099','fmc','Ainsley has a secret code. What is the code?','9912','The code is a random number between 1000 and 9999.',NULL,0,'2025-05-22 07:08:12','2025-05-22 07:08:12'),(28,1,0,'paper_20250522_080812_b099','fmc','Samuel has 10 sweets.\nRylee took 2/10 of them.\nHow many did Rylee take?','2','2/10 of 10 = 2',NULL,0,'2025-05-22 07:08:12','2025-05-22 07:08:12'),(29,1,0,'paper_20250522_080812_b099','fmc','What is the smallest number of coins which will make 8p?','7','Use 1 × 2p and 6 × 1p coins → Total: 7 coins',NULL,0,'2025-05-22 07:08:12','2025-05-22 07:08:12'),(30,1,0,'paper_20250522_080812_b099','fmc','How many odd numbers are there between 21 and 61 ?','20','There are 20 [\'even\', \'odd\'] numbers between 21 and 61.',NULL,0,'2025-05-22 07:08:12','2025-05-22 07:08:12');
/*!40000 ALTER TABLE `fmc_question_save` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `generated_problems`
--

DROP TABLE IF EXISTS `generated_problems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `generated_problems` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(255) NOT NULL,
  `question` text NOT NULL,
  `answer` varchar(255) NOT NULL,
  `operation` varchar(50) NOT NULL,
  `level` int DEFAULT NULL,
  `attempted` tinyint(1) DEFAULT NULL,
  `user_answer` varchar(255) DEFAULT NULL,
  `correct` tinyint(1) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_generated_problems_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `generated_problems`
--

LOCK TABLES `generated_problems` WRITE;
/*!40000 ALTER TABLE `generated_problems` DISABLE KEYS */;
/*!40000 ALTER TABLE `generated_problems` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `level_attempts`
--

DROP TABLE IF EXISTS `level_attempts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `level_attempts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `operation` varchar(50) NOT NULL,
  `level` int NOT NULL,
  `attempt_number` int NOT NULL,
  `score` int NOT NULL,
  `total_questions` int NOT NULL,
  `is_passed` tinyint(1) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `level_attempts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `level_attempts`
--

LOCK TABLES `level_attempts` WRITE;
/*!40000 ALTER TABLE `level_attempts` DISABLE KEYS */;
INSERT INTO `level_attempts` VALUES (1,1,'Jo','addition',0,1,10,10,1,'2025-04-28 16:10:40'),(2,1,'Jo','multiplication',0,1,10,10,1,'2025-04-28 21:14:46'),(3,1,'Jo','multiplication',0,2,10,10,1,'2025-04-28 21:14:48'),(4,1,'Jo','addition',0,2,10,10,1,'2025-04-28 22:01:12'),(5,1,'Jo','addition',0,3,10,10,1,'2025-04-29 14:40:33'),(6,1,'Jo','addition',0,4,10,10,1,'2025-05-02 20:35:09'),(7,3,'arjun1234','addition',0,1,10,10,1,'2025-05-22 17:02:51');
/*!40000 ALTER TABLE `level_attempts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `paper_sets`
--

DROP TABLE IF EXISTS `paper_sets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paper_sets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `username` varchar(255) NOT NULL,
  `operation` varchar(50) NOT NULL,
  `level` int NOT NULL,
  `sublevel` varchar(10) NOT NULL,
  `paper_number` int NOT NULL,
  `code` varchar(10) DEFAULT NULL,
  `questions_json` json NOT NULL,
  `is_exam_ready` tinyint(1) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `paper_sets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `paper_sets`
--

LOCK TABLES `paper_sets` WRITE;
/*!40000 ALTER TABLE `paper_sets` DISABLE KEYS */;
/*!40000 ALTER TABLE `paper_sets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_text` varchar(500) NOT NULL,
  `option_a` varchar(255) NOT NULL,
  `option_b` varchar(255) NOT NULL,
  `option_c` varchar(255) NOT NULL,
  `option_d` varchar(255) NOT NULL,
  `option_e` varchar(255) NOT NULL,
  `correct_answer` varchar(5) NOT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_questions_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_responses`
--

DROP TABLE IF EXISTS `quiz_responses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quiz_responses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` int NOT NULL,
  `question_index` int NOT NULL,
  `selected_answer` varchar(10) NOT NULL,
  `correct_answer` varchar(10) NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `session_id` (`session_id`),
  CONSTRAINT `quiz_responses_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `quiz_sessions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_responses`
--

LOCK TABLES `quiz_responses` WRITE;
/*!40000 ALTER TABLE `quiz_responses` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_responses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz_sessions`
--

DROP TABLE IF EXISTS `quiz_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quiz_sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `operation` varchar(50) NOT NULL,
  `level` int NOT NULL,
  `session_id` varchar(100) NOT NULL,
  `question_data` json NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  `score` int DEFAULT '0',
  `start_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `end_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_id` (`session_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `quiz_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz_sessions`
--

LOCK TABLES `quiz_sessions` WRITE;
/*!40000 ALTER TABLE `quiz_sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `quiz_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `saved_answers`
--

DROP TABLE IF EXISTS `saved_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `saved_answers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `username` varchar(255) NOT NULL,
  `student_name` varchar(255) NOT NULL,
  `operation` varchar(50) NOT NULL,
  `level` int DEFAULT NULL,
  `sublevel` varchar(50) NOT NULL,
  `question_number` int NOT NULL,
  `answer` varchar(255) NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_saved_answers_id` (`id`),
  CONSTRAINT `saved_answers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `saved_answers`
--

LOCK TABLES `saved_answers` WRITE;
/*!40000 ALTER TABLE `saved_answers` DISABLE KEYS */;
/*!40000 ALTER TABLE `saved_answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uploaded_files`
--

DROP TABLE IF EXISTS `uploaded_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uploaded_files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `file_path` varchar(500) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_uploaded_files_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uploaded_files`
--

LOCK TABLES `uploaded_files` WRITE;
/*!40000 ALTER TABLE `uploaded_files` DISABLE KEYS */;
/*!40000 ALTER TABLE `uploaded_files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_answers`
--

DROP TABLE IF EXISTS `user_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_answers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `question_id` int NOT NULL,
  `selected_answer` varchar(10) NOT NULL,
  `correct_answer` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_user_answers_id` (`id`),
  CONSTRAINT `user_answers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_answers`
--

LOCK TABLES `user_answers` WRITE;
/*!40000 ALTER TABLE `user_answers` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_logs`
--

DROP TABLE IF EXISTS `user_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action` varchar(50) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_logs`
--

LOCK TABLES `user_logs` WRITE;
/*!40000 ALTER TABLE `user_logs` DISABLE KEYS */;
INSERT INTO `user_logs` VALUES (1,5,'deactivated','2025-05-23 10:47:35');
/*!40000 ALTER TABLE `user_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_progress`
--

DROP TABLE IF EXISTS `user_progress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_progress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `ninja_stars` int DEFAULT NULL,
  `user_name` varchar(255) NOT NULL,
  `operation` varchar(50) NOT NULL,
  `level_completed` int NOT NULL,
  `dojo_points` int NOT NULL,
  `current_level` int DEFAULT NULL,
  `total_attempts` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_user_progress_id` (`id`),
  CONSTRAINT `user_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_progress`
--

LOCK TABLES `user_progress` WRITE;
/*!40000 ALTER TABLE `user_progress` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_progress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_scores`
--

DROP TABLE IF EXISTS `user_scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_scores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `operation` varchar(50) NOT NULL,
  `level` int NOT NULL,
  `set_number` int DEFAULT NULL,
  `score` int NOT NULL,
  `total_questions` int NOT NULL,
  `is_completed` tinyint(1) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_user_scores_id` (`id`),
  CONSTRAINT `user_scores_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_scores`
--

LOCK TABLES `user_scores` WRITE;
/*!40000 ALTER TABLE `user_scores` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_scores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `ninja_stars` int DEFAULT NULL,
  `awarded_title` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Jo','mjyothionline@gmail.com','$2b$12$1DETWEc2MzUD8ANdsoAT2en5rAWVScadQUw3Qhq86l9qnGEtkY/Wa',5,'Math Ninja 🥇','2025-04-26 18:46:06','2025-04-29 14:40:33',0,1),(2,'Naishu','mnaishada@gmail.com','$2b$12$B3IirZ1NdqEwMYG2avMUYOqie9w6ILpUmccxeANNt2J4tJPUg1UFC',0,'Beginner','2025-04-26 18:52:21','2025-04-26 18:52:21',0,1),(3,'arjun1234','arjunm0303@gmail.com','$2b$12$rI9HMQecLHk.lchuo16iyuMxA/kllrwlFcaaPrvYP7X4ECnc.OTfO',5,'Math Ninja 🥇','2025-04-26 18:52:43','2025-05-22 17:02:51',0,1),(4,'Aryan','aaryanm0303@gmail.com','$2b$12$zGzf884XFiy1EOYzFLXDXeVDdogrfCVEg9KY7LcOyVzSNAHhYBfYO',0,'Beginner','2025-04-26 18:53:19','2025-04-26 18:53:19',0,1),(5,'Arjun','arjunm@gmail.com','$2b$12$02VPOrnzR3dUwSXy1XhIVOP4Pw1pfJwfGja.65LY0C/syN9Orj3wC',0,'Beginner','2025-05-23 11:47:17','2025-05-23 11:47:35',0,0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-26 15:35:25
