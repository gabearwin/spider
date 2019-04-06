create table `image`
(
  `id`    varchar(255) primary key,
  `url`   varchar(255) null,
  `title` varchar(255) null,
  `thumb` varchar(255) null
) default charset = utf8;