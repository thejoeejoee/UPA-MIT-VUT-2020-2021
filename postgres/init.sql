CREATE USER computer WITH PASSWORD 'computer';
CREATE USER superset WITH PASSWORD 'superset';

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO computer;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO superset;

CREATE SCHEMA superset;
GRANT ALL PRIVILEGES ON SCHEMA superset TO superset;
