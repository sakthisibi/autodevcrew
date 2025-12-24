# 🎉 AutoDevCrew - HOW TO USE (Simple Guide)

## ✅ **System is READY!**

You can now use AutoDevCrew in 3 easy ways:

---

## 🚀 **METHOD 1: Interactive Mode** (Easiest - Recommended)

```bash
python main.py
```

You'll see a menu:
```
🤖 AutoDevCrew Pro - Complete SDLC Automation
============================================================

📋 Main Menu:
1. 🚀 Process single task         <-- Start here!
2. 📦 Batch process from file
3. ☁️  Deploy to cloud
4. 🔄 Generate GitHub workflow
5. 📊 System diagnostics
6. ⚙️  Privacy settings
7. ⚡ Performance optimization
8. 🗃️  Task history
9. 🚪 Exit
```

**Try it:**
1. Run `python main.py`
2. Press `1` and Enter
3. Type: `Create a Python function to add two numbers`
4. Press Enter for defaults
5. Watch the magic happen! ✨

---

## 💻 **METHOD 2: Command Line** (Quick Tasks)

```bash
python main.py --task "Create a hello world function"
```

**More examples:**

```bash
# Simple function
python main.py --task "Write a function to calculate factorial"

# With project name
python main.py --task "Create a REST API endpoint" --project my-api

# Lightweight mode (for slower computers)
python main.py --task "Your task" --lightweight

# Maximum privacy (no external calls)
python main.py --task "Your task" --privacy strict
```

---

## 🌐 **METHOD 3: Web Interface** (Beautiful UI)

```bash
python main.py --mode ui
```

**This will:**
1. Start a web server
2. Open your browser automatically
3. Show a beautiful dashboard
4. Let you enter tasks visually

**Access at:** http://localhost:8501

---

## 🎯 **Quick Examples to Try**

### Example 1: Simple Function
```bash
python main.py --task "Create a function to reverse a string"
```

### Example 2: Web Scraper
```bash
python main.py --task "Write a Python script to scrape news headlines"
```

### Example 3: API Endpoint
```bash
python main.py --task "Create a FastAPI endpoint for user login"
```

### Example 4: Data Processing
```bash
python main.py --task "Write code to read CSV and calculate averages"
```

---

## ⚙️ **Common Options**

| Option | Description | Example |
|--------|-------------|---------|
| `--task` | Describe what to build | `--task "Create calculator"` |
| `--project` | Project name | `--project my-app` |
| `--lightweight` | Use less memory | `--lightweight` |
| `--privacy` | Privacy level | `--privacy strict` |
| `--mode ui` | Web interface | `--mode ui` |
| `--help` | Show all options | `--help` |

---

## 📊 **What Happens When You Run a Task?**

1. **Engineer Agent** → Generates the code
2. **Tester Agent** → Validates syntax and logic
3. **DevOps Agent** → Simulates deployment
4. **Summarizer Agent** → Creates a report

**You get:**
- ✅ Generated code
- ✅ Test results
- ✅ Deployment status
- ✅ Summary report

---

## 🔧 **Advanced Features**

### Deploy to Cloud
```bash
python main.py --mode deploy --deploy-to huggingface
```

### Check System Status
```bash
python main.py
# Then select option 5
```

### Generate GitHub Workflow
```bash
python main.py
# Then select option 4
```

---

## ❓ **Troubleshooting**

### If you see import errors:
```bash
pip install langchain streamlit pyyaml
```

### If Ollama is not installed:
The system works in demo mode without Ollama!
You can install it later from https://ollama.ai

### If something doesn't work:
```bash
python main.py --help
```

---

## 📚 **Learn More**

- **Detailed Guide:** See `QUICKSTART.md`
- **Full Documentation:** See `README.md`
- **Status Report:** See `IMPLEMENTATION_STATUS.md`

---

## 🎉 **You're All Set!**

**Start now:**
```bash
python main.py
```

**Press 1, enter a task, and watch it work!**

---

**Questions? The system is fully documented:**
- Type `python main.py --help`
- Open `QUICKSTART.md`
- Check the interactive menu options
