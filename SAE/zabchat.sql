-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mar. 19 déc. 2023 à 14:55
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
('kick', '2023-12-15 11:18:48', '2023-12-16 11:18:49');

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
(2, 'test> test blabla', '2023-12-19 10:34:10', '127.0.0.1');

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
(2, 'test> test comptabilité', '2023-12-19 10:34:30', '127.0.0.1');

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
(2, 'test> test general', '2023-12-19 10:34:02', '127.0.0.1'),
(2, 'test> tout fonctionne corectement', '2023-12-19 10:35:52', '127.0.0.1'),
(2, 'test> test', '2023-12-19 10:50:47', '127.0.0.1'),
(2, 'test> non pas la deco', '2023-12-19 10:51:01', '127.0.0.1'),
(2, 'test> salut', '2023-12-19 10:54:32', '127.0.0.1'),
(2, 'test> salut', '2023-12-19 11:01:16', '127.0.0.1'),
(2, 'test> saliut', '2023-12-19 11:53:23', '127.0.0.1'),
(2, 'test> laz', '2023-12-19 11:53:26', '127.0.0.1'),
(2, 'test> sdf', '2023-12-19 11:54:26', '127.0.0.1'),
(2, 'test> earger', '2023-12-19 11:54:29', '127.0.0.1'),
(2, 'test> fdgdfg', '2023-12-19 11:56:07', '127.0.0.1'),
(2, 'test> salut', '2023-12-19 11:56:53', '127.0.0.1'),
(2, 'test> aezr', '2023-12-19 11:57:03', '127.0.0.1'),
(2, 'test> rt', '2023-12-19 11:57:15', '127.0.0.1'),
(2, 'test> test', '2023-12-19 12:00:07', '127.0.0.1');

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
(2, 'test> test marketing', '2023-12-19 10:34:21', '127.0.0.1');

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `dateInscription` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `rights` int NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`user_id`, `username`, `password`, `dateInscription`, `rights`) VALUES
(1, 'Jacques', 'test', '2023-12-08 11:05:32', 4),
(2, 'test', 'test', '2023-12-05 15:49:05', 4),
(5, 'salut', 'salut', '2023-12-08 10:28:22', 1),
(8, 'test2', 'test', '2023-12-12 17:38:05', 0),
(9, 'kick', 'kick', '2023-12-15 11:17:30', 4),
(10, 'visiteur', 'test', '2023-12-15 15:13:13', 1);

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
