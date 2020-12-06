up:
	docker-compose up mongo redis postgres superset mongo-admin postgres-admin django-admin

init:
	docker-compose exec superset superset-init
	docker-compose run --rm django-admin migrate

create-user:
	docker-compose run superset superset fab create-user

create-admin:
	docker-compose run superset superset fab create-admin

down:
	docker-compose down

scrape:
	docker-compose up scraper

compute:
	docker-compose up computer

backup-superset:
	docker-compose run superset superset export-datasources -f /etc/superset/datasources
	docker-compose run superset superset export-dashboards -f /etc/superset/dashboards
	$(eval CID := $(shell docker ps | grep superset | cut -d ' ' -f 1))
	docker cp $(CID):/etc/superset/datasources ./superset/datasources
	docker cp $(CID):/etc/superset/dashboards ./superset/dashboards

restore-superset:
	docker-compose run superset superset import-datasources -p /etc/superset/datasources
	docker-compose run superset superset set_database_uri -d Weather -u postgresql://superset:superset@postgres/upa
	docker-compose run superset superset import-dashboards -p /etc/superset/dashboards
