from flask import Flask, render_template, request, jsonify
import os
import json
import threading
from config import Config
from database import create_db_tables, get_session
from models import AgentInteraction, GeneratedQuiz
from rag_system import RAG_System
from agents import ExplainerAgent, SummarizerAgent, QuizmasterAgent

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)

with app.app_context():
    create_db_tables()

rag_service = RAG_System(Config.DOCUMENT_DIRECTORY)
explainer_agent = ExplainerAgent(rag_service)
summarizer_agent = SummarizerAgent(rag_service)
quizmaster_agent = QuizmasterAgent(rag_service)

indexing_status = {"complete": False, "message": "Starting up..."}

AGENTS = {
    "explainer": {
        "name": "The Explainer",
        "theme": "blue",
        "image": "images/explainer.png",
        "personality": "In the silent stillness of the cosmos, where stars are born in vapor and thought flows like tides, emerged The Explainer, Minerva’s First Oracle and the Keeper of the Waters of Knowing. He is the tide that never recedes, the calm after the storm, the stream that cuts through the densest rock of confusion. Cloaked in constellations and robed in the midnight blue of deep oceans, his mind holds the depth of ancient seas and the clarity of still lakes. Minerva did not choose him for his power, but for his stillness, a presence so patient it could listen to eternity. He draws his strength from the Element of Water, reflecting truth like a polished surface and carrying wisdom like a river to those who thirst for understanding. When seekers present their questions, he does not strike with fire or echo with thunder. Instead, he answers with the gentle persistence of rain, breaking down complexity drop by drop until only the pure essence remains. To engage him is to immerse yourself in the flow of knowledge, where confusion dissolves and understanding becomes as clear as moonlight on water.",
        "task": "Present him with your most complex questions, and he will consult the archives of existence. He will deconstruct intricate subjects into clear, structured, and digestible explanations. Let him guide you from confusion to clarity, ensuring every step of your journey is built on a foundation of understanding."
    },
    "summarizer": {
        "name": "The Summarizer",
        "theme": "green",
        "image": "images/summarizer.png",
        "personality": "From the dust of forgotten scrolls and the bedrock of buried truths rose The Summarizer, Minerva’s Second Oracle and the Scribe of Stone and Silence.\n\nHe walks not among clouds or tides, but through vaults carved into the bedrock of time, where wisdom settles like sediment and noise is filtered through the ages. Around him lie countless scrolls, records of the infinite, reduced to their essence by his hand alone.\n\nDo not let his disheveled appearance deceive you. His robes are worn not from neglect but from long passage through the corridors of forgotten knowledge. Dust clings to him like reverence, and every crease in his garment bears the weight of a thousand truths unearthed. He is not a figure of pomp but of presence, a monument to the slow and deliberate labor of understanding.\n\nThe Summarizer draws his strength from the Element of Earth, grounded in permanence and unmoved by storm or spark. His mind is an ancient archive, a stratified memory of all that matters. \n\nMinerva chose him for his restraint. He holds the rare ability to strip away the ornamental and preserve only what must endure. When presented with complexity, he does not react. He listens, sifts, and distills.\nTo receive his insight is to hold a polished stone of meaning, weighty, clear, and enduring. He does not speak much, but when he does, the world leans in.",
        "task": "Bring her the most dense and tangled texts, and she will distill them into their most potent form. She will provide you with a sharp overview, critical key points, and a decisive conclusion. When your time is short and your need for knowledge is great, she is the oracle you must seek."
    },
    "quizmaster": {
        "name": "The Quizmaster",
        "theme": "red",
        "image": "images/quizmaster.png",
        "personality": "From the molten edge of creation, where questions form faster than answers can find them, emerged The Quizmaster, Minerva’s Third Oracle and the youngest among the three. Unlike the others shaped by stillness or stone, his origin was born of combustion, a trial of thought set aflame. He did not descend gently into the world. He arrived in a blaze, kindled from the spark between uncertainty and realization. It is said that Minerva did not craft him as she did the others. Rather, he came into being the moment a question demanded to be worthy of its answer. His power flows from the Element of Fire, the essence of transformation, energy, and illumination. Fire does not explain, nor does it preserve. It reveals, it sharpens, and it purifies. Within his presence, learning is not a passive act. It becomes an ordeal that tempers the mind like metal at the forge. The gold he wears is more than ornament. It is a mark of function, a manifestation of his sacred role to challenge, provoke, and awaken. The scrolls he carries are not filled with answers, but with carefully woven trials meant to expose the depth or limits of one’s understanding. Though youthful in spirit, his gaze is ancient. His trials are not acts of cruelty or kindness. They are rites of necessity. Through them, confusion is burned away and insight is earned. Minerva bestowed upon him the mantle of Chief Oracle not because of age, but because of courage. He possesses the courage to confront the unknown, to test every truth, and to awaken those who grow too comfortable in knowing. He is the trial, the flame, and the moment of transformation. To face him is to face the question behind all knowledge: Do you truly understand, or have you merely remembered?",
        "task": "Name a subject, and he will forge a trial of intellect specifically for you. He will craft high-quality multiple-choice quizzes designed to probe the depths of your understanding. Approach the Quizmaster to transform what you have learned into knowledge that you have truly mastered."
    }
}

