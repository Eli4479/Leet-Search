# ⚡ Leet-Search – Semantic LeetCode Search Engine

> **Find LeetCode problems by meaning — not just by name.**

Have you ever faced a situation where you vaguely remembered a LeetCode problem you once solved — but couldn’t recall its exact title?
Or come across a question in an online assessment (OA) that felt _familiar_ — like a slightly tweaked version of a LeetCode problem — but no amount of keyword guessing could help you find it again?

**Leet-Search** is built to solve exactly that.

A semantic search engine for LeetCode problems — built with FastAPI, Next.js, and pgvector.

> 🔗 **Live App**: [leet-search-sepia.vercel.app](https://leet-search-sepia.vercel.app)
> 📦 **Repository**: [github.com/Eli4479/Leet-Search](https://github.com/Eli4479/Leet-Search)

---

## 🧠 Features

- 🔍 **Semantic Search** — vector-based querying of LeetCode problem descriptions
- 🧩 **Modular FastAPI Architecture** — clean separation of concerns (routes, services, controllers)
- 🔗 **Supabase** — hosted PostgreSQL with `pgvector`

---

## 📂 Folder Structure

```
leet-search/
├── backend/
│   ├── app/
│   │   ├── controllers/          # Handles endpoint logic
│   │   ├── database/             # DB connection + Supabase client
│   │   ├── models/               # Pydantic schemas & data models
│   │   ├── routes/               # API route registration
│   │   ├── services/             # Core business logic
│   │   ├── utils/                # Helper utility functions
│   │   └── main.py               # FastAPI app entrypoint
│   ├── .env                      # Environment variables
│   └── requirements.txt          # Python dependencies
│
├── frontend/
│   ├── .next/                    # Next.js build output
│   ├── node_modules/
│   ├── public/                   # Static assets
│   ├── src/                      # All frontend source code
│   ├── .gitignore
│   ├── components.json
│   ├── eslint.config.mjs
│   ├── next-env.d.ts
│   ├── next.config.ts
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.mjs
│   ├── .env
│   ├── README.md
│   └── tsconfig.json
├── .gitignore
└── README.md                     #  Project documentation
```

---

## 🔐 Environment Variables

In your `.env` file in frontend (excluded via `.gitignore`), define:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api
```

In your `.env` file in backend (excluded via `.gitignore`), define:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-service-role-key
```

---

## 🧪 API Example

### **Endpoint**

```http
POST /api/search?page=1
```

### **Request Body**

```json
{
  "query": "graph dfs",
  "limit": 5
}
```

### **Response**

```json
[
  {
    "id": "1472",
    "title": "Design Browser History",
    "url": "https://leetcode.com/problems/design-browser-history/",
    "paid_only": false,
    "match_percentage": 77.24,
    "content": "formated HTML content of the problem.",
    "original_content": "original HTML content of the problem."
  },
  ...
]
```

### 💡 Explanation of Response Fields:

| Field              | Description                           |
| ------------------ | ------------------------------------- |
| `id`               | LeetCode problem ID                   |
| `title`            | Name of the problem                   |
| `url`              | Direct LeetCode URL                   |
| `paid_only`        | Whether the problem is paid-only      |
| `match_percentage` | Similarity score with query (0–100%)  |
| `content`          | Formatted HTML content of the problem |
| `original_content` | Original HTML content (for reference) |

---

## 🛠 Tech Stack

| Tool/Service | Description                                 |
| ------------ | ------------------------------------------- |
| 🐍 FastAPI   | Fast Python web framework (ASGI-compatible) |
| 🔗 Supabase  | PostgreSQL + pgvector for embeddings        |
| 🚀 Next.js   | React framework for the frontend            |
| 💎 shadcn/ui | Beautiful UI components for Next.js         |

---

## 🤝 Contributing

We’re thrilled you’re considering contributing to **Leet-Search** — a fast, intelligent semantic search engine for LeetCode problems!

Whether you're:

- Fixing bugs 🐛
- Improving performance ⚡
- Enhancing the UI/UX 💅
- Refining search algorithms 🔍
- Writing tests or documentation 🧪📝
- **Your contribution matters 💪🏻**

### 🙋‍♂️ How to Contribute

1. **Fork** the repo and create your branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Commit your changes**:

   ```bash
   git commit -m "feat: brief description of your change"
   ```

3. **Push to GitHub**:

   ```bash
   git push origin feature/your-feature-name
   ```

4. **Open a Pull Request** [here](https://github.com/Eli4479/Leet-Search/pulls) 🚀

> Found a bug or have a feature idea?
> Open an [Issue](https://github.com/Eli4479/Leet-Search/issues) – we’d love to discuss it with you!

### 🧠 Ideas to Contribute

- 🔥 Add support for more problem platforms (e.g., Codeforces, GFG)
- ✨ Enhance the frontend UX (Next.js + Tailwind)
- 🧠 Improve vector similarity logic or embeddings
- 🧪 Write unit tests for routes/services
- 🛡 Add rate limiting, error logging, or caching

---

## 🛠 Getting Started (Local Setup)

Want to run **Leet-Search** on your machine? Here's how:

### 🔁 Clone the Repository

```bash
git clone https://github.com/Eli4479/Leet-Search.git
cd Leet-Search
```

### 🔧 Backend Setup (FastAPI + Supabase)

1. **Navigate to backend** and create a virtual environment:

   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file**:

   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-supabase-service-role-key
   ```

4. **Start the FastAPI server**:

   ```bash
   uvicorn app.main:app --reload
   ```

   API will run at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 🌍 Frontend Setup (Next.js + Tailwind)

1. **Navigate to frontend and install packages**:

   ```bash
   cd ../frontend
   npm install
   ```

2. **Start the frontend dev server**:

   ```bash
   npm run dev
   ```

   Your app will run at: [http://localhost:3000](http://localhost:3000)

## 📦 Populate the Database

Prepare the LeetCode problem embeddings and load them into Supabase:

### 1️⃣ Create the Table in Supabase

- Open your Supabase project
- Go to **SQL Editor**
- Open the file `backend/scripts/sql.txt`
- Copy its contents and **run the query**

This will create the `problems_bge` table with the necessary columns (including `vector` type for embeddings).

### 2️⃣ Edit `main.py`

Open `backend/app/main.py` and **un-comment** the following line:

```python
# populate_db()
```

Change it to:

```python
populate_db()
```

### 3️⃣ Run the Backend Server

```bash
cd backend
uvicorn app.main:app --reload
```

This will:

- Fetch LeetCode problems (free + paid)
- Format and clean problem content
- Generate embeddings using OpenAI (or your configured model)
- Save the output to:
  `backend/scripts/problems.csv`

### 4️⃣ Upload CSV to Supabase

- Go to your Supabase **Table Editor**
- Select the `problems_bge` table
- Click **"Import Data"**
- Upload the generated CSV file from:

```bash
backend/scripts/problems.csv
```

> ✅ NOTE: After populating, you have to **comment out `populate_db()` again** to avoid re-triggering on future backend runs.

### ✅ Test It Works

1. Visit `http://localhost:3000`
2. Type a query like `graph dfs`
3. Confirm the results load from your FastAPI backend

## 🧑‍💻 Dev Tips

- Format code before committing (`black`, `prettier`, etc.)
- Use conventional commit messages (e.g. `feat:`, `fix:`, `docs:`)
- Open small, focused PRs with clear descriptions

---

## ⚠️ Performance Note

> ⚡ **Heads up!** The currently deployed version of Leet-Search is hosted on the **free tier of Render.com**, which may result in **slow cold starts** or **delayed responses**.

For the best experience:

- Set up the project **locally** using the instructions above

> Running locally ensures **faster search results** and full control over the backend.

---

## 👋 Final Note

Whether you're here to contribute, learn, or get inspired — thank you for checking out **Leet-Search**!

> Built with ❤️ and ☕ by [Aryan Patel](https://github.com/Eli4479)

```

```
