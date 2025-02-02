# Monolithic_income_and_expense_traccker
 database_url = os.environ.get("DATABASE_URL")
DATABASES = {
    'default': dj_database_url.parse(database_url)
}