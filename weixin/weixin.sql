create table `weixin`
(
  `id`       int(11) auto_increment not null,
  `title`    varchar(255)           not null,
  `content`  text                   not null,
  `date`     varchar(255)           not null,
  `wechat`   varchar(255)           not null,
  `nickname` varchar(255)           not null,
  primary key (`id`)
) default charset = utf8;