import os
import streamlit as st
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import requests
import base64
import json
import io
from IPython.display import Audio
load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_API_URL = "https://api.sarvam.ai"

def get_gemini_response(input_text, prompt):
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
    prompt_template = PromptTemplate(
        input_variables=["input"],
        template=prompt
    )
    final_prompt = prompt_template.format(input=input_text)
    response = model.predict(final_prompt)
    return response

def generate_course_titles(profession, target_audience, course_content, course_description):
    input_text = f"""
    Profession: {profession}
    Target Audience: {target_audience}
    Course Content: {course_content}
    Course Description: {course_description}
    """
    prompt = """
    Based on the following information, generate 5 engaging and unique course titles:
    {input}

    Return the titles as a numbered list.
    """
    response = get_gemini_response(input_text, prompt)
    return [title.strip() for title in response.split("\n") if title.strip()]

def generate_course_outline(title, profession, target_audience, course_content, course_description):
    input_text = f"""
    Course Title: {title}
    Profession: {profession}
    Target Audience: {target_audience}
    Course Content: {course_content}
    Course Description: {course_description}
    """
    prompt = """
    Based on the following information, create a course outline with atmost 9 modules:
    {input}

    Generate a list of module names, each on a new line. Do not include any additional information or numbering.
    """
    response = get_gemini_response(input_text, prompt)
    return [module.strip() for module in response.split("\n") if module.strip()][:9]

def generate_module_content(title, module_name, course_info):
    input_text = f"""
    Course Title: {title}
    Module Name: {module_name}
    Profession: {course_info['profession']}
    Target Audience: {course_info['target_audience']}
    Course Content: {course_info['course_content']}
    Course Description: {course_info['course_description']}
    """
    prompt = """
    Based on the following information, generate approximately 200 words of lecture content for the specified module in paragraphs:
    {input}

    The content should be educational, engaging, and relevant to the course and target audience. Also add 3 mcqs (along with the answer key at the end) based on the lecture content.
    """
    response = get_gemini_response(input_text, prompt)
    return response

def sarvam_api_call(endpoint, data):
    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(f"{SARVAM_API_URL}/{endpoint}", headers=headers, json=data)
    return response.json()



def perform_translation(text, source_lang="en-IN", target_lang="hi-IN"):
    url = f"{SARVAM_API_URL}/translate"
    
    payload = {
        "source_language_code": source_lang,
        "target_language_code": target_lang,
        "speaker_gender": "Female",
        "mode": "formal",
        "model": "mayura:v1",
        "enable_preprocessing": True,
        "input": text
    }
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Translation failed with status code: {response.status_code}")
        st.error(f"Error message: {response.text}")
        return None

def perform_tts(text, speaker="meera"):
    url = f"{SARVAM_API_URL}/text-to-speech"
    
    payload = {
        "inputs": [text[:400]],
        "target_language_code": "hi-IN",
        "speaker": "meera",
        "pitch": 0,
        "pace": 1.65,
        "loudness": 1.5,
        "speech_sample_rate": 8000,
        "enable_preprocessing": True,
        "model": "bulbul:v1"
    }
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    if response.status_code == 200:
        aud_str=response.text[12:-3]
        audio_data=base64.b64decode(aud_str)
        return audio_data
    else:
        st.error(f"TTS failed with status code: {response.status_code}")
        st.error(f"Error message: {response.text}")
        return None

