-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : ven. 08 déc. 2023 à 15:42
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
-- Structure de la table `blablachat`
--

DROP TABLE IF EXISTS `blablachat`;
CREATE TABLE IF NOT EXISTS `blablachat` (
  `idsent` int NOT NULL,
  `message` varchar(1024) COLLATE utf8mb4_general_ci NOT NULL,
  `dateEnvoi` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `idsent` (`idsent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `generalchat`
--

DROP TABLE IF EXISTS `generalchat`;
CREATE TABLE IF NOT EXISTS `generalchat` (
  `idsent` int NOT NULL,
  `message` varchar(1024) COLLATE utf8mb4_general_ci NOT NULL,
  `dateEnvoi` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `idsent` (`idsent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `generalchat`
--

INSERT INTO `generalchat` (`idsent`, `message`, `dateEnvoi`) VALUES
(2, 'test2', '2023-12-05 16:02:03'),
(2, 'oui', '2023-12-05 16:04:25'),
(2, 'test> salut', '2023-12-08 11:17:07'),
(2, 'test> ca fonctionne ?', '2023-12-08 11:17:20'),
(5, 'salut> salut comment ca va ?', '2023-12-08 11:19:20'),
(5, 'salut> hoho', '2023-12-08 11:19:27'),
(2, 'test> que chez toi', '2023-12-08 11:19:34'),
(2, 'test> salut comment ca va ?', '2023-12-08 11:20:53'),
(5, 'salut> bien et toi ?', '2023-12-08 11:21:04'),
(5, 'salut> je comprend', '2023-12-08 11:21:10'),
(2, 'test> be oui', '2023-12-08 11:21:19'),
(5, 'salut> salut', '2023-12-08 11:29:29'),
(5, 'salut> salut', '2023-12-08 11:29:31'),
(2, 'test> salut', '2023-12-08 11:29:35'),
(5, 'salut> test', '2023-12-08 11:35:45'),
(5, 'salut> oui', '2023-12-08 11:35:47'),
(2, 'test> salut', '2023-12-08 11:36:01'),
(2, 'test> ca fonctionne', '2023-12-08 11:36:07'),
(5, 'salut> ca va ?', '2023-12-08 11:39:05'),
(2, 'test> oui et toi ?', '2023-12-08 11:39:11'),
(2, 'test> a ben parfait', '2023-12-08 11:39:28'),
(2, 'test> bye', '2023-12-08 11:39:33'),
(5, 'salut> test', '2023-12-08 11:44:13'),
(2, 'test> salut', '2023-12-08 11:44:25'),
(2, 'test> bye', '2023-12-08 11:44:35'),
(5, 'salut> ha', '2023-12-08 11:45:02'),
(5, 'salut> salut a toi', '2023-12-08 11:46:27'),
(2, 'test> ha salut', '2023-12-08 11:46:34'),
(2, 'test> je déco', '2023-12-08 11:46:40'),
(2, 'test> bye', '2023-12-08 11:46:43'),
(2, 'test> re', '2023-12-08 11:48:13'),
(5, 'salut> re', '2023-12-08 11:48:16'),
(2, 'test> bye', '2023-12-08 11:48:20'),
(2, 'test> salut', '2023-12-08 11:49:44'),
(2, 'test> sadze', '2023-12-08 11:49:50'),
(2, 'test> eaz', '2023-12-08 11:49:52'),
(5, 'salut> fez', '2023-12-08 11:49:55'),
(2, 'bye', '2023-12-08 11:50:01'),
(2, 'test> salut salut', '2023-12-08 11:51:22'),
(5, 'salut> salu test', '2023-12-08 11:51:30'),
(2, 'bye', '2023-12-08 11:51:35'),
(2, 'test> parfait', '2023-12-08 13:16:36'),
(2, 'test> ca fonctionne meme malgré un win+L', '2023-12-08 13:16:57'),
(5, 'salut> salut comment ca va ?', '2023-12-08 13:21:17'),
(2, 'test> bien et toi ?', '2023-12-08 13:21:27'),
(5, 'salut> parfait ca fonctionne', '2023-12-08 13:21:35'),
(2, 'test> je confirme', '2023-12-08 13:21:39'),
(2, 'test> et toi ?', '2023-12-08 13:21:43'),
(5, 'salut> meme pluseurs messges d\'affilé /', '2023-12-08 13:21:56'),
(5, 'salut> oui', '2023-12-08 13:22:00'),
(5, 'salut> je pense', '2023-12-08 13:22:04'),
(5, 'salut> en plus ca ecrit bien dans la base de donnée', '2023-12-08 13:22:33'),
(5, 'bye', '2023-12-08 13:23:04'),
(2, 'bye', '2023-12-08 13:30:23'),
(5, 'salut> ca fonctionne', '2023-12-08 13:34:15'),
(2, 'test> oui', '2023-12-08 13:34:18'),
(2, 'test> oui', '2023-12-08 13:34:20'),
(2, 'test> uoirf', '2023-12-08 13:34:23'),
(2, 'bye', '2023-12-08 13:34:26'),
(5, 'salut> oui', '2023-12-08 13:35:10'),
(5, 'bye', '2023-12-08 13:35:26'),
(5, 'bye', '2023-12-08 13:35:34'),
(5, 'salut> etzt', '2023-12-08 13:36:53'),
(2, 'test> GSGs', '2023-12-08 13:36:55'),
(2, 'test> gSG', '2023-12-08 13:36:56'),
(2, 'test> GSdgs', '2023-12-08 13:36:56'),
(2, 'test> gtrgfdg', '2023-12-08 13:36:57'),
(2, 'test> dfgdf', '2023-12-08 13:36:58'),
(2, 'test> gdh', '2023-12-08 13:36:58'),
(2, 'test> dfh', '2023-12-08 13:36:59'),
(5, 'salut> dhfhdf4dhdh', '2023-12-08 13:37:04'),
(5, 'salut> dfh', '2023-12-08 13:37:04'),
(5, 'salut> dhf', '2023-12-08 13:37:05'),
(5, 'salut> d', '2023-12-08 13:37:05'),
(5, 'salut> fh', '2023-12-08 13:37:06'),
(5, 'salut> dfhq', '2023-12-08 13:38:17'),
(5, 'salut> dfhdfh', '2023-12-08 13:38:19'),
(5, 'salut> dhf', '2023-12-08 13:38:19'),
(5, 'salut> hdf', '2023-12-08 13:38:20'),
(2, 'test> dhgfsh', '2023-12-08 13:38:23'),
(2, 'test> sdfh', '2023-12-08 13:38:24'),
(2, 'bye', '2023-12-08 13:38:26'),
(5, 'salut> ok', '2023-12-08 13:38:38'),
(5, 'salut> o', '2023-12-08 13:38:40'),
(5, 'salut> osfds', '2023-12-08 13:38:41'),
(5, 'salut> sdg', '2023-12-08 13:38:42'),
(5, 'salut> nf', '2023-12-08 13:38:44'),
(5, 'salut>     dfhg', '2023-12-08 13:38:46');

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `dateInscription` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `rights` int NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`user_id`, `username`, `password`, `dateInscription`, `rights`) VALUES
(1, 'Jacques', 'test', '2023-12-08 11:05:32', 4),
(2, 'test', 'test', '2023-12-05 15:49:05', 4),
(5, 'salut', 'salut', '2023-12-08 10:28:22', 1);

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `blablachat`
--
ALTER TABLE `blablachat`
  ADD CONSTRAINT `blablachat_ibfk_1` FOREIGN KEY (`idsent`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `generalchat`
--
ALTER TABLE `generalchat`
  ADD CONSTRAINT `generalchat_ibfk_1` FOREIGN KEY (`idsent`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
