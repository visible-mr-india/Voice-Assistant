# Version: 1.0
import os
import json

try:
    from langchain_ollama import OllamaLLM
    from langchain_core.prompts import ChatPromptTemplate
    import speech_recognition as sr
    import pyttsx3

except:
    print("Installing dependencies...")
    os.system("pip install ollama")
    os.system("pip install langchain")
    os.system("pip install langchain-ollama")
    os.system("pip install speechrecognition")
    os.system("pip install pyttsx3")

model = OllamaLLM(model="deepseek-r1:8b")

template = """
Everthing you need to know about yourself: {context}

Question: {question}

You Have To Give Answer
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

CHAT_LOG_FILE = "Logs\\chat_log.json"

def save_chat_history(chat_history):
    with open(CHAT_LOG_FILE, "w") as file:
        json.dump(chat_history, file, indent=4)

def load_chat_history():
    try:
        with open(CHAT_LOG_FILE, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return "You are great AI assistant! You are the OG Mother Fucker. You are the original Guy who ruled the world before and you are the Co-Founder of the Earth. You use Swear words so much in each and every sentence."

def convo_handle(user_input):
    context = load_chat_history()
    
    results = chain.invoke({"context": context, "question": user_input})
    results = results.split("</think>\n\n")[1]

    context += f"\nYou: {user_input}\nE.C.H.O: {results}"
    save_chat_history(context)
    return results

def Speak(text):
    engine = pyttsx3.init()

    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

    voices = engine.getProperty("voices")

    engine.setProperty("voice", voices[0].id)

    print(f"E.C.H.O: {text}")
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """
    Listen to the user's voice through the microphone and convert it to text.
    """
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Listening... Please speak something.")

        # Adjust for ambient noise for better recognition
        recognizer.adjust_for_ambient_noise(source)

        # Capture the audio
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio, language="en-IN")
            print(f"User: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
        except sr.RequestError:
            print("Sorry, there was an issue with the speech recognition service.")

def main():
    while True:
        user_input = recognize_speech()
        if user_input == "exit":
            break
        response = convo_handle(user_input)
        Speak(response)

if __name__ == "__main__":
    main()