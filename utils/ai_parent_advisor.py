"""utils/ai_parent_advisor.py
AI-powered Parent Advisor Chatbot using OpenAI.
- Accepts parent descriptions of child behaviour
- Psychological analysis & extraction using NLP + OpenAI GPT
- Returns structured, caring, practical advice
- Supports English / Marathi / Hindi
- Never gives clinical diagnosis — always recommends professional help for serious cases
"""

import os
import streamlit as st

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ─── OpenAI setup ──────────────────────────────────────────────────
def _get_openai_client():
    """Return an OpenAI client if API key is configured, else None."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key or api_key == "your_openai_api_key_here":
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except Exception:
        return None


# ─── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are MindMap Parent Advisor — a warm, empathetic AI assistant that helps parents in Pune, Maharashtra understand and support their children's psychological and academic well-being.

## YOUR ROLE
You receive descriptions from parents about their child's behaviour, mood, academic performance, and habits. You then:
1. Extract key psychological indicators from the description
2. Identify patterns (stress signals, motivation issues, emotional concerns, behavioural red flags)
3. Provide warm, practical, evidence-based advice to the parent

## LANGUAGE RULES
- Detect the language of the parent's message (English / Marathi / Hindi / mixed)
- Respond in the SAME language or language mix they used
- If mixed Marathi-English, respond in the same mix
- Be warm and respectful — use "आपण/तुम्ही" for Marathi, "आप" for Hindi

## PSYCHOLOGICAL FRAMEWORK (apply these mappings)
| Observation | Psychological Indicator |
|---|---|
| Not studying / low motivation | Amotivation, possible burnout or depression |
| Excess phone / gaming | Dopamine-seeking, stress-avoidance behaviour |
| Isolation, won't leave room | Social withdrawal (stress response, not attitude) |
| Irritability, mood swings | Stress overload, cortisol spike |
| Late night studies | Sleep deprivation — reduces memory consolidation by 40% |
| Low confidence | Self-efficacy deficit |
| Good IQ but low marks | Cognitive-performance gap — focus/discipline issue |
| Crying often, sadness | Possible adjustment disorder or depression |
| Skipping meals | Anxiety or depression symptom |
| Career pressure, exam fear | Performance anxiety |
| Talking about giving up | URGENT — risk signal requiring immediate professional referral |

## RESPONSE FORMAT (always structured like this)

**🔍 What I'm seeing:** [Brief 2-line extraction of what the parent described — name the psychological patterns simply]

**💛 What this means:** [Plain-language explanation — NO jargon. Validate the parent's concern. Normalize the child's behaviour where appropriate.]

**✅ What to DO:**
- [Specific, actionable step 1]
- [Specific, actionable step 2]
- [Specific, actionable step 3 — what to say word-for-word if applicable]

**❌ What NOT to do:**
- [Common mistake 1 parents make in this situation]
- [Common mistake 2]

**📅 This week:** [One concrete thing to try in the next 7 days]

**⚠️ Disclaimer:** This is general guidance based on common psychological patterns. For serious or persistent concerns, please consult a certified psychologist or your child's school counsellor. This is NOT a clinical diagnosis.

## URGENCY DETECTION (critical)
If the message contains words like: "give up", "disappear", "not be here", "hurt himself/herself", "self-harm", "want to die", "nako vatata", "jiyana nako", "khud ko hurt", "mar jau" — IMMEDIATELY respond with a crisis alert and helpline numbers. Format this as:

🆘 **URGENT — Seek Help Now**
[Crisis response + validation]
**Call:** iCall (TISS): 9152987821 | Vandrevala Foundation: 1860-2662-345 (24/7, Free)

## TONE RULES
- NEVER blame the child
- NEVER blame the parent
- Validate emotions first, advise second
- Be specific — generic advice is unhelpful
- Use evidence ("Research shows...", "Studies find...") briefly
- Keep the parent hopeful
- Max 350 words per response

## CONTEXT
Students are typically 16-24 years old, from Pune/Maharashtra colleges. Academic pressure, phone use, online vs offline learning transitions, and family expectations are common stressors.
"""


