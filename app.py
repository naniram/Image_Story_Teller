import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
import io

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
# Configure the Gemini model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Predefined prompt
STORY_PROMPT = """
Analyze this image in detail and create a short story based on what you see. 
Consider the setting, characters, mood, and any actions or events depicted. 
The story should be creative, engaging, and directly inspired by the elements in the image.
Aim for a story of about 200-300 words.
"""

def generate_story_from_image(image, prompt):
   
    response = model.generate_content([prompt, image])
    return response.text

def main():
    st.title("Visual Storytelling Generator")
    st.write("Upload an image and let AI create a story based on it!")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        if st.button('Generate Story'):
            with st.spinner('Creating your story...'):
                story = generate_story_from_image(image, STORY_PROMPT)
                st.subheader("Generated Story")
                st.write(story)
                
                # Option to download the story
                st.download_button(
                    label="Download Story",
                    data=story.encode(),
                    file_name="generated_story.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()