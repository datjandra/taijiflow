import streamlit as st
import plotly.graph_objects as go
from menu import menu

def calculate_scores(sleep_hours, exercise_days, exercise_minutes,
                     fruit_veggies, hydration_glasses, processed_foods,
                     stress_level, social_interactions, cognitive_activities):
    
    # Sleep Quality
    sleep_hours_score = min(100, max(0, (sleep_hours - 4) / 5 * 100))
    sleep_quality_score = sleep_hours_score  # Simplified calculation

    # Physical Activity
    frequency_score = min(100, exercise_days / 5 * 100)
    duration_score = min(100, exercise_minutes / 60 * 100)
    physical_activity_score = (frequency_score + duration_score) / 2
    
    # Nutrition
    fruit_veggie_score = min(100, fruit_veggies / 10 * 100)
    hydration_score = min(100, max(0, (hydration_glasses - 4) / 8 * 100))
    processed_food_score = 100 - min(100, processed_foods / 21 * 100)
    nutrition_score = (fruit_veggie_score + hydration_score + processed_food_score) / 3
    
    # Mental Well-being
    stress_score = 100 - min(100, stress_level / 10 * 100)
    social_engagement_score = min(100, social_interactions / 5 * 100)
    cognitive_activities_score = min(100, cognitive_activities / 5 * 100)
    mental_wellbeing_score = (stress_score + social_engagement_score + cognitive_activities_score) / 3
    
    # Overall Score
    overall_score = (sleep_quality_score + physical_activity_score + nutrition_score + mental_wellbeing_score) / 4    
    return sleep_quality_score, physical_activity_score, nutrition_score, mental_wellbeing_score, overall_score

def main():
  st.set_page_config(page_title="Progress Tracking")
  st.title("Wellness Score")
  menu()

  # User inputs
  sleep_hours = st.slider('Average hours of sleep per night:', 0, 10, 7)
  
  exercise_days = st.slider('Days of exercise per week:', 0, 7, 5)
  exercise_minutes = st.slider('Minutes of exercise per session:', 0, 120, 60)
  
  fruit_veggies = st.slider('Number of servings of fruits and vegetables per day:', 0, 10, 5)
  hydration_glasses = st.slider('Number of glasses of water per day:', 0, 12, 8)
  processed_foods = st.slider('Number of processed food servings per week:', 0, 21, 3)
  
  stress_level = st.slider('Stress level (0-10):', 0, 10, 3)
  social_interactions = st.slider('Social interactions per week:', 0, 7, 3)
  cognitive_activities = st.slider('Cognitive activities per week:', 0, 7, 3)

  sleep_quality_score, physical_activity_score, nutrition_score, mental_wellbeing_score, overall_score = calculate_scores(
      sleep_hours, exercise_days, exercise_minutes,
      fruit_veggies, hydration_glasses, processed_foods,
      stress_level, social_interactions, cognitive_activities
  )

  # Create radar chart
  categories = ['Sleep Quality', 'Physical Activity', 'Nutrition', 'Mental Well-being']
  values = [sleep_quality_score, physical_activity_score, nutrition_score, mental_wellbeing_score]

  # Radar chart
  fig = go.Figure()
  fig.add_trace(go.Scatterpolar(
      r=values + [values[0]],  # Close the radar chart
      theta=categories + [categories[0]],
      fill='toself'
  ))

  fig.update_layout(
      polar=dict(
          radialaxis=dict(visible=True, range=[0, 100])
      ),
      showlegend=False,
      title='Wellness Score'
  )

  # Display radar chart and overall score
  st.plotly_chart(fig)
  st.write(f'Wellness Score: {round(overall_score)}')

if __name__ == "__main__":
  main()