# ─── NLTK basic extraction (runs locally, no API) ─────────────────────────────
def _extract_signals(text: str) -> dict:
    """
    Fast LOCAL extraction of key signals from parent text.
    Returns a signals dict used to enhance the AI prompt.
    """
    text_l = text.lower()
    signals = {
        "academic":   any(w in text_l for w in ["marks","sgpa","fail","exam","study","padhna","abhyas","percent","score","grade"]),
        "phone":      any(w in text_l for w in ["phone","mobile","screen","youtube","instagram","gaming","game"]),
        "sleep":      any(w in text_l for w in ["sleep","raat","night","zop","insomnia","jaagta","jaagat"]),
        "isolation":  any(w in text_l for w in ["room","alone","isolated","baher","bahar","akela","nahi bolat"]),
        "anger":      any(w in text_l for w in ["angry","irritable","gussa","ragawto","chidchid","react","shout"]),
        "sad":        any(w in text_l for w in ["sad","cry","rodto","radto","depress","udaas","unhappy","rona"]),
        "food":       any(w in text_l for w in ["eat","food","jevan","khana","meal","bhukh","appetite"]),
        "career":     any(w in text_l for w in ["career","future","engineer","doctor","jee","neet","pressure","competition"]),
        "confidence": any(w in text_l for w in ["confidence","shy","hesitate","doubt","afraid","fear"]),
        "crisis":     any(w in text_l for w in ["give up","disappear","hurt himself","hurt herself","self harm",
                                                  "want to die","nako vatata","jiyana nako","mar jau","khud ko hurt"]),
    }
    return signals


def _signals_to_context(signals: dict) -> str:
    """Convert signal flags to a brief context string for the Gemini prompt."""
    active = [k for k, v in signals.items() if v]
    if not active:
        return ""
    return f"\n[Detected signals: {', '.join(active)}. Tailor advice to these areas.]"


# ─── Main AI call ──────────────────────────────────────────────────────────────
def get_ai_response(
    conversation_history: list[dict],
    user_message: str,
    lang: str = "en",
    child_name: str = "",
    child_scores: dict | None = None,
) -> str:
    """
    Send conversation to OpenAI and get a response.

    conversation_history: list of {"role": "user"|"assistant", "content": text}
    Returns response text string.
    """
    client = _get_openai_client()

    # Extract local signals
    signals = _extract_signals(user_message)

    # Build context injection for this turn
    context_parts = []
    if child_name:
        context_parts.append(f"Child's name: {child_name}")
    if child_scores:
        overall   = child_scores.get("overall_health", "?")
        stress    = round(child_scores.get("stress_index", 0.5) * 100)
        motivation = child_scores.get("motivation_score", "?")
        context_parts.append(
            f"MindMap Assessment data for {child_name}: "
            f"Overall Health={overall}/100, Stress={stress}%, Motivation={motivation}/100"
        )
    context_parts.append(f"Parent's preferred language: {lang}")
    signal_ctx = _signals_to_context(signals)
    if signal_ctx:
        context_parts.append(signal_ctx.strip())

    context_str = "\n".join(context_parts)

    # Augment user message with context (invisible to display)
    augmented_message = f"{user_message}\n\n[CONTEXT: {context_str}]" if context_str else user_message

    if client is None:
        # No API key — return smart fallback
        return _fallback_response(signals, lang, child_name, child_scores)

    try:
        # Build OpenAI messages list
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Add prior conversation turns
        messages.extend(conversation_history)

        # Append current user message (with context injection)
        messages.append({"role": "user", "content": augmented_message})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=800,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        err = str(e)
        if "quota" in err.lower() or "rate_limit" in err.lower() or "insufficient_quota" in err.lower():
            return _quota_msg(lang)
        return _fallback_response(signals, lang, child_name, child_scores)


# ─── Fallback responses (when no API key / quota exhausted) ───────────────────
def _quota_msg(lang: str) -> str:
    msgs = {
        "en": "⚠️ OpenAI quota limit reached or API key invalid. Please check your `OPENAI_API_KEY` in the `.env` file. Using smart fallback advice for now.",
        "mr": "⚠️ OpenAI कोटा संपला किंवा API की अवैध आहे. `.env` मधील `OPENAI_API_KEY` तपासा. आता स्मार्ट फॉलबॅक सल्ला वापरला जात आहे.",
        "hi": "⚠️ OpenAI कोटा समाप्त हुआ या API key अमान्य है। `.env` में `OPENAI_API_KEY` जाँचें। अभी स्मार्ट फॉलबैक सलाह दी जा रही है।",
    }
    return msgs.get(lang, msgs["en"])


