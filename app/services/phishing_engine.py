"""
Phishing Detection Engine

Combines rule-based phishing detection
with the trained machine learning model.
"""

import re
from urllib.parse import urlparse

from app.ai.phishing_predictor import predict_phishing


class PhishingEngine:

    def analyze(
        self,
        sender: str,
        subject: str,
        body: str,
        urls: list[str] | None = None,
    ):
        reasons = []
        rule_score = 0

        # ------------------------------------------
        # Combine email text
        # ------------------------------------------

        email_text = (
            f"{subject} {body}"
        ).lower()

        # ------------------------------------------
        # 1. Urgency Detection
        # ------------------------------------------

        urgency_keywords = [
            "urgent",
            "immediately",
            "act now",
            "account suspended",
            "account will be closed",
            "verify now",
            "action required",
            "final warning",
        ]

        urgency_found = [
            keyword
            for keyword in urgency_keywords
            if keyword in email_text
        ]

        if urgency_found:
            rule_score += 20

            reasons.append(
                "Urgency or pressure-based language detected."
            )

        # ------------------------------------------
        # 2. Credential Request Detection
        # ------------------------------------------

        credential_keywords = [
            "password",
            "login",
            "username",
            "verify your account",
            "confirm your account",
            "credentials",
            "sign in",
        ]

        credential_found = [
            keyword
            for keyword in credential_keywords
            if keyword in email_text
        ]

        if credential_found:
            rule_score += 25

            reasons.append(
                "Possible credential or account verification request detected."
            )

        # ------------------------------------------
        # 3. Suspicious URL Detection
        # ------------------------------------------

        if urls:

            for url in urls:

                parsed = urlparse(url)

                domain = parsed.netloc.lower()

                # HTTP instead of HTTPS
                if parsed.scheme.lower() == "http":

                    rule_score += 10

                    reasons.append(
                        f"URL does not use HTTPS: {url}"
                    )

                # IP address instead of domain
                if re.match(
                    r"^\d{1,3}(\.\d{1,3}){3}$",
                    domain,
                ):

                    rule_score += 20

                    reasons.append(
                        f"URL uses an IP address instead of a domain: {url}"
                    )

                # Suspicious URL keywords
                suspicious_url_words = [
                    "login",
                    "verify",
                    "secure",
                    "account",
                    "update",
                    "password",
                ]

                if any(
                    word in domain
                    for word in suspicious_url_words
                ):

                    rule_score += 10

                    reasons.append(
                        f"Suspicious keyword detected in URL domain: {url}"
                    )

        # ------------------------------------------
        # 4. Suspicious Sender Detection
        # ------------------------------------------

        sender_lower = sender.lower()

        suspicious_sender_words = [
            "security",
            "support",
            "admin",
            "verify",
            "account",
        ]

        if any(
            word in sender_lower
            for word in suspicious_sender_words
        ):

            rule_score += 10

            reasons.append(
                "Sender address contains a security-sensitive keyword."
            )

        # ------------------------------------------
        # Limit Rule Score
        # ------------------------------------------

        rule_score = min(
            rule_score,
            100,
        )

        # ------------------------------------------
        # 5. AI Prediction
        # ------------------------------------------

        ai_result = predict_phishing(
            f"{subject} {body}"
        )

        ai_probability = (
            ai_result["phishing_probability"]
        )

        ai_score = ai_probability * 100

        # ------------------------------------------
        # AI Reason
        # ------------------------------------------

        if ai_probability >= 0.70:

            reasons.append(
                f"AI model detected phishing-like email patterns with "
                f"{ai_probability * 100:.2f}% probability."
            )

        elif ai_probability >= 0.40:

            reasons.append(
                f"AI model detected moderately suspicious email patterns "
                f"with {ai_probability * 100:.2f}% probability."
            )

        # ------------------------------------------
        # 6. Combine Rule + AI Scores
        # ------------------------------------------

        risk_score = (
            (rule_score * 0.40)
            + (ai_score * 0.60)
        )

        risk_score = round(
            min(risk_score, 100)
        )

        # ------------------------------------------
        # 7. Final Classification
        # ------------------------------------------

        if risk_score >= 70:

            classification = "Phishing"

        elif risk_score >= 40:

            classification = "Suspicious"

        else:

            classification = "Safe"

        # ------------------------------------------
        # 8. Confidence
        # ------------------------------------------

        confidence = risk_score / 100

        # ------------------------------------------
        # No reasons for safe emails
        # ------------------------------------------

        if not reasons:

            reasons.append(
                "No significant phishing indicators detected."
            )

        # ------------------------------------------
        # Final Result
        # ------------------------------------------

        return {
            "classification": classification,
            "risk_score": risk_score,
            "confidence": confidence,
            "ai_probability": ai_probability,
            "rule_score": rule_score,
            "reasons": reasons,
        }