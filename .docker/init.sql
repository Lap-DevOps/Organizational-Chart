CREATE USER dev_user NOSUPERUSER;
ALTER USER dev_user WITH PASSWORD 'dev_user_password';
ALTER ROLE dev_user SET client_encoding TO 'utf8';
ALTER ROLE dev_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE dev_user SET timezone TO 'UTC';

CREATE DATABASE dev_database WITH
  ENCODING 'UTF8'
  OWNER = dev_user
  LC_COLLATE = 'en_US.utf8'
  LC_CTYPE = 'en_US.utf8';

GRANT ALL PRIVILEGES ON DATABASE dev_database TO dev_user;


CREATE USER test_user NOSUPERUSER;
ALTER USER test_user WITH PASSWORD 'test_user_password';
ALTER ROLE test_user SET client_encoding TO 'utf8';
ALTER ROLE test_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE test_user SET timezone TO 'UTC';

CREATE DATABASE test_database WITH
  ENCODING 'UTF8'
  OWNER = test_user
  LC_COLLATE = 'en_US.utf8'
  LC_CTYPE = 'en_US.utf8';

GRANT ALL PRIVILEGES ON DATABASE test_database TO test_user;


CREATE USER prod_user NOSUPERUSER;
ALTER USER prod_user WITH PASSWORD 'prod_user_password';
ALTER ROLE prod_user SET client_encoding TO 'utf8';
ALTER ROLE prod_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE prod_user SET timezone TO 'UTC';

CREATE DATABASE prod_database WITH
  ENCODING 'UTF8'
  OWNER = prod_user
  LC_COLLATE = 'en_US.utf8'
  LC_CTYPE = 'en_US.utf8';

GRANT ALL PRIVILEGES ON DATABASE prod_database TO prod_user;

