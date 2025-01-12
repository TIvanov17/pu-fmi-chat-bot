from flask import Flask
from controller.home import home
from database.db import create_table
from sockets.socketio_bp import socketio

app = Flask(__name__)
app.register_blueprint(home)
socketio.init_app(app)

if __name__ == "__main__":
    create_table()
    socketio.run(app, host='0.0.0.0', debug=True)
