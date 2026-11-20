-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Aug 21, 2026 at 01:13 AM
-- Server version: 8.4.7
-- PHP Version: 8.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `thuvien_db`
--
CREATE DATABASE IF NOT EXISTS `thuvien_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `thuvien_db`;

-- --------------------------------------------------------

--
-- Table structure for table `dangnhap`
--

DROP TABLE IF EXISTS `dangnhap`;
CREATE TABLE IF NOT EXISTS `dangnhap` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mathe` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mapin` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `dangnhap`
--

INSERT INTO `dangnhap` (`id`, `mathe`, `mapin`) VALUES
(1, 'user123', '123456');

-- --------------------------------------------------------

--
-- Table structure for table `sach`
--

DROP TABLE IF EXISTS `sach`;
CREATE TABLE IF NOT EXISTS `sach` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tensach` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tacgia` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `giatien` decimal(10,2) NOT NULL,
  `conhang` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `sach`
--

INSERT INTO `sach` (`id`, `tensach`, `tacgia`, `giatien`, `conhang`) VALUES
(1, 'Lap trinh PHP', 'Nguyen Van A', 150.00, 1),
(2, 'Co so du lieu MySQL', 'Tran Thi B', 200.00, 0),
(3, 'Hoc may co ban', 'Le Van C', 350.00, 1);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