def main():
    st.set_page_config(page_title="Course Creation Copilot", page_icon="🎓", layout="wide")
    st.title("Course Creation Copilot 🎓")

    if 'step' not in st.session_state:
        st.session_state.step = 'input'
    if 'course_titles' not in st.session_state:
        st.session_state.course_titles = []
    if 'selected_title' not in st.session_state:
        st.session_state.selected_title = ''
    if 'course_outline' not in st.session_state:
        st.session_state.course_outline = []
    if 'course_info' not in st.session_state:
        st.session_state.course_info = {
            'profession': '',
            'target_audience': '',
            'course_content': '',
            'course_description': ''
        }
    if 'module_content' not in st.session_state:
        st.session_state.module_content = ''

    # Sidebar navigation
    st.sidebar.title("Navigation")
    step = st.sidebar.selectbox(
        "Go to step:",
        ['Input Information', 'Select Course Title', 'Customize Outline', 'Generate Content'],
        index=['input', 'select_title', 'customize_outline', 'generate_content'].index(st.session_state.step)
    )

    # Back button
    if st.sidebar.button("Back"):
        if st.session_state.step == 'select_title':
            st.session_state.step = 'input'
        elif st.session_state.step == 'customize_outline':
            st.session_state.step = 'select_title'
        elif st.session_state.step == 'generate_content':
            st.session_state.step = 'customize_outline'

    if step == 'Input Information':
        st.session_state.step = 'input'
    elif step == 'Select Course Title':
        st.session_state.step = 'select_title'
    elif step == 'Customize Outline':
        st.session_state.step = 'customize_outline'
    elif step == 'Generate Content':
        st.session_state.step = 'generate_content'

    if st.session_state.step == 'input':
        st.header("Step 1: Input Course Information")
        st.session_state.course_info['profession'] = st.text_input("What is your profession?", value=st.session_state.course_info['profession'])
        st.session_state.course_info['target_audience'] = st.text_input("Who is your target audience?", value=st.session_state.course_info['target_audience'])
        st.session_state.course_info['course_content'] = st.text_area("Describe the course content:", value=st.session_state.course_info['course_content'])
        st.session_state.course_info['course_description'] = st.text_area("Provide a brief course description: [opt]", value=st.session_state.course_info['course_description'])

        if st.button("Generate Course Titles"):
            with st.spinner("Generating course titles..."):
                st.session_state.course_titles = generate_course_titles(
                    st.session_state.course_info['profession'],
                    st.session_state.course_info['target_audience'],
                    st.session_state.course_info['course_content'],
                    st.session_state.course_info['course_description']
                )
                st.session_state.step = 'select_title'

    elif st.session_state.step == 'select_title':
        st.header("Step 2: Select Course Title")
        st.write("Choose a course title from the options below:")
        for i, title in enumerate(st.session_state.course_titles):
            if st.button(f"{i+1}. {title}"):
                st.session_state.selected_title = title
                with st.spinner("Generating course outline..."):
                    st.session_state.course_outline = generate_course_outline(
                        title,
                        st.session_state.course_info['profession'],
                        st.session_state.course_info['target_audience'],
                        st.session_state.course_info['course_content'],
                        st.session_state.course_info['course_description']
                    )
                st.session_state.step = 'customize_outline'

    elif st.session_state.step == 'customize_outline':
        st.header("Step 3: Customize Course Outline")
        st.subheader(st.session_state.selected_title)
        st.write("Drag and drop to reorder modules or add your own:")
        
        # Allow user to add custom modules
        new_module = st.text_input("Add a new module:")
        if st.button("Add Module"):
            if new_module:
                st.session_state.course_outline.append(new_module)

        updated_outline = st.session_state.course_outline.copy()
        for i, module in enumerate(st.session_state.course_outline):
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                updated_outline[i] = st.text_input(f"Module {i+1}", value=module, key=f"module_{i}")
            with col2:
                if st.button("🗑️", key=f"delete_{i}"):
                    updated_outline.pop(i)
        
        st.session_state.course_outline = updated_outline

        if st.button("Generate Content for First Module (to generate contents for other modules, subscribe to Pro version)"):
            st.session_state.step = 'generate_content'

    elif st.session_state.step == 'generate_content':
        st.header("Step 4: Generate Content for First Module")
        st.subheader(st.session_state.selected_title)
        st.write(f"First Module: {st.session_state.course_outline[0]}")

        if not st.session_state.module_content:
            with st.spinner("Generating content for the first module..."):
                st.session_state.module_content = generate_module_content(
                    st.session_state.selected_title,
                    st.session_state.course_outline[0],
                    st.session_state.course_info
                )

        st.write("Generated Content:")
        st.write(st.session_state.module_content)

        st.subheader("Audio Processing Options")
        option = st.selectbox(
            "Choose an audio processing option:",
            ["None", "Translation to Hindi", "TTS (Text-to-Speech)"]
        )

        if option == "Translation to Hindi":
            if st.button("Translate to Hindi"):
                with st.spinner("Translating..."):
                    print(st.session_state.module_content)
                    result = perform_translation(st.session_state.module_content)
                    print(result)
                    if result:
                        st.write("Hindi Translation:")
                        st.write(result['translated_text'])
                        st.subheader("Audio Processing Options for Hindi")
                        optionh = st.selectbox(
                            "Text to Speech for Hindi Content:",
                            ["None", "TTS (Hindi-to-Speech)"]
                        )
                        if optionh == "TTS (Hindi-to-Speech)":
                            speakerh = st.selectbox("Choose a speaker:", ["meera", "pavithra", "maitreyi","arvind","amol","amartya"])
                            if st.button("Generate Hindi Speech"):
                                with st.spinner("Generating speech..."):
                                    # print(st.session_state.module_content)
                                    audio_datah = perform_tts(st.session_state.module_content, speakerh)
                                    print(audio_datah)
                                    if audio_datah:
                                        with open("t2sh.wav", "wb") as wav_audioh: 
                                            wav_audioh.write(audio_data)
                                        with open("t2sh.wav", "rb") as wav_audio_file:
                                            audio_bytesh = wav_audio_file.read()
                                        st.audio(audio_bytesh, format="audio/wav")
                                    
                                        # audio_file = "t2s.wav" 
                                        # Audio(audio_file) 
                                        
                                    else:
                                        st.error("Speech generation failed. Please try again.")
                    else:
                        st.error("Translation failed. Please try again.")
                    
                    # st.write("Hindi Translation:", result)

                    # st.write("Hindi Translation:", result['translated_text'])

       
        elif option == "TTS (Text-to-Speech)":
            speaker = st.selectbox("Choose a speaker:", ["meera", "pavithra", "maitreyi","arvind","amol","amartya"])
            if st.button("Generate Speech"):
                with st.spinner("Generating speech..."):
                    # print(st.session_state.module_content)
                    audio_data = perform_tts(st.session_state.module_content, speaker)
                    print(audio_data)
                    if audio_data:
                        with open("t2s.wav", "wb") as wav_audio: 
                            wav_audio.write(audio_data)
                        with open("t2s.wav", "rb") as wav_audio_file:
                            audio_bytes = wav_audio_file.read()
                        st.audio(audio_bytes, format="audio/wav")
                       
                        # audio_file = "t2s.wav" 
                        # Audio(audio_file) 
                        
                    else:
                        st.error("Speech generation failed. Please try again.")

if __name__ == "__main__":
    main()

