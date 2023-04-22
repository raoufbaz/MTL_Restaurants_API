
create table violations
(
    id_poursuite  integer primary key,
    business_id   integer,
    date          date,
    description   varchar(300),
    adresse       varchar(60),
    date_jugement date,
    etablissement varchar(200),
    montant       integer,
    proprietaire  varchar(200),
    ville         varchar(100),
    status        varchar(100),
    date_status   date,
    categorie     varchar(50)
);
