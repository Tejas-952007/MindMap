import { createContext, useContext, useState, ReactNode } from "react";

export type Language = "en" | "mr" | "hi";
export type Role = "student" | "parent" | "teacher";

export const translations = {
  en: {
    appName: "MindMap",
    tagline: "Understand Your Mind. Guide Your Future.",
    nav: {
      home: "Home",
      insights: "Global Context",
      assessment: "Assessment",
      results: "Results",
      report: "Full Report",
      parents: "Parent Guide",
      teachers: "Teacher Dashboard",
      about: "About",
    },
    role: { student: "Student", parent: "Parent", teacher: "Teacher" },
    startAssessment: "Start Assessment",
    language: "Language",
    privacy: "100% Private",
    multilingual: "Trilingual",
  },
  mr: {
    appName: "MindMap",
    tagline: "आपले मन समजून घ्या. भविष्य घडवा.",
    nav: {
      home: "मुख्यपृष्ठ",
      insights: "जागतिक संदर्भ",
      assessment: "मूल्यांकन",
      results: "निकाल",
      report: "पूर्ण अहवाल",
      parents: "पालक मार्गदर्शन",
      teachers: "शिक्षक डॅशबोर्ड",
      about: "माहिती",
    },
    role: { student: "विद्यार्थी", parent: "पालक", teacher: "शिक्षक" },
    startAssessment: "मूल्यांकन सुरू करा",
    language: "भाषा",
    privacy: "१००% गोपनीय",
    multilingual: "त्रिभाषिक",
  },
  hi: {
    appName: "MindMap",
    tagline: "अपने मन को समझें। भविष्य बनाएं।",
    nav: {
      home: "होम",
      insights: "वैश्विक संदर्भ",
      assessment: "मूल्यांकन",
      results: "परिणाम",
      report: "पूरी रिपोर्ट",
      parents: "अभिभावक मार्गदर्शिका",
      teachers: "शिक्षक डैशबोर्ड",
      about: "जानकारी",
    },
    role: { student: "छात्र", parent: "अभिभावक", teacher: "शिक्षक" },
    startAssessment: "मूल्यांकन शुरू करें",
    language: "भाषा",
    privacy: "१००% गोपनीय",
    multilingual: "त्रिभाषिक",
  },
};

interface AppContextType {
  language: Language;
  setLanguage: (l: Language) => void;
  role: Role;
  setRole: (r: Role) => void;
  t: (typeof translations)["en"];
}

const AppContext = createContext<AppContextType | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const [language, setLanguage] = useState<Language>("en");
  const [role, setRole] = useState<Role>("student");

  const t = translations[language];

  return (
    <AppContext.Provider value={{ language, setLanguage, role, setRole, t }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be inside AppProvider");
  return ctx;
}
