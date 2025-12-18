# 🏠 Bangalore House Price Predictor

[![Flask](https://img.shields.io/badge/Flask-3.0.0-blue)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://python.org/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.8.0-orange)](https://scikit-learn.org/)

A comprehensive web application that predicts house prices in Bangalore using linear regression machine learning models. Built with Flask and featuring a modern, responsive dark theme design.

## 🌟 Features

- **🤖 Linear Regression Model**: Fast and accurate price predictions using Linear Regression
- **📊 Model Analysis**: Compare Linear, Lasso, and Ridge Regression performance (Linear used for predictions)
- **📍 240+ Locations**: Comprehensive coverage of Bangalore neighborhoods
- **⚡ Real-time Predictions**: Instant price estimates
- **📱 Responsive Design**: Modern dark theme with smooth animations
- **🔗 RESTful API**: Programmatic access to prediction model
- **🚀 Production Ready**: Docker support, health checks, and monitoring

## 🎯 Live Demo

🌐 **[[Visit Live Application](http://192.168.1.6:5000)]**

### Quick Test:
- **2 BHK, 1200 sqft in Electronic City**: ~₹67-96 Lakhs
- **3 BHK, 1800 sqft in Koramangala**: ~₹150-235 Lakhs
- **4 BHK, 2500 sqft in Whitefield**: ~₹174-250 Lakhs

## 📸 Screenshots

### Home Page
**[[Home Page](http://192.168.1.6:5000)]**

### About Information
**[[About Information](http://192.168.1.6:5000/about)]**

### Prediction Form
**[[Prediction Form](http://192.168.1.6:5000/predict)]**

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Local Development

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/bangalore-house-predictor.git
cd bangalore-house-predictor
```

2. **Create Virtual Environment**
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Prepare Model Files**
Ensure these files are in the root directory:
- `linear_regression_model.pkl`
- `Cleaned_data.csv`

5. **Run the Application**
```bash
python app.py
```

Visit: `http://localhost:5000`

## 🐳 Docker Deployment

### Quick Start with Docker
```bash
# Build and run
docker build -t bangalore-predictor .
docker run -p 5000:5000 bangalore-predictor
```

### Using Docker Compose
```bash
docker-compose up -d
```

## 📊 Model Performance

| Model | R² Score | Type | Usage |
|-------|----------|------|-------|
| **Linear Regression** | 0.8554 | Linear | ✅ **Production Model** (predictions) |
| **Ridge Regression** | 0.8554 | L2 Regularized | 📊 Analysis only (handles multicollinearity) |
| **Lasso Regression** | 0.6527 | L1 Regularized | 📊 Analysis only (feature selection) |

**Note:** Linear Regression is used for all predictions due to its optimal balance of accuracy (85.54% R²), speed, and interpretability. Lasso and Ridge models are included in the notebook for educational comparison purposes.

## 🔗 API Documentation

### Base URL
```
https://your-domain.com/api
```

### Endpoints

#### 1. **Predict House Price**
```http
POST /api/predict
Content-Type: application/json

{
  "total_sqft": 1200,
  "bath": 2,
  "bhk": 2,
  "location": "Electronic City",
  "models": ["lr"]
}
```

**Response:**
```json
{
  "status": "success",
  "predictions": {
    "lr": 85.50
  },
  "input": {
    "total_sqft": 1200,
    "bath": 2,
    "bhk": 2,
    "location": "Electronic City"
  }
}
```

#### 2. **Get Available Locations**
```http
GET /api/locations
```

**Response:**
```json
{
  "locations": ["Electronic City", "Whitefield", "Koramangala", "..."],
  "count": 240
}
```

#### 3. **Health Check**
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": 1,
  "locations_available": 240
}
```

## 🏗️ Architecture

### Project Structure
```
BangaloreHousePrediction/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Multi-container setup
├── DEPLOYMENT.md            # Deployment guide
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   ├── predict.html        # Prediction form
│   ├── results.html        # Results display
│   └── about.html          # About page
├── static/                  # Static assets
│   ├── css/
│   │   └── style.css       # Custom styles
│   └── js/
│       └── main.js         # JavaScript functionality
├── models/                  # ML model files (*.pkl)
├── data/                    # Dataset files
└── .env.example            # Environment template
```

### Technology Stack

**Backend:**
- **Flask** - Web framework
- **Scikit-learn** - Machine learning (Linear Regression)
- **Pandas/NumPy** - Data manipulation
- **Joblib** - Model serialization

**Frontend:**
- **Bootstrap 5** - UI framework with custom dark theme
- **Font Awesome** - Icons
- **JavaScript ES6** - Client-side logic with animations
- **CSS3** - Modern responsive design

**Deployment:**
- **Docker** - Containerization
- **Gunicorn** - WSGI server
- **Nginx** - Reverse proxy
- **Cloud platforms** - AWS, GCP, Heroku

## 🔧 Configuration

### Environment Variables

Create `.env` file from `.env.example`:

```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
FLASK_DEBUG=False

# Server Configuration
PORT=5000
WORKERS=4

# Security
SECRET_KEY=your_super_secret_key

# Features
ENABLE_API_RATE_LIMITING=True
API_RATE_LIMIT=100
```

### Model Configuration

The application uses **Linear Regression** exclusively for all predictions:

```python
# Production model
model = 'lr'  # Linear Regression (R² = 0.8554)

# Lasso and Ridge models are available in the Jupyter notebook
# for educational analysis and comparison purposes only
```

## 📈 Usage Examples

### Web Interface

1. **Navigate** to the prediction page
2. **Enter** property details:
   - Square feet (400-10,000)
   - Number of bedrooms (BHK)
   - Number of bathrooms
   - Location from dropdown
3. **Click** "Predict House Price"
4. **View** instant results with animated price display

### API Integration

```python
import requests

# Prediction request
response = requests.post('https://your-domain.com/api/predict', 
    json={
        'total_sqft': 1500,
        'bath': 3,
        'bhk': 3, 
        'location': 'Koramangala',
        'models': ['lr']
    }
)

result = response.json()
print(f"Predicted price: ₹{result['predictions']['lr']} Lakhs")
```

### JavaScript Integration

```javascript
// Using the built-in API helper
const prediction = await BangaloreHomes.makePrediction({
    total_sqft: 1800,
    bath: 3,
    bhk: 3,
    location: 'HSR Layout'
});

console.log('Prediction results:', prediction);
```

## 🧪 Testing

### Run Tests
```bash
# Unit tests
python -m pytest tests/

# API tests
python test_api.py

# Load testing
ab -n 1000 -c 10 http://localhost:5000/
```

### Model Validation
```bash
# Check model accuracy
python validate_models.py

# Cross-validation scores
python cross_validate.py
```

## 🚀 Deployment Options

### 1. **Heroku** (Easiest)
```bash
heroku create bangalore-predictor
git push heroku main
```

### 2. **AWS EC2** (Full Control)
```bash
# Launch instance and configure
ssh -i key.pem ubuntu@ec2-instance
git clone <repo>
sudo apt install nginx
# Configure reverse proxy
```

### 3. **Google Cloud Run** (Serverless)
```bash
gcloud run deploy --source .
```

### 4. **Digital Ocean** (Cost-effective)
```bash
# Use App Platform or Droplets
# Follow deployment guide
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📊 Model Training

The models were trained on 13,000+ Bangalore property records with the following preprocessing:

1. **Data Cleaning**:
   - Outlier removal (price, size, bathrooms)
   - Location standardization
   - Missing value handling

2. **Feature Engineering**:
   - Price per square foot calculation
   - Location one-hot encoding
   - BHK/bathroom ratio validation

3. **Model Training**:
   - Train-test split (80-20)
   - Cross-validation
   - Hyperparameter tuning

4. **Evaluation Metrics**:
   - R² Score (coefficient of determination)
   - Mean Absolute Error (MAE)
   - Root Mean Square Error (RMSE)

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup
```bash
# Fork the repository
git clone https://github.com/yourusername/bangalore-house-predictor.git

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and test
python -m pytest

# Commit and push
git commit -m "Add your feature"
git push origin feature/your-feature-name

# Create Pull Request
```

### Contribution Areas
- 🐛 Bug fixes and improvements
- ✨ New features and enhancements
- 📚 Documentation updates
- 🧪 Test coverage improvements
- 🎨 UI/UX enhancements
- 🚀 Performance optimizations

### Code Style
- Follow PEP 8 for Python
- Use meaningful variable names
- Add docstrings for functions
- Write unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Sujith G**
- 💼 LinkedIn: https://linkedin.com/in/sujith-g-347664278/
- 📧 Email: sujithg2515@gmail.com
- 🐙 GitHub: https://github.com/Sujith56846

## 🙏 Acknowledgments

- **Bangalore Real Estate Data** - Dataset source kaggle
- **Scikit-learn Community** - ML algorithms
- **Flask Team** - Web framework
- **Bootstrap Team** - UI components
- **Contributors** - Community support

## 📞 Support

Need help? Here are your options:

1. 📖 **Documentation**: Check [DEPLOYMENT.md](DEPLOYMENT.md)
2. 🐛 **Bug Reports**: [GitHub Issues](https://github.com/Sujith56846)
3. 📧 **Email**: sujithg2515@gmail.com

🍴 **Fork** to create your own version

Made with ❤️ for the Bangalore real estate community






