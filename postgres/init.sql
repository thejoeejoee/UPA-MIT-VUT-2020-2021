-- create user for computer container
CREATE USER computer WITH PASSWORD 'computer';

-- create user for django-admin db management
CREATE USER django_admin WITH PASSWORD 'django_admin';

-- create user for superset container
CREATE USER superset WITH PASSWORD 'superset';

-- database upa already exists from container initialization
-- allow everything in upa.public for user `computer`
GRANT INSERT, UPDATE, DELETE, TRUNCATE, SELECT ON ALL TABLES IN SCHEMA public TO computer;
-- allow everything in upa.public for user `django_admin`
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO django_admin;
-- allow selects in upa.public for user `superset`
GRANT SELECT ON ALL TABLES IN SCHEMA public TO superset;

-- allow select for user `superset` on all tables created by user `upa`
ALTER DEFAULT PRIVILEGES
    FOR USER upa
    IN SCHEMA public
    GRANT SELECT ON TABLES TO superset;

-- allow select for user `superset` on all tables created by user `computer`
ALTER DEFAULT PRIVILEGES
    FOR USER computer
    IN SCHEMA public
    GRANT SELECT ON TABLES TO superset;

-- allow select for user `superset` on all tables created by user `django_admin`
ALTER DEFAULT PRIVILEGES
    FOR USER django_admin
    IN SCHEMA public
    GRANT SELECT ON TABLES TO superset;

-- database for superset configuration
CREATE DATABASE superset;
-- and allow everything
GRANT ALL PRIVILEGES ON DATABASE superset TO superset;