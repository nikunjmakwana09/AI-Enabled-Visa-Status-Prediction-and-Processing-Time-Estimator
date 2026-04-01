import os
from google import genai
from dotenv import load_dotenv
import streamlit as st
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

# Configure API
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found. Check .env configuration.")

client = genai.Client(api_key=API_KEY)


@st.cache_data(ttl=86400)
def generate_embassy_report(office_name, office_code, region, predicted_days):

    try:

        prompt = f"""
SYSTEM ROLE:
You are a professional visa advisory assistant helping applicants understand
visa processing timelines and embassy services.

Your responses must be accurate, professional, and easy for applicants to understand.

----------------------------------------

TASK:
Generate a helpful embassy intelligence report for visa applicants.

The goal is to help applicants understand:
- embassy contact information
- visa processing expectations
- possible delay reasons
- helpful guidance

----------------------------------------

DATA INPUT:

Embassy Name: {office_name}
Embassy Code: {office_code}
Region: {region}
AI Estimated Processing Time: {predicted_days} days

----------------------------------------

OUTPUT FORMAT:

Return the response using the following sections.

### Embassy Overview
Provide a short description of the embassy and its visa services.

### Embassy Contact Information
Address:
Phone:
Email:
Official Website:
(CRITICAL RULE: If you do not know the EXACT official phone number or email, output "Please refer to the official embassy website" instead of guessing.)

### Visa Processing Insights
Explain possible reasons for the estimated processing time.

### Expected Delay Risk
Classify as:
Low / Moderate / High

Explain briefly.

### Practical Guidance for Applicants
Provide 3-5 clear recommendations.

### Helpful Tips
Provide additional advice to help applicants avoid delays.

----------------------------------------

WRITING STYLE:

• Professional but easy to understand
• Avoid technical AI or ML language
• Write for visa applicants
• Use bullet points where appropriate
• Keep the report concise but informative
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response.candidates:
            report = response.candidates[0].content.parts[0].text
            return report

        else:
            raise ValueError("Empty response from Gemini")

    except Exception as e:

        logging.error(f"Gemini API error for {office_code}: {e}")

        fallback_report = f"""
### AI Insight Temporarily Unavailable

**Embassy:** {office_name}  
**Estimated Processing Time:** {predicted_days} days  

The AI advisory system is currently unavailable.

You can still rely on the estimated processing time shown above.  
Please try again later for detailed embassy insights.
"""
        return fallback_report.strip()
