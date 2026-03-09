-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: autolavadodb
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `role_id` int unsigned NOT NULL,
  `username` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_name` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `second_last_name` varchar(60) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone_number` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  UNIQUE KEY `uk_email` (`email`),
  KEY `idx_role_id` (`role_id`),
  CONSTRAINT `fk_users_role` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,1,'Amau','amau@example.com','$argon2id$v=19$m=102400,t=2,p=8$w9g7x9gbw1irtVaK0ZqzNg$XpKJ/jt16kd46U9/FtL9vB2FTqh4qXhY6CRYrvm16vA','Amaury','Romero','Martinez','+527641022230',NULL,1,'2026-03-04 11:18:15','2026-03-04 17:56:33'),(2,1,'Uri','uri@example.com','$argon2id$v=19$m=102400,t=2,p=8$wzjHeC9FaC3F2HtPqdU6hw$W+Wg1Ak8YbnUodB5jY1e5DQO622ZQPlvjjEFSeUC5LI','Uriel','Medina','Torres','+9644488422279','Chiveria',1,'2026-03-04 12:09:32','2026-03-04 15:51:21'),(3,3,'amaug','amaug@example.com','$argon2id$v=19$m=102400,t=2,p=8$aS1FaI1xLqX0/r93Tumd8w$9sBeyqIgeph4rxpDkjbgjdxZhXTwkKKG0Py31OoA4Bo','Amaury','Romero',NULL,'+59728720052812',NULL,1,'2026-03-04 15:34:14','2026-03-04 15:34:14'),(4,3,'amaug12','amaug12@example.com','$argon2id$v=19$m=102400,t=2,p=8$+B9jTMmZM4aQEuJ8z3kP4Q$k9IQOkICmBTcS1PtHKN923jB6Aj7h5AMeIE57dq2Mm4','Amaury','Romero','Martinez','+59728720052812','Ameles',1,'2026-03-04 15:36:58','2026-03-04 15:36:58'),(5,3,'amaug123','amaug123@example.com','$argon2id$v=19$m=102400,t=2,p=8$AQCgVCrFWAvBeG9NSem99w$/HtdqrL7qtfLcAHEUsenH1n7Y6NARTzBGKEcm+7SkUM','Amaury','Romero','Martinez','+59728720052812','Ameles',1,'2026-03-04 15:41:03','2026-03-04 15:41:03'),(6,2,'JUAN','Juan@example.com','$argon2id$v=19$m=102400,t=2,p=8$wxhjzPnfG+Oc856T0rqX8g$nE+Eais++sVtPeslygRws+S66EtnQe6pCshJoyjO0lI','Juan','Romero','Gomez','+1133561956','Alatriste',1,'2026-03-04 15:49:35','2026-03-04 15:49:35');
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

-- Dump completed on 2026-03-04 18:00:06
