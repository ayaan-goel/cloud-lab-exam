from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import pymysql
import boto3
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ── AWS / DB Config from environment variables ──────────────────────────────
DB_HOST     = os.environ.get("DB_HOST", "localhost")
DB_USER     = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_NAME     = os.environ.get("DB_NAME", "notesdb")
S3_BUCKET   = os.environ.get("S3_BUCKET", "your-bucket-name")
AWS_REGION  = os.environ.get("AWS_REGION", "us-east-1")

# ── S3 client (uses EC2 IAM Role automatically) ─────────────────────────────
s3 = boto3.client("s3", region_name=AWS_REGION)

# ── Database helpers ─────────────────────────────────────────────────────────
def get_db():
    return pymysql.connect(
        host=DB_HOST, user=DB_USER,
        password=DB_PASSWORD, database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                content TEXT,
                image_url VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()

# ── HTML Template ────────────────────────────────────────────────────────────
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>AWS Notes App — EC2 + RDS + S3</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#0d1117 0%,#161b22 50%,#0d1117 100%);min-height:100vh;color:#e6edf3}
    .header{background:linear-gradient(90deg,#FF9900,#FF6600);padding:20px 40px;display:flex;align-items:center;gap:16px;box-shadow:0 4px 20px rgba(255,153,0,0.3)}
    .header h1{font-size:1.8rem;color:#fff;font-weight:700}
    .badges{display:flex;gap:8px;margin-left:auto}
    .badge{background:rgba(255,255,255,0.2);border-radius:50px;padding:4px 12px;font-size:0.75rem;font-weight:600;color:#fff;border:1px solid rgba(255,255,255,0.3)}
    .container{max-width:900px;margin:40px auto;padding:0 20px}
    .form-card{background:rgba(22,27,34,0.8);border:1px solid rgba(48,54,61,0.8);border-radius:16px;padding:28px;margin-bottom:32px;backdrop-filter:blur(10px)}
    .form-card h2{font-size:1.1rem;margin-bottom:20px;color:#FF9900}
    .form-row{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}
    input,textarea{width:100%;padding:12px 16px;background:rgba(13,17,23,0.8);border:1px solid rgba(48,54,61,1);border-radius:10px;color:#e6edf3;font-size:0.9rem;outline:none;transition:border .2s}
    input:focus,textarea:focus{border-color:#FF9900}
    textarea{resize:vertical;min-height:80px;grid-column:1/-1}
    input[type=file]{padding:10px;color:#8b949e}
    .btn{padding:12px 24px;background:linear-gradient(135deg,#FF9900,#FF6600);color:#fff;border:none;border-radius:10px;font-size:0.95rem;font-weight:600;cursor:pointer;width:100%;transition:opacity .2s,transform .1s}
    .btn:hover{opacity:0.85;transform:scale(1.01)}
    .notes-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px}
    .note-card{background:rgba(22,27,34,0.8);border:1px solid rgba(48,54,61,0.8);border-radius:14px;overflow:hidden;transition:transform .2s,box-shadow .2s}
    .note-card:hover{transform:translateY(-4px);box-shadow:0 12px 30px rgba(255,153,0,0.1)}
    .note-img{width:100%;height:160px;object-fit:cover;background:#1c2128}
    .note-img-placeholder{width:100%;height:160px;background:linear-gradient(135deg,#1c2128,#21262d);display:flex;align-items:center;justify-content:center;font-size:2.5rem}
    .note-body{padding:16px}
    .note-title{font-size:1rem;font-weight:600;margin-bottom:8px;color:#e6edf3}
    .note-content{font-size:0.85rem;color:#8b949e;line-height:1.5;margin-bottom:12px}
    .note-meta{font-size:0.75rem;color:#6e7681;display:flex;justify-content:space-between;align-items:center}
    .del-btn{background:rgba(248,81,73,0.15);border:1px solid rgba(248,81,73,0.3);color:#f85149;padding:4px 12px;border-radius:8px;font-size:0.75rem;cursor:pointer;transition:background .2s}
    .del-btn:hover{background:rgba(248,81,73,0.3)}
    .empty{text-align:center;color:#6e7681;padding:60px 20px;font-style:italic}
    .arch-bar{background:rgba(255,153,0,0.05);border:1px solid rgba(255,153,0,0.2);border-radius:10px;padding:12px 20px;margin-bottom:28px;font-size:0.82rem;color:#FF9900;text-align:center}
  </style>
</head>
<body>
  <div class="header">
    <span style="font-size:2rem">☁️</span>
    <h1>AWS Notes App</h1>
    <div class="badges">
      <span class="badge">🖥 EC2</span>
      <span class="badge">🗄 RDS MySQL</span>
      <span class="badge">🪣 S3</span>
    </div>
  </div>
  <div class="container">
    <div class="arch-bar">
      Architecture: <strong>EC2</strong> (Flask) → <strong>RDS MySQL</strong> (notes data) + <strong>S3</strong> (image uploads)
    </div>
    <div class="form-card">
      <h2>➕ Add New Note</h2>
      <form action="/add" method="POST" enctype="multipart/form-data">
        <div class="form-row">
          <input type="text" name="title" placeholder="Note title..." required/>
          <input type="file" name="image" accept="image/*"/>
        </div>
        <div class="form-row">
          <textarea name="content" placeholder="Write your note here..."></textarea>
        </div>
        <button type="submit" class="btn">Save Note to AWS</button>
      </form>
    </div>
    <div class="notes-grid">
      {% for note in notes %}
      <div class="note-card">
        {% if note.image_url %}
          <img class="note-img" src="{{ note.image_url }}" alt="{{ note.title }}"/>
        {% else %}
          <div class="note-img-placeholder">📝</div>
        {% endif %}
        <div class="note-body">
          <div class="note-title">{{ note.title }}</div>
          <div class="note-content">{{ note.content or 'No content.' }}</div>
          <div class="note-meta">
            <span>{{ note.created_at.strftime('%d %b %Y') }}</span>
            <form action="/delete/{{ note.id }}" method="POST" style="margin:0">
              <button type="submit" class="del-btn">Delete</button>
            </form>
          </div>
        </div>
      </div>
      {% endfor %}
      {% if not notes %}
        <div class="empty" style="grid-column:1/-1">No notes yet — add your first one above!</div>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM notes ORDER BY created_at DESC")
        notes = cur.fetchall()
    conn.close()
    return render_template_string(HTML, notes=notes)

@app.route("/add", methods=["POST"])
def add_note():
    title   = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    image   = request.files.get("image")
    image_url = None

    # Upload image to S3 if provided
    if image and image.filename:
        filename = f"{uuid.uuid4()}_{secure_filename(image.filename)}"
        s3.upload_fileobj(
            image, S3_BUCKET, filename,
            ExtraArgs={"ContentType": image.content_type}
        )
        image_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{filename}"

    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO notes (title, content, image_url) VALUES (%s, %s, %s)",
            (title, content, image_url)
        )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    conn = get_db()
    with conn.cursor() as cur:
        # Optionally delete from S3 too
        cur.execute("SELECT image_url FROM notes WHERE id=%s", (note_id,))
        row = cur.fetchone()
        if row and row["image_url"]:
            key = row["image_url"].split("/")[-1]
            try:
                s3.delete_object(Bucket=S3_BUCKET, Key=key)
            except Exception:
                pass
        cur.execute("DELETE FROM notes WHERE id=%s", (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
