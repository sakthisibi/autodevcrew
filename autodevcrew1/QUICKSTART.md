# 🚀 AutoDevCrew - Quick Start Guide

## 📋 Table of Contents
1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Interactive Mode](#interactive-mode)
4. [Command Line Mode](#command-line-mode)
5. [Web UI Mode](#web-ui-mode)
6. [Cloud Deployment](#cloud-deployment)
7. [Common Use Cases](#common-use-cases)
8. [Troubleshooting](#troubleshooting)

---

## 1. Installation

### Step 1: Install Basic Dependencies

```bash
# Navigate to the project directory
cd d:\autodevcrew

# Install core dependencies (required)
pip install langchain langchain-openai pydantic pyyaml streamlit

# Install optional dependencies (for full features)
pip install torch cryptography psutil uvicorn fastapi
```

### Step 2: Install Ollama (for local LLM)

**Option A: Download Ollama**
1. Visit https://ollama.ai
2. Download for Windows
3. Install and run Ollama
4. Pull the llama2 model:
```bash
ollama pull llama2
```

**Option B: Skip for now** (system will work in demo mode)

### Step 3: Verify Installation

```bash
python main.py --help
```

You should see:
```
usage: main.py [-h] [--mode {cli,api,ui,deploy}] [--task TASK] ...
```

---

## 2. Basic Usage

### ⚡ Quickest Start - Interactive Mode

```bash
python main.py
```

This launches the interactive menu:
```
🤖 AutoDevCrew Pro - Complete SDLC Automation
============================================================

📋 Main Menu:
1. 🚀 Process single task
2. 📦 Batch process from file
3. ☁️  Deploy to cloud (HuggingFace/Colab)
4. 🔄 Generate GitHub Actions workflow
5. 📊 System diagnostics
6. ⚙️  Privacy settings
7. ⚡ Performance optimization
8. 🗃️  Task history
9. 🚪 Exit

Enter choice (1-9):
```

---

## 3. Interactive Mode (Recommended for Beginners)

### Option 1: Process a Single Task

```bash
python main.py
# Select: 1

# Then enter:
Enter task description: Create a Python function to calculate factorial
Project name (optional): math-utils
Priority (low/medium/high/critical) [medium]: medium
Trigger CI/CD pipeline? (y/n) [n]: n
```

**What happens:**
1. ✅ Engineer Agent generates the code
2. ✅ Tester Agent validates syntax
3. ✅ DevOps Agent simulates deployment
4. ✅ Summarizer Agent creates report
5. 📊 Results displayed in terminal

### Option 2: System Diagnostics

```bash
python main.py
# Select: 5
```

**Output shows:**
- Hardware info (RAM, CPU, GPU)
- Privacy settings
- Available models
- Memory usage
- Agent status

### Option 3: Cloud Deployment

```bash
python main.py
# Select: 3
# Choose: 1 (HuggingFace) or 2 (Colab)
```

---

## 4. Command Line Mode

### Process a Single Task

```bash
python main.py --task "Create a REST API for user authentication" --project my-api
```

**Output:**
```json
{
  "success": true,
  "task": "Create a REST API for user authentication",
  "generated_code": "...",
  "test_report": "Syntax OK",
  "deployment_status": "Successfully deployed!",
  "summary": {...},
  "execution_time": 1.5
}
```

### With Privacy Mode

```bash
python main.py --task "Build a web scraper" --privacy strict
```

**Privacy Levels:**
- `strict` - Complete offline, no external calls (default)
- `moderate` - Local by default, optional external
- `open` - Full cloud capabilities

### With Lightweight Mode

```bash
python main.py --task "Generate a calculator app" --lightweight
```

**Benefits:**
- Optimized for 4GB+ RAM
- Uses quantized models
- Reduced memory footprint

---

## 5. Web UI Mode (Streamlit)

### Launch Web Dashboard

```bash
python main.py --mode ui
```

**OR directly:**

```bash
streamlit run ui/streamlit_app.py
```

**Opens browser at:** http://localhost:8501

### Using the Web UI

1. **Enter task description** in the text area
2. **Optional:** Set project name and priority
3. **Click "Submit Task"**
4. **Watch real-time progress**
5. **View results** in formatted display

**Features:**
- 📝 Code viewer with syntax highlighting
- 🧪 Test results display
- 🚀 Deployment status
- 📊 Summary and reports
- 💾 Download generated code

---

## 6. Cloud Deployment

### Deploy to HuggingFace Spaces

```bash
python main.py --mode deploy --deploy-to huggingface
```

**What it does:**
1. Creates deployment package
2. Generates HF Spaces configuration
3. Prepares app.py and requirements.txt
4. Shows next steps for upload

**Output:**
```
✅ Deployment package ready!
📁 Location: C:\Users\...\Temp\autodevcrew_deploy_xxx\huggingface_space

Next steps:
1. Create a new Space at https://huggingface.co/spaces
2. Upload contents of the folder
3. Set space visibility to public
```

### Deploy to Google Colab

```bash
python main.py --mode deploy --deploy-to colab
```

**Output:**
- Generates Colab notebook
- Provides Colab URL
- Includes setup instructions

**Or open existing notebook:**
```
colab_notebooks/autodevcrew_colab.ipynb
```

---

## 7. Common Use Cases

### Use Case 1: Generate a Simple Function

```bash
python main.py --task "Create a function to reverse a string in Python"
```

### Use Case 2: Build a REST API Endpoint

```bash
python main.py --task "Create a FastAPI endpoint for user registration with email validation" --project user-api
```

### Use Case 3: Data Processing Script

```bash
python main.py --task "Write a script to read CSV file and calculate averages" --lightweight
```

### Use Case 4: Generate Tests

```bash
python main.py --task "Generate unit tests for a sorting algorithm"
```

### Use Case 5: Security-Focused

```bash
python main.py --task "Create password validation function with security checks" --privacy strict
```

---

## 8. API Server Mode

### Start the API Server

```bash
python main.py --mode api --host 0.0.0.0 --port 8000
```

**Access at:** http://localhost:8000

**Endpoints:**
- `GET /` - API status
- (More endpoints can be added)

---

## 9. Advanced Usage

### Generate GitHub Actions Workflow

**Interactive:**
```bash
python main.py
# Select: 4
# Enter task ID: my-workflow
```

**Output:**
- Creates `github-actions-my-workflow.yml`
- Ready to copy to `.github/workflows/`

### Multiple Privacy Levels

```bash
# Maximum privacy (offline only)
python main.py --privacy strict --task "Your task"

# Moderate (local by default)
python main.py --privacy moderate --task "Your task"

# Open (full features)
python main.py --privacy open --task "Your task"
```

---

## 10. Configuration

### Edit Configuration File

Open `config/development.yaml`:

```yaml
# Privacy Settings
privacy_level: "strict"  # Change to: strict, moderate, or open

# Lightweight Mode
lightweight_mode: true   # Set to true for low-resource systems

# LLM Configuration
llm:
  provider: "local"      # local, ollama, or openai
  model: "llama2"        # Model name
  temperature: 0.7       # Creativity (0.0-1.0)
```

**Apply changes:**
```bash
python main.py --config config/development.yaml
```

---

## 11. Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Ollama not working

**Solution:**
```bash
# Check if Ollama is running
ollama list

# Pull the model
ollama pull llama2

# Test
ollama run llama2 "Hello"
```

### Issue: Web UI won't start

**Solution:**
```bash
# Install Streamlit specifically
pip install streamlit

# Run directly
streamlit run ui/streamlit_app.py
```

### Issue: Privacy mode blocks operations

**Solution:**
```bash
# Use moderate mode instead
python main.py --privacy moderate
```

### Issue: Low memory warnings

**Solution:**
```bash
# Enable lightweight mode
python main.py --lightweight
```

---

## 12. Quick Reference

### Most Common Commands

```bash
# Interactive mode (easiest)
python main.py

# Process a task
python main.py --task "Your task here"

# Web UI
python main.py --mode ui

# Lightweight mode
python main.py --lightweight --task "Your task"

# Maximum privacy
python main.py --privacy strict --task "Your task"

# Deploy to cloud
python main.py --mode deploy --deploy-to huggingface

# Help
python main.py --help
```

---

## 13. Example Session

```bash
# Start AutoDevCrew
python main.py

# Output:
🤖 AutoDevCrew Pro - Complete SDLC Automation
============================================================

📋 Main Menu:
1. 🚀 Process single task
2. 📦 Batch process from file
3. ☁️  Deploy to cloud (HuggingFace/Colab)
4. 🔄 Generate GitHub Actions workflow
5. 📊 System diagnostics
6. ⚙️  Privacy settings
7. ⚡ Performance optimization
8. 🗃️  Task history
9. 🚪 Exit

Enter choice (1-9): 1

🚀 Single Task Processing
----------------------------------------
Enter task description: Create a hello world function
Project name (optional): demo
Priority (low/medium/high/critical) [medium]: medium
Trigger CI/CD pipeline? (y/n) [n]: n

# Processing...
INFO:__main__:Processing task: Create a hello world function...
INFO:__main__:Initializing agents...
INFO:__main__:Created task ID: 1
INFO:__main__:Orchestrating task: Create a hello world function

✅ Task completed!
Execution time: 1.23s
Code quality: N/A
```

---

## 🎉 You're Ready!

**Start with:**
```bash
python main.py
```

**Then try:**
- Option 1: Process your first task
- Option 5: Check system diagnostics
- Switch to web UI with `python main.py --mode ui`

---

## 📚 Additional Resources

- **Full Documentation:** See `README.md`
- **Configuration Guide:** See `config/development.yaml`
- **Implementation Status:** See `IMPLEMENTATION_STATUS.md`
- **Colab Notebook:** `colab_notebooks/autodevcrew_colab.ipynb`

---

**Need help?** Run `python main.py --help` or start with interactive mode!
