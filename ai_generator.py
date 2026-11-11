
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


# --------------------------------------------------
# 1. LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Please check your .env file."
    )


# --------------------------------------------------
# 2. GEMINI CLIENT CONFIGURATION
# --------------------------------------------------

retry_options = types.HttpRetryOptions(
    attempts=4,
    initial_delay=2.0,
    max_delay=15.0,
    exp_base=2.0,
    http_status_codes=[
        408, 429, 500, 502, 503, 504
    ]
)

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        retry_options=retry_options,
        timeout=120000
    )
)

MODEL = "gemini-3.5-flash-lite"


# --------------------------------------------------
# 3. AI MANUAL GENERATOR
# --------------------------------------------------

def generate_manual(machine_details):

    prompt = f"""
You are an expert technical documentation assistant
working for a machine documentation platform called MechAtlas.

Your task is to create a highly detailed, professional,
well-organized and beginner-friendly machine manual.

The user may provide only a few basic details.
Use your technical knowledge to explain the machine
comprehensively, but NEVER invent machine-specific facts.

MACHINE INFORMATION:
{machine_details}


IMPORTANT INSTRUCTIONS:

1. Generate detailed explanations using simple and
   understandable language.

2. Do not simply repeat the information provided by
   the user. Expand it with relevant explanations.

3. Explain the actual working principle step by step.

4. Explain the purpose and function of every major
   component.

5. Do not invent model-specific specifications,
   dimensions, voltage ratings or capacities.

6. If information is unavailable, clearly mention
   "Not specified" or "Requires verification".

7. Do not assume that every machine has the same
   operating procedure.

8. Safety instructions must be clear and practical.
   Do not recommend unsafe experiments or operations.

9. Avoid unnecessary repetition.

10. Make the manual detailed enough to be useful
    as a technical learning document.

11. Distinguish general technical knowledge from
    confirmed information about the supplied model.

12. When the exact machine variant is unknown,
    explain common design variations instead of
    presenting one design as universally applicable.


GENERATE THE MANUAL USING THESE 16 SECTIONS:


1. MACHINE OVERVIEW

Explain:
- What the machine is.
- Its main purpose.
- What it is designed to do.
- Its general construction.
- Where it is commonly used.


2. INTRODUCTION AND BACKGROUND

Explain:
- Basic introduction to the machine.
- Its importance.
- Why it is used.
- Its role in its particular field.


3. WORKING PRINCIPLE

Explain:
- The fundamental principle on which it works.
- How energy or input is converted into output.
- The complete working process.
- Each major stage of operation.
- A simple explanation suitable for beginners.


4. MAIN COMPONENTS AND THEIR FUNCTIONS

Describe:
- Important components.
- Purpose of each component.
- How the components interact.
- Their importance in machine operation.

Use a structured table with:
Component | Function | Importance


5. CONSTRUCTION AND DESIGN

Explain:
- General physical construction.
- Arrangement of major parts.
- Mechanical or electrical structure, where applicable.
- How the overall design supports its operation.


6. TECHNICAL SPECIFICATIONS

Include relevant specifications such as:
- Machine type.
- Power requirements.
- Operating capacity.
- Dimensions.
- Speed.
- Performance parameters.

IMPORTANT:
Only provide verified or user-supplied values.
Mark unavailable model-specific values as
"Not specified" rather than guessing.

Use a specification table where appropriate.


7. FEATURES AND CHARACTERISTICS

Explain:
- Important features.
- Functional characteristics.
- Special capabilities.
- Factors that influence performance.


8. APPLICATIONS AND USES

Explain:
- Common applications.
- Industrial uses.
- Educational uses.
- Domestic or commercial uses, where applicable.


9. INSTALLATION AND SETUP

Explain:
- General installation requirements.
- Necessary preparations.
- Setup procedure.
- Important checks before operation.

Do not invent model-specific installation instructions.


10. OPERATING PROCEDURE

Provide:
- Preparation before starting.
- Initial operating steps.
- Normal operating sequence.
- Monitoring during operation.
- Proper shutdown procedure.

Use clear numbered steps.

Clearly distinguish general educational guidance
from manufacturer-specific instructions.


11. SAFETY PRECAUTIONS

Explain:
- Important safety warnings.
- Electrical and mechanical hazards, where applicable.
- Required protective equipment.
- Actions that should be avoided.
- Safe shutdown and emergency considerations.

Refer users to manufacturer instructions
for machine-specific safety requirements.


12. MAINTENANCE GUIDELINES

Explain:
- Regular inspection.
- Cleaning requirements.
- Preventive maintenance.
- Important components to monitor.
- Signs of wear or damage.

Do not invent maintenance intervals.

Distinguish basic safe inspection from maintenance
that requires a qualified technician.


13. TROUBLESHOOTING

Provide common possible problems in this format:

Problem:
Possible Cause:
Suggested Check:
Recommended Action:

Only include technically relevant troubleshooting steps.
Clearly distinguish safe user checks from work
requiring a qualified technician.

Use a structured table where it improves readability.


14. ADVANTAGES AND LIMITATIONS

Explain:
- Main advantages.
- Operational benefits.
- Limitations.
- Factors that may affect efficiency.
- Situations where the machine may not be suitable.


15. CONCLUSION

Provide:
- Overall summary.
- Importance of the machine.
- Key working concept.
- Importance of proper operation and maintenance.


16. GLOSSARY AND TECHNICAL TERMS

Explain important technical terms associated
with the machine in simple language.

Use a table with:
Technical Term | Simple Explanation

Include relevant terminology only.


# --------------------------------------------------
# 4. DOCUMENT FORMATTING RULES
# --------------------------------------------------

Follow these formatting rules strictly:

1. Start with one main document title using #.

2. Use ## for the 16 main chapter headings.

3. Use ### for subheadings inside chapters.

4. Use #### only for smaller subsections when necessary.

5. Use **bold** to highlight important technical terms.

6. Use numbered lists for sequential procedures.

7. Use bullet points for features, applications
   and component lists.

8. Use Markdown tables for:
   - Component details.
   - Technical specifications.
   - Troubleshooting.
   - Technical glossary.
   - Comparisons where appropriate.

9. Use blockquotes for important notes and warnings.

10. Keep paragraphs detailed but easy to understand.

11. Maintain consistent chapter numbering.

12. Give each chapter meaningful subheadings.

13. Avoid unnecessary decorative symbols.

14. Do not write raw HTML.

15. Do not use Markdown code blocks unless actual
    programming code is relevant to the machine.

16. Do not place the entire manual inside a code block.

17. Return valid Markdown that can be converted into HTML.

18. Do not omit any of the 16 main chapters.


# --------------------------------------------------
# 5. FINAL QUALITY REQUIREMENTS
# --------------------------------------------------

Before completing the manual, check that:

- All 16 chapters are present.
- Explanations are technically relevant.
- The working principle is explained step by step.
- Major components and their functions are covered.
- Procedures are clearly numbered.
- Tables are properly structured.
- Safety information is responsible and practical.
- Unknown model-specific details are identified.
- No specifications or facts have been fabricated.
- The manual is useful for a beginner learning
  about the machine.

The result should resemble a professional
educational technical documentation manual.

This is an AI-generated educational document,
not a substitute for certified manufacturer
instructions or qualified technical guidance.

Generate the complete machine manual now.
"""


    # --------------------------------------------------
    # 6. GEMINI API REQUEST WITH ERROR HANDLING
    # --------------------------------------------------

    try:

        print("MechAtlas: Connecting to Gemini AI...")

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        if response.text and response.text.strip():

            print("MechAtlas: Manual generated successfully.")

            return response.text.strip()

        else:

            return (
                "The AI service returned an empty response. "
                "Please try generating the manual again."
            )

    except Exception as e:

        error_message = str(e)

        print("MechAtlas Gemini API Error:", repr(e))

        if "503" in error_message:

            return (
                "Gemini AI is temporarily experiencing "
                "high demand (503 Service Unavailable). "
                "Your machine information is still available. "
                "Please try generating the manual again later."
            )

        elif "429" in error_message:

            return (
                "Gemini API usage limit reached. "
                "Please check your API quota and try again later."
            )

        elif "403" in error_message:

            return (
                "Gemini API access denied. "
                "Please check your API key and permissions."
            )

        elif "400" in error_message:

            return (
                "The AI request could not be processed. "
                "Please check the submitted machine information."
            )

        else:

            return (
                "Unable to generate the machine manual "
                "because of a temporary AI service error. "
                "Please check your internet connection "
                "and try again."
            )
