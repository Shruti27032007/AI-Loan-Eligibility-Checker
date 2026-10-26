# Finova AI — AI Loan Eligibility Checker

A beginner-friendly Flask + HTML/CSS/JavaScript starter for the college project shown in the project brief.

## Features included
- Loan eligibility demo logic
- EMI calculator
- Credit score analyzer
- Claude AI integration point
- Optional Google Sheets webhook
- Responsive dark glassmorphism UI
- Git/deployment friendly structure

## 1. Install Python
Use Python 3.10+.

## 2. Open terminal in this folder
Windows example:
```powershell
cd ai_loan_eligibility_checker
```

## 3. Create a virtual environment
```powershell
python -m venv venv
venv\Scripts\activate
```

## 4. Install packages
```powershell
pip install -r requirements.txt
```

## 5. Create .env
Copy `.env.example` to `.env`.

At first, leave the Claude and Google Sheets values empty. The app will still run.

## 6. Start the website
```powershell
python app.py
```

Open:
http://127.0.0.1:5000

## 7. Claude
Add your Anthropic API key to `.env` and set `ANTHROPIC_MODEL` to a model available in your Anthropic account. Never put the API key inside JavaScript or HTML.

## 8. Google Sheets
For the college demo, create a Google Apps Script Web App that accepts POST JSON and appends selected fields to a spreadsheet. Put its web-app URL in `GOOGLE_SHEETS_WEBHOOK_URL`.

## Important project note
Do not ask users for real bank passwords, OTPs, card CVVs, or other highly sensitive credentials. This is an educational prototype.

## Suggested next upgrades
1. Login/signup
2. Better eligibility rules with explainable factors
3. Credit-score charts
4. Loan comparison
5. Dashboard/history
6. PDF report
7. ML model trained on a public dataset
8. Google Sheets persistence
9. Deployment on Render/another suitable backend host + a frontend host if needed
