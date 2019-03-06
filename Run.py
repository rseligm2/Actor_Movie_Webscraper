from flask import Flask


def create_app(self):
    app = Flask(__name__)

    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


    return app

app = create_app()
app.run(debug=True)