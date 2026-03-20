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

## 🎯 Figma AI Enhancement Prompt (Copy-Paste This)

```
I'm building a web application called "MindMap" — an AI-powered student 
psychological health assessment platform. I need you to redesign and 
enhance the UI/UX for a modern, premium feel.

CURRENT STATE:
- Dark theme web app with indigo/violet/cyan color palette
- 7 pages: Home, Global Context, Assessment, Results, Report, Parent Guide, Teacher Dashboard
- Built with Streamlit (Python) — some UI constraints exist
- Screenshots of current design are attached

ENHANCEMENT GOALS:
1. Make the design feel more PREMIUM and polished
2. Improve information hierarchy and visual flow
3. Add micro-interactions and subtle animations concepts
4. Better use of whitespace and card layouts
5. Improve the assessment form UX (multi-step with clear progress)
6. Design a more engaging chatbot interface for Parent Guide
7. Create better data visualization layouts for Teacher Dashboard
8. Ensure accessibility (WCAG AA compliance)
9. Design responsive layouts (desktop + tablet)
10. Keep the dark theme but make it feel more sophisticated

DESIGN CONSTRAINTS:
- Must work within Streamlit framework limitations
- Keep the sidebar navigation pattern
- Maintain trilingual support (English, Marathi, Hindi)
- Charts are rendered via Plotly (interactive)
- Target users: Indian college students, parents, teachers

COLOR SYSTEM TO KEEP/EVOLVE:
- Primary: Indigo (#4F46E5) → Violet (#7C3AED)
- Accent: Cyan (#06B6D4)
- Semantic: Emerald (success), Amber (warning), Rose (danger)
- Background: Deep navy/dark (#0F0F1A, #1A1A2E)
- Fonts: Space Grotesk (headings) + Inter (body)

DELIVERABLES NEEDED:
1. Full design system (tokens, components, spacing)
2. Redesigned wireframes for all 7 pages
3. Component library (cards, buttons, pills, charts, forms)
4. Interaction/animation specifications
5. Responsive breakpoint designs
```

---

## 📁 Attached Screenshots

| # | File | Description |
|---|------|-------------|
| 01 | `01_home.png` | Home page – hero, stat pills, language cards |
| 02 | `02_home_scrolled.png` | Home page scrolled – explainer, comparison |
| 03 | `03_global_context.png` | Global Context – charts, gauges |
| 04 | `04_global_context_scrolled.png` | Global Context scrolled – insights |
| 05 | `05_assessment.png` | Assessment – multi-tab form |
| 06 | `06_assessment_scrolled.png` | Assessment – form fields |
| 07 | `07_parent_guide.png` | Parent Guide – AI chatbot |
| 08 | `08_parent_guide_scrolled.png` | Parent Guide – conversation guide |
| 09 | `09_teacher_dashboard.png` | Teacher Dashboard – upload |
| 10 | `10_teacher_dashboard_scrolled.png` | Teacher Dashboard – analysis |

---

## 🔧 How to Use This in Figma AI

### Step 1: Figma मध्ये नवीन Project तयार करा
1. [figma.com](https://figma.com) वर जा → New Design File
2. Frame Size: **1440 x 900** (Desktop)

### Step 2: Screenshots Import करा
1. `figma_export/` folder मधले सगळे `.png` files drag & drop करा Figma मध्ये
2. प्रत्येक screenshot एका separate Frame मध्ये ठेवा
3. Frame names ठेवा: "Current - Home", "Current - Assessment", etc.

### Step 3: Figma AI ला Prompt द्या
1. Figma मध्ये **Figma AI** (✨ icon) वर click करा
2. वर दिलेला **Enhancement Prompt** copy-paste करा
3. Screenshots select करा reference म्हणून
4. "Generate" वर click करा

### Step 4: Alternative — Manual Wireframe approach
1. Screenshots चं observation करा 
2. "Make a design" feature वापरा Figma AI मध्ये
3. Individual components redesign करा
4. Auto Layout वापरून responsive बनवा

### Step 5: Design Export करा
1. Enhanced design ready झाल्यावर CSS Inspect वापरा
2. Colors, spacing, fonts note करा
3. ते values `assets/style.css` मध्ये update करा

---

## 💡 Alternative AI Design Tools (Figma AI व्यतिरिक्त)

| Tool | Best For | URL |
|------|----------|-----|
| **Figma AI (Make Design)** | Full page redesign from prompt | Built into Figma |
| **Galileo AI** | Generate UI from text description | [usegalileo.ai](https://usegalileo.ai) |
| **Uizard** | Screenshot → editable wireframe | [uizard.io](https://uizard.io) |
| **Locofy** | Figma design → code export | [locofy.ai](https://locofy.ai) |
| **V0 by Vercel** | AI-generated React components | [v0.dev](https://v0.dev) |
| **Relume** | AI sitemap + wireframe generator | [relume.io](https://relume.io) |

---

*Generated for MindMap Project — February 2026*
