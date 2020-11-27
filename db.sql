-- データベース
CREATE DATABASE tradingbot;

-- テーブル
CREATE TABLE `entry` (`side` varchar(255) NOT NULL);

CREATE TABLE `execution_history_binance` (
    `id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `date` datetime(6) NOT NULL,
    `price` decimal(65, 30) unsigned NOT NULL,
    `size` decimal(65, 30) unsigned NOT NULL,
    PRIMARY KEY (`id`),
    KEY `index_execution_history_2` (`date`)
);

CREATE TABLE `ticker` (
    `date` timestamp NOT NULL,
    `best_bid` int unsigned NOT NULL,
    `best_ask` int unsigned NOT NULL
);