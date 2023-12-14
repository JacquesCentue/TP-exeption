-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 14 déc. 2023 à 10:38
-- Version du serveur : 8.0.31
-- Version de PHP : 8.0.26

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
  PRIMARY KEY (`ban`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='voici la table de bannissement, sont recensé: les noms et ip';

--
-- Déchargement des données de la table `ban`
--

INSERT INTO `ban` (`ban`, `dateban`) VALUES
('test', '2023-12-13 11:20:26'),
('test2', '2023-12-13 10:51:47'),
('zgr', '2023-12-13 10:45:29');

-- --------------------------------------------------------

--
-- Structure de la table `blablachat`
--

DROP TABLE IF EXISTS `blablachat`;
CREATE TABLE IF NOT EXISTS `blablachat` (
  `idsent` int NOT NULL,
  `message` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
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
  `message` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `dateEnvoi` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ipEnvoi` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  KEY `idsent` (`idsent`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `generalchat`
--

INSERT INTO `generalchat` (`idsent`, `message`, `dateEnvoi`, `ipEnvoi`) VALUES
(2, 'test2', '2023-12-05 16:02:03', '0'),
(2, 'oui', '2023-12-05 16:04:25', '0'),
(2, 'test> salut', '2023-12-08 11:17:07', '0'),
(2, 'test> ca fonctionne ?', '2023-12-08 11:17:20', '0'),
(5, 'salut> salut comment ca va ?', '2023-12-08 11:19:20', '0'),
(5, 'salut> hoho', '2023-12-08 11:19:27', '0'),
(2, 'test> que chez toi', '2023-12-08 11:19:34', '0'),
(2, 'test> salut comment ca va ?', '2023-12-08 11:20:53', '0'),
(5, 'salut> bien et toi ?', '2023-12-08 11:21:04', '0'),
(5, 'salut> je comprend', '2023-12-08 11:21:10', '0'),
(2, 'test> be oui', '2023-12-08 11:21:19', '0'),
(5, 'salut> salut', '2023-12-08 11:29:29', '0'),
(5, 'salut> salut', '2023-12-08 11:29:31', '0'),
(2, 'test> salut', '2023-12-08 11:29:35', '0'),
(5, 'salut> test', '2023-12-08 11:35:45', '0'),
(5, 'salut> oui', '2023-12-08 11:35:47', '0'),
(2, 'test> salut', '2023-12-08 11:36:01', '0'),
(2, 'test> ca fonctionne', '2023-12-08 11:36:07', '0'),
(5, 'salut> ca va ?', '2023-12-08 11:39:05', '0'),
(2, 'test> oui et toi ?', '2023-12-08 11:39:11', '0'),
(2, 'test> a ben parfait', '2023-12-08 11:39:28', '0'),
(2, 'test> bye', '2023-12-08 11:39:33', '0'),
(5, 'salut> test', '2023-12-08 11:44:13', '0'),
(2, 'test> salut', '2023-12-08 11:44:25', '0'),
(2, 'test> bye', '2023-12-08 11:44:35', '0'),
(5, 'salut> ha', '2023-12-08 11:45:02', '0'),
(5, 'salut> salut a toi', '2023-12-08 11:46:27', '0'),
(2, 'test> ha salut', '2023-12-08 11:46:34', '0'),
(2, 'test> je déco', '2023-12-08 11:46:40', '0'),
(2, 'test> bye', '2023-12-08 11:46:43', '0'),
(2, 'test> re', '2023-12-08 11:48:13', '0'),
(5, 'salut> re', '2023-12-08 11:48:16', '0'),
(2, 'test> bye', '2023-12-08 11:48:20', '0'),
(2, 'test> salut', '2023-12-08 11:49:44', '0'),
(2, 'test> sadze', '2023-12-08 11:49:50', '0'),
(2, 'test> eaz', '2023-12-08 11:49:52', '0'),
(5, 'salut> fez', '2023-12-08 11:49:55', '0'),
(2, 'bye', '2023-12-08 11:50:01', '0'),
(2, 'test> salut salut', '2023-12-08 11:51:22', '0'),
(5, 'salut> salu test', '2023-12-08 11:51:30', '0'),
(2, 'bye', '2023-12-08 11:51:35', '0'),
(2, 'test> parfait', '2023-12-08 13:16:36', '0'),
(2, 'test> ca fonctionne meme malgré un win+L', '2023-12-08 13:16:57', '0'),
(5, 'salut> salut comment ca va ?', '2023-12-08 13:21:17', '0'),
(2, 'test> bien et toi ?', '2023-12-08 13:21:27', '0'),
(5, 'salut> parfait ca fonctionne', '2023-12-08 13:21:35', '0'),
(2, 'test> je confirme', '2023-12-08 13:21:39', '0'),
(2, 'test> et toi ?', '2023-12-08 13:21:43', '0'),
(5, 'salut> meme pluseurs messges d\'affilé /', '2023-12-08 13:21:56', '0'),
(5, 'salut> oui', '2023-12-08 13:22:00', '0'),
(5, 'salut> je pense', '2023-12-08 13:22:04', '0'),
(5, 'salut> en plus ca ecrit bien dans la base de donnée', '2023-12-08 13:22:33', '0'),
(5, 'bye', '2023-12-08 13:23:04', '0'),
(2, 'bye', '2023-12-08 13:30:23', '0'),
(5, 'salut> ca fonctionne', '2023-12-08 13:34:15', '0'),
(2, 'test> oui', '2023-12-08 13:34:18', '0'),
(2, 'test> oui', '2023-12-08 13:34:20', '0'),
(2, 'test> uoirf', '2023-12-08 13:34:23', '0'),
(2, 'bye', '2023-12-08 13:34:26', '0'),
(5, 'salut> oui', '2023-12-08 13:35:10', '0'),
(5, 'bye', '2023-12-08 13:35:26', '0'),
(5, 'bye', '2023-12-08 13:35:34', '0'),
(5, 'salut> etzt', '2023-12-08 13:36:53', '0'),
(2, 'test> GSGs', '2023-12-08 13:36:55', '0'),
(2, 'test> gSG', '2023-12-08 13:36:56', '0'),
(2, 'test> GSdgs', '2023-12-08 13:36:56', '0'),
(2, 'test> gtrgfdg', '2023-12-08 13:36:57', '0'),
(2, 'test> dfgdf', '2023-12-08 13:36:58', '0'),
(2, 'test> gdh', '2023-12-08 13:36:58', '0'),
(2, 'test> dfh', '2023-12-08 13:36:59', '0'),
(5, 'salut> dhfhdf4dhdh', '2023-12-08 13:37:04', '0'),
(5, 'salut> dfh', '2023-12-08 13:37:04', '0'),
(5, 'salut> dhf', '2023-12-08 13:37:05', '0'),
(5, 'salut> d', '2023-12-08 13:37:05', '0'),
(5, 'salut> fh', '2023-12-08 13:37:06', '0'),
(5, 'salut> dfhq', '2023-12-08 13:38:17', '0'),
(5, 'salut> dfhdfh', '2023-12-08 13:38:19', '0'),
(5, 'salut> dhf', '2023-12-08 13:38:19', '0'),
(5, 'salut> hdf', '2023-12-08 13:38:20', '0'),
(2, 'test> dhgfsh', '2023-12-08 13:38:23', '0'),
(2, 'test> sdfh', '2023-12-08 13:38:24', '0'),
(2, 'bye', '2023-12-08 13:38:26', '0'),
(5, 'salut> ok', '2023-12-08 13:38:38', '0'),
(5, 'salut> o', '2023-12-08 13:38:40', '0'),
(5, 'salut> osfds', '2023-12-08 13:38:41', '0'),
(5, 'salut> sdg', '2023-12-08 13:38:42', '0'),
(5, 'salut> nf', '2023-12-08 13:38:44', '0'),
(5, 'salut>     dfhg', '2023-12-08 13:38:46', '0'),
(2, 'test> salut samut', '2023-12-12 14:01:01', '0'),
(5, 'salut> salut commenbt ca va ?', '2023-12-12 14:01:10', '0'),
(5, 'salut> ca fonctionne l\'import', '2023-12-12 14:01:21', '0'),
(2, 'test> test ip', '2023-12-12 14:10:35', '127'),
(5, 'salut> test ip distant', '2023-12-12 14:11:34', '127'),
(5, 'salut> test encore', '2023-12-12 14:12:18', '127.0.0.1'),
(2, 'test> rezdrr', '2023-12-12 14:37:57', '127.0.0.1'),
(2, 'test> conctionne sur le réseau local', '2023-12-12 14:50:09', '127.0.0.1'),
(2, 'test> OK', '2023-12-12 14:52:45', '127.0.0.1'),
(5, 'salut> test', '2023-12-12 15:12:02', '127.0.0.1'),
(5, 'salut> test', '2023-12-12 15:21:51', '127.0.0.1'),
(2, 'test> ca marche ?', '2023-12-12 15:29:37', '192.168.154.45'),
(2, 'test> il faut croire', '2023-12-12 15:30:10', '192.168.154.45'),
(2, 'test> pare feu desactivé', '2023-12-12 15:33:48', '192.168.1.126'),
(2, 'test> attend je vais maintenant l\'activer', '2023-12-12 15:34:03', '192.168.1.126'),
(2, 'bye', '2023-12-12 15:34:06', '192.168.1.126'),
(2, 'test> ca fonctionne coté client avec parefeu', '2023-12-12 15:34:49', '192.168.1.126'),
(2, 'bye', '2023-12-12 15:34:53', '192.168.1.126'),
(5, 'bye', '2023-12-12 15:35:18', '192.168.1.145'),
(2, 'test> je peut communiquer avec un poste a distance avec comme regle python en réseau privé', '2023-12-12 15:53:38', '192.168.1.126'),
(2, 'test> je suis lmibre ', '2023-12-12 15:53:48', '192.168.1.126'),
(2, 'test> test', '2023-12-12 15:55:17', '192.168.1.126'),
(2, 'test> oui', '2023-12-12 15:55:20', '192.168.1.126'),
(2, 'test> ca marche, il faut juste autorizer python.exe dans le pare feu du serveur sur windows', '2023-12-12 15:56:00', '192.168.1.126'),
(2, 'test> maintenant je peut faire une table de bannisement via ip ou login simplement en implémantant 2 listes : banip et banuser qui a chaques démarrage su serveur la liste se met a jour ', '2023-12-12 15:57:55', '192.168.1.126'),
(2, 'test> ou bien peut etre mettre cette liste dans 1 car de toute facon il faut que les 2 éléments soit vérifiés', '2023-12-12 15:59:15', '192.168.1.126'),
(2, 'test> non je vais garder les 2 séparés je pense', '2023-12-12 16:00:06', '192.168.1.126'),
(2, 'test> tout va bien sans passer par un ide parfait', '2023-12-12 16:01:40', '192.168.1.126'),
(2, 'test> test', '2023-12-12 17:20:19', '192.168.1.145'),
(2, 'test> oui oui hon hon baguette', '2023-12-12 17:20:30', '192.168.1.145'),
(2, 'test> ca fonctionne le banissement', '2023-12-12 18:10:14', '192.168.1.145'),
(5, 'salut> salut atoiu', '2023-12-13 10:58:42', '192.168.1.145'),
(2, 'test> ca fonctionne', '2023-12-13 10:58:50', '192.168.1.145'),
(2, 'test> et le remote app ?', '2023-12-13 10:59:50', '192.168.1.145'),
(1, 'Jacques> fonctionne', '2023-12-13 11:00:00', '192.168.1.126'),
(2, 'test> salut', '2023-12-13 11:08:37', '192.168.1.145'),
(2, 'test> fzegcy', '2023-12-13 11:11:21', '192.168.1.145'),
(2, 'test> non', '2023-12-13 11:20:35', '192.168.1.145');

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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`user_id`, `username`, `password`, `dateInscription`, `rights`) VALUES
(1, 'Jacques', 'test', '2023-12-08 11:05:32', 4),
(2, 'test', 'test', '2023-12-05 15:49:05', 4),
(5, 'salut', 'salut', '2023-12-08 10:28:22', 1),
(8, 'test2', 'test', '2023-12-12 17:38:05', 0);

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
