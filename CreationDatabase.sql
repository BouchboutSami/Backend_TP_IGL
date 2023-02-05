CREATE DATABASE testp;

CREATE TABLE `annonces` 
(`id_annonce` int NOT NULL AUTO_INCREMENT,
`categorie` varchar(100) NOT NULL,
`type_annonce` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
`surface` int DEFAULT NULL,
`description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
`prix` int DEFAULT NULL,
`id_contact` int DEFAULT NULL,
`wilaya` varchar(500) NOT NULL, 
`commune` varchar(500) NOT NULL,
`image` mediumblob,`titre` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
`date_publication` date NOT NULL, 
`telephone` varchar(255) DEFAULT NULL,
PRIMARY KEY (`id_annonce`)) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `isadmin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `messages` ( 
`id_message` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
`create_time` datetime DEFAULT NULL COMMENT 'Create Time',
`Message_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
`id_destinataire` int NOT NULL,
`id_emetteur` int NOT NULL,   PRIMARY KEY (`id_message`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


