help: ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

up: ## Runs all containers in this terminal
	docker-compose up mongo redis postgres superset mongo-admin postgres-admin django-admin

upd: ## Runs all containers detached
	docker-compose up -d mongo redis postgres superset mongo-admin postgres-admin django-admin

init: ## Initializes superset, creates admin and migrates database
	docker-compose exec superset superset-init
	docker-compose run --rm django-admin migrate

create-user: ## Creates user
	docker-compose run superset superset fab create-user

create-admin: ## Creates admin
	docker-compose run superset superset fab create-admin

down: ## Stops all running containers
	docker-compose down

scrape: ## Scrapes data from directory pocasi and fills MongoDB
	docker-compose up scraper

compute: ## Updates Postgres with data computed from MongoDB
	docker-compose up computer

backup-superset: ## Backups all data sources and dashboards from Superset
	docker-compose run superset superset export-datasources -f /etc/superset/datasources
	docker-compose run superset superset export-dashboards -f /etc/superset/dashboards
	$(eval CID := $(shell docker ps | grep superset | cut -d ' ' -f 1))
	docker cp $(CID):/etc/superset/datasources ./superset/datasources
	docker cp $(CID):/etc/superset/dashboards ./superset/dashboards

restore-superset: ## Restores all data sources and dashboards from backup
	docker-compose run superset superset import-datasources -p /etc/superset/datasources
	docker-compose run superset superset set_database_uri -d Weather -u postgresql://superset:superset@postgres/upa
	docker-compose run superset superset import-dashboards -p /etc/superset/dashboards
