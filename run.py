from app import create_app
from app import db
app = create_app()
db.create_all(app=create_app())
if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)
