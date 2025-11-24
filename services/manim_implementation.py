import subprocess
import uuid
import os
import json 
from .llm import GeminiClient
import re 

client = GeminiClient.get_instance("AIzaSyD53G1Bwg1V39PyNBYQvKn7Gq89fXUBprw")
# ---------------------------
# Fake LLM (fixed response)
# ---------------------------
class manim_handler:
    def extract_valid_json(self,raw_output: str):
        """
        Safely extract JSON from LLM output, even if code contains newlines or quotes.
        Returns a dictionary.
        """
        try:
            # Step 1: Find the first and last curly braces
            start = raw_output.find('{')
            end = raw_output.rfind('}') + 1
            if start == -1 or end == -1:
                raise ValueError("No JSON object found in response")

            json_part = raw_output[start:end]

            # Step 2: Escape control characters inside string values
            # Replace raw newlines and carriage returns inside quotes with \n
            def escape_control_chars(match):
                inner = match.group(1)
                inner = inner.replace('\n', '\\n').replace('\r', '')
                inner = inner.replace('"', '\\"')
                return f'"{inner}"'

            # Regex finds all string values in JSON (naive but works for single-level JSON)
            json_part = re.sub(r'"(.*?)"', escape_control_chars, json_part, flags=re.DOTALL)

            # Step 3: Load as JSON
            return json.loads(json_part)
        except Exception as e:
            raise ValueError(f"❌ JSON extraction failed: {e}\nRaw output:\n{raw_output}")

    def llm_generate_manim_code(self,prompt: str) -> str:
        
        PROMPT =r"""You are an expert in Python and Manim (Community v0.19+). Write a complete Python script for a Manim Scene that animates [describe algorithm or visualization, e.g., Bubble Sort on array [4,2,7,1,3]].
always use the module import manim
Requirements:
-Do not compicate the syntax to an extent where it has high posibility of failing but try 
--Every visual element that needs text (array values, nodes, labels) must be a single VGroup containing the shape (Rectangle, Circle, etc.) and a centered Text element.
-Do not use raw coordinates. Use VGroup.arrange(direction=RIGHT/UP, buff=0.4) or relative positioning for consistent spacing.
-Animate movements or swaps for the entire VGroup, never individual sub-elements.
-Update labels using label.become(new_label) and center it in the parent shape with new_label.move_to(shape.get_center()).
-Avoid hardcoding positions; rely on VGroup.arrange or precomputed target positions corresponding to logical indices.
-Ensure code is fully compatible with Manim Community v0.19+, with proper imports, correct indentation, and no syntax errors.
-Include concise comments explaining key steps, but do not over-comment trivial lines.
- Make sure all the namespaces are included and defined properly 
-Always call methods when you intend to get a value.
-Never pass a method object to move_to(), scale(), or any animation function—pass only the result of the method.
-Wrap the generated Python code inside a JSON object exactly like this:
{
"code": "<full Python code here>"
}
Output requirements 
1. All newlines, tabs, and quotes inside the code must be properly escaped.
2. Use double quotes for JSON keys and string values.
3. Do not include markdown, backticks, or any explanation.
4. Ensure the output is always a single JSON object.
Instruction: Generate the Manim code in the JSON format above only, do not include any explanations, text, or extra formatting outside the JSON.
         """+f"\nContext on what to genenrate:{prompt} "
        raw_output = client.get_response(PROMPT)
        print("LLM Output:", raw_output)
        data=self.extract_valid_json(raw_output)

        # Optionally clean unwanted wrapper text
        return data["code"]
    # ---------------------------
    # Extract Scene class name
    # ---------------------------

    def extract_scene_name(self,code: str) -> str:
        for line in code.splitlines():
            if "class " in line and "(Scene)" in line:
                return line.split("class ")[1].split("(")[0].strip()
        return "Scene"


    # ---------------------------
    # Run Manim and locate output
    # ---------------------------

    def run_manim(self,code: str) -> str:
        scene_id = str(uuid.uuid4())
        script_name = f"{scene_id}.py"

        # Write file
        with open(script_name, "w", encoding="utf-8") as f:

            f.write(code)

        print(f"[INFO] Running manim for scene: {script_name}")

        # Use python -m manim (works on Windows)
        cmd = ["python", "-m", "manim", script_name, "-ql"]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print("[ERROR] Manim failed:")
            print(e)
            return {"error":e}

        scene_name = self.extract_scene_name(code)

        # Correct manim output folder:
        # output_path = os.path.join(
        #     "media",
        #     "videos",
        #     script_name.replace(".py", ""),
        #     "480p15",
        #     f"{scene_name}.mp4"
        # )
        output_path = rf"C:\languages\DocLogic\media\videos\{scene_id}\480p15\{scene_name}.mp4"
        # if os.path.exists(self,output_path):
        #     return output_path
        # else:
        #     print("[ERROR] Video not found at:", output_path)
        #     return None
        import os

        directory = f"C:/languages/DocLogic/media/videos/{scene_id}/480p15"

        # List all .mp4 files
        mp4_files = [f for f in os.listdir(directory) if f.lower().endswith(".mp4")]

        scene_name=mp4_files[0]

        output_path = rf"C:\languages\DocLogic\media\videos\{scene_id}\480p15\{scene_name}"

        if os.path.exists(output_path):
            return output_path
        else:
            print("[ERROR] Video not found at:", output_path)
            return None
    def create_local_video_page(self,video_path, back_url="window.location.href='http://localhost:8501'", output_html="C:/languages/DocLogic/local_video.html"):
            video_abs_path = os.path.abspath(video_path)
            video_url = "file:///" + video_abs_path.replace("\\", "/")
            filename = os.path.basename(video_abs_path)
            video_url =video_url.replace("file:///C:/languages/DocLogic/","http://localhost:9000/")
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Video Player</title>
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        background: #0d0d0d;
                        color: #eaeaea;
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: flex-start;
                        height: 100vh;
                    }}

                    .container {{
                        width: 90%;
                        max-width: 900px;
                        margin-top: 40px;
                        padding: 25px;
                        background: rgba(255, 255, 255, 0.05);
                        border-radius: 16px;
                        backdrop-filter: blur(10px);
                        box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
                    }}

                    h2 {{
                        text-align: center;
                        margin-bottom: 20px;
                        font-size: 26px;
                        letter-spacing: 1px;
                        color: #ffffffd9;
                    }}

                    .buttons {{
                        display: flex;
                        justify-content: center;
                        margin-bottom: 20px;
                        gap: 20px;
                    }}

                    .btn {{
                        padding: 10px 18px;
                        border-radius: 8px;
                        background: linear-gradient(135deg, #292929, #1a1a1a);
                        color: #d4d4d4;
                        text-decoration: none;
                        font-size: 15px;
                        transition: 0.3s ease-in-out;
                        border: 1px solid #333;
                        box-shadow: 0 0 8px rgba(255, 255, 255, 0.05);
                    }}

                    .btn:hover {{
                        color: white;
                        border-color: #5f5fff;
                        box-shadow: 0 0 12px #5f5fff;
                        transform: translateY(-2px);
                    }}

                    video {{
                        width: 100%;
                        border-radius: 12px;
                        outline: none;
                        box-shadow: 0 0 25px rgba(0, 0, 0, 0.6);
                    }}
                </style>
            </head>

            <body>

                <div class="container">
                   
                    <div class="buttons">
                        <a class="btn" onclick="{back_url}">Back</a>
                        <a class="btn" href="{video_url}" download="{filename}">Download</a>
                    </div>

                    <h2>Video Player</h2>

                    <video controls autoplay>
                        <source src="{video_url}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>

                </div>

            </body>
            </html>
            """

            with open(f"{output_html}", "w", encoding="utf-8") as f:
                f.write(html_content)

            html_abs_path = os.path.abspath(output_html)
            html_url = "file:///" + html_abs_path.replace("\\", "/")
            return "http://localhost:9000/local_video.html"
 
    def create_manim_video(self,user_prompt ):
        print("\n[INFO] Asking LLM (mock)...\n")
        code = self.llm_generate_manim_code(user_prompt)
        print("[INFO] LLM produced code:\n")
        print(code)
        error=""
        rendered_file=""
        for i in range (0,5):
            try : 
             rendered_file = self.run_manim(code)
              
            except Exception as e : 
                print("Retrying to generate "+(i+1))
                error = e 
            if not isinstance(rendered_file, dict) :
                print("\n[SUCCESS] Video generated at:")
                print(rendered_file)
                return {"file":rendered_file}
            else:
                print("\n[FAILED-loop] Something went wrong generating the video.")
                    
                prompt =f"Please fix this code make sure you use right imports , variable declaration , right syntax if it is confusing make simple version of this \n code :{code}"
                print(prompt)
                code=self.llm_generate_manim_code(prompt=prompt)

        if not isinstance(rendered_file, dict) :
                print("\n[SUCCESS] Video generated at:")
                print(rendered_file)
                return {"file":rendered_file}
        else:
                print("\n[FAILED] Something went wrong generating the video.")
                return None 




# obj=manim_handler()
# status = obj.create_manim_video("explaining how chromosomes work")

