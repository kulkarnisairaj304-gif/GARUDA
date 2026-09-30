# Garuda Frontend Prototype

React + TypeScript + Tailwind prototype aligned with the current FastAPI backend.

## Run
npm install
npm run dev

FastAPI is expected at http://127.0.0.1:8000.

The Phishing Detection page calls POST /phishing/analyze and uses the current response fields: classification, risk_score, confidence, ai_probability, rule_score and reasons.

This is intentionally a prototype: dashboard/project/application/scan data is mocked, while phishing analysis is wired to the real backend.
