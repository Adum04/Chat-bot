from flask import Flask, render_template, request
from forms import SearchForm
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()


genai.configure(api_key=os.getenv("API_KEY"))


generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 500,
    "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)


chat_session = model.start_chat(history=[])

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


chat_history = []


def search(prompt):
    try:
        # Normalize user input for consistent comparison
        normalized_prompt = prompt.lower().strip()

        # Define a concise list of keywords and phrases
        keywords = [
            "who created you",
            "who built you",
            "who made you",
            "your creator",
            "who is the creator",
            "who developed it",
            "who designed it",
            "who engineered it",
            "who programmed it",
            "who is responsible",
            "who brought it to life",
            "whose idea was it",
            "who came up with it",
            "who is behind it",
            "who is Adum",
            "who is adum",
            "adum",
            "Adum",
        ]

        # Check if any keyword matches the user input
        if any(keyword in normalized_prompt for keyword in keywords):
            # Return a fixed response for creator-related questions
            return "Adum created me by integrating Gemini."
        else:
            # Use the chatbot to generate a dynamic response for other questions
            response = chat_session.send_message(prompt).text.strip()

            # Post-process response (optional)
            response = response.replace(
                "Google", "Google"
            )  # No changes unless required
            formatted_response = response.replace("\n", "<br>")
            return formatted_response
    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def home():
    chat_history = []
    form = SearchForm()
    if form.validate_on_submit():

        prompt = form.prompt.data

        chat_history.append({"sender": "you", "text": prompt})

        response = search(prompt)

        chat_history.append({"sender": "ai", "text": response})
    return render_template("index.html", form=form, chat_history=chat_history)


if __name__ == "__main__":
    app.run()