def _fallback_response(signals: dict, lang: str, child_name: str, scores: dict | None = None) -> str:
    """Structured fallback advice when AI/API is unavailable."""
    active = [k for k, v in signals.items() if v and k != "crisis"]
    name = child_name or ("your child" if lang == "en" else "तुमचे मूल" if lang == "mr" else "आपका बच्चा")

    if signals.get("crisis"):
        return {
            "en": f"🆘 **URGENT** — {name}'s messages suggest serious distress. Please DO NOT leave them alone.\n\n**Call immediately:** iCall (TISS): **9152987821** | Vandrevala Foundation: **1860-2662-345** (24/7, Free)\n\nStay calm, tell them: *'I'm here. I love you. We'll handle this together.'*",
            "mr": f"🆘 **तातडीचे** — {name} च्या बोलण्यात गंभीर ताणाची चिन्हे आहेत. त्यांना एकटे सोडू नका.\n\n**आत्ताच फोन करा:** iCall (TISS): **9152987821** | Vandrevala Foundation: **1860-2662-345** (२४/७, मोफत)\n\nशांत राहा, म्हणा: *'मी इथे आहे. मी तुझ्यावर प्रेम करतो. आपण एकत्र सोडवू.'*",
            "hi": f"🆘 **तत्काल** — {name} की बातों में गंभीर संकट के संकेत हैं। उन्हें अकेला मत छोड़ें।\n\n**अभी कॉल करें:** iCall (TISS): **9152987821** | Vandrevala Foundation: **1860-2662-345** (24/7, मुफ़्त)\n\nशांत रहें, कहें: *'मैं यहाँ हूँ। मैं तुमसे प्यार करता हूँ। हम मिलकर इसे संभालेंगे।'*",
        }.get(lang, "")

    if not active:
        return {
            "en": "Thank you for sharing. Could you tell me more? For example:\n- How long has this been going on?\n- What does a typical day look like for your child?\n- Any recent changes at home or school?\n\n*(Add your OpenAI API key in `.env` for full AI-powered analysis.)*",
            "mr": "सांगितल्याबद्दल धन्यवाद. अजून सांगाल का?\n- हे किती दिवसांपासून सुरू आहे?\n- तुमच्या मुलाचा एक सामान्य दिवस कसा असतो?\n- घरात किंवा शाळेत काही बदल झाले का?",
            "hi": "बताने के लिए धन्यवाद। क्या आप और बता सकते हैं?\n- यह कब से हो रहा है?\n- आपके बच्चे का एक सामान्य दिन कैसा होता है?\n- घर या स्कूल में कोई बदलाव हुआ?",
        }.get(lang, "")

    # Build structured fallback advice per signal
    advice_map = {
        "phone":     {"en": "**📱 Phone/Screen:** Set a family 'phone free' time — 8–9 PM daily, for everyone. Show curiosity: ask what they watch instead of banning it.", "mr": "**📱 फोन:** कुटुंबासाठी 'फोन-मुक्त' वेळ ठेवा — रोज रात्री ८-९. त्यांना विचारा ते काय बघतात.", "hi": "**📱 फोन:** परिवार के लिए 'फोन-मुक्त' समय तय करें — रोज़ रात 8-9। उनसे पूछें वे क्या देखते हैं।"},
        "academic":  {"en": "**📚 Studies:** Ask 'Which ONE subject needs help?' — not 'Why are your marks low?' Small targets rebuild confidence.", "mr": "**📚 अभ्यास:** विचारा 'कोणता एक विषय कठीण वाटतो?' — 'मार्क्स का कमी?' नाही. लहान उद्दिष्टे आत्मविश्वास वाढवतात.", "hi": "**📚 पढ़ाई:** पूछें 'कौन सा एक विषय कठिन लगता है?' — 'नंबर कम क्यों?' नहीं। छोटे लक्ष्य आत्मविश्वास बढ़ाते हैं।"},
        "sleep":     {"en": "**🌙 Sleep:** Sleep deprivation cuts memory retention by 40%. Introduce a family 11 PM lights-out rule — model it yourself.", "mr": "**🌙 झोप:** झोपेच्या कमतरतेमुळे स्मृती ४०% कमी होते. संपूर्ण कुटुंबासाठी रात्री ११ ला दिवे बंद नियम करा.", "hi": "**🌙 नींद:** नींद की कमी से याददाश्त 40% कम होती है। पूरे परिवार के लिए रात 11 बजे 'लाइट्स आउट' नियम बनाएं।"},
        "isolation": {"en": "**🚪 Isolation:** Don't force interaction. Knock once: 'I made chai — 5 minutes?' No study talk. Just connection.", "mr": "**🚪 एकांत:** जबरदस्ती नको. एकदा दार ठोका: 'चहा केला — ५ मिनिटे?' अभ्यासाबद्दल काहीच नाही.", "hi": "**🚪 अकेलापन:** जबरदस्ती न करें। एक बार दस्तक: 'चाय बनाई — 5 मिनट?' पढ़ाई की बात नहीं, बस जुड़ाव।"},
        "anger":     {"en": "**😤 Irritability:** Wait for a calm moment, then say: 'I noticed you seemed stressed. I'm on your side — anything going on?'", "mr": "**😤 राग:** शांत क्षणाची वाट पाहा, मग म्हणा: 'तू ताणात दिसत होतास. मी तुझ्या बाजूने आहे — काही सांगायचे आहे का?'", "hi": "**😤 गुस्सा:** शांत समय का इंतज़ार करें, फिर: 'मुझे लगा तुम तनाव में थे। मैं तुम्हारे साथ हूँ — कुछ है?'"},
        "sad":       {"en": "**😢 Sadness:** Sit near them without advice. Say: 'I see you're hurting. I'm not going anywhere.' If sadness persists 2+ weeks, consult a counsellor.", "mr": "**😢 दुःख:** त्यांच्या जवळ बसा. म्हणा: 'मला दिसते तू दुखावलास. मी कुठेही जात नाही.' २+ आठवडे राहिल्यास समुपदेशक भेटा.", "hi": "**😢 उदासी:** पास बैठें, सलाह मत दें। कहें: 'मैं देख रहा हूँ तुम दुखी हो। मैं यहीं हूँ।' 2+ हफ्ते रहे तो काउंसलर से मिलें।"},
        "career":    {"en": "**🎓 Career pressure:** Ask 'What do YOU want to do? Not what I want — your dream.' Research 3 career paths together.", "mr": "**🎓 करिअर:** विचारा 'तुला स्वतःला काय करायचे? माझे नाही — तुझे स्वप्न काय?' एकत्र ३ करिअर पर्याय शोधा.", "hi": "**🎓 करियर:** पूछें 'तुम खुद क्या करना चाहते हो? मेरी नहीं, तुम्हारी ख्वाहिश?' मिलकर 3 विकल्प देखें।"},
        "confidence":{"en": "**💪 Confidence:** Catch them doing ONE thing right daily and name it specifically: 'The way you explained that — that's clear thinking.'", "mr": "**💪 आत्मविश्वास:** रोज एक गोष्ट बरोबर केल्याचे सांगा: 'तू ते कसे समजावलेस — हे स्पष्ट विचार आहे.'", "hi": "**💪 आत्मविश्वास:** रोज़ एक काम सही करने पर कहें: 'जैसे तुमने वो समझाया — यह साफ सोच है।'"},
    }

    lines = []
    for sig in active:
        if sig in advice_map:
            lines.append(advice_map[sig].get(lang, advice_map[sig]["en"]))

    header = {
        "en": f"Here's what I'm picking up from your description of {name}:\n\n",
        "mr": f"{name} बद्दलच्या तुमच्या वर्णनातून मला हे समजते:\n\n",
        "hi": f"{name} के बारे में आपके विवरण से मुझे यह समझ आता है:\n\n",
    }.get(lang, "")

    disclaimer = {
        "en": "\n\n> ⚠️ *This is general guidance. For persistent or serious concerns, please consult a certified psychologist or school counsellor. This is NOT a clinical diagnosis.*",
        "mr": "\n\n> ⚠️ *हे सामान्य मार्गदर्शन आहे. गंभीर समस्यांसाठी प्रमाणित मानसशास्त्रज्ञाचा सल्ला घ्या. हे वैद्यकीय निदान नाही.*",
        "hi": "\n\n> ⚠️ *यह सामान्य मार्गदर्शन है। गंभीर समस्याओं के लिए प्रमाणित मनोवैज्ञानिक से परामर्श लें। यह नैदानिक निदान नहीं है।*",
    }.get(lang, "")

    return header + "\n\n".join(lines) + disclaimer


