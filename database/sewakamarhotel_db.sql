-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 03 Jun 2022 pada 07.43
-- Versi server: 10.4.18-MariaDB
-- Versi PHP: 8.0.3

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
-- Struktur dari tabel `kamar`
--

CREATE TABLE `kamar` (
  `kode_kamar` varchar(100) NOT NULL,
  `nama_kamar` varchar(100) NOT NULL,
  `harga_kamar` int(11) NOT NULL,
  `jumlah_kamar` int(11) NOT NULL,
  `kamar_tersedia` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `kamar`
--

INSERT INTO `kamar` (`kode_kamar`, `nama_kamar`, `harga_kamar`, `jumlah_kamar`, `kamar_tersedia`) VALUES
('RC01', 'Grandhika Suite', 1500000, 10, 7),
('RC02', 'Grandhika Premiere', 1000000, 15, 13),
('RC03', 'Executive Deluxe', 750000, 20, 18),
('RC04', 'Deluxe', 500000, 50, 48);

-- --------------------------------------------------------

--
-- Struktur dari tabel `reservasi`
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
-- Dumping data untuk tabel `reservasi`
--

INSERT INTO `reservasi` (`kode_reservasi`, `kode_user`, `kode_kamar`, `tgl_checkin`, `tgl_checkout`, `jumlah_malam`, `total_biaya`) VALUES
('AR01', 'lixxx', 'RC01', '2022-06-03', '2022-06-05', 2, 3000000),
('AR02', 'muel', 'RC02', '2022-06-15', '2022-06-20', 5, 5000000),
('AR03', 'reyy', 'RC03', '2022-06-03', '2022-06-04', 1, 750000),
('AR04', 'xzandel', 'RC04', '2022-06-10', '2022-06-13', 3, 1500000),
('AR05', 'lixxx', 'RC02', '2022-06-25', '2022-06-30', 5, 5000000),
('AR06', 'muel', 'RC01', '2022-06-19', '2022-06-22', 3, 4500000),
('AR07', 'xzandel', 'RC03', '2022-06-05', '2022-06-07', 2, 1500000),
('AR08', 'reyy', 'RC04', '2022-06-03', '2022-06-06', 3, 1500000);

-- --------------------------------------------------------

--
-- Struktur dari tabel `statuscheck`
--

CREATE TABLE `statuscheck` (
  `kode_reservasi` varchar(100) NOT NULL,
  `isCheckin` varchar(100) NOT NULL,
  `isCheckout` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `statuscheck`
--

INSERT INTO `statuscheck` (`kode_reservasi`, `isCheckin`, `isCheckout`) VALUES
('AR01', 'YES', 'NO'),
('AR02', 'NO', 'NO'),
('AR03', 'YES', 'NO'),
('AR04', 'NO', 'NO'),
('AR05', 'NO', 'NO'),
('AR06', 'NO', 'NO'),
('AR07', 'NO', 'NO'),
('AR08', 'YES', 'NO');

-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
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
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`kode_user`, `nama`, `no_telepon`, `email`, `password`, `status`) VALUES
('admin', 'Admin', '081234567890', 'admin@gmail.com', 'admin123', 'ADMIN'),
('ferrygun88', 'Ferry Gunawan', '081297507252', 'ferrygun88@gmail.com', 'f3rry123', 'ADMIN'),
('keruvin', 'Kelvin Chandra', '081212305860', 'kelvinchandra799@gmail.com', 'chandra123', 'ADMIN'),
('lixxx', 'Felix Setiawan', '082111211221', 'felixsetiawan41@gmail.com', 'setiawan123', 'CLIENT'),
('muel', 'Samuel Sulianto', '081285603610', 'samj8148@gmail.com', 'sulianto123', 'CLIENT'),
('platykus', 'Kevin Kusuma', '081314845533', 'kusumakevin09@gmail.com', 'kuskus123', 'ADMIN'),
('reyy', 'Reynaldo Krisno', '0895331059723', 'reynaldokrisno21@gmail.com', 'aldo123', 'CLIENT'),
('user', 'User', '081234567890', 'user@gmail.com', 'user123', 'CLIENT'),
('xzandel', 'Christopher Wiliam Saroinsong', '085959555495', 'saroinsong22@gmail.com', 'toper123', 'CLIENT');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `kamar`
--
ALTER TABLE `kamar`
  ADD PRIMARY KEY (`kode_kamar`);

--
-- Indeks untuk tabel `reservasi`
--
ALTER TABLE `reservasi`
  ADD PRIMARY KEY (`kode_reservasi`),
  ADD KEY `kode_kamar` (`kode_kamar`),
  ADD KEY `kode_user` (`kode_user`);

--
-- Indeks untuk tabel `statuscheck`
--
ALTER TABLE `statuscheck`
  ADD PRIMARY KEY (`kode_reservasi`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`kode_user`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `reservasi`
--
ALTER TABLE `reservasi`
  ADD CONSTRAINT `reservasi_ibfk_1` FOREIGN KEY (`kode_kamar`) REFERENCES `kamar` (`kode_kamar`),
  ADD CONSTRAINT `reservasi_ibfk_2` FOREIGN KEY (`kode_user`) REFERENCES `user` (`kode_user`);

--
-- Ketidakleluasaan untuk tabel `statuscheck`
--
ALTER TABLE `statuscheck`
  ADD CONSTRAINT `statuscheck_ibfk_1` FOREIGN KEY (`kode_reservasi`) REFERENCES `reservasi` (`kode_reservasi`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
