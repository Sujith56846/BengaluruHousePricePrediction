from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os
import json
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Global variables to store models and data
models = {}
location_list = []
model_info = {}

def load_models():
    """Load all trained models and prepare data"""
    global models, location_list, model_info
    
    try:
        # Load model
        models['lr'] = joblib.load('linear_regression_model.pkl')
        
        # Load cleaned data to get location list
        if os.path.exists('Cleaned_data.csv'):
            df = pd.read_csv('Cleaned_data.csv')
            location_list = sorted(df['location'].unique().tolist())
        else:
            # Fallback location list
            location_list = [
                'Electronic City', 'Whitefield', 'Koramangala', 'JP Nagar', 
                'Marathahalli', 'Indira Nagar', 'HSR Layout', 'BTM Layout',
                'Hebbal', 'Yelahanka', 'Banashankari', 'Jayanagar', 'other'
            ]
        
        # Model information
        model_info = {
            'lr': {'name': 'Linear Regression', 'description': 'Fast and accurate prediction model'}
        }
        
        print("✅ Models loaded successfully!")
        print(f"📍 {len(location_list)} locations available")
        
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        # Create dummy model for testing if file doesn't exist
        models = {'lr': None}

def predict_price(total_sqft, bath, bhk, location, selected_models=None):
    """Make price prediction using Linear Regression model"""
    if selected_models is None:
        selected_models = ['lr']
    
    predictions = {}
    
    # Create input data
    input_data = {
        'total_sqft': float(total_sqft),
        'bath': int(bath), 
        'bhk': int(bhk),
        'location': location
    }
    
    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])
    
    try:
        for model_key in selected_models:
            if model_key in models and models[model_key] is not None:
                pred = models[model_key].predict(input_df)[0]
                predictions[model_key] = round(float(pred), 2)
            else:
                # Fallback calculation for demo
                base_price = total_sqft * 0.08 + bhk * 15 + bath * 5
                location_multiplier = 1.2 if location in ['Koramangala', 'Indira Nagar'] else 1.0
                predictions[model_key] = round(base_price * location_multiplier, 2)
                
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        # Fallback predictions
        base_price = total_sqft * 0.08 + bhk * 15 + bath * 5
        for model_key in selected_models:
            predictions[model_key] = round(base_price * (1 + np.random.uniform(-0.1, 0.1)), 2)
    
    return predictions

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html', locations=location_list)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Prediction page"""
    if request.method == 'GET':
        return render_template('predict.html', 
                             locations=location_list, 
                             models=model_info)
    
    elif request.method == 'POST':
        try:
            # Get form data
            total_sqft = request.form['total_sqft']
            bath = request.form['bath'] 
            bhk = request.form['bhk']
            location = request.form['location']
            # Use Linear Regression model
            selected_models = ['lr']
            
            # Make predictions
            predictions = predict_price(total_sqft, bath, bhk, location, selected_models)
            
            # Calculate statistics
            prices = list(predictions.values())
            avg_price = round(np.mean(prices), 2)
            min_price = round(min(prices), 2) 
            max_price = round(max(prices), 2)
            price_range = round(max_price - min_price, 2)
            
            # Prepare results
            results = {
                'input': {
                    'total_sqft': total_sqft,
                    'bath': bath,
                    'bhk': bhk, 
                    'location': location
                },
                'predictions': predictions,
                'statistics': {
                    'average': avg_price,
                    'minimum': min_price,
                    'maximum': max_price,
                    'range': price_range
                },
                'model_info': {k: model_info[k] for k in selected_models if k in model_info}
            }
            
            return render_template('results.html', results=results)
            
        except Exception as e:
            error_msg = f"Error making prediction: {str(e)}"
            return render_template('predict.html', 
                                 locations=location_list,
                                 models=model_info,
                                 error=error_msg)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    try:
        data = request.get_json()
        
        total_sqft = data.get('total_sqft')
        bath = data.get('bath')
        bhk = data.get('bhk') 
        location = data.get('location')
        selected_models = data.get('models', ['lr'])
        
        predictions = predict_price(total_sqft, bath, bhk, location, selected_models)
        
        return jsonify({
            'status': 'success',
            'predictions': predictions,
            'input': data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/locations')
def api_locations():
    """API endpoint to get available locations"""
    return jsonify({
        'locations': location_list,
        'count': len(location_list)
    })

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': len([k for k, v in models.items() if v is not None]),
        'locations_available': len(location_list)
    })

if __name__ == '__main__':
    # Load models on startup
    load_models()
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting Bangalore House Price Prediction Web App")
    print(f"📍 Running on port {port}")
    print(f"🔧 Debug mode: {debug_mode}")
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)