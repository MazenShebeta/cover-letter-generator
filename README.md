# 📝 Markdown → PDF Cover Letter Generator

Generate beautiful, consistent cover letters as PDF files from Markdown using a styled HTML template and headless Chrome.

## ✨ Features

- Simple Markdown input with dynamic variable injection from `.env`
- Automatically fills in current date, contact info, and more
- Outputs both `.html` and `.pdf` versions
- Optional custom CSS styling per letter
- Headless Chrome rendering for pixel-perfect PDF output
- CLI with optional Chrome path override

---

## 📦 Requirements

- Python 3.7+
- [Google Chrome](https://www.google.com/chrome/) or [Chromium](https://www.chromium.org/)
- Python packages:
  ```bash
  pip install -r requirements.txt
  ```
  > Required packages:
  > - `python-dotenv`
  > - `markdown`

---

## 📄 Usage

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/cover-letter-generator.git
cd cover-letter-generator
```

### 2. Set Up Your `.env`

Create a `.env` file in the root directory - you could use the .env.example as a reference - with your personal and application-specific data:

```env
# 🔒 Personal Information
NAME=Jane Doe
LOCATION=Berlin, Germany
EMAIL=janedoe@example.com
PHONE=(+49) 123 456 789
LINKEDIN=https://linkedin.com/in/janedoe
GITHUB=https://github.com/janedoe
PORTFOLIO=https://janedoe.dev 

# 🏢 Application-Specific Info
CURRENT_COMPANY=Tech Solutions GmbH   
APPLYING_COMPANY=Acme Corp
JOB_TITLE=Full Stack Developer
HIRING_MANAGER_NAME=Alex Smith        

# 💼 Context About You
FIELD_OF_EXPERTISE=web development
GENERAL_PROJECT_TYPE=internal tools and scalable platforms
SHORT_PROJECT_OR_IMPACT=modernizing a legacy dashboard for a logistics client  
TECH_STACK=React, Node.js, NestJS, PostgreSQL 

# 💡 Why This Company?
WHAT_ATTRACTS_YOU=engineering excellence and a learning-first culture          
POSITIVE_NOTE_ABOUT_COMPANY=delivers consistent value through small, iterative releases 
```

### 3. Write Your Markdown Letter

Customize your cover letter in Markdown using variable placeholders:

```markdown
**{{NAME}}**  
{{LOCATION}}  
{{EMAIL}} | {{PHONE}}  
[LinkedIn]({{LINKEDIN}}) | [GitHub]({{GITHUB}})  
[Portfolio]({{PORTFOLIO}})  

{{current_date}}

Dear {{HIRING_MANAGER_NAME}},

I’m writing to express my interest in the **{{JOB_TITLE}}** role at **{{APPLYING_COMPANY}}**. With a background in {{FIELD_OF_EXPERTISE}} and experience working on {{GENERAL_PROJECT_TYPE}}, I’m confident in my ability to contribute meaningfully to your team and help drive {{APPLYING_COMPANY}}’s goals.

At {{CURRENT_COMPANY}}, I’ve worked on {{SHORT_PROJECT_OR_IMPACT}}, using technologies such as {{TECH_STACK}} to build scalable, maintainable solutions. My approach blends technical precision with user empathy and cross-team collaboration.

What excites me most is {{WHAT_ATTRACTS_YOU}}, and I truly admire how your team {{POSITIVE_NOTE_ABOUT_COMPANY}}.

Thank you for considering my application — I’d love the opportunity to bring my energy and experience to your team.

Sincerely,  
**{{NAME}}**
```

### 4. Add Optional Styling

Create a `cover_letter.css` for styling. Default fallback is provided if missing:

```css
body {
  font-family: "Georgia", serif;
  font-size: 10.5pt;
  margin: 1in;
  color: #222;
  line-height: 1.5;
}
```

### 5. Generate Your Cover Letter

Run the generator with your Markdown input:

```bash
python3 cover_letter_template.py cover_letter.md
```

This will output:

- `cover_letter.html`
- `cover_letter.pdf`

### Optional CLI Flags

Use a custom Chrome binary:

```bash
python3 cover_letter_template.py cover_letter.md --chrome-path "/path/to/chrome"
```

Generate only HTML (no PDF):

```bash
python3 cover_letter_template.py cover_letter.md --no-pdf
```

---

## 📁 Project Structure

```
├── cover_letter.md         # Your Markdown template
├── cover_letter.css        # Optional CSS
├── cover_letter.html       # Rendered HTML output
├── cover_letter.pdf        # Final PDF output
├── cover_letter_template.py
├── .env                    # Your variable data
└── README.md
```

---

## 💡 Tips

- Use Git branches or folders for different company letters.
- Add metadata like language or region in the filename if applying globally.
- Use the output PDF for direct uploads or attach via email templates.
- Combine with a job tracker for batch applications.

---

## 🛠️ License

MIT — free to use, modify, and share.

---

## 🌱 Inspired By

Built with inspiration from [resume.md](https://github.com/mikepqr/resume.md) by [@mikepqr](https://github.com/mikepqr).  

---

Made with ❤️ by [Mazen Shebeta](https://github.com/MazenShebeta)
