from flask import Flask
from app.settings import DevelopmentConfig

def create_app():
    app = Flask(__name__) 
    app.config.from_object(DevelopmentConfig)    
    from app.routes.calculator_routes import calculator_blueprint
    app.register_blueprint(calculator_blueprint)   


    return app

app= create_app()

if __name__ == '__main__':
    app.run(debug=True)