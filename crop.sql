/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.4.22-MariaDB : Database - hate_speech
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`hate_speech` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `hate_speech`;

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `firstname` varchar(100) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `useremail` varchar(100) DEFAULT NULL,
  `userpassword` int(10) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact` bigint(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `user` */

insert  into `user`(`firstname`,`lastname`,`useremail`,`userpassword`,`address`,`contact`) values ('tinku','sai','tinku@gmail.com',2626,'chennai',7458963210),('viswa','prasad','v@gmail.com',7410,'Bangolore',7896541023);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
