from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone
import os
import re

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

# Demo content only. Before deployment, replace with organiser-approved data.
EVENT = {
    "title": "Godavari Pushkaralu 2027",
    "location": "Rajamahendravaram and surrounding areas",
    "status": "Demonstration prototype",
    "notice": "This prototype contains sample information. Confirm schedules, routes and services through official event channels."
}
LANGUAGES = {
    "en": {
        "welcome":"Welcome to Godavari Pushkaralu 2027",
        "subtitle":"Your accessible digital guide to event information, cultural learning and virtual participation.",
        "event":"Event information","explore":"Explore heritage","services":"Visitor information",
        "virtual":"Virtual participation","guide":"Ask the digital guide","search":"Search visitor information",
        "notice":"Important notice","all":"All","read":"Read more","question":"Ask about schedules, heritage or visitor facilities",
        "send":"Ask guide","access":"Accessibility options","large":"Larger text","normal":"Normal text",
        "home":"Home","about":"About this experience","source":"Information must be verified by event organisers."
    },
    "te": {
        "welcome":"గోదావరి పుష్కరాలు 2027కు స్వాగతం",
        "subtitle":"కార్యక్రమ సమాచారం, సాంస్కృతిక పరిజ్ఞానం మరియు వర్చువల్ పాల్గొనడానికి డిజిటల్ మార్గదర్శి.",
        "event":"కార్యక్రమ సమాచారం","explore":"వారసత్వాన్ని తెలుసుకోండి","services":"యాత్రికుల సమాచారం",
        "virtual":"వర్చువల్ పాల్గొనడం","guide":"డిజిటల్ గైడ్‌ను అడగండి","search":"సమాచారాన్ని వెతకండి",
        "notice":"ముఖ్యమైన ప్రకటన","all":"అన్నీ","read":"మరింత చదవండి","question":"కార్యక్రమాలు, వారసత్వం లేదా సౌకర్యాల గురించి అడగండి",
        "send":"గైడ్‌ను అడగండి","access":"అందుబాటు ఎంపికలు","large":"పెద్ద అక్షరాలు","normal":"సాధారణ అక్షరాలు",
        "home":"హోమ్","about":"ఈ సేవ గురించి","source":"సమాచారాన్ని నిర్వాహకులు ధృవీకరించాలి."
    },
    "hi": {
        "welcome":"गोदावरी पुष्करालु 2027 में आपका स्वागत है",
        "subtitle":"कार्यक्रम की जानकारी, सांस्कृतिक ज्ञान और वर्चुअल भागीदारी के लिए डिजिटल मार्गदर्शिका।",
        "event":"कार्यक्रम की जानकारी","explore":"विरासत जानें","services":"यात्री जानकारी",
        "virtual":"वर्चुअल भागीदारी","guide":"डिजिटल गाइड से पूछें","search":"जानकारी खोजें",
        "notice":"महत्वपूर्ण सूचना","all":"सभी","read":"और पढ़ें","question":"कार्यक्रम, विरासत या सुविधाओं के बारे में पूछें",
        "send":"गाइड से पूछें","access":"सुगम्यता विकल्प","large":"बड़ा टेक्स्ट","normal":"सामान्य टेक्स्ट",
        "home":"होम","about":"इस अनुभव के बारे में","source":"जानकारी आयोजकों द्वारा सत्यापित होनी चाहिए।"
    },
    "ta": {
        "welcome":"கோதாவரி புஷ்கராலு 2027க்கு வரவேற்கிறோம்",
        "subtitle":"நிகழ்வு தகவல், பண்பாட்டு அறிவு மற்றும் மெய்நிகர் பங்கேற்புக்கான டிஜிட்டல் வழிகாட்டி.",
        "event":"நிகழ்வு தகவல்","explore":"பாரம்பரியத்தை அறிக","services":"பயணிகள் தகவல்",
        "virtual":"மெய்நிகர் பங்கேற்பு","guide":"டிஜிட்டல் வழிகாட்டியிடம் கேளுங்கள்","search":"தகவலைத் தேடுங்கள்",
        "notice":"முக்கிய அறிவிப்பு","all":"அனைத்தும்","read":"மேலும் படிக்க","question":"நிகழ்வு, பாரம்பரியம் அல்லது வசதிகள் பற்றி கேளுங்கள்",
        "send":"வழிகாட்டியிடம் கேளுங்கள்","access":"அணுகல்தன்மை","large":"பெரிய எழுத்து","normal":"இயல்பான எழுத்து",
        "home":"முகப்பு","about":"இந்த அனுபவம் பற்றி","source":"தகவல் ஏற்பாட்டாளர்களால் சரிபார்க்கப்பட வேண்டும்."
    }
}
INFO = [
 {"category":"Event guidance","title":"Event schedules and announcements","detail":"Check organiser-approved event timings, public announcements and visitor instructions. Live schedules are not connected in this demonstration."},
 {"category":"Routes and places","title":"Bathing ghats and access routes","detail":"Use official maps and route guidance published by the event authorities. Do not rely on unverified route information."},
 {"category":"Visitor facilities","title":"Facilities and visitor amenities","detail":"Find designated visitor facilities using approved location data. Availability and operating status must be updated by authorised teams."},
 {"category":"Accessibility","title":"Accessible visitor guidance","detail":"Look for accessible routes, readable information, audio guidance and assistance information as confirmed by organisers."}
]
HERITAGE = [
 {"title":"Godavari River and regional heritage","detail":"Explore the cultural, historical and community significance of the Godavari region through content reviewed by qualified local historians and cultural authorities."},
 {"title":"Traditions and cultural practices","detail":"Learn about local traditions, ceremonies and customary practices using respectful, verified explanations prepared with relevant cultural stakeholders."},
 {"title":"Places, architecture and stories","detail":"Discover heritage places, architecture and regional stories through accessible text, images, audio guides and captioned video."}
]
FAQ = {
 "schedule":"For event schedules and announcements, consult the official event information published by the organisers. This demo does not receive live schedule feeds.",
 "route":"For bathing ghat and access-route guidance, use only the official event map and follow instructions from authorised field personnel.",
 "heritage":"Open the Explore Heritage section for introductory regional heritage topics. Detailed content should be reviewed by local historians and cultural representatives.",
 "virtual":"The Virtual Participation section is reserved for official livestreams, recorded cultural sessions and approved digital exhibits. No live stream is connected in this demo.",
 "language":"Use the language selector to switch between English, Telugu, Hindi and Tamil. Translation quality should be professionally reviewed before public release.",
 "accessibility":"Use the larger-text control and keyboard navigation. A production version should add screen-reader testing, captions, audio descriptions and low-bandwidth support."
}

