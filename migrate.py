import argparse
from database import mysql

MIGRATE_FILE = 'migrate.sql'
DESCRIPTION = 'Migrate structure of database into DEV or PROD'

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument("--prod", help="Migrate in production database", action="store_true", required=False)
args = parser.parse_args()


def migrate(is_production: bool):
    mysql.sql_conn = mysql.db_connection(is_migrate=True)
    mysql.execute_query(MIGRATE_FILE, is_production)
    mysql.sql_conn.close()


if __name__ == '__main__':
    migrate(args.prod)