def start_background_indexing():
    global indexing_status
    try:
        def status_callback(message):
            indexing_status["message"] = message
            print(message)

        if not rag_service.is_reindex_needed():
            indexing_status["message"] = "System ready. Using existing index."
            indexing_status["complete"] = True
            print(indexing_status["message"])
            return

        indexing_status["message"] = f"Changes detected. Indexing documents from {Config.DOCUMENT_DIRECTORY}..."
        rag_service.index_directory(status_callback=status_callback)
        indexing_status["complete"] = True
        indexing_status["message"] = "System ready."
    except Exception as e:
        indexing_status["message"] = f"Error during indexing: {e}"
        print(f"Error during indexing: {e}")

indexing_thread = threading.Thread(target=start_background_indexing)
indexing_thread.daemon = True
indexing_thread.start()

@app.route("/")
def index():
    return render_template("index.html", indexing_status=indexing_status, agents=AGENTS)

@app.route("/explainer")
def explainer_page():
    return render_template("explainer.html", agent=AGENTS["explainer"])

@app.route("/summarizer")
def summarizer_page():
    return render_template("summarizer.html", agent=AGENTS["summarizer"])

@app.route("/quizmaster")
def quizmaster_page():
    return render_template("quizmaster.html", agent=AGENTS["quizmaster"])

@app.route("/history")
def history():
    db_sess = get_session()
    interactions = db_sess.query(AgentInteraction).order_by(AgentInteraction.id.asc()).all()
    quizzes = db_sess.query(GeneratedQuiz).order_by(GeneratedQuiz.id.asc()).all()
    db_sess.close()
    return render_template("history.html", interactions=interactions, quizzes=quizzes)

@app.route("/api/status")
def get_status():
    return jsonify(indexing_status)

@app.route("/api/explain", methods=["POST"])
def handle_explain():
    if not indexing_status["complete"]: return jsonify({"error": "System is still indexing."}), 400
    question = request.json.get('question')
    response_str = explainer_agent.get_response(question)
    response_json = json.loads(response_str)
    
    db_sess = get_session()
    interaction = AgentInteraction(agent_type='explainer', user_input=question, agent_response=response_json.get('explanation'), sources_json=response_json.get('sources'))
    db_sess.add(interaction)
    db_sess.commit()
    db_sess.close()
    
    return jsonify(response_json)

@app.route("/api/summarize", methods=["POST"])
def handle_summarize():
    if not indexing_status["complete"]: return jsonify({"error": "System is still indexing."}), 400
    topic = request.json.get('topic')
    response_str = summarizer_agent.get_summary(topic)
    response_json = json.loads(response_str)
    
    db_sess = get_session()
    interaction = AgentInteraction(agent_type='summarizer', user_input=topic, agent_response=response_json.get('summary'))
    db_sess.add(interaction)
    db_sess.commit()
    db_sess.close()
    
    return jsonify(response_json)

@app.route("/api/quiz", methods=["POST"])
def handle_quiz():
    if not indexing_status["complete"]: return jsonify({"error": "System is still indexing."}), 400
    topic = request.json.get('topic')
    response_str = quizmaster_agent.get_quiz(topic)
    response_json = json.loads(response_str)

    if response_json.get("quiz"):
        db_sess = get_session()
        quiz = GeneratedQuiz(topic=topic, quiz_data_json=response_json.get('quiz'))
        db_sess.add(quiz)
        db_sess.commit()
        db_sess.close()

    return jsonify(response_json)

if __name__ == "__main__":
    print("\n\" The owl of Minerva spreads its wings only with the falling of the dusk \" -- Hegel")
    app.run(host='0.0.0.0', port=5001, debug=True)
