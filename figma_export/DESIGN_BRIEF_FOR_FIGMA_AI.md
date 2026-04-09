# 🧠 MindMap – UI/UX Design Brief for Figma AI Enhancement

## 📋 Project Overview

**App Name:** MindMap – Student Psychological Health Assessment  
**Type:** Web Application (Streamlit-based, Python)  
**Target Users:** Students, Parents, Teachers  
**Region:** Pune, Maharashtra, India 🇮🇳  
**Languages Supported:** English, मराठी (Marathi), हिंदी (Hindi)  

**Purpose:** AI-powered comparative psychological analysis of students in online vs. offline learning environments. Uses indirect lifestyle questions to detect stress, anxiety, and wellbeing without students feeling explicitly assessed.

---

## 🎨 Current Design System

### Color Palette

| Token         | Hex       | Usage                              |
|---------------|-----------|-------------------------------------|
| Indigo        | `#4F46E5` | Primary brand color, buttons, links |
| Violet        | `#7C3AED` | Secondary accent, gradients         |
| Cyan          | `#06B6D4` | Charts, progress bars               |
| Emerald       | `#10B981` | Success states, positive scores     |
| Amber         | `#F59E0B` | Warnings, moderate scores           |
| Rose          | `#F43F5E` | Errors, high-risk alerts            |
| BG Dark       | `#0F0F1A` | Main background                     |
| BG Card       | `#1A1A2E` | Card backgrounds                    |
| BG Glass      | `rgba(79,70,229,0.08)` | Glass/frosted overlays |
| Text Primary  | `#E2E8F0` | Main text                           |
| Text Muted    | `#94A3B8` | Secondary text                      |
| Text Accent   | `#A5B4FC` | Highlighted text, metrics           |
| Border Subtle | `rgba(255,255,255,0.07)` | Card borders        |

### Gradients Used
- **Hero:** `linear-gradient(135deg, #1e1b4b, #312e81, #1e1b4b)`
- **Buttons:** `linear-gradient(135deg, #4F46E5, #7C3AED)`
- **Sidebar:** `linear-gradient(180deg, #111827, #0F0F1A)`
- **Section titles underline:** `linear-gradient(90deg, #4F46E5, #06B6D4)`
- **Text gradient:** `linear-gradient(135deg, #A5B4FC, #818CF8, #C4B5FD)`

### Typography

| Usage           | Font            | Weight | Size      |
|-----------------|-----------------|--------|-----------|
| Headings        | Space Grotesk   | 700    | 1.15-2rem |
| Body            | Inter           | 400    | 0.88-1rem |
| Stat pills      | Inter           | 600    | 0.88rem   |
| Metric values   | Space Grotesk   | 700    | 2rem      |
| Footer/Caption  | Inter           | 400    | 0.65rem   |

### Border Radius
- Cards: `12px`
- Hero: `14px`
- Buttons: `10px`
- Stat pills: `50px` (fully rounded)
- Inputs: `8px`
- Tabs: `8px 8px 0 0`

### Shadows & Effects
- Card hover: `0 8px 24px rgba(79,70,229,0.15)`
- Button default: `0 4px 15px rgba(79,70,229,0.3)`
- Button hover: `0 8px 25px rgba(79,70,229,0.45)`
- Hero glow: `0 0 40px rgba(79,70,229,0.12)`
- Hover animation: `translateY(-2px)` with `0.2s ease`

---

## 📄 Pages & Screens (7 Total)

### 1. 🏠 Home (Information Page)
- Hero banner with brain emoji, app title, tagline
- 4 stat pills (800+ profiles, ML insights, privacy, multilingual)
- 3 language info cards (Marathi, English, Hindi)
- "What is MindMap?" explainer section
- Online vs. Offline comparison cards
- India-specific research insights

### 2. 🌍 Global Context
- COVID impact line chart (India learning mode shift)
- Student satisfaction gauges (Maharashtra 2024)
- Hybrid learning insights
- Student archetype cards (Overloaded Achievers, Digital Natives, Social Learners)

### 3. 📝 Assessment (Multi-step Form)
- 5-tab navigation: About You → Study Habits → Daily Life → Activities → Your Future
- Progress indicator
- Form fields: text inputs, dropdowns, sliders, radio buttons
- Section-by-section flow with Next/Previous buttons

### 4. 📊 Results (Post-Assessment)
- Overall health score gauge (0-100)
- Risk alert badges
- Category scores (stress, anxiety, social health, etc.)
- Strengths chips (green) and improvement chips (amber)
- Detailed recommendations

### 5. 📑 Full Report (PDF Export)
- Comprehensive summary
- Printable/downloadable PDF report
- All assessment data and predictions

### 6. 👨‍👩‍👧 Parent Guide
- AI Parent Advisor chatbot (OpenAI-powered)
- Chat interface with message bubbles
- "Situation-by-Situation Conversation Guide"
- Expandable FAQ cards for specific behaviors

### 7. 👩‍🏫 Teacher Dashboard
- CSV/Excel upload for class data
- Class-level analysis with charts
- Individual student profile viewer
- Demo dataset option (800 Pune students)

---