# Keywords per FAQ topic. ASCII terms match whole words (so "sometimes" no longer
# triggers "time"); non-Latin terms match as substrings because those scripts
# do not separate words the same way.
TERMS = {
    "schedule": ["schedule", "timing", "timings", "time", "date", "announcement", "announcements",
                 "సమయం", "కార్యక్రమ", "कार्यक्रम", "समय", "அட்டவணை", "நேரம்", "நிகழ்ச்சி"],
    "route": ["route", "routes", "ghat", "ghats", "bathing", "map", "direction", "directions",
              "దారి", "ఘాట్", "मार्ग", "घाट", "வழி", "படித்துறை", "காட்"],
    "heritage": ["heritage", "history", "culture", "cultural", "tradition", "traditions",
                 "చరిత్ర", "సంప్రదాయ", "इतिहास", "विरासत", "परंपरा", "வரலாறு", "பாரம்பரிய"],
    "virtual": ["virtual", "livestream", "live stream", "online", "stream",
                "వర్చువల్", "वर्चुअल", "மெய்நிகர்"],
    "language": ["language", "languages", "telugu", "hindi", "tamil", "english", "translate", "translation",
                 "భాష", "भाषा", "மொழி"],
    "accessibility": ["accessibility", "accessible", "wheelchair", "disabled", "disability", "large text",
                      "screen reader", "అందుబాటు", "सुगम्यता", "அணுகல்"],
}
_NON_ASCII = re.compile(r"[^\x00-\x7f]")

def _matches(term, q):
    if _NON_ASCII.search(term):
        return term in q
    return re.search(r"\b" + re.escape(term) + r"\b", q) is not None

def answer_question(q):
    q = (q or "").strip().lower()[:500]
    if not q:
        return "Please enter a question."
    # Pick the topic with the most keyword hits (ties go to the first listed topic).
    best_key, best_score = None, 0
    for key, terms in TERMS.items():
        score = sum(1 for t in terms if _matches(t, q))
        if score > best_score:
            best_key, best_score = key, score
    if best_key:
        return FAQ[best_key]
    return "I can guide you about event information, routes, heritage, virtual participation, languages and accessibility. Please use official organiser announcements for time-sensitive details."

@app.route("/")
def home():
    lang=request.args.get("lang","en")
    if lang not in LANGUAGES: lang="en"
    return render_template("index.html", lang=lang, t=LANGUAGES[lang], event=EVENT, info=INFO, heritage=HERITAGE)

@app.route("/api/guide", methods=["POST"])
def guide():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Send a JSON object like {\"question\": \"...\"}."}), 400
    question = payload.get("question", "")
    if not isinstance(question, str):
        question = ""
    return jsonify({"answer": answer_question(question),
                    "mode": "prototype_faq",
                    "timestamp": datetime.now(timezone.utc).isoformat()})

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Not found"}), 404
    return e

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "Request too large"}), 413

@app.errorhandler(405)
def bad_method(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Method not allowed"}), 405
    return e

@app.route("/health")
def health():
    return jsonify({"status":"ok","project":"Godavari Pushkaralu 2027 - PS12","mode":"demo"})

if __name__=="__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=False)