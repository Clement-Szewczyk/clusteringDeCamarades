-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql-serveur-catho.alwaysdata.net
-- Generation Time: May 27, 2025 at 11:08 AM
-- Server version: 10.11.10-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `serveur-catho_camarade`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `auth_user_id` int(11) NOT NULL,
  `auth_user_email` varchar(255) NOT NULL,
  `auth_user_mdp` varchar(255) NOT NULL,
  `auth_user_name` varchar(100) NOT NULL,
  `auth_user_firstname` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `formular`
--

CREATE TABLE `formular` (
  `formular_id` int(11) NOT NULL,
  `formular_title` varchar(100) NOT NULL,
  `formular_description` text NOT NULL,
  `formular_creator` int(11) NOT NULL,
  `formular_start` datetime NOT NULL,
  `formular_end` datetime NOT NULL,
  `formular_nb_vote_per_person` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `role_id` int(11) NOT NULL,
  `role_name` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `student_id` int(11) NOT NULL,
  `student_email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `teacher`
--

CREATE TABLE `teacher` (
  `teacher_email` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_role`
--

CREATE TABLE `user_role` (
  `user_role_userid` int(11) NOT NULL,
  `user_role_roleid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `vote`
--

CREATE TABLE `vote` (
  `vote_idvote` int(11) NOT NULL,
  `vote_userid` int(11) NOT NULL,
  `vote_formid` int(11) NOT NULL,
  `vote_studentid` int(11) NOT NULL,
  `weigth` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`auth_user_id`);

--
-- Indexes for table `formular`
--
ALTER TABLE `formular`
  ADD PRIMARY KEY (`formular_id`),
  ADD KEY `fk_creator_formular` (`formular_creator`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`role_id`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`student_id`);

--
-- Indexes for table `teacher`
--
ALTER TABLE `teacher`
  ADD PRIMARY KEY (`teacher_email`);

--
-- Indexes for table `user_role`
--
ALTER TABLE `user_role`
  ADD PRIMARY KEY (`user_role_userid`),
  ADD KEY `fk_roleid_role` (`user_role_roleid`);

--
-- Indexes for table `vote`
--
ALTER TABLE `vote`
  ADD PRIMARY KEY (`vote_idvote`),
  ADD KEY `fk_userid_vote` (`vote_userid`),
  ADD KEY `fk_formid_vote` (`vote_formid`),
  ADD KEY `fk_studentid_vote` (`vote_studentid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `auth_user_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `formular`
--
ALTER TABLE `formular`
  MODIFY `formular_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `student`
  MODIFY `student_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_role`
--
ALTER TABLE `user_role`
  MODIFY `user_role_userid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `vote`
--
ALTER TABLE `vote`
  MODIFY `vote_idvote` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `formular`
--
ALTER TABLE `formular`
  ADD CONSTRAINT `fk_creator_formular` FOREIGN KEY (`formular_creator`) REFERENCES `auth_user` (`auth_user_id`);

--
-- Constraints for table `user_role`
--
ALTER TABLE `user_role`
  ADD CONSTRAINT `fk_roleid_role` FOREIGN KEY (`user_role_roleid`) REFERENCES `role` (`role_id`),
  ADD CONSTRAINT `fk_userid_role` FOREIGN KEY (`user_role_userid`) REFERENCES `auth_user` (`auth_user_id`);

--
-- Constraints for table `vote`
--
ALTER TABLE `vote`
  ADD CONSTRAINT `fk_formid_vote` FOREIGN KEY (`vote_formid`) REFERENCES `formular` (`formular_id`),
  ADD CONSTRAINT `fk_studentid_vote` FOREIGN KEY (`vote_studentid`) REFERENCES `student` (`student_id`),
  ADD CONSTRAINT `fk_userid_vote` FOREIGN KEY (`vote_userid`) REFERENCES `auth_user` (`auth_user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