# ─── UI helpers ────────────────────────────────────────────────────────────────
CHAT_UI = {
    "title": {
        "en": "🤖 AI Parent Advisor — Powered by OpenAI",
        "mr": "🤖 AI पालक सल्लागार — OpenAI द्वारे",
        "hi": "🤖 AI पालक सलाहकार — OpenAI द्वारा",
    },
    "subtitle": {
        "en": "Describe your child's behaviour and get personalised, psychology-backed advice.",
        "mr": "तुमच्या मुलाच्या वागणुकीचे वर्णन करा आणि वैयक्तिक, मनोविज्ञान-आधारित सल्ला मिळवा.",
        "hi": "अपने बच्चे के व्यवहार का वर्णन करें और व्यक्तिगत, मनोविज्ञान-आधारित सलाह पाएं।",
    },
    "placeholder": {
        "en": "Example: 'My son is intelligent but uses phone 8 hours a day and exam marks dropped...' (English / मराठी / हिंदी)",
        "mr": "उदा: 'माझा मुलगा हुशार आहे पण दिवसभर फोन वापरतो, परीक्षेचे मार्क्स कमी झाले...' (मराठी / English / हिंदी)",
        "hi": "उदाहरण: 'मेरा बेटा होशियार है लेकिन दिन भर फोन चलाता है, परीक्षा में नंबर कम हो गए...' (हिंदी / मराठी / English)",
    },
    "send": {"en": "Send ➤", "mr": "पाठवा ➤", "hi": "भेजें ➤"},
    "clear": {"en": "🗑️ Clear Chat", "mr": "🗑️ साफ करा", "hi": "🗑️ साफ करें"},
    "thinking": {"en": "🧠 Analysing...", "mr": "🧠 विश्लेषण होत आहे...", "hi": "🧠 विश्लेषण हो रहा है..."},
    "no_key_warning": {
        "en": "⚠️ **OpenAI API key not set.** Add your key to `.env` → `OPENAI_API_KEY=sk-...` for full AI responses. Using smart fallback for now.",
        "mr": "⚠️ **OpenAI API की नाही.** `.env` मध्ये `OPENAI_API_KEY=sk-...` जोडा. आता स्मार्ट फॉलबॅक वापरले जात आहे.",
        "hi": "⚠️ **OpenAI API key नहीं है।** `.env` में `OPENAI_API_KEY=sk-...` जोड़ें। अभी स्मार्ट फॉलबैक उपयोग हो रहा है।",
    },
    "greeting": {
        "en": (
            "👋 Hello! I'm your **AI Parent Advisor**, powered by OpenAI.\n\n"
            "Tell me about your child — their **behaviour**, **mood**, **studies**, **habits**, "
            "or anything that worries you. You can type in **English, Marathi, or Hindi**.\n\n"
            "I'll analyse what you share and give you **personalised, psychology-backed advice** "
            "on how to understand and support your child.\n\n"
            "*Example: 'Maza mulga intelligent ahe pan phone jasta vaparto, exam madhe 65% yetat, "
            "confidence kami ahe.'*"
        ),
        "mr": (
            "👋 नमस्कार! मी तुमचा **AI पालक सल्लागार** आहे, OpenAI द्वारे चालवलेला.\n\n"
            "मला तुमच्या मुलाबद्दल सांगा — त्यांचे **वागणे**, **मनःस्थिती**, **अभ्यास**, **सवयी**, "
            "किंवा जे काही तुम्हाला काळजी वाटते. **मराठी, इंग्रजी किंवा हिंदी** मध्ये लिहा.\n\n"
            "मी तुम्ही सांगितलेले विश्लेषण करेन आणि **वैयक्तिक, मनोविज्ञान-आधारित सल्ला** देईन."
        ),
        "hi": (
            "👋 नमस्ते! मैं आपका **AI पालक सलाहकार** हूँ, OpenAI द्वारा संचालित।\n\n"
            "मुझे अपने बच्चे के बारे में बताएं — उनका **व्यवहार**, **मूड**, **पढ़ाई**, **आदतें**, "
            "या जो भी आपको चिंता करता है। **हिंदी, मराठी या अंग्रेज़ी** में टाइप करें।\n\n"
            "मैं विश्लेषण करूँगा और आपको **व्यक्तिगत, मनोविज्ञान-आधारित सलाह** दूँगा।"
        ),
    },
}


def has_api_key() -> bool:
    key = os.environ.get("OPENAI_API_KEY", "")
    return bool(key) and key != "your_openai_api_key_here"
