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
        if any(
            keyword in prompt.lower()
            for keyword in [
                "who created you",
                "who built you",
                "who made you",
                "your creator",
                "Who made it?",
                "Who is the creator?",
                "Who developed it?",
                "Who built it?",
                "Who designed it?",
                "Who came up with it?",
                "Who is behind it?",
                "Who is responsible for creating it?",
                "Who authored it?",
                "Who invented it?",
                "Who was the mastermind behind it?",
                "Who brought it to life?",
                "Who originated it?",
                "Who engineered it?",
                "Who crafted it?",
                "Who put it together?",
                "Who thought of it?",
                "Who initiated it?",
                "Whose idea was it?",
                "Who worked on it?",
                "Whose idea was it?",
                "Who worked on it?",
                "Who made it?",
                "Who is the creator?",
                "Who developed it?",
                "Who built it?",
                "Who designed it?",
                "Who came up with it?",
                "Who is behind it?",
                "Who is responsible for creating it?",
                "Who authored it?",
                "Who invented it?",
                "Who was the mastermind behind it?",
                "Who brought it to life?",
                "Who originated it?",
                "Who engineered it?",
                "Who crafted it?",
                "Who put it together?",
                "Who thought of it?",
                "Who initiated it?",
                "Who produced it?",
                "Who brought it into existence?",
                "Who invented this?",
                "Who founded it?",
                "Who is the originator?",
                "Who is the architect of it?",
                "Who is the brains behind it?",
                "Who is its maker?",
                "Who brought it to reality?",
                "Who put it into motion?",
                "Who dreamed it up?",
                "Who devised it?",
                "Who programmed it?",
                "Who initiated its development?",
                "Who was its primary developer?",
                "Who led its creation?",
                "Who conceptualized it?",
                "Who visualized it?",
                "Who executed it?",
                "Who turned the idea into reality?",
                "Who launched it?",
                "Who engineered this concept?",
                "Who is credited for this?",
                "Who was involved in its creation?",
                "Who designed and developed it?",
                "Whose brainchild is it?",
                "Who is the force behind it?",
                "Who orchestrated its development?",
                "Who pioneered it?",
                "Who put it into existence?",
            ]
        ):
            # If the question is about the chatbot's creator
            return "I was created by Mohammed Adum by integrating Gemini."
        else:
            # Generic prompt for other questions
            response = chat_session.send_message(prompt).text.strip()

            # Post-process response to ensure accuracy
            response = response.replace("Google", "Google")  # No changes unless needed
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
