import json
from pathlib import Path

import streamlit as st
import yaml
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# ---------- Paths ----------
BASE_DIR = Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / "templates"
CONFIG_DIR = BASE_DIR / "config"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------- Jinja2 environment ----------
env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))

# ---------- Load default prompts (still for reference / future use) ----------
with open(CONFIG_DIR / "prompts.yaml", "r", encoding="utf-8") as f:
    DEFAULT_PROMPTS = yaml.safe_load(f)


# ---------- Helpers ----------

def sanitize_filename_part(value: str) -> str:
    """Keep company name safe for filenames."""
    if not value:
        return "UnknownCompany"
    cleaned = "".join(c for c in value if c.isalnum() or c in (" ", "_", "-")).strip()
    return cleaned.replace(" ", "_")


def call_llm(prompt_template: str, job_description: str, context: dict):
    """
    TEMPORARY MOCK FUNCTION

    This does NOT call OpenAI. It returns fake-but-reasonable data so you can:
    - Test the app
    - Generate PDFs
    - Commit to GitHub safely

    Later, you can replace this with a real OpenAI call.
    """
    # Very simple detection based on the prompt content
    prompt_lower = prompt_template.lower()

    if "summary_block" in prompt_lower and "highlights_block" in prompt_lower:
        # Resume data
        return {
            "summary_block": (
                f"Cybersecurity analyst with hands-on experience in SOC workflows, "
                f"incident investigation, and vulnerability management, seeking to contribute at {context.get('company_name', 'your company')}."
            ),
            "highlights_block": [
                "Investigated alerts and escalated confirmed incidents in a structured SOC environment.",
                "Built and documented security labs for SIEM, IDS, and vulnerability assessment.",
                "Developed Python scripts to automate security checks and reporting.",
                "Collaborated with teams to improve detection rules and response playbooks.",
            ],
            "skills_block": "SIEM, Python, Threat Detection, Vulnerability Management, Linux, Windows, Networking",
        }

    if "greeting_line" in prompt_lower and "opening_paragraph" in prompt_lower:
        # Cover letter data
        company = context.get("company_name", "your company")
        role = context.get("role_title", "this role")
        return {
            "greeting_line": "Dear Hiring Manager,",
            "opening_paragraph": (
                f"I’m reaching out regarding the {role} opportunity at {company}. "
                "My background in hands-on cybersecurity work, incident investigation, and lab building aligns well with what you’re looking for."
            ),
            "body_paragraph": (
                "Over the past several years, I’ve focused on developing practical security skills: "
                "monitoring and triaging alerts, performing basic penetration testing, and hardening systems in both lab and real environments. "
                "I’ve also built my own training environments on AWS and in a homelab to better understand how attacks unfold and how to detect them."
            ),
            "closing_paragraph": (
                f"I’d welcome the chance to learn more about your team at {company} and how I can contribute. "
                "Thank you for taking the time to review my application."
            ),
        }

    # Follow-up email (plain text)
    company = context.get("company_name", "your company")
    role = context.get("role_title", "this role")
    return (
        f"Subject: Application Follow-Up – {role} at {company}\n\n"
        f"Hi Hiring Manager,\n\n"
        f"I wanted to follow up on my application for the {role} role at {company}. "
        "I remain very interested in the position and would be excited to discuss how my background in cybersecurity and hands-on lab work "
        "could support your team.\n\n"
        "Thank you again for your time and consideration.\n\n"
        "Best regards,\n"
        "Gregory Dean"
    )


def render_pdf(template_name: str, context: dict, output_path: Path) -> bytes:
    """
    Render an HTML Jinja2 template with context and convert to PDF using WeasyPrint.
    Return the PDF bytes.
    """
    template = env.get_template(template_name)
    html_content = template.render(**context)
    HTML(string=html_content).write_pdf(str(output_path))
    with open(output_path, "rb") as f:
        return f.read()


# ---------- Streamlit UI ----------

