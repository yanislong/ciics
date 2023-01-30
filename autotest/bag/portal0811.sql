-- MySQL dump 10.17  Distrib 10.3.14-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: portaltest
-- ------------------------------------------------------
-- Server version	10.3.14-MariaDB-1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `collvaule`
--

DROP TABLE IF EXISTS `collvaule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `collvaule` (
  `id` int(11) DEFAULT NULL,
  `code` varchar(16) DEFAULT NULL,
  `value` varchar(1025) DEFAULT NULL,
  `remarks` varchar(1024) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `interfaceInfo`
--

DROP TABLE IF EXISTS `interfaceInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interfaceInfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `intername` varchar(255) DEFAULT NULL,
  `interaddr` varchar(8194) DEFAULT NULL,
  `header` varchar(8194) DEFAULT NULL,
  `inputtime` varchar(100) DEFAULT NULL,
  `param` text DEFAULT NULL,
  `option` varchar(30) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `descp` varchar(1024) DEFAULT NULL,
  `expected` varchar(100) DEFAULT NULL,
  `account` varchar(200) DEFAULT NULL COMMENT 'test username and password',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7635 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `interfaceRespond`
--

DROP TABLE IF EXISTS `interfaceRespond`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interfaceRespond` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `intername` varchar(255) DEFAULT NULL,
  `interaddr` varchar(2048) DEFAULT NULL,
  `requestparam` varchar(8194) DEFAULT NULL,
  `respondbody` mediumtext DEFAULT NULL,
  `code` char(3) DEFAULT NULL,
  `respondtime` decimal(8,6) DEFAULT NULL,
  `inputtime` varchar(50) DEFAULT NULL,
  `descp` varchar(1024) DEFAULT NULL,
  `result` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14155 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `qianyun`
--

DROP TABLE IF EXISTS `qianyun`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qianyun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dns_time` decimal(10,8) DEFAULT NULL,
  `conn_time` decimal(10,8) DEFAULT NULL,
  `startData_time` decimal(10,8) DEFAULT NULL,
  `total_time` decimal(10,8) DEFAULT NULL,
  `updata` float DEFAULT NULL,
  `downdata` float DEFAULT NULL,
  `insertTime` varchar(200) DEFAULT NULL,
  `content` varchar(4000) DEFAULT NULL,
  `code` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45850 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `qianyun_post`
--

DROP TABLE IF EXISTS `qianyun_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qianyun_post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dns_time` decimal(10,8) DEFAULT NULL,
  `conn_time` decimal(10,8) DEFAULT NULL,
  `startData_time` decimal(10,8) DEFAULT NULL,
  `total_time` decimal(10,8) DEFAULT NULL,
  `updata` float DEFAULT NULL,
  `downdata` float DEFAULT NULL,
  `insertTime` varchar(200) DEFAULT NULL,
  `content` varchar(4000) DEFAULT NULL,
  `code` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1345 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `testdata`
--

DROP TABLE IF EXISTS `testdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `testdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(1000) DEFAULT NULL,
  `dataDesc` varchar(8000) DEFAULT NULL,
  `insertTime` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `uitestresult`
--

DROP TABLE IF EXISTS `uitestresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `uitestresult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mode` varchar(100) DEFAULT NULL,
  `stime` varchar(100) DEFAULT NULL,
  `etime` varchar(100) DEFAULT NULL,
  `result` varchar(8000) DEFAULT NULL,
  `exectime` varchar(100) DEFAULT NULL,
  `env` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=442 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `account` varchar(35) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-11 17:32:39
