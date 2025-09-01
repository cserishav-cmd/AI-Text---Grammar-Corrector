✨ AI Text & Grammar Corrector Pro

  📝 A Flask-based web app powered by Google Gemini AI that corrects
  grammar, spelling, and style in real-time. Save corrections, view
  diffs, and download results as .txt or .pdf.

------------------------------------------------------------------------

🚀 Features

-   ✅ Grammar & Spelling Correction using Gemini API
-   ✅ Correction History stored in SQLite database
-   ✅ Download Results in TXT or PDF format
-   ✅ Side-by-Side Diff Viewer (highlighting changes)
-   ✅ Light/Dark Theme Toggle 🌙☀️
-   ✅ Responsive UI (Bootstrap + Icons)

------------------------------------------------------------------------

🎥 Demo Video

[ ➡️ [VIDEO LINK HERE](https://youtu.be/L0K1jMdvNGU) ⬅️ ]

------------------------------------------------------------------------

🏗️ Project Structure

    ├── app.py              # Flask app (routes, DB, file downloads)
    ├── model.py            # Gemini AI correction module
    ├── index.html          # Frontend UI (Bootstrap, dark mode)
    ├── requirements.txt    # Dependencies
    ├── database.db         # SQLite database (history storage)
    └── README.md           # You are here 🌍

------------------------------------------------------------------------

⚙️ Installation & Setup

1️⃣ Clone the Repository

    git clone https://github.com/your-username/ai-text-corrector.git
    cd ai-text-corrector

2️⃣ Create & Activate Virtual Environment

    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows

3️⃣ Install Dependencies

    pip install -r requirements.txt

4️⃣ Set Up Environment Variables

Create a .env file in the project root:

    GEMINI_API_KEY=your_api_key_here

5️⃣ Run the Application

    python app.py

Now open http://127.0.0.1:5000/ in your browser. 🎉

------------------------------------------------------------------------

📂 Database

-   SQLite database: database.db
-   Table: history
    -   id → Primary key
    -   original_text → User input
    -   corrected_text → AI-corrected output
    -   timestamp → Auto-added

------------------------------------------------------------------------

🔮 Future Enhancements

-   ✨ Add multi-language support
-   ✨ Export corrections as Word documents (.docx)
-   ✨ User authentication & profiles
-   ✨ Deploy to Heroku / Render / Railway for free hosting

------------------------------------------------------------------------

🛠️ Tech Stack

-   Backend: Flask (Python)
-   Frontend: Bootstrap 5 + Icons
-   AI Engine: Google Gemini API
-   Database: SQLite
-   Export: FPDF

------------------------------------------------------------------------

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue
first.

------------------------------------------------------------------------

📜 License

MIT License – feel free to use, modify, and share.
