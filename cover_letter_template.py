#!/usr/bin/env python3
import argparse, base64, os, re, shutil, subprocess, tempfile
import markdown
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

variables = {
    "NAME": os.getenv("NAME"),
    "LOCATION": os.getenv("LOCATION"),
    "EMAIL": os.getenv("EMAIL"),
    "PHONE": os.getenv("PHONE"),
    "LINKEDIN": os.getenv("LINKEDIN"),
    "GITHUB": os.getenv("GITHUB"),
    "PORTFOLIO": os.getenv("PORTFOLIO"),
    "HIRING_MANAGER_NAME": os.getenv("HIRING_MANAGER_NAME"),
    "JOB_TITLE": os.getenv("JOB_TITLE"),
    "APPLYING_COMPANY": os.getenv("APPLYING_COMPANY"),
    "FIELD_OF_EXPERTISE": os.getenv("FIELD_OF_EXPERTISE"),
    "GENERAL_PROJECT_TYPE": os.getenv("GENERAL_PROJECT_TYPE"),
    "COMPANY_GOAL_OR_MISSION": os.getenv("COMPANY_GOAL_OR_MISSION"),
    "SHORT_PROJECT_OR_IMPACT": os.getenv("SHORT_PROJECT_OR_IMPACT"),
    "TECH_STACK": os.getenv("TECH_STACK"),
    "APPLYING_COMPANY": os.getenv("APPLYING_COMPANY"),
    "WHAT_ATTRACTS_YOU": os.getenv("WHAT_ATTRACTS_YOU"),
    "POSITIVE_NOTE_ABOUT_COMPANY": os.getenv("POSITIVE_NOTE_ABOUT_COMPANY"),
    "KEY_PROJECT": os.getenv("KEY_PROJECT"),
    "CONTRIBUTION_SUMMARY": os.getenv("CONTRIBUTION_SUMMARY"),
    "CURRENT_COMPANY": os.getenv("CURRENT_COMPANY"),
    "current_date": datetime.today().strftime('%B %d, %Y'), 
}

preamble = """\
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
<div id="letter">
"""

postamble = """\
</div>
</body>
</html>
"""

def guess_chrome_path() -> str:
    # Add your own logic or fallback paths
    return shutil.which("chrome") or shutil.which("google-chrome") or shutil.which("chromium")

def title(md: str) -> str:
    for line in md.splitlines():
        if re.match("^#[^#]", line):
            return line.lstrip("#").strip()
    return "Cover Letter"

def preprocess_markdown(md: str, vars: dict) -> str:
    # Conditional rendering: removing sections based on the availability of values in `vars`
    if not vars.get("APPLYING_COMPANY"):
        md = re.sub(r"\{\{#IF APPLYING_COMPANY\}\}.*\{\{\/IF\}\}", "", md, flags=re.DOTALL)
    
    if not vars.get("KEY_PROJECT"):
        md = re.sub(r"\{\{#IF KEY_PROJECT\}\}.*\{\{\/IF\}\}", "", md, flags=re.DOTALL)
    
    return md

def substitute_variables(md: str, vars: dict) -> str:
    # Remove unused conditional blocks entirely
    lines = md.splitlines()
    output_lines = []

    for line in lines:
        # Skip lines with empty variables
        if any(f"{{{{{key}}}}}" in line and not val for key, val in vars.items()):
            continue
        output_lines.append(line)

    md = "\n".join(output_lines)

    # Replace remaining placeholders
    for key, val in vars.items():
        md = md.replace(f"{{{{{key}}}}}", val or "")
    
    return md



def make_html(md: str, prefix: str = "cover_letter") -> str:
    try:
        with open(prefix + ".css") as cssfp:
            css = cssfp.read()
    except FileNotFoundError:
        css = ""
    return "".join((
        preamble.format(title=title(md), css=css),
        markdown.markdown(md, extensions=["smarty", "abbr"]),
        postamble,
    ))

def sanitize_filename(name: str) -> str:
    """Remove invalid characters from file name."""
    return re.sub(r"[^\w\-_.]", "_", name)

def write_pdf(html: str, prefix: str = "cover_letter", chrome: str = "", variables: dict = None) -> None:
    chrome = chrome or guess_chrome_path()
    if not chrome:
        raise ValueError("Chrome path could not be found or is not set.")

    html64 = base64.b64encode(html.encode("utf-8")).decode("utf-8")
    
    temp_user_data = tempfile.mkdtemp(prefix='cover_letter_')
    options = [
        "--no-sandbox",
        "--headless",
        "--print-to-pdf-no-header",
        "--no-pdf-header-footer",
        "--disable-gpu",
        f"--user-data-dir={temp_user_data}"
    ]

    try:
        name = variables.get("NAME", "").strip()
        company = variables.get("APPLYING_COMPANY", "").strip()
        title = variables.get("JOB_TITLE", "").strip()
        
        # if name and company and title:
        #     pdf_name = f"{sanitize_filename(name)}-{sanitize_filename(company)}-{sanitize_filename(title)}"
        # else:
        pdf_name = prefix

        subprocess.run([
            chrome, *options,
            f"--print-to-pdf={pdf_name}.pdf",
            f"data:text/html;base64,{html64}"
        ], check=True)

        print(f"PDF saved as: {pdf_name}.pdf")

    finally:
        shutil.rmtree(temp_user_data, ignore_errors=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", default="cover_letter.md", nargs="?", help="Markdown input file")
    parser.add_argument("--no-pdf", action="store_true")
    parser.add_argument("--chrome-path")
    args = parser.parse_args()

    prefix, _ = os.path.splitext(os.path.abspath(args.file))

    with open(args.file, encoding="utf-8") as mdfp:
        md = mdfp.read()

    md = substitute_variables(md, variables)

    html = make_html(md, prefix=prefix)

    with open(prefix + ".html", "w", encoding="utf-8") as htmlfp:
        htmlfp.write(html)

    if not args.no_pdf:
        write_pdf(html, prefix=prefix, chrome=args.chrome_path, variables=variables)