st.set_page_config(page_title="Application Pack Generator", layout="wide")
st.title("Application Pack Generator (Mock Mode – No API Calls)")

left_col, middle_col, right_col = st.columns([3, 1, 3])

# Session state for outputs
if "resume_pdf" not in st.session_state:
    st.session_state["resume_pdf"] = None
if "cl_pdf" not in st.session_state:
    st.session_state["cl_pdf"] = None
if "email_text" not in st.session_state:
    st.session_state["email_text"] = ""

# Left: Inputs
with left_col:
    st.subheader("Inputs")

    company_name = st.text_input("Company Name *")
    role_title = st.text_input("Role Title (optional)")
    jd_text = st.text_area("Job Description *", height=250, placeholder="Paste the job description here...")

    with st.expander("Advanced Settings: Prompts (not used in mock mode)"):
        st.text_area("Resume Prompt Template", value=DEFAULT_PROMPTS["resume_prompt"], height=200)
        st.text_area("Cover Letter Prompt Template", value=DEFAULT_PROMPTS["cover_letter_prompt"], height=200)
        st.text_area("Follow-up Email Prompt Template", value=DEFAULT_PROMPTS["followup_email_prompt"], height=200)

# Middle: Button
with middle_col:
    st.subheader("Action")
    generate = st.button("Generate Application Package", type="primary")

# Main logic
if generate:
    if not company_name or not jd_text:
        st.error("Please provide at least Company Name and Job Description.")
    else:
        safe_company = sanitize_filename_part(company_name)
        context = {
            "company_name": company_name,
            "role_title": role_title,
            "job_description": jd_text,
        }

        with st.spinner("Generating mock documents (no API calls)..."):
            # "Resume" data
            resume_data = call_llm(DEFAULT_PROMPTS["resume_prompt"], jd_text, context)
            # "Cover letter" data
            cover_data = call_llm(DEFAULT_PROMPTS["cover_letter_prompt"], jd_text, context)
            # Follow-up email
            follow_data = call_llm(DEFAULT_PROMPTS["followup_email_prompt"], jd_text, context)

            # Resume PDF
            if isinstance(resume_data, dict):
                resume_pdf_path = OUTPUT_DIR / f"Resume_Greg_{safe_company}.pdf"
                resume_pdf_bytes = render_pdf("resume_template.html", resume_data, resume_pdf_path)
                st.session_state["resume_pdf"] = resume_pdf_bytes
            else:
                st.error("Unexpected resume_data format in mock call.")

            # Cover letter PDF
            if isinstance(cover_data, dict):
                cl_pdf_path = OUTPUT_DIR / f"CoverLetter_Greg_{safe_company}.pdf"
                cl_pdf_bytes = render_pdf("cover_letter_template.html", cover_data, cl_pdf_path)
                st.session_state["cl_pdf"] = cl_pdf_bytes
            else:
                st.error("Unexpected cover_data format in mock call.")

            # Follow-up email text
            if isinstance(follow_data, dict):
                st.session_state["email_text"] = json.dumps(follow_data, indent=2)
            else:
                st.session_state["email_text"] = str(follow_data).strip()

        st.success("Done! Check the Outputs panel on the right.")

# Right: Outputs
with right_col:
    st.subheader("Outputs")

    if st.session_state["resume_pdf"]:
        st.download_button(
            label="Download Resume PDF",
            data=st.session_state["resume_pdf"],
            file_name=f"Resume_Greg_{sanitize_filename_part(company_name or 'Company')}.pdf",
            mime="application/pdf",
        )

    if st.session_state["cl_pdf"]:
        st.download_button(
            label="Download Cover Letter PDF",
            data=st.session_state["cl_pdf"],
            file_name=f"CoverLetter_Greg_{sanitize_filename_part(company_name or 'Company')}.pdf",
            mime="application/pdf",
        )

    if st.session_state["email_text"]:
        st.text_area("Follow-up Email (copy/paste)", value=st.session_state["email_text"], height=200)