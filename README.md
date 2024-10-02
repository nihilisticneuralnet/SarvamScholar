![logo](https://github.com/user-attachments/assets/174ff08d-6a90-4898-b348-6b3b4581be5e)

# SarvamScholar
### *Your Course Content Copilot: Because Teaching Shouldn’t Feel Like Rocket Science!*

This project accelerates course creation by providing AI-powered copilots for translating content, generating voiceovers. By integrating Sarvam and Gemini APIs, it simplifies translation, TTS, and lecture generation, reducing the time to create high-quality online courses. GenAI excels at content generation, personalizing modules, and refining educational experiences through rapid, scalable, and production-grade outputs, making it the ideal solution for this challenge.

## Installation

Follow these steps to set up the project:

1. **Clone the Repository**: Run `git clone https://github.com/nihilisticneuralnet/SarvamScholar.git` to clone the repository to your local machine.

2. **Install Dependencies**: Navigate to the project directory and install the required packages by running `cd <repository-directory>` followed by `pip install -r requirements.txt`. 

3. **Set Up Environment Variables**: In the `.env` file in the project root directory and insert your Gemini and Sarvam API keys as follows:
   ```plaintext
   GEMINI_API_KEY=<your-gemini-api-key>
   SARVAM_API_KEY=<your-sarvam-api-key>
   ```
   Replace `<your-gemini-api-key>` and `<your-sarvam-api-key>` with your actual API keys.

4. **Run the Application**: Finally, run the application using Streamlit by executing `python -m streamlit run app.py`.

Ensure you have all the necessary libraries installed before running these commands.

## Architecture Flow
![architecture_flow](https://github.com/user-attachments/assets/e81002a9-668f-422f-b778-b5866d66b3df)

## Results

### Image Outputs
 1: Input your Course Content | 2. Select Course Title | 3. Customize Course Outlines | 4. Course Content | 5. Hindi Translation of the Content | 
| --- | --- | --- | --- | --- | 
| <img src="img/Screenshot 2024-10-02 231659.png" width="200"/> | <img src="img/Screenshot 2024-10-02 231713.png" width="200"/> | <img src="img/Screenshot 2024-10-02 231723.png" width="200"/> | <img src="img/Screenshot 2024-10-02 231737.png" width="200"/> | <img src="img/Screenshot 2024-10-02 231753.png" width="200"/> | 


### Video Outputs
<video width="640" height="480" controls>
  <source src="img/screen-capture.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
