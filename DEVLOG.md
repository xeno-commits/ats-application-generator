```markdown
# Dev Log – ATS Application Generator

## Goal

Build a local automation tool that:

- Accepts a job description
- Generates a tailored resume
- Generates a tailored cover letter
- Generates a professional follow-up email
- Exports documents as PDFs

## Phase 1 – Infrastructure

- Created Python virtual environment
- Built Streamlit UI layout
- Implemented HTML + CSS master templates
- Integrated WeasyPrint for PDF generation
- Structured prompt configuration via YAML

## Phase 2 – Mock Mode

- Implemented mock LLM function to simulate API output
- Validated full document generation pipeline
- Added session state management
- Implemented two separate PDF download buttons
- Implemented copy-paste follow-up email output

## Next Phase

- Restore OpenAI API integration
- Implement ATS keyword extraction
- Improve formatting precision
- Add job-role profile selector
- Add document version history
