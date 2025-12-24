# 🤖 AutoDevCrew

**Multi-Agent SDLC Automation with Privacy-First Architecture**

AutoDevCrew is a comprehensive, production-ready multi-agent system that automates the entire Software Development Lifecycle (SDLC) using specialized AI agents. Built with privacy, offline operation, and hardware flexibility in mind.

---

## 🌟 Key Features

### 🤖 **Multi-Agent Architecture**
- **Engineer Agent**: Generates high-quality code using local LLMs
- **Tester Agent**: Validates, tests, and performs security scans
- **DevOps Agent**: Handles builds, deployments, and CI/CD integration
- **Summarizer Agent**: Creates comprehensive project reports

### 🔒 **Privacy-First Design**
- **Strict Mode**: Complete offline operation, zero external API calls
- **Data Encryption**: Optional encryption for sensitive information
- **Local Storage**: All data stored locally with configurable retention policies
- **Anonymization**: Built-in data anonymization for privacy compliance

### ⚡ **Hardware Optimization**
- **Lightweight Mode**: Optimized for mid-range hardware (4GB+ RAM)
- **Quantized Models**: Support for 4-bit/8-bit/FP16 quantization
- **CPU/GPU Flexibility**: Auto-detects hardware and adjusts accordingly
- **Memory Efficient**: Smart memory management and model offloading

### ☁️ **Deployment Options**
- **HuggingFace Spaces**: One-click deployment to HF Spaces
- **Google Colab**: Ready-to-use Colab notebook with free GPU
- **Docker**: Complete Docker configuration
- **Local**: Full local installation support

### 🔄 **CI/CD Integration**
- **GitHub Actions**: Auto-generated workflows
- **Webhook Support**: Real-time event processing
- **Auto PR Creation**: Automated pull requests with generated code
- **Security Scanning**: Integrated vulnerability detection

---

## 📁 Project Structure

```
AutoDevCrew/
├── agents/                    # AI Agents
│   ├── engineer_agent.py     # Code generation
│   ├── tester_agent.py       # Testing & validation
│   ├── devops_agent.py       # Build & deployment
│   └── summarizer_agent.py   # Report generation
│
├── core/                      # Core Modules
│   ├── privacy_manager.py    # Privacy & offline mode
│   ├── lightweight_mode.py   # Hardware optimization
│   └── cloud_deployer.py     # Cloud deployment
│
├── integrations/              # External Integrations
│   └── github_integration.py # GitHub Actions, webhooks
│
├── ui/                        # User Interfaces
│   └── streamlit_app.py      # Web dashboard
│
├── db/                        # Database
│   ├── storage.py            # Data persistence
│   └── schema.py             # Database schema
│
├── config/                    # Configuration
│   └── development.yaml      # Dev configuration
│
├── quantized_models/          # Optimized Models
│   ├── llama2-4bit/
│   ├── mistral-4bit/
│   └── codellama-8bit/
│
├── colab_notebooks/           # Google Colab
│   └── autodevcrew_colab.ipynb
│
├── huggingface_spaces/        # HuggingFace Deployment
│   ├── app.py
│   └── requirements.txt
│
├── main.py                    # Main entry point
└── requirements.txt           # Dependencies
```

---

## 🚀 Quick Start

### 1. **Installation**

```bash
# Clone the repository
git clone https://github.com/yourusername/autodevcrew.git
cd autodevcrew

# Install dependencies
pip install -r requirements.txt

# Optional: Setup Ollama for local LLMs
# Download from: https://ollama.ai
ollama pull llama2
```

### 2. **Run Interactive Mode**

```bash
python main.py
```

### 3. **Run with Streamlit UI**

```bash
python main.py --mode ui
```

### 4. **Process a Single Task**

```bash
python main.py --task "Create a REST API for user authentication" --project my-api
```

### 5. **Deploy to Cloud**

```bash
# Deploy to HuggingFace Spaces
python main.py --mode deploy --deploy-to huggingface

# Deploy to Google Colab
python main.py --mode deploy --deploy-to colab
```

---

## 💡 Usage Examples

### **CLI Mode - Single Task**
```bash
python main.py --task "Build a web scraper for news articles" \
               --privacy strict \
               --lightweight
```

### **API Mode**
```bash
python main.py --mode api --host 0.0.0.0 --port 8000
```

### **With GitHub Integration**
```bash
export GITHUB_TOKEN="your_token_here"
export GITHUB_REPOSITORY="username/repo"

python main.py --task "Fix security vulnerabilities" \
               --project security-fixes
```

