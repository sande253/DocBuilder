from repository.mongodb import MongoDBHandler
from .llm import GeminiClient
import matplotlib.pyplot as plt

from datetime import datetime
import json, os, subprocess
from google.adk.tools import FunctionTool
import re 
from .manim_implementation import manim_handler
TEMP_DIR = r"C:\languages\DocLogic\temp_dir"
os.makedirs(TEMP_DIR, exist_ok=True)

client = GeminiClient.get_instance("AIzaSyD_LZvBS3iqIYU-2a6ZgFrdn89uaQhG9FM")
mongo = MongoDBHandler(db_name="wt", collection_name="latex")
# Directory to save charts
CHART_DIR = r"C:\languages\DocLogic\charts"
os.makedirs(CHART_DIR, exist_ok=True)


class Handler:

    # ---------- LLM LATEX GENERATION ----------
    @staticmethod
    def _get_latex_from_llm(text: str) -> str:
        """Ask the LLM to generate LaTeX code for the provided text."""
        PROMPT = r"""
        You are a LaTeX generator.
Use suitable format based on needs 
use new page or clearpage if required based on needs 
represent data in good format 
Title & Headings — Clearly indicate what the document is about.
Sections/Subsections — Logical division of content (e.g., Introduction, Methods, Results, Conclusion).
Paragraph Flow — Smooth transitions; each paragraph should have one key idea.
Formatting Consistency — Font, spacing, margins, bullet styles, etc.
Return only the LaTeX content.
TEXT:
""" + text

        raw_output = client.get_response(PROMPT)
        print("LLM Output:", raw_output)
        # Optionally clean unwanted wrapper text
        return raw_output.strip()
    def generate_video_from_text(self,prompt:str):
         obj=manim_handler()
         status = obj.create_manim_video(prompt)
         if status :
             url=obj.create_local_video_page(video_path=status.get("file"))
             return url
         return {"failed":"failed due to model overload from source servers "}

    # ---------- CREATE / UPDATE ----------
    def create_new_document(self, text: str, document_name:str):
        """Create a new document with LaTeX code generated from text."""
        user_name="sathvik"
        latex_code = self._get_latex_from_llm(text)
        session_id = mongo.create_document(
            document_name=document_name,
            original_text=text,
            latex_code=latex_code,
            user_name=user_name
        )
        return {
            "session_id": session_id,
            "original_text": text,
            "latex_code": latex_code
        }

    def update_document(self, session_id: str, new_text: str):
        """Regenerate LaTeX for an existing document."""
        new_latex = self._get_latex_from_llm(new_text)
        updated = mongo.update_document(session_id, {
            "original_text": new_text,
            "latex_code": new_latex,
            "timestamp": datetime.now().isoformat()
        })
        if updated == 0:
            raise ValueError(f"No document found for session_id {session_id}")
        return new_latex

    # ---------- RETRIEVE ----------
    def get_document(self, session_id: str):
        """Retrieve a single document by session_id."""
        doc = mongo.read_by_session(session_id)
        if not doc:
            raise ValueError(f"No document found for session_id {session_id}")
        return doc
    def extract_valid_json(self,raw_output: str):
        """
        Cleans and extracts JSON safely from LLM output.
        """
        try:
            start = raw_output.find('{')
            end = raw_output.rfind('}') + 1
            if start == -1 or end == -1:
                raise ValueError("No JSON object found in response")

            json_part = raw_output[start:end]

            # Fix common issues
            json_part = json_part.replace("“", '"').replace("”", '"').replace("’", "'")
            json_part = re.sub(r',\s*([\]}])', r'\1', json_part)

            return json.loads(json_part)
        except Exception as e:
            raise ValueError(f" JSON extraction failed: {e}\nRaw output:\n{raw_output}")


    def generate_statistical_chart(self,text: str) -> str:
        """
        Uses LLM to generate statistical chart data from text,
        creates the chart with Matplotlib, saves it, and returns full image path.

        Args:
            text (str): User-provided text description (e.g. "show GDP growth by year")
        Returns:
            str: Full file path of saved chart image
        """

        PROMPT = f"""
        You are a data visualization expert.
        Based on the given text, produce statistical data in JSON format only.
        The JSON **must strictly follow** this structure:

        {{
            "title": "string",
            "chart_type": "bar" | "line" | "pie",
            "x_label": "string",
            "y_label": "string",
            "data": {{
                "<label1>": number,
                "<label2>": number,
                ...
            }}
        }}

        The 'data' keys are labels (like months, countries, or years),
        and the values are numeric values suitable for plotting.
        TEXT: {text}
        """

        # Get response from LLM
        raw_output = client.get_response(PROMPT)
        print("🔹 Raw LLM Output:\n", raw_output)

        # Extract valid JSON
        info = self.extract_valid_json(raw_output)

        # Extract data safely
        title = info.get("title", "Generated Chart")
        chart_type = info.get("chart_type", "bar").lower()
        x_label = info.get("x_label", "")
        y_label = info.get("y_label", "")
        data = info.get("data", {})

        if not data:
            raise ValueError("⚠️ No data points returned by LLM")

        x = list(data.keys())
        y = list(data.values())

        # Create chart
        plt.figure(figsize=(8, 5))
        if chart_type == "bar":
            plt.bar(x, y)
        elif chart_type == "line":
            plt.plot(x, y, marker="o")
        elif chart_type == "pie":
            plt.pie(y, labels=x, autopct="%1.1f%%")
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")

        plt.title(title)
        if chart_type != "pie":
            plt.xlabel(x_label)
            plt.ylabel(y_label)

        # Save chart
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chart_{timestamp}.png"
        full_path = os.path.join(CHART_DIR, filename)

        plt.tight_layout()
        plt.savefig(full_path, dpi=300)
        plt.close()

        print(f"✅ Chart saved at: {full_path}")
        return full_path
    # ---------- COMPILE ----------
    def compile_to_pdf(self, session_id: str):
        """Compile LaTeX code of a document into a PDF file."""
        doc = self.get_document(session_id)
        latex_code = doc.get("latex_code", "")

       

        latex_full = latex_code

        # Hardcoded PDF path
        pdf_path = os.path.join(TEMP_DIR, "tmpbu9gupv5.pdf")
        tex_path = os.path.splitext(pdf_path)[0] + ".tex"

        # Write LaTeX code to file
        with open(tex_path, "w", encoding="utf-8") as tex_file:
            tex_file.write(latex_full)

        # Run pdflatex
        subprocess.run(
            [
                r"C:\Users\sathv\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe",
                "-interaction=nonstopmode",
                f"-output-directory={TEMP_DIR}",
                tex_path
            ],
            capture_output=True,
            text=True
        )

        # Return result
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                return "compiled"
        return "not compiled"

    # ---------- TOOLS ----------
    def get_all_tools(self):
        return [
            FunctionTool(func=self.create_new_document),
            FunctionTool(func=self.update_document),
            FunctionTool(func=self.get_document),
            FunctionTool(func=self.compile_to_pdf),
            FunctionTool(func=self.generate_statistical_chart),
            FunctionTool(func=self.generate_video_from_text)
        ]
