import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

# Set page config
st.set_page_config(
    page_title="Bangalore House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        height: 3em;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        border-color: #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_model_and_data():
    """Load the trained model and location data"""
    try:
        # Load the saved linear regression model
        model = joblib.load('linear_regression_model.pkl')
        
        # Load cleaned data and process it the same way as during training
        if os.path.exists('Cleaned_data.csv'):
            df = pd.read_csv('Cleaned_data.csv')
            
            # Drop the same columns that were dropped during training
            columns_to_drop = ['size', 'price_per_sqft']
            for col in columns_to_drop:
                if col in df.columns:
                    df = df.drop(col, axis=1)
            
            # Get unique locations from the processed dataset (these are the ones model was trained on)
            if 'location' in df.columns:
                locations = sorted(df['location'].unique().tolist())
            else:
                locations = ['other']
        else:
            # If cleaned data doesn't exist, provide a default list
            locations = ['other']
        
        return model, locations
    
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.error("Please ensure 'linear_regression_model.pkl' exists in the directory.")
        return None, []

def predict_price(model, total_sqft, bath, bhk, location):
    """Make price prediction using the loaded model"""
    try:
        # Create input data matching the training format
        input_data = {
            'location': location,
            'total_sqft': float(total_sqft),
            'bath': int(bath), 
            'bhk': int(bhk)
        }
        
        # Convert to DataFrame with correct column order
        input_df = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        # Check if prediction is valid
        if np.isnan(prediction) or prediction <= 0:
            st.warning("⚠️ The prediction seems unusual. Please verify your inputs.")
            return None
            
        return round(float(prediction), 2)
    
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        st.info("💡 Tip: Make sure you selected a valid location from the dropdown list.")
        return None

def main():
    # Load model and data
    model, locations = load_model_and_data()
    
    if model is None:
        st.error("⚠️ Unable to load the model. Please ensure 'linear_regression_model.pkl' exists.")
        return
    
    # Main title with styling
    st.title("🏠 Bangalore House Price Predictor")
    st.markdown("---")
    
    # Create two columns for input and output
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Property Details")
        
        # Input fields
        total_sqft = st.number_input(
            "Total Square Feet",
            min_value=300,
            max_value=30000,
            value=1200,
            step=50
        )
        
        bhk = st.selectbox(
            "BHK (Bedrooms)",
            options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            index=2
        )
        
        bath = st.selectbox(
            "Bathrooms",
            options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            index=1
        )
        
        location = st.selectbox(
            "Location",
            options=locations,
            index=0 if locations else None
        )
    
    with col2:
        st.header("� Predicted Price")
        
        # Add some spacing
        st.write("")
        st.write("")
        
        # Predict button
        if st.button("🚀 Predict Price", type="primary", use_container_width=True):
            with st.spinner("Calculating..."):
                predicted_price = predict_price(model, total_sqft, bath, bhk, location)
                
                if predicted_price:
                    # Display prediction
                    st.success("✅ Prediction Complete!")
                    
                    # Large price display
                    st.markdown(f"<h1 style='text-align: center; color: #FF4B4B;'>₹ {predicted_price} Lakhs</h1>", unsafe_allow_html=True)
                    st.markdown(f"<h4 style='text-align: center; color: #666;'>≈ ₹ {predicted_price * 100000:,.0f}</h4>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
