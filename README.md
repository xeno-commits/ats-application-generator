# ATS Application Generator (Mock Mode)

A local desktop web application built with Python and Streamlit that generates:

- A tailored resume (PDF)
- A tailored cover letter (PDF)
- A formal follow-up email

This project is designed to automate and streamline the job application process by dynamically adapting documents to a pasted job description.

---

## 🚀 Current Status

**Mock Mode Enabled**

This version does NOT make real OpenAI API calls.  
It generates structured mock content so the full application workflow can be tested without API billing.

The OpenAI integration can be restored later by re-enabling the LLM call logic.

---

## 🏗️ Architecture

- **Frontend / UI**: Streamlit
- **Templating Engine**: Jinja2
- **PDF Rendering**: WeasyPrint (HTML → PDF)
- **Prompt Storage**: YAML configuration
- **Execution Environment**: Local Windows 11 + Python venv

Flow:

1. User inputs:
   - Company name
   - Role title (optional)
   - Job description
2. Mock LLM function generates structured data
3. Jinja2 injects data into HTML templates
4. WeasyPrint renders formatted PDFs
5. User downloads:
   - Resume PDF
   - Cover Letter PDF
   - Follow-up email text

---

## 📁 Project Structure

ats-tool/

│

├── app.py

├── requirements.txt

├── .gitignore

│

├── templates/

│ ├── resume_template.html

│ └── cover_letter_template.html

│

├── config/

│ └── prompts.yaml

│

└── output/

---

## 🖥️ How To Run Locally

```bash
### 1️⃣ Create Virtual Environment
python -m venv .venv

2️⃣ Activate (Windows PowerShell)
.\.venv\Scripts\Activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Streamlit
streamlit run app.py

App will open at:
http://localhost:8501
```
---

## 🧠 How It Works (Mock Mode)

**The call_llm() function currently returns structured mock content instead of calling OpenAI.**

**This allows:**
- UI testing
- PDF generation testing
- GitHub-safe publishing
-  Zero API cost

**to enable real LLM integration later:**
- Restore OpenAI client logic
- Add .env with OPENAI_API_KEY
- Re-enable model calls inside call_llm()
---

## 🔒 Security Notes

**The following are excluded via .gitignore:**
- .venv/
- .env
- output/
- Python cache files
- Never commit API keys to GitHub.
---

## 📌 Future Improvements
- Real OpenAI API integration
- ATS keyword extraction logic
- Automatic skill matching
- Role-based resume profile selector
- Deployment version (optional cloud hosting)
- Enhanced UI styling
- Versioned document history
---

## 🎯 Purpose

**This tool was built to:**
- Automate repetitive application customization
- Maintain consistent formatting across documents
- Improve ATS keyword alignment
- Reduce manual editing time
