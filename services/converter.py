from repository.mongodb import MongoDBHandler
from .llm import GeminiClient
from datetime import datetime
import json, os, tempfile, subprocess
from google.adk.tools import FunctionTool
TEMP_DIR = r"C:\languages\DocLogic\temp_dir"
os.makedirs(TEMP_DIR, exist_ok=True)

client = GeminiClient.get_instance("AIzaSyD_LZvBS3iqIYU-2a6ZgFrdn89uaQhG9FM")
mongo = MongoDBHandler(db_name="wt", collection_name="latex")


class Handler:

    # ---------- LLM PAGE GENERATION ----------
    @staticmethod
    def _get_pages_from_llm(text: str) -> list:
        """Ask the LLM to split content into page-format JSON."""
        PROMPT = f"""
        You are a LaTeX page generator.
        Split the following text logically into pages and return only valid JSON.
        Return Format:
        {{
          "pages": [
             {{ "pageno": <int>, "content": "<LaTeX code>" }}
          ]
        }}
        Text: {text}
        """
        raw_output = client.get_response(PROMPT)
        print(raw_output)
        try:
            start = raw_output.find('{')
            end = raw_output.rfind('}') + 1
            json_part = raw_output[start:end]
            parsed = json.loads(json_part)
            return parsed.get("pages", [])
        except Exception as e:
            print("⚠️ LLM output not valid JSON:", e)
            print("Raw output:", raw_output)
            return []

    # ---------- CREATE / ADD / UPDATE / INSERT ----------
    def create_new_document(self, text: str):
        """Create a new document with pages generated from text."""
        pages = self._get_pages_from_llm(text)
        formatted = [
            {
                "pageno": p["pageno"],
                "original_text": text,
                "latex_code": p["content"],
                "summary": "",
                "timestamp": datetime.now().isoformat()
            } for p in pages
        ]
        session_id =mongo.create_document(document_name="random",pages=formatted,user_name="sathvik")
        return {"pages":formatted,"session_id":session_id}

    def add_page(self, session_id: str, text: str):
        """Append a new page to the document."""
        pages = self._get_pages_from_llm(text)
        for p in pages:
            page_doc = {
                "pageno": p["pageno"],
                "original_text": text,
                "latex_code": p["content"],
                "summary": "",
                "timestamp": datetime.now().isoformat()
            }
            mongo.add_page(session_id, page_doc)
        return pages

    def insert_page(self, session_id: str, position: int, text: str):
        """Insert a new page at a specific position."""
        pages = self._get_pages_from_llm(text)
        for p in pages:
            page_doc = {
                "pageno": position,
                "original_text": text,
                "latex_code": p["content"],
                "summary": "",
                "timestamp": datetime.now().isoformat()
            }
            mongo.insert_page_at(session_id, position, page_doc)
        return pages

    def update_page(self, session_id: str, page_no: int, new_text: str):
        """Regenerate a specific page."""
        pages = self._get_pages_from_llm(new_text)
        if not pages:
            raise ValueError("LLM returned no valid pages")
        new_latex = pages[0]["content"]
        mongo.update_page(session_id, page_no, {
            "original_text": new_text,
            "latex_code": new_latex,
            "timestamp": datetime.now().isoformat()
        })
        return new_latex

    # ---------- RETRIEVE ----------
    def get_all_pages(self, session_id: str):
        """Retrieve all pages of a particular session."""
        doc = mongo.readBySession(session_id)
        if not doc:
            return []
        return doc.get("pages", [])

    # ---------- COMPILE ----------
    def compile_to_pdf(self, latex_code: str):
        """Compile given LaTeX code to PDF bytes."""
        with tempfile.NamedTemporaryFile(suffix=".tex", dir=TEMP_DIR, delete=False) as tex_file:
            tex_file.write(latex_code.encode("utf-8"))
            tex_path = tex_file.name

        pdf_path = tex_path.replace(".tex", ".pdf")

        subprocess.run(
            [r"C:\Users\sathv\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe",
             "-interaction=nonstopmode",
             f"-output-directory={TEMP_DIR}",
             tex_path],
            capture_output=True,
            text=True
        )

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                #return f.read()
                return "compiled "
        return "not compiled "
    def get_all_tools(self):
        tool1=FunctionTool(func=self.create_new_document)
        tool2=FunctionTool(func=self.add_page)
        tool3=FunctionTool(func=self.update_page)
        
        tool4=FunctionTool(func=self.get_all_pages)
        tool5=FunctionTool(func=self.insert_page)
        
        tool7=FunctionTool(func=self.compile_to_pdf)
        return [tool1,tool2,tool3,tool4,tool5,tool7]
