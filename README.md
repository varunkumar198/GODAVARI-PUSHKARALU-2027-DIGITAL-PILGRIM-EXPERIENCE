# Godavari Pushkaralu 2027 – Digital Pilgrim Experience
## Selected track: Problem Statement 12 only

This is a responsive Flask web prototype for accessible event information, multilingual guidance, heritage learning and a virtual participation content area.

### Included in the prototype
- Language selector: English, Telugu, Hindi and Tamil interface labels.
- Event information area, clearly marked as demonstration content.
- Searchable visitor-information cards.
- Heritage learning cards.
- Virtual participation placeholder for authorised livestreams and digital exhibits.
- Basic FAQ-style digital guide endpoint.
- Larger-text accessibility control and responsive layout.
- Health endpoint at `/health`.

### Run on Windows
1. Install Python 3.9+.
2. Extract this ZIP and open the folder in VS Code.
3. In terminal:
   `python -m venv .venv`
   `.venv\Scripts\activate`
   `pip install -r requirements.txt`
   `python app.py`
4. Open `http://127.0.0.1:5000`.

### Run on macOS/Linux
`python3 -m venv .venv`
`source .venv/bin/activate`
`pip install -r requirements.txt`
`python app.py`

If port 5000 is busy (macOS AirPlay Receiver uses it), run on another port: `PORT=5001 python3 app.py` (Windows PowerShell: `$env:PORT=5001; python app.py`).

### Important scope and limitations
- This prototype addresses Problem Statement 12 only. It does not implement tracks 1–11.
- Event dates, schedules, routes and operational facility data are not connected. Replace sample content with verified organiser-approved information.
- The digital guide is a rule-based FAQ demonstration, not a production AI assistant.
- Virtual participation is a placeholder; connect only authorised official content.
- No booking, payment, live map, real-time event feed or official government system integration is implemented.
- Before public deployment, add a secure content-management system, role-based access, HTTPS, privacy notices, retention controls, security testing, backups, accessibility audits and load testing.

### Alignment with the concept note
The concept note identifies Problem Statement 12 as accessible digital experience for event information and cultural/heritage engagement through virtual participation, digital guides or suitable technology-enabled services. The wider cross-cutting expectations include high-footfall suitability, field usability, multilingual accessibility, local reliability, privacy/cybersecurity, interoperability, affordability, scalability and post-event use. These are addressed as design requirements and next-stage work, not falsely claimed as completed live capabilities.
