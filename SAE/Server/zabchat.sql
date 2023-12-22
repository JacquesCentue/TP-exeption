-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : ven. 22 déc. 2023 à 14:24
-- Version du serveur : 8.2.0
-- Version de PHP : 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `zabchat`
--
CREATE DATABASE IF NOT EXISTS `zabchat` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `zabchat`;

-- --------------------------------------------------------

--
-- Structure de la table `ban`
--

DROP TABLE IF EXISTS `ban`;
CREATE TABLE IF NOT EXISTS `ban` (
  `ban` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `dateban` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dateUnban` datetime NOT NULL DEFAULT '5000-01-01 00:00:00',
  PRIMARY KEY (`ban`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='voici la table de bannissement, sont recensé: les noms et ip';

--
-- Déchargement des données de la table `ban`
--

INSERT INTO `ban` (`ban`, `dateban`, `dateUnban`) VALUES
('ban', '2023-12-22 14:31:41', '5000-01-01 00:00:00'),
('kick', '2023-12-22 14:30:05', '2023-12-23 14:30:06');

-- --------------------------------------------------------

--
-- Structure de la table `blablachat`
--

DROP TABLE IF EXISTS `blablachat`;
CREATE TABLE IF NOT EXISTS `blablachat` (
  `idsent` int NOT NULL,
  `message` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `dateEnvoi` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ipEnvoi` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  KEY `idsent` (`idsent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `blablachat`
--

INSERT INTO `blablachat` (`idsent`, `message`, `dateEnvoi`, `ipEnvoi`) VALUES
(1, 'Jacques> test bla bla', '2023-12-22 14:26:46', '127.0.0.1'),
(20, 'ban> je veut me faire ban', '2023-12-22 14:31:32', '127.0.0.1');

-- --------------------------------------------------------

--
-- Structure de la table `comptachat`
--

DROP TABLE IF EXISTS `comptachat`;
CREATE TABLE IF NOT EXISTS `comptachat` (
  `idsent` int NOT NULL,
  `message` varchar(1024) COLLATE utf8mb4_general_ci NOT NULL,
  `dateEnvoi` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ipEnvoi` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  KEY `iduser` (`idsent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `comptachat`
--

INSERT INTO `comptachat` (`idsent`, `message`, `dateEnvoi`, `ipEnvoi`) VALUES
(1, 'Jacques> test compta', '2023-12-22 14:27:11', '127.0.0.1');

-- --------------------------------------------------------

--
-- Structure de la table `generalchat`
--

DROP TABLE IF EXISTS `generalchat`;
CREATE TABLE IF NOT EXISTS `generalchat` (
  `idsent` int NOT NULL,
  `message` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `dateEnvoi` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ipEnvoi` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  KEY `idsent` (`idsent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `generalchat`
--

INSERT INTO `generalchat` (`idsent`, `message`, `dateEnvoi`, `ipEnvoi`) VALUES
(1, 'Jacques> Test general', '2023-12-22 14:26:35', '127.0.0.1');

-- --------------------------------------------------------

--
-- Structure de la table `infochat`
--

DROP TABLE IF EXISTS `infochat`;
CREATE TABLE IF NOT EXISTS `infochat` (
  `idsent` int NOT NULL,
  `message` varchar(1024) COLLATE utf8mb4_general_ci NOT NULL,
  `dateEnvoi` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ipEnvoi` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  KEY `iduser` (`idsent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `infochat`
--

INSERT INTO `infochat` (`idsent`, `message`, `dateEnvoi`, `ipEnvoi`) VALUES
(1, 'Jacques> test info', '2023-12-22 14:26:53', '127.0.0.1');

-- --------------------------------------------------------

--
-- Structure de la table `marketingchat`
--

DROP TABLE IF EXISTS `marketingchat`;
CREATE TABLE IF NOT EXISTS `marketingchat` (
  `idsent` int NOT NULL,
  `message` varchar(1024) COLLATE utf8mb4_general_ci NOT NULL,
  `dateEnvoi` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ipEnvoi` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  KEY `iduser` (`idsent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `marketingchat`
--

INSERT INTO `marketingchat` (`idsent`, `message`, `dateEnvoi`, `ipEnvoi`) VALUES
(1, 'Jacques> test marketing', '2023-12-22 14:27:02', '127.0.0.1');

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `dateInscription` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `rights` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`user_id`, `username`, `password`, `dateInscription`, `rights`) VALUES
(1, 'Jacques', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', '2023-12-08 11:05:32', 8),
(2, 'test', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', '2023-12-05 15:49:05', 6),
(5, 'salut', 'ec9c3a34e791bda21bbcb69ea0eb875857497e0d48c75771b3d1adb5073ce791', '2023-12-08 10:28:22', 1),
(8, 'test2', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', '2023-12-12 17:38:05', 0),
(9, 'kick', '0db10f2c2f332cd27cf1407fa16c686337b2b23f46125d6e17740dbfc6df427e', '2023-12-15 11:17:30', 4),
(10, 'visiteur', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', '2023-12-15 15:13:13', 1),
(18, 'test10', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', '2023-12-21 15:12:37', 1),
(20, 'ban', 'b2a96c3d3fc2b6accdb4816e22467a7448defe3208a72a79a96d671e4087106e', '2023-12-22 14:31:00', 8);

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `blablachat`
--
ALTER TABLE `blablachat`
  ADD CONSTRAINT `blablachat_ibfk_1` FOREIGN KEY (`idsent`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `comptachat`
--
ALTER TABLE `comptachat`
  ADD CONSTRAINT `comptachat_ibfk_1` FOREIGN KEY (`idsent`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `generalchat`
--
ALTER TABLE `generalchat`
  ADD CONSTRAINT `generalchat_ibfk_1` FOREIGN KEY (`idsent`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `infochat`
--
ALTER TABLE `infochat`
  ADD CONSTRAINT `infochat_ibfk_1` FOREIGN KEY (`idsent`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `marketingchat`
--
ALTER TABLE `marketingchat`
  ADD CONSTRAINT `marketingchat_ibfk_1` FOREIGN KEY (`idsent`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