### **Interactive Mode Features**
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
```

---

## ⚙️ Configuration

### **config/development.yaml**

```yaml
# Privacy Settings
privacy_level: "strict"  # strict, moderate, open
data_retention: "local_only"

# Lightweight Mode
lightweight_mode: true
quantization: "int  4"  # fp16, int8, int4, gptq

# LLM Configuration
llm:
  provider: "local"  # local, ollama, openai
  model: "llama2"
  temperature: 0.7
  max_tokens: 2048

# Agents
agents:
  engineer:
    quality_threshold: 70
  tester:
    coverage_target: 80
    security_scan: true
  devops:
    environments: ["development"]
    simulate_only: true

# GitHub Integration
github:
  enabled: false
  create_issues: false
```

---

## 🔒 Privacy Modes

### **Strict Mode** (Default)
- ✅ Complete offline operation
- ✅ All processing local
- ✅ No external network calls
- ✅ Maximum privacy

### **Moderate Mode**
- ✅ Local by default
- ⚠️ Optional external calls for updates
- ✅ Whitelisted domains only

### **Open Mode**
- ⚠️ Full cloud capabilities
- ⚠️ External API access allowed
- ⚠️ Use with caution for sensitive data

---

## ⚡ Hardware Requirements

### **Minimum (Lightweight Mode)**
- **RAM**: 4GB
- **Storage**: 10GB
- **CPU**: 2 cores
- **GPU**: Optional (CPU-only with quantized models)

### **Recommended**
- **RAM**: 8GB+
- **Storage**: 20GB+
- **CPU**: 4+ cores
- **GPU**: 4GB+ VRAM (for faster inference)

### **Optimal**
- **RAM**: 16GB+
- **Storage**: 50GB+
- **CPU**: 8+ cores
- **GPU**: 8GB+ VRAM (RTX 3060+)

---

## 🌐 Deployment

### **HuggingFace Spaces**
```bash
# Automated deployment
python main.py --mode deploy --deploy-to huggingface

# Manual deployment
1. Create a new Space at huggingface.co/spaces
2. Copy contents of huggingface_spaces/ to your Space
3. Set SDK to "streamlit"
4. Deploy!
```

### **Google Colab**
```bash
# Open the Colab notebook
colab_notebooks/autodevcrew_colab.ipynb

# Or generate deployment package
python main.py --mode deploy --deploy-to colab
```

### **Docker**
```bash
# Build image
docker build -t autodevcrew .

# Run container
docker run -p 8501:8501 autodevcrew
```

---

## 🔄 GitHub Actions Integration

### **Generate Workflow**
```bash
python main.py --mode cli
# Select option 4: Generate GitHub Actions workflow
```

### **Example Workflow**
- Triggers on push/PR
- Runs AutoDevCrew pipeline
- Creates automated PRs with generated code
- Performs security scans
- Uploads artifacts

---

## 📊 System Diagnostics

```python
# View system status
python main.py --mode cli
# Select option 5: System diagnostics

# Output includes:
- Hardware profile (RAM, CPU, GPU)
- Privacy settings
- Available models
- Memory usage
- Agent metrics
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LangChain**: LLM orchestration framework
- **Autogen**: Multi-agent conversation framework
- **Streamlit**: Web UI framework
- **Ollama**: Local LLM runtime
- **HuggingFace**: Model hosting and spaces

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/autodevcrew/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/autodevcrew/discussions)
- **Email**: support@autodevcrew.io

---

## 🗺️ Roadmap

### **v1.1** (Current)
- ✅ Multi-agent SDLC automation
- ✅ Privacy-first architecture
- ✅ Lightweight mode
- ✅ Cloud deployment

### **v1.2** (Upcoming)
- ⏳ VS Code extension
- ⏳ Advanced workflow types (Agile, Kanban)
- ⏳ Real-time collaboration
- ⏳ Enterprise features

### **v2.0** (Future)
- 📅 Custom agent creation
- 📅 Plugin ecosystem
- 📅 Multi-language support
- 📅 Advanced monitoring & analytics

---

**Made with ❤️ by the AutoDevCrew Team**

[![Star on GitHub](https://img.shields.io/github/stars/yourusername/autodevcrew?style=social)](https://github.com/yourusername/autodevcrew)
[![Deploy to HuggingFace](https://img.shields.io/badge/🤗-Deploy%20to%20Spaces-yellow)](https://huggingface.co/spaces)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/autodevcrew/blob/main/colab_notebooks/autodevcrew_colab.ipynb)
