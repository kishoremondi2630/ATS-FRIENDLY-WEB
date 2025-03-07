from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import docx2txt
import PyPDF2
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

nlp = spacy.load("en_core_web_sm")  # Load NLP model

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def extract_text_from_resume(file_path):
    if file_path.endswith(".pdf"):
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + " "
        return text
    elif file_path.endswith(".docx"):
        return docx2txt.process(file_path)
    return ""

def calculate_similarity(job_desc, resume_text):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([job_desc, resume_text])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    return round(similarity[0][0] * 100, 2)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "job_desc" not in request.form or "resume" not in request.files:
        return jsonify({"error": "Missing inputs"}), 400

    job_desc = request.form["job_desc"]
    resume = request.files["resume"]

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], resume.filename)
    resume.save(file_path)

    resume_text = extract_text_from_resume(file_path)
    match_percentage = calculate_similarity(job_desc, resume_text)

    return jsonify({"match_percentage": match_percentage})

if __name__ == "__main__":
    app.run(debug=True)
