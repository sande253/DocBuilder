import os

def create_local_video_page(video_path, back_url, output_html="local_video.html"):
    video_abs_path = os.path.abspath(video_path)
    video_url = "file:///" + video_abs_path.replace("\\", "/")
    filename = os.path.basename(video_abs_path)

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
            <a href="file:///C:/languages/DocLogic/local_video.html"/>
            <div class="buttons">
                <a class="btn" href="{back_url}">⬅ Back</a>
                <a class="btn" href="{video_url}" download="{filename}">⬇ Download</a>
            </div>

            <h2>🎬 Video Player</h2>

            <video controls autoplay>
                <source src="{video_url}" type="video/mp4">
                Your browser does not support the video tag.
            </video>

        </div>

    </body>
    </html>
    """

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    html_abs_path = os.path.abspath(output_html)
    html_url = "file:///" + html_abs_path.replace("\\", "/")
    return html_url

# Example usage
if __name__ == "__main__":
    video_path = r"C:/languages/manim/media/videos/957c9612-8195-406e-8b41-d5020619121b/480p15/BubbleSortPerfect.mp4"
    link = create_local_video_page(video_path,"http:localhost:8501")
    print("HTML page created! Open in browser:")
    print(link)
