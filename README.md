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
