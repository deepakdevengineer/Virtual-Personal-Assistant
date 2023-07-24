import openai
import speech_recognition as sr

# Set up your API key
openai.api_key = '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'

def capture_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that. Please try again.")
        return None


def generate_chat_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024
    )
    generated_text = response['choices'][0]['text']
    return generated_text

def handle_voice_command():
    voice_command = capture_voice()
    if voice_command:
        prompt = f"User: {voice_command}\nChatGPT:"
        generated_text = generate_chat_response(prompt)
        print("ChatGPT: " + generated_text)
        # Perform actions based on generated_text in your virtual assistant logic


if __name__ == "__main__":
    while True:
        handle_voice_command()