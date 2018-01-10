from src.app import app

app.run(debug=app.config['DEBUG'], port=4990)