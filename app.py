from flask import Flask
from models import db, migrate, login_manager
from models import user
from models import user,product,gift,language
import os

app = Flask(__name__)
app.config["UPLOADS_FOLDER"] = os.path.join(os.getcwd(), "static", "uploads")
app.config["SECRET_KEY"] = "342afc9ac23241fa1372f913"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://sammy:akbarov@127.0.0.1:5432/epicfood"
app.config["WTF_CSRF_ENABLED"] = False
app.config["WTF_CSRF_SECRET_KEY"] = "fgkgsd23gkfsdk32fds4r3t43t43"

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

if __name__ == '__main__':
    from routes.main_route import *
    from routes.auth_route import *
    from routes.product_route import *
    from routes.gift_route import *
    from routes.language_route import *
    app.run(debug=True, port=8080, host='0.0.0.0')
