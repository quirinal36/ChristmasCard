from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

from app.models import ChristmasLetter

if __name__ == '__main__':
    app.run()