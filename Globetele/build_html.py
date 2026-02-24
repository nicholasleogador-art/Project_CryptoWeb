import os
import json

# 1. List all the files your dashboard needs to run
files_to_pack = [
    "Home.py",
    "navbar.py",
    "data_cleaning.py",
    "Data1.csv",
    "pages/1_Problem.py",
    "pages/2_Solution.py",
    "pages/3_Impact.py",
    "pages/5_GlobeUser.py"
]

files_dict = {}

# 2. Read each file and store it safely
print("Packing files...")
for path in files_to_pack:
    normalized_path = os.path.normpath(path)
    if os.path.exists(normalized_path):
        with open(normalized_path, "r", encoding="utf-8") as f:
            files_dict[path.replace("\\", "/")] = f.read()
            print(f"  [OK] {path}")
    else:
        print(f"  [WARNING] Could not find {path} - Skipping.")

# 3. Create the stlite HTML template with the UPGRADED v0.66.0 engine
html_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Thesis Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.66.0/build/stlite.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.66.0/build/stlite.css" />
  </head>
  <body>
    <div id="root"></div>
    <script>
      stlite.mount({{   
        requirements: ["pandas", "plotly"],
        entrypoint: "Home.py",
        files: {json.dumps(files_dict)}
      }}, document.getElementById("root"));
    </script>
  </body>
</html>
"""

# 4. Save the final HTML file
output_name = "dashboard.html"
with open(output_name, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"\n✅ Success! You can now send '{output_name}' to your boss.")