import streamlit as st
import time

# Define breathing parameters
BREATHE_IN_DURATION = 3  # seconds
BREATHE_OUT_DURATION = 3  # seconds
DEFAULT_CYCLES = 3  # default number of cycles
DEFAULT_MP3_URL = "https://freepd.com/music/Infinite%20Wonder.mp3"  # default MP3 URL

# Define HTML, CSS, and JavaScript for the breathing bubble
def get_bubble_css_js(expand_duration, contract_duration, cycles, mp3_url):
    return f"""
    <style>
    .bubble {{
        width: 100px;
        height: 100px;
        background-color: #87CEFA;
        border-radius: 50%;
        margin: auto;
        transition: transform 1s ease-in-out;
    }}

    .bubble.expand {{
        transform: scale(1.5);
    }}

    .bubble.contract {{
        transform: scale(1);
    }}
    </style>
    <script>
    function startBreathingAnimation() {{
        const bubble = document.querySelector('.bubble');
        const audio = document.querySelector('#exercise-audio');
        
        const expandDuration = {expand_duration}; // seconds
        const contractDuration = {contract_duration}; // seconds
        const totalCycles = {cycles}; // number of cycles
        
        function breatheIn() {{
            bubble.classList.add('expand');
            bubble.classList.remove('contract');
        }}

        function breatheOut() {{
            bubble.classList.add('contract');
            setTimeout(() => {{
                bubble.classList.remove('contract');
            }}, 1000);
        }}

        function startCycle(cycleCount) {{
            breatheIn();
            setTimeout(() => {{
                breatheOut();
                setTimeout(() => {{
                    if (cycleCount > 1) {{
                        startCycle(cycleCount - 1);
                    }}
                }}, contractDuration * 1000);
            }}, expandDuration * 1000);
        }}
        
        // Start audio playback
        audio.play();
        
        startCycle(totalCycles);

        // Stop audio after the total cycle duration
        setTimeout(() => {{
            audio.pause();
            audio.currentTime = 0;
        }}, (expandDuration + contractDuration) * totalCycles * 1000);
    }}
    </script>
    """

def main():
    st.title("Simple Breathing Exercise")
    
    st.write(f"""
    Follow the breathing exercise instructions below:
    
    - Breathe in for {BREATHE_IN_DURATION} seconds
    - Breathe out for {BREATHE_OUT_DURATION} seconds
    """)
    
    # User input for number of cycles
    cycles = st.number_input('Number of cycles', min_value=1, value=DEFAULT_CYCLES, step=1)
    
    # User input for MP3 URL
    mp3_url = st.text_input('MP3 URL', value=DEFAULT_MP3_URL)
    
    if st.button('Start Exercise'):
        st.write("Get ready to start...")
        time.sleep(2)
        
        # Display HTML and JavaScript with user-configured cycles and MP3 URL
        bubble_css_js = get_bubble_css_js(BREATHE_IN_DURATION, BREATHE_OUT_DURATION, cycles, mp3_url)
        st.markdown(bubble_css_js, unsafe_allow_html=True)
        
        # Embed the audio element
        st.markdown(f'<audio id="exercise-audio" src="{mp3_url}" preload="auto"></audio>', unsafe_allow_html=True)
        st.markdown('<div class="bubble"></div>', unsafe_allow_html=True)
        
        # Run JavaScript to start the animation and audio
        st.markdown('<script>startBreathingAnimation();</script>', unsafe_allow_html=True)
        
        # Wait for the entire cycle duration
        total_cycle_duration = (BREATHE_IN_DURATION + BREATHE_OUT_DURATION) * cycles
        st.write("You can close this tab after the exercise completes.")
        time.sleep(total_cycle_duration)  # Adjust based on total cycle duration
        
        st.write("Exercise complete! Great job!")

if __name__ == "__main__":
    main()
