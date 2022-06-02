-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 02, 2022 at 10:17 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sewakamarhotel_db`
--
CREATE DATABASE IF NOT EXISTS `sewakamarhotel_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `sewakamarhotel_db`;

-- --------------------------------------------------------

--
-- Table structure for table `kamar`
--

CREATE TABLE `kamar` (
  `kode_kamar` varchar(100) NOT NULL,
  `nama_kamar` varchar(100) NOT NULL,
  `harga_kamar` int(11) NOT NULL,
  `jumlah_kamar` int(11) NOT NULL,
  `kamar_tersedia` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `kamar`
--

INSERT INTO `kamar` (`kode_kamar`, `nama_kamar`, `harga_kamar`, `jumlah_kamar`, `kamar_tersedia`) VALUES
('KAMAR1', 'KAMAR NOMOR 123', 10000, 10, 3);

-- --------------------------------------------------------

--
-- Table structure for table `reservasi`
--

CREATE TABLE `reservasi` (
  `kode_reservasi` varchar(100) NOT NULL,
  `kode_user` varchar(100) NOT NULL,
  `kode_kamar` varchar(100) NOT NULL,
  `tgl_checkin` date NOT NULL,
  `tgl_checkout` date NOT NULL,
  `jumlah_malam` int(11) NOT NULL,
  `total_biaya` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `reservasi`
--

INSERT INTO `reservasi` (`kode_reservasi`, `kode_user`, `kode_kamar`, `tgl_checkin`, `tgl_checkout`, `jumlah_malam`, `total_biaya`) VALUES
('awdadawda', 'user', 'KAMAR1', '2022-06-02', '2022-06-03', 1, 10000),
('RES1', 'user', 'KAMAR1', '2022-06-01', '2022-06-02', 1, 10000),
('RES2', 'user', 'KAMAR1', '2022-06-01', '2022-06-13', 12, 120000),
('RES3', 'user', 'KAMAR1', '2022-06-01', '2022-10-02', 123, 1230000),
('ressssss', 'user', 'KAMAR1', '2022-06-02', '2022-06-14', 12, 120000),
('tes1234', 'user', 'KAMAR1', '2022-06-02', '2022-06-03', 1, 10000);

-- --------------------------------------------------------

--
-- Table structure for table `statuscheck`
--

CREATE TABLE `statuscheck` (
  `kode_reservasi` varchar(100) NOT NULL,
  `isCheckin` varchar(100) NOT NULL,
  `isCheckout` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `statuscheck`
--

INSERT INTO `statuscheck` (`kode_reservasi`, `isCheckin`, `isCheckout`) VALUES
('awdadawda', 'NO', 'NO'),
('RES1', 'YES', 'YES'),
('RES2', 'YES', 'YES'),
('RES3', 'YES', 'YES'),
('ressssss', 'NO', 'NO'),
('tes1234', 'NO', 'NO');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `kode_user` varchar(100) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `no_telepon` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`kode_user`, `nama`, `no_telepon`, `email`, `password`, `status`) VALUES
('admin', 'Admin', '081234567890', 'admin@gmail.com', 'admin123', 'ADMIN'),
('ferrygun88', 'Ferry Gunawan', '081297507252', 'ferrygun88@gmail.com', 'f3rry123', 'ADMIN'),
('user', 'User', '081234567890', 'user@gmail.com', 'user123', 'CLIENT');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `kamar`
--
ALTER TABLE `kamar`
  ADD PRIMARY KEY (`kode_kamar`);

--
-- Indexes for table `reservasi`
--
ALTER TABLE `reservasi`
  ADD PRIMARY KEY (`kode_reservasi`),
  ADD KEY `kode_kamar` (`kode_kamar`),
  ADD KEY `kode_user` (`kode_user`);

--
-- Indexes for table `statuscheck`
--
ALTER TABLE `statuscheck`
  ADD PRIMARY KEY (`kode_reservasi`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`kode_user`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reservasi`
--
ALTER TABLE `reservasi`
  ADD CONSTRAINT `reservasi_ibfk_1` FOREIGN KEY (`kode_kamar`) REFERENCES `kamar` (`kode_kamar`),
  ADD CONSTRAINT `reservasi_ibfk_2` FOREIGN KEY (`kode_user`) REFERENCES `user` (`kode_user`);

--
-- Constraints for table `statuscheck`
--
ALTER TABLE `statuscheck`
  ADD CONSTRAINT `statuscheck_ibfk_1` FOREIGN KEY (`kode_reservasi`) REFERENCES `reservasi` (`kode_reservasi`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
