"""
Scanner Engine

Performs basic security checks on an application.
"""

import requests


class ScannerEngine:

    def run_scan(self, base_url: str):

        results = {
            "target": base_url,
            "checks": [],
        }

        try:

            response = requests.get(
                base_url,
                timeout=10,
                allow_redirects=True,
            )

            # ------------------------------------------
            # HTTP Response Check
            # ------------------------------------------

            results["checks"].append({
                "check": "HTTP Response",
                "status": "Passed",
                "details": f"Application responded with status code {response.status_code}",
            })

            # ------------------------------------------
            # HTTPS Check
            # ------------------------------------------

            if response.url.startswith("https://"):

                results["checks"].append({
                    "check": "HTTPS",
                    "status": "Passed",
                    "details": "Application is using HTTPS.",
                })

            else:

                results["checks"].append({
                    "check": "HTTPS",
                    "status": "Warning",
                    "details": "Application is not using HTTPS.",
                })

            # ------------------------------------------
            # Security Headers
            # ------------------------------------------

            required_headers = [
                "Content-Security-Policy",
                "X-Frame-Options",
                "X-Content-Type-Options",
                "Strict-Transport-Security",
            ]

            for header in required_headers:

                if header in response.headers:

                    results["checks"].append({
                        "check": header,
                        "status": "Passed",
                        "details": "Security header is present.",
                    })

                else:

                    results["checks"].append({
                        "check": header,
                        "status": "Warning",
                        "details": "Security header is missing.",
                    })

            # ------------------------------------------
            # Server Information
            # ------------------------------------------

            server = response.headers.get(
                "Server",
                "Not disclosed",
            )

            results["checks"].append({
                "check": "Server Information",
                "status": "Info",
                "details": f"Server: {server}",
            })

            return results

        except requests.RequestException as e:

            return {
                "target": base_url,
                "checks": [],
                "error": str(e),
            }