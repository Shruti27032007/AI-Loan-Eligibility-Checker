import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def calculate_emi(principal, annual_rate, years):
    months = years * 12
    monthly_rate = annual_rate / 12 / 100
    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = principal * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
    total = emi * months
    interest = total - principal
    return round(emi, 2), round(interest, 2), round(total, 2)

def eligibility(data):
    income = float(data.get("income", 0))
    age = int(data.get("age", 0))
    credit = int(data.get("credit_score", 0))
    employment = data.get("employment", "").lower()

    score = 0
    reasons = []

    if 21 <= age <= 60:
        score += 25
        reasons.append("Age is within the typical working-age range.")
    else:
        reasons.append("Age is outside the demo model's preferred range.")

    if income >= 300000:
        score += 30
        reasons.append("Annual income meets the demo threshold.")
    elif income >= 180000:
        score += 20
        reasons.append("Annual income is moderate.")
    else:
        reasons.append("Annual income is below the demo threshold.")

    if credit >= 750:
        score += 30
        reasons.append("Credit score is strong.")
    elif credit >= 650:
        score += 20
        reasons.append("Credit score is in the moderate range.")
    else:
        reasons.append("Credit score is below the demo preferred range.")

    if employment in {"salaried", "self-employed", "business"}:
        score += 15
        reasons.append("Employment information is provided.")
    else:
        reasons.append("Employment type needs review.")

    eligible = score >= 60
    return {
        "eligible": eligible,
        "score": score,
        "reasons": reasons,
        "disclaimer": "This is an educational/demo eligibility model, not a bank approval decision."
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/eligibility")
def api_eligibility():
    data = request.get_json(force=True)
    return jsonify(eligibility(data))

@app.post("/api/emi")
def api_emi():
    data = request.get_json(force=True)
    principal = float(data.get("principal", 0))
    rate = float(data.get("rate", 0))
    years = int(data.get("years", 1))
    emi, interest, total = calculate_emi(principal, rate, years)
    return jsonify({"emi": emi, "interest": interest, "total": total})

@app.post("/api/credit")
def api_credit():
    data = request.get_json(force=True)
    credit = int(data.get("credit_score", 0))
    if credit >= 750:
        level = "Excellent"
        tips = ["Maintain timely payments.", "Keep credit utilisation low.", "Avoid unnecessary new credit applications."]
    elif credit >= 700:
        level = "Good"
        tips = ["Continue timely payments.", "Keep utilisation controlled.", "Monitor your credit report."]
    elif credit >= 650:
        level = "Fair"
        tips = ["Pay every bill on time.", "Reduce outstanding balances.", "Avoid multiple loan applications in a short period."]
    else:
        level = "Needs Improvement"
        tips = ["Focus on on-time payments.", "Reduce outstanding debt.", "Review your credit report for errors."]
    return jsonify({"level": level, "tips": tips})

@app.post("/api/ai-tips")
def api_ai_tips():
    data = request.get_json(force=True)
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()

    if not api_key:
        return jsonify({
            "source": "demo",
            "message": "Claude API key is not configured yet. The app is running in demo mode.",
            "tips": [
                "Create a realistic monthly budget before taking a loan.",
                "Compare the total repayment amount, not only the EMI.",
                "Maintain an emergency fund before increasing debt."
            ]
        })

    # Claude integration is intentionally isolated here.
    # Set ANTHROPIC_API_KEY and, if needed, update ANTHROPIC_MODEL in .env
    # to a model available to your Anthropic account.
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        model = os.getenv("ANTHROPIC_MODEL", "").strip()
        if not model:
            return jsonify({"source": "config", "message": "Set ANTHROPIC_MODEL in .env to a model available to your account."}), 500

        prompt = f"""
You are a financial education assistant for a student project.
Give short, general educational guidance. Do not claim to approve loans or provide regulated financial advice.
User information:
Income: {data.get('income')}
Age: {data.get('age')}
Credit score: {data.get('credit_score')}
Employment: {data.get('employment')}
Loan amount: {data.get('loan_amount')}
Tenure: {data.get('tenure')}

Return 4 concise bullet points.
"""
        msg = client.messages.create(
            model=model,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        text = "".join(getattr(block, "text", "") for block in msg.content)
        return jsonify({"source": "claude", "message": text})
    except Exception as exc:
        return jsonify({"source": "error", "message": f"Claude request failed: {str(exc)}"}), 500

@app.post("/api/save")
def api_save():
    # Optional Google Sheets webhook. For a college demo, an Apps Script
    # Web App URL can receive this JSON and append it to a Sheet.
    webhook = os.getenv("GOOGLE_SHEETS_WEBHOOK_URL", "").strip()
    data = request.get_json(force=True)
    if not webhook:
        return jsonify({"saved": False, "message": "Google Sheets webhook is not configured. Data was not sent anywhere."})
    try:
        r = requests.post(webhook, json=data, timeout=10)
        return jsonify({"saved": r.ok, "status": r.status_code})
    except Exception as exc:
        return jsonify({"saved": False, "message": str(exc)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG", "0") == "1")
