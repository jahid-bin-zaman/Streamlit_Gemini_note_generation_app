import streamlit as st
from api_calling import note_generator
from api_calling import audio_generator
from api_calling import quiz_generator
from PIL import Image

from google.genai import errors

# Title

st.title("Note Summary and Quiz Generator", anchor=False)
st.markdown("Upload up to 3 images to generate Note Summary and Quizzes")
st.divider()


with st.sidebar:
    st.header("Controls")
    
    # Working with images
    
    images = st.file_uploader(
        "Upload the photos of your note",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )
    
    pil_images = []
    
    for img in images:
        pil_img = Image.open(img)
        pil_images.append(pil_img)

    if images:
        if len(images)>3:
            st.error("Upload at max 3 images")
        else:
            st.success("Succesfully uploaded")
            
            cols = st.columns(len(images))
            for i, image in enumerate(images):
                with cols[i]:
                    st.image(image)
                    
    
    # Working with difficulty
    
    difficulty = st.selectbox(
        "Enter the difficulty of quiz",
        ("Easy", "Medium", "Hard"),
        index = None
    )
     
    pressed = st.button("Click to Initiate", type="primary")
    

if pressed:
    if not images:
        st.error("You must upload a image")

    if not difficulty:
        st.error("You must select a difficulty")
    
    
    if images and difficulty:
        
        # Note Generation
        with st.container(border=True):
            st.subheader("Your note", anchor=False)
            
            # the portion below will be replaced by API call
            with st.spinner("Generating note"):
                try:
                    generated_notes = note_generator(pil_images)
                    st.markdown(generated_notes)
                except errors.ServerError as e:
                    st.error("The server is busy right now. Please wait a moment and try again later.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
            
        
        # Audio Transcript Generation
        
        # clearing the markdown
        generated_notes = generated_notes.replace('#', '')
        generated_notes = generated_notes.replace('$', '')
        generated_notes = generated_notes.replace('*', '')
        generated_notes = generated_notes.replace('_', '')
        generated_notes = generated_notes.replace('"', '')
        generated_notes = generated_notes.replace("'", '')
        
        with st.container(border=True):
            st.subheader("Audio Transcript", anchor=False)
            
            with st.spinner("Generating audio"):
                try:
                    st.audio(audio_generator(generated_notes))
                except errors.ServerError as e:
                    st.error("The server is busy right now. Please wait a moment and try again later.")
                except Exception as e:
                    st.error(f"An unexpected error occured: {e}")
                    
        
        # Quiz Generation
        with st.container(border=True):
            with st.spinner("Generating audio"):
                try:
                    st.markdown(quiz_generator(pil_images, difficulty))
                except errors.ServerError as e:
                    st.error("The server is busy right now. Please wait a moment and try again later.")
                except Exception as e:
                    st.error(f"An unexpected error occured: {e}")