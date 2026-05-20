# TaijiFlow

**A personalized Tai Chi and Qigong exercise recommendation platform powered by AI**

<p align="center">
  <img src="https://raw.githubusercontent.com/datjandra/taijiflow/refs/heads/main/baduanjin.jpg" alt="TaijiFlow Baduanjin Illustration" width="900">
</p>

## Overview

TaijiFlow is an intelligent wellness application that combines modern AI technology with traditional Chinese exercise practices. It provides personalized Tai Chi and Qigong exercise recommendations based on your health profile, medical conditions, wellness goals, and lifestyle factors. The app also includes video demonstrations and integrates scientific research to support your wellness journey.

## Key Features

### 🏠 **Home - Personalized Exercise Advisor**
The main interface where you can receive AI-powered exercise recommendations by entering:
- Your age, gender, height, and weight
- Any medical conditions you may have
- Lifestyle risks (e.g., smoking, sedentary lifestyle)
- Your wellness goals (e.g., improved flexibility, stress relief)

The system uses Google's Generative AI to create personalized exercise routines and searches PubMed for relevant scientific research to support recommendations.

### 👵 **Healthy Aging Advisor**
A specialized tool focused on wellness strategies for older adults, helping you maintain mobility, balance, and overall health through age-appropriate exercises.

### 🖼️ **Posture Analysis**
An image-based tool that analyzes your posture and provides feedback on alignment and form, helping you perform Tai Chi and Qigong movements correctly.

### 🕊️ **Breathing Exercise**
Guided breathing exercises to complement your Tai Chi and Qigong practice, promoting relaxation and mindfulness.

### 📋 **Wellness Assessment**
A comprehensive assessment tool to evaluate your current wellness status and track your progress over time.

## Technology Stack

**Frontend & Framework:**
- Streamlit - Interactive web application framework
- Plotly - Data visualization

**AI & Machine Learning:**
- Google Generative AI - Exercise recommendation engine
- Clarifai - Computer vision capabilities for posture analysis

**Data & Research:**
- PubMed API - Search for scientific evidence
- Twelve Labs API - Video search and analysis for exercise demonstrations

**Other:**
- Python 3.x
- Requests library for API interactions

## Installation

### Prerequisites
- Python 3.7 or higher
- API keys for:
  - Google Generative AI (GOOGLE_API_KEY)
  - Twelve Labs (TL_KEY, TL_INDEX)
  - Clarifai (if using image features)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/datjandra/taijiflow.git
cd taijiflow
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.streamlit/secrets.toml` file with your API keys:
```toml
GOOGLE_API_KEY = "your-google-api-key"
TL_KEY = "your-twelve-labs-key"
TL_INDEX = "your-twelve-labs-index"
GEM_MODEL = "gemini-pro"
GEM_EXERCISE_PROMPT = "You are a Tai Chi and Qigong expert..."
GEM_CONFIG_TEMPERATURE = "0.7"
SEARCH_OPTIONS = "visual,motion,text_in_video"
```

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser to `http://localhost:8501`

## How It Works

1. **User Profile Input**: Enter your personal health information and wellness goals
2. **Research Integration**: The app searches PubMed for relevant scientific studies on Tai Chi/Qigong for your specific needs
3. **AI Recommendation**: Google Generative AI analyzes your profile and research findings to suggest personalized exercises
4. **Video Demonstrations**: The app retrieves relevant video clips showing proper form and technique
5. **Scientific Context**: References to peer-reviewed research are provided to support the recommendations

## License

This project is licensed under the GNU Lesser General Public License v2.1 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Disclaimer

These exercises are not intended to replace professional medical advice, diagnosis, or treatment. Always consult with your healthcare provider before starting any new exercise program, especially if you have existing medical conditions.
