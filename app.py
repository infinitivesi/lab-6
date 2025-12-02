import os
from flask import Flask, render_template, session
from flask_cors import CORS
from models import init_db
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.shop import shop_bp
from routes.api import api_bp

app = Flask(__name__)
app.secret_key = '1234'  # Необхідно для роботи з сесіями
# Пароль адміністратора: можна встановити змінною оточення ADMIN_PASSWORD
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'prikol123')

# ============================================
# НАЛАШТУВАННЯ CORS
# ============================================
# Дозволяємо запити з фронтенду
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5000", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Ініціалізація Flasgger для документації API (опціонально)
try:
    from flasgger import Swagger
    # Configure basic swagger metadata via app.config
    app.config.setdefault('SWAGGER', {
        'title': 'Flask Shop API',
        'uiversion': 3
    })
    swagger = Swagger(app)
except ImportError:
    print("Warning: Flasgger not installed. Install with: pip install Flasgger")

# Ініціалізація бази даних
init_db()

# Реєстрація блюпрінтів
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(api_bp)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api-demo')
def api_demo():
    return render_template('api_demo.html')

if __name__ == '__main__':
    app.run(debug=True)