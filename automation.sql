CREATE DATABASE  IF NOT EXISTS `automation` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `automation`;
-- MySQL dump 10.13  Distrib 5.6.17, for Win64 (x86_64)
--
-- Host: 42.192.200.79    Database: automation
-- ------------------------------------------------------
-- Server version	5.7.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `api_test_plan`
--

DROP TABLE IF EXISTS `api_test_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_test_plan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `description` longtext,
  `plan_id` varchar(50) NOT NULL,
  `interfaceIds` json NOT NULL,
  `project_id` int(11) NOT NULL,
  `create_user` varchar(30) NOT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_test_plan`
--

LOCK TABLES `api_test_plan` WRITE;
/*!40000 ALTER TABLE `api_test_plan` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_test_plan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `api_test_plan_task`
--

DROP TABLE IF EXISTS `api_test_plan_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `api_test_plan_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `api_task_uid` varchar(50) NOT NULL,
  `test_plan_uid` varchar(50) NOT NULL,
  `state` varchar(10) DEFAULT NULL,
  `api_job_number` int(11) DEFAULT NULL,
  `success_num` int(11) DEFAULT NULL,
  `failed_num` int(11) DEFAULT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `used_time` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `api_test_plan_task`
--

LOCK TABLES `api_test_plan_task` WRITE;
/*!40000 ALTER TABLE `api_test_plan_task` DISABLE KEYS */;
/*!40000 ALTER TABLE `api_test_plan_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add crontab',7,'add_crontabschedule'),(26,'Can change crontab',7,'change_crontabschedule'),(27,'Can delete crontab',7,'delete_crontabschedule'),(28,'Can view crontab',7,'view_crontabschedule'),(29,'Can add interval',8,'add_intervalschedule'),(30,'Can change interval',8,'change_intervalschedule'),(31,'Can delete interval',8,'delete_intervalschedule'),(32,'Can view interval',8,'view_intervalschedule'),(33,'Can add periodic task',9,'add_periodictask'),(34,'Can change periodic task',9,'change_periodictask'),(35,'Can delete periodic task',9,'delete_periodictask'),(36,'Can view periodic task',9,'view_periodictask'),(37,'Can add periodic tasks',10,'add_periodictasks'),(38,'Can change periodic tasks',10,'change_periodictasks'),(39,'Can delete periodic tasks',10,'delete_periodictasks'),(40,'Can view periodic tasks',10,'view_periodictasks'),(41,'Can add solar event',11,'add_solarschedule'),(42,'Can change solar event',11,'change_solarschedule'),(43,'Can delete solar event',11,'delete_solarschedule'),(44,'Can view solar event',11,'view_solarschedule'),(45,'Can add clocked',12,'add_clockedschedule'),(46,'Can change clocked',12,'change_clockedschedule'),(47,'Can delete clocked',12,'delete_clockedschedule'),(48,'Can view clocked',12,'view_clockedschedule'),(49,'Can add task result',13,'add_taskresult'),(50,'Can change task result',13,'change_taskresult'),(51,'Can delete task result',13,'delete_taskresult'),(52,'Can view task result',13,'view_taskresult'),(53,'Can add chord counter',14,'add_chordcounter'),(54,'Can change chord counter',14,'change_chordcounter'),(55,'Can delete chord counter',14,'delete_chordcounter'),(56,'Can view chord counter',14,'view_chordcounter'),(57,'Can add 分支状态',15,'add_gitcasemodel'),(58,'Can change 分支状态',15,'change_gitcasemodel'),(59,'Can delete 分支状态',15,'delete_gitcasemodel'),(60,'Can view 分支状态',15,'view_gitcasemodel'),(61,'Can add gitlab信息',16,'add_gitlabmodel'),(62,'Can change gitlab信息',16,'change_gitlabmodel'),(63,'Can delete gitlab信息',16,'delete_gitlabmodel'),(64,'Can view gitlab信息',16,'view_gitlabmodel'),(65,'Can add 接口',17,'add_interfacemodel'),(66,'Can change 接口',17,'change_interfacemodel'),(67,'Can delete 接口',17,'delete_interfacemodel'),(68,'Can view 接口',17,'view_interfacemodel'),(69,'Can add 数据映射接口实例',18,'add_interfacecachemodel'),(70,'Can change 数据映射接口实例',18,'change_interfacecachemodel'),(71,'Can delete 数据映射接口实例',18,'delete_interfacecachemodel'),(72,'Can view 数据映射接口实例',18,'view_interfacecachemodel'),(73,'Can add 在线postman测试历史记录',19,'add_interfacehistory'),(74,'Can change 在线postman测试历史记录',19,'change_interfacehistory'),(75,'Can delete 在线postman测试历史记录',19,'delete_interfacehistory'),(76,'Can view 在线postman测试历史记录',19,'view_interfacehistory'),(77,'Can add 接口任务',20,'add_interfacejobmodel'),(78,'Can change 接口任务',20,'change_interfacejobmodel'),(79,'Can delete 接口任务',20,'delete_interfacejobmodel'),(80,'Can view 接口任务',20,'view_interfacejobmodel'),(81,'Can add 项目',21,'add_projectmodel'),(82,'Can change 项目',21,'change_projectmodel'),(83,'Can delete 项目',21,'delete_projectmodel'),(84,'Can view 项目',21,'view_projectmodel'),(85,'Can add 接口测试计划',22,'add_apitestplanmodel'),(86,'Can change 接口测试计划',22,'change_apitestplanmodel'),(87,'Can delete 接口测试计划',22,'delete_apitestplanmodel'),(88,'Can view 接口测试计划',22,'view_apitestplanmodel'),(89,'Can add 接口测试计划任务',23,'add_apitestplantaskmodel'),(90,'Can change 接口测试计划任务',23,'change_apitestplantaskmodel'),(91,'Can delete 接口测试计划任务',23,'delete_apitestplantaskmodel'),(92,'Can view 接口测试计划任务',23,'view_apitestplantaskmodel'),(93,'Can add case测试计划',24,'add_casetestplanmodel'),(94,'Can change case测试计划',24,'change_casetestplanmodel'),(95,'Can delete case测试计划',24,'delete_casetestplanmodel'),(96,'Can view case测试计划',24,'view_casetestplanmodel'),(97,'Can add case测试计划任务',25,'add_casetestplantaskmodel'),(98,'Can change case测试计划任务',25,'change_casetestplantaskmodel'),(99,'Can delete case测试计划任务',25,'delete_casetestplantaskmodel'),(100,'Can view case测试计划任务',25,'view_casetestplantaskmodel'),(101,'Can add case测试计划任务',26,'add_casejobmodel'),(102,'Can change case测试计划任务',26,'change_casejobmodel'),(103,'Can delete case测试计划任务',26,'delete_casejobmodel'),(104,'Can view case测试计划任务',26,'view_casejobmodel');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branch_status`
--

DROP TABLE IF EXISTS `branch_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `branch_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gitlab_url` varchar(100) NOT NULL,
  `gitlab_project_id` int(11) NOT NULL,
  `gitlab_project_name` varchar(100) NOT NULL,
  `branch_name` varchar(20) NOT NULL,
  `status` varchar(10) NOT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branch_status`
--

LOCK TABLES `branch_status` WRITE;
/*!40000 ALTER TABLE `branch_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `branch_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `case_job`
--

DROP TABLE IF EXISTS `case_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `case_job` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_task_id` int(11) NOT NULL,
  `case_path` varchar(300) NOT NULL,
  `state` varchar(10) NOT NULL,
  `result` varchar(100) DEFAULT NULL,
  `log` longtext,
  `report_path` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `case_job`
--

LOCK TABLES `case_job` WRITE;
/*!40000 ALTER TABLE `case_job` DISABLE KEYS */;
/*!40000 ALTER TABLE `case_job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `case_test_plan`
--

DROP TABLE IF EXISTS `case_test_plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `case_test_plan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `description` longtext,
  `parallel` tinyint(1) NOT NULL,
  `timer_enable` tinyint(1) NOT NULL,
  `crontab` varchar(300) DEFAULT NULL,
  `plan_id` varchar(50) NOT NULL,
  `case_paths` json NOT NULL,
  `env_file` varchar(300) DEFAULT NULL,
  `project_id` int(11) NOT NULL,
  `gitlab_url` varchar(100) NOT NULL,
  `gitlab_project_name` varchar(100) NOT NULL,
  `branch_name` varchar(20) NOT NULL,
  `create_user` varchar(30) NOT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `case_test_plan`
--

LOCK TABLES `case_test_plan` WRITE;
/*!40000 ALTER TABLE `case_test_plan` DISABLE KEYS */;
/*!40000 ALTER TABLE `case_test_plan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `case_test_plan_task`
--

DROP TABLE IF EXISTS `case_test_plan_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `case_test_plan_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_task_uid` varchar(50) NOT NULL,
  `test_plan_uid` varchar(50) NOT NULL,
  `state` varchar(10) DEFAULT NULL,
  `case_job_number` int(11) DEFAULT NULL,
  `finish_num` int(11) DEFAULT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  `used_time` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `case_test_plan_task`
--

LOCK TABLES `case_test_plan_task` WRITE;
/*!40000 ALTER TABLE `case_test_plan_task` DISABLE KEYS */;
/*!40000 ALTER TABLE `case_test_plan_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_clockedschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_clockedschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_clockedschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clocked_time` datetime(6) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_clockedschedule`
--

LOCK TABLES `django_celery_beat_clockedschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_clockedschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_clockedschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_crontabschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_crontabschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_crontabschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(240) NOT NULL,
  `hour` varchar(96) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(124) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  `timezone` varchar(63) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_crontabschedule`
--

LOCK TABLES `django_celery_beat_crontabschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_crontabschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_crontabschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_intervalschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_intervalschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_intervalschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_intervalschedule`
--

LOCK TABLES `django_celery_beat_intervalschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_intervalschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_intervalschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_periodictask`
--

DROP TABLE IF EXISTS `django_celery_beat_periodictask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_periodictask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime(6) DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime(6) DEFAULT NULL,
  `total_run_count` int(10) unsigned NOT NULL,
  `date_changed` datetime(6) NOT NULL,
  `description` longtext NOT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `interval_id` int(11) DEFAULT NULL,
  `solar_id` int(11) DEFAULT NULL,
  `one_off` tinyint(1) NOT NULL,
  `start_time` datetime(6) DEFAULT NULL,
  `priority` int(10) unsigned DEFAULT NULL,
  `headers` longtext NOT NULL,
  `clocked_id` int(11) DEFAULT NULL,
  `expire_seconds` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` (`crontab_id`),
  KEY `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` (`interval_id`),
  KEY `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` (`solar_id`),
  KEY `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` (`clocked_id`),
  CONSTRAINT `django_celery_beat_p_clocked_id_47a69f82_fk_django_ce` FOREIGN KEY (`clocked_id`) REFERENCES `django_celery_beat_clockedschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_crontab_id_d3cba168_fk_django_ce` FOREIGN KEY (`crontab_id`) REFERENCES `django_celery_beat_crontabschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_interval_id_a8ca27da_fk_django_ce` FOREIGN KEY (`interval_id`) REFERENCES `django_celery_beat_intervalschedule` (`id`),
  CONSTRAINT `django_celery_beat_p_solar_id_a87ce72c_fk_django_ce` FOREIGN KEY (`solar_id`) REFERENCES `django_celery_beat_solarschedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_periodictask`
--

LOCK TABLES `django_celery_beat_periodictask` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_periodictask` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_periodictask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_periodictasks`
--

DROP TABLE IF EXISTS `django_celery_beat_periodictasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime(6) NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_periodictasks`
--

LOCK TABLES `django_celery_beat_periodictasks` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_periodictasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_periodictasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_beat_solarschedule`
--

DROP TABLE IF EXISTS `django_celery_beat_solarschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_beat_solarschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event` varchar(24) NOT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq` (`event`,`latitude`,`longitude`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_beat_solarschedule`
--

LOCK TABLES `django_celery_beat_solarschedule` WRITE;
/*!40000 ALTER TABLE `django_celery_beat_solarschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_beat_solarschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_results_chordcounter`
--

DROP TABLE IF EXISTS `django_celery_results_chordcounter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_results_chordcounter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` varchar(255) NOT NULL,
  `sub_tasks` longtext NOT NULL,
  `count` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_results_chordcounter`
--

LOCK TABLES `django_celery_results_chordcounter` WRITE;
/*!40000 ALTER TABLE `django_celery_results_chordcounter` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_results_chordcounter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_celery_results_taskresult`
--

DROP TABLE IF EXISTS `django_celery_results_taskresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_celery_results_taskresult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `content_type` varchar(128) NOT NULL,
  `content_encoding` varchar(64) NOT NULL,
  `result` longtext,
  `date_done` datetime(6) NOT NULL,
  `traceback` longtext,
  `meta` longtext,
  `task_args` longtext,
  `task_kwargs` longtext,
  `task_name` varchar(255) DEFAULT NULL,
  `worker` varchar(100) DEFAULT NULL,
  `date_created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `django_celery_results_taskresult_date_done_49edada6` (`date_done`),
  KEY `django_celery_results_taskresult_status_cbbed23a` (`status`),
  KEY `django_celery_results_taskresult_task_name_90987df3` (`task_name`),
  KEY `django_celery_results_taskresult_worker_f8711389` (`worker`),
  KEY `django_celery_results_taskresult_date_created_099f3424` (`date_created`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_celery_results_taskresult`
--

LOCK TABLES `django_celery_results_taskresult` WRITE;
/*!40000 ALTER TABLE `django_celery_results_taskresult` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_celery_results_taskresult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(15,'case','gitcasemodel'),(16,'case','gitlabmodel'),(5,'contenttypes','contenttype'),(12,'django_celery_beat','clockedschedule'),(7,'django_celery_beat','crontabschedule'),(8,'django_celery_beat','intervalschedule'),(9,'django_celery_beat','periodictask'),(10,'django_celery_beat','periodictasks'),(11,'django_celery_beat','solarschedule'),(14,'django_celery_results','chordcounter'),(13,'django_celery_results','taskresult'),(18,'interface','interfacecachemodel'),(19,'interface','interfacehistory'),(20,'interface','interfacejobmodel'),(17,'interface','interfacemodel'),(21,'project','projectmodel'),(6,'sessions','session'),(22,'testplan','apitestplanmodel'),(23,'testplan','apitestplantaskmodel'),(26,'testplan','casejobmodel'),(24,'testplan','casetestplanmodel'),(25,'testplan','casetestplantaskmodel');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2022-03-06 15:18:34.499917'),(2,'auth','0001_initial','2022-03-06 15:18:34.815981'),(3,'admin','0001_initial','2022-03-06 15:18:35.622029'),(4,'admin','0002_logentry_remove_auto_add','2022-03-06 15:18:35.779612'),(5,'admin','0003_logentry_add_action_flag_choices','2022-03-06 15:18:35.793516'),(6,'contenttypes','0002_remove_content_type_name','2022-03-06 15:18:35.998236'),(7,'auth','0002_alter_permission_name_max_length','2022-03-06 15:18:36.151345'),(8,'auth','0003_alter_user_email_max_length','2022-03-06 15:18:36.177547'),(9,'auth','0004_alter_user_username_opts','2022-03-06 15:18:36.194221'),(10,'auth','0005_alter_user_last_login_null','2022-03-06 15:18:36.305772'),(11,'auth','0006_require_contenttypes_0002','2022-03-06 15:18:36.311563'),(12,'auth','0007_alter_validators_add_error_messages','2022-03-06 15:18:36.328664'),(13,'auth','0008_alter_user_username_max_length','2022-03-06 15:18:36.440670'),(14,'auth','0009_alter_user_last_name_max_length','2022-03-06 15:18:36.569937'),(15,'auth','0010_alter_group_name_max_length','2022-03-06 15:18:36.633183'),(16,'auth','0011_update_proxy_permissions','2022-03-06 15:18:36.661922'),(17,'django_celery_beat','0001_initial','2022-03-06 15:18:36.817710'),(18,'django_celery_beat','0002_auto_20161118_0346','2022-03-06 15:18:37.099616'),(19,'django_celery_beat','0003_auto_20161209_0049','2022-03-06 15:18:37.260238'),(20,'django_celery_beat','0004_auto_20170221_0000','2022-03-06 15:18:37.276283'),(21,'django_celery_beat','0005_add_solarschedule_events_choices','2022-03-06 15:18:37.289442'),(22,'django_celery_beat','0006_auto_20180322_0932','2022-03-06 15:18:37.432521'),(23,'django_celery_beat','0007_auto_20180521_0826','2022-03-06 15:18:37.628441'),(24,'django_celery_beat','0008_auto_20180914_1922','2022-03-06 15:18:37.665878'),(25,'django_celery_beat','0006_auto_20180210_1226','2022-03-06 15:18:37.690914'),(26,'django_celery_beat','0006_periodictask_priority','2022-03-06 15:18:37.770204'),(27,'django_celery_beat','0009_periodictask_headers','2022-03-06 15:18:37.868828'),(28,'django_celery_beat','0010_auto_20190429_0326','2022-03-06 15:18:38.418586'),(29,'django_celery_beat','0011_auto_20190508_0153','2022-03-06 15:18:38.589083'),(30,'django_celery_beat','0012_periodictask_expire_seconds','2022-03-06 15:18:38.786406'),(31,'django_celery_results','0001_initial','2022-03-06 15:18:38.838121'),(32,'django_celery_results','0002_add_task_name_args_kwargs','2022-03-06 15:18:39.097610'),(33,'django_celery_results','0003_auto_20181106_1101','2022-03-06 15:18:39.110683'),(34,'django_celery_results','0004_auto_20190516_0412','2022-03-06 15:18:39.273141'),(35,'django_celery_results','0005_taskresult_worker','2022-03-06 15:18:39.347493'),(36,'django_celery_results','0006_taskresult_date_created','2022-03-06 15:18:39.480384'),(37,'django_celery_results','0007_remove_taskresult_hidden','2022-03-06 15:18:39.588156'),(38,'django_celery_results','0008_chordcounter','2022-03-06 15:18:39.641560'),(39,'sessions','0001_initial','2022-03-06 15:18:39.690504'),(40,'case','0001_initial','2022-03-06 15:19:04.806755'),(41,'project','0001_initial','2022-03-06 15:19:26.173220'),(42,'interface','0001_initial','2022-03-06 15:20:03.320347'),(43,'testplan','0001_initial','2022-03-06 15:20:13.827098');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gitlab_info`
--

DROP TABLE IF EXISTS `gitlab_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gitlab_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `gitlab_url` varchar(200) NOT NULL,
  `desc` varchar(10) DEFAULT NULL,
  `private_token` varchar(30) NOT NULL,
  `create_date` datetime(6) NOT NULL,
  `update_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gitlab_info_gitlab_url_private_token_eabe99b4_uniq` (`gitlab_url`,`private_token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gitlab_info`
--

LOCK TABLES `gitlab_info` WRITE;
/*!40000 ALTER TABLE `gitlab_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `gitlab_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interface`
--

DROP TABLE IF EXISTS `interface`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interface` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `desc` longtext,
  `addr` varchar(1000) NOT NULL,
  `request_mode` varchar(8) NOT NULL,
  `headers` json DEFAULT NULL,
  `params` json DEFAULT NULL,
  `formData` json DEFAULT NULL,
  `urlencoded` json DEFAULT NULL,
  `raw` json DEFAULT NULL,
  `asserts` json DEFAULT NULL,
  `parameters` json DEFAULT NULL,
  `extract` json DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interface`
--

LOCK TABLES `interface` WRITE;
/*!40000 ALTER TABLE `interface` DISABLE KEYS */;
/*!40000 ALTER TABLE `interface` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interface_cache`
--

DROP TABLE IF EXISTS `interface_cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interface_cache` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `desc` longtext,
  `addr` varchar(1000) NOT NULL,
  `request_mode` varchar(8) NOT NULL,
  `headers` json DEFAULT NULL,
  `formData` json DEFAULT NULL,
  `urlencoded` json DEFAULT NULL,
  `raw` json DEFAULT NULL,
  `params` json DEFAULT NULL,
  `asserts` json DEFAULT NULL,
  `extract` json DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interface_cache`
--

LOCK TABLES `interface_cache` WRITE;
/*!40000 ALTER TABLE `interface_cache` DISABLE KEYS */;
/*!40000 ALTER TABLE `interface_cache` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interface_history`
--

DROP TABLE IF EXISTS `interface_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interface_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `addr` varchar(1000) NOT NULL,
  `request_mode` varchar(8) NOT NULL,
  `headers` json DEFAULT NULL,
  `formData` json DEFAULT NULL,
  `urlencoded` json DEFAULT NULL,
  `raw` json DEFAULT NULL,
  `params` json DEFAULT NULL,
  `user` varchar(40) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interface_history`
--

LOCK TABLES `interface_history` WRITE;
/*!40000 ALTER TABLE `interface_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `interface_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interface_job`
--

DROP TABLE IF EXISTS `interface_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interface_job` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `interfaceType` varchar(10) NOT NULL,
  `interface_id` int(11) NOT NULL,
  `test_plan_id` varchar(50) NOT NULL,
  `api_test_plan_task_id` int(11) NOT NULL,
  `extracts` json NOT NULL,
  `state` varchar(10) NOT NULL,
  `result` longtext,
  `status_code` int(11) DEFAULT NULL,
  `elapsed` double DEFAULT NULL,
  `create_date` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interface_job`
--

LOCK TABLES `interface_job` WRITE;
/*!40000 ALTER TABLE `interface_job` DISABLE KEYS */;
/*!40000 ALTER TABLE `interface_job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `desc` longtext,
  `env_variable` json DEFAULT NULL,
  `bound_case_info` json DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `create_user` varchar(20) NOT NULL,
  `update_user` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-03-06 15:30:22
