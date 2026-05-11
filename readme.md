# 🛍️ Customer Feedback Triage System — ShopSphere

An AI-powered customer feedback analysis system that uses advanced prompt engineering techniques to extract structured insights from customer reviews for ShopSphere e-commerce platform.

---

## 📌 Project Overview

This system analyzes customer reviews and extracts:
- Overall sentiment (Positive, Negative, Neutral, Mixed)
- Aspect-level breakdown (product quality, delivery, service etc.)
- Structured JSON output for automated triage
- Comparison of multiple prompting techniques

---

## 🗂️ Project Structure
GenAI/
├── customer_triage_system.py   ← Core analysis system
├── .env                        ← API key (not pushed to GitHub)
├── requirements.txt            ← Python dependencies
└── README.md

---

## 🚀 How It Works
Customer Review (CSV)
↓
3 Prompting Techniques Applied
↓
Zero-Shot  → basic sentiment only
Few-Shot   → sentiment + aspects
CoT        → deep reasoning + aspects
↓
Results compared against Ground Truth
↓
Best technique identified

---

## 🧠 Prompting Techniques Used

### 1️⃣ Zero-Shot
No examples given
Model answers directly
→ Gets sentiment right
→ Misses aspect breakdown

### 2️⃣ Few-Shot
3 worked examples shown
Model learns output format
→ Gets sentiment right
→ Correctly identifies aspects

### 3️⃣ Chain-of-Thought (CoT)
Step by step reasoning forced
Model thinks before answering
→ Best for complex mixed reviews
→ Occasionally overthinks neutral cases

### 4️⃣ Self-Consistency (Bonus)
CoT runs 3 times
Most common answer selected
→ Most reliable output
→ Reduces randomness

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/ambastlinkin-droid/GenAI.git
cd GenAI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install openai pandas python-dotenv
```

---

## 🔐 Setup API Key

Create a `.env` file in the root folder:
OPENAI_API_KEY=your-openai-api-key-here

---

## ▶️ Run the System

```bash
python customer_triage_system.py
```

---

## 📊 Sample Output
--- Review #2 ---
Text: The product is great, but the shipping box was
completely crushed and it arrived two days late.
Ground Truth: Mixed — 3 aspects
Zero-Shot:    Mixed — no aspects
Few-Shot:     Mixed — 3 aspects ✅
CoT:          Mixed — 3 aspects ✅

---

## 🗃️ Dataset

6 customer reviews covering:

| Review | Type |
|---|---|
| #1 Coffee maker | Simple Positive |
| #2 Shipping box | Mixed |
| #3 Wrong headphones | Negative + Action |
| #4 T-shirt quality | Simple Negative |
| #5 Generic product | Neutral |
| #6 Battery life | Complex Mixed |

---

## 📈 Technique Comparison

| Technique | Sentiment Accuracy | Aspect Detection | Best For |
|---|---|---|---|
| Zero-Shot | ✅ 6/6 | ❌ None | Quick sentiment only |
| Few-Shot | ✅ 6/6 | ✅ Good | Structured output |
| CoT | ⚠️ 5/6 | ✅ Good | Complex reviews |
| Self-Consistency | ✅ Best | ✅ Best | Production use |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| OpenAI GPT-4o-mini | AI model |
| openai | OpenAI SDK |
| pandas | Data handling |
| python-dotenv | API key management |

---

## 👨‍💻 Author

**Shubham Kumar**
