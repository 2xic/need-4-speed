# INIT FIREBIRD
ls
${FBPATH}/bin/isql -user sysdba -sql_dialect 3  <<EOL
CREATE DATABASE 'test_database';
commit;
CONNECT 'test_database';
CREATE TABLE ARKIV (
	ID VARCHAR(10) NOT NULL,
	TEXT VARCHAR(10) NOT NULL,
	CONSTRAINT PK_ARKIV PRIMARY KEY (ID)
);
commit;
quit;
EOL

${FBPATH}/bin/isql -user sysdba -sql_dialect 3  <<EOL
CONNECT 'test_database';
SELECT * from ARKIV;
quit;
EOL

# INIT POSTGRES
service postgresql restart

psql -U postgres  <<EOF
CREATE TABLE ARKIV (
	ID VARCHAR(10) NOT NULL,
	TEXT VARCHAR(10) NOT NULL,
	CONSTRAINT PK_ARKIV PRIMARY KEY (ID)
);
EOF

psql -U postgres  <<EOL
SELECT * from ARKIV;
EOL

python3 -m scripts.insert_random_data
