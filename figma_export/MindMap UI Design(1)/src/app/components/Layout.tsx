import { useState } from "react";
import { Outlet, NavLink } from "react-router";
import { Menu, X, ChevronDown, Globe } from "lucide-react";
import { useApp, Language, Role } from "../context/AppContext";

const BG_DARK = "#0F0F1A";
const BG_CARD = "#1A1A2E";
const BORDER = "rgba(255,255,255,0.07)";
const TEXT = "#E2E8F0";
const MUTED = "#94A3B8";
const INDIGO = "#4F46E5";

function NavItem({ to, emoji, label, end }: { to: string; emoji: string; label: string; end?: boolean }) {
  return (
    <NavLink
      to={to}
      end={end}
      className={({ isActive }) =>
        `flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group relative ${isActive ? "" : "hover:bg-white/5"}`
      }
      style={({ isActive }) => ({
        background: isActive ? "linear-gradient(135deg, rgba(79,70,229,0.25), rgba(124,58,237,0.15))" : undefined,
        border: isActive ? `1px solid rgba(79,70,229,0.3)` : "1px solid transparent",
        color: isActive ? "#A5B4FC" : MUTED,
      })}
    >
      {({ isActive }) => (
        <>
          {isActive && (
            <div className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 rounded-r-full"
              style={{ backgroundColor: INDIGO }} />
          )}
          <span className="text-base">{emoji}</span>
          <span className="text-xs font-medium">{label}</span>
        </>
      )}
    </NavLink>
  );
}

export function Layout() {
  const { t, language, setLanguage, role, setRole } = useApp();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [langOpen, setLangOpen] = useState(false);
  const [roleOpen, setRoleOpen] = useState(false);

  const langs: { code: Language; flag: string; name: string }[] = [
    { code: "en", flag: "🇬🇧", name: "English" },
    { code: "mr", flag: "🇮🇳", name: "मराठी" },
    { code: "hi", flag: "🇮🇳", name: "हिंदी" },
  ];

  const roles: { code: Role; emoji: string }[] = [
    { code: "student", emoji: "🎓" },
    { code: "parent", emoji: "👨‍👩‍👧" },
    { code: "teacher", emoji: "👩‍🏫" },
  ];

  const navItems = [
    { to: "/", emoji: "🏠", label: t.nav.home, end: true },
    { to: "/insights", emoji: "🌍", label: t.nav.insights },
    { to: "/assessment", emoji: "📝", label: t.nav.assessment },
    { to: "/results", emoji: "📊", label: t.nav.results },
    { to: "/report", emoji: "📑", label: t.nav.report },
    { to: "/parents", emoji: "👨‍👩‍👧", label: t.nav.parents },
    { to: "/teachers", emoji: "👩‍🏫", label: t.nav.teachers },
    { to: "/about", emoji: "ℹ️", label: t.nav.about },
  ];

  const SidebarContent = () => (
    <div className="flex flex-col h-full" style={{ background: "linear-gradient(180deg, #111827 0%, #0F0F1A 100%)" }}>
      {/* Logo */}
      <div className="px-5 py-5 border-b" style={{ borderColor: BORDER }}>
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center text-lg flex-shrink-0"
            style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)" }}>
            🧠
          </div>
          <div>
            <div style={{ color: TEXT, fontFamily: "Space Grotesk, sans-serif", fontWeight: 700, fontSize: "1.05rem", letterSpacing: "-0.02em" }}>
              MindMap
            </div>
            <div style={{ color: MUTED, fontSize: "0.65rem" }}>AI Mental Health Platform</div>
          </div>
        </div>
      </div>

      {/* Selectors */}
      <div className="px-4 py-3 space-y-2 border-b" style={{ borderColor: BORDER }}>
        {/* Role Selector */}
        <div className="relative">
          <button
            onClick={() => { setRoleOpen(!roleOpen); setLangOpen(false); }}
            className="w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs transition-all"
            style={{ backgroundColor: "rgba(79,70,229,0.1)", border: "1px solid rgba(79,70,229,0.2)", color: TEXT }}
          >
            <span className="flex items-center gap-2">
              {roles.find(r => r.code === role)?.emoji}
              <span>{t.role[role]}</span>
            </span>
            <ChevronDown className="w-3.5 h-3.5" style={{ color: MUTED }} />
          </button>
          {roleOpen && (
            <div className="absolute left-0 right-0 top-full mt-1 rounded-xl overflow-hidden z-50 shadow-xl"
              style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
              {roles.map(r => (
                <button key={r.code} onClick={() => { setRole(r.code); setRoleOpen(false); }}
                  className="w-full flex items-center gap-2 px-3 py-2 text-xs transition-colors hover:bg-white/5"
                  style={{ color: role === r.code ? "#A5B4FC" : MUTED }}>
                  {r.emoji} {t.role[r.code]}
                  {role === r.code && <span className="ml-auto">✓</span>}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Language Selector */}
        <div className="relative">
          <button
            onClick={() => { setLangOpen(!langOpen); setRoleOpen(false); }}
            className="w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs transition-all"
            style={{ backgroundColor: "rgba(6,182,212,0.08)", border: "1px solid rgba(6,182,212,0.15)", color: TEXT }}
          >
            <span className="flex items-center gap-2">
              <Globe className="w-3.5 h-3.5" style={{ color: "#06B6D4" }} />
              <span>{langs.find(l => l.code === language)?.name}</span>
            </span>
            <ChevronDown className="w-3.5 h-3.5" style={{ color: MUTED }} />
          </button>
          {langOpen && (
            <div className="absolute left-0 right-0 top-full mt-1 rounded-xl overflow-hidden z-50 shadow-xl"
              style={{ backgroundColor: BG_CARD, border: `1px solid ${BORDER}` }}>
              {langs.map(l => (
                <button key={l.code} onClick={() => { setLanguage(l.code); setLangOpen(false); }}
                  className="w-full flex items-center gap-2 px-3 py-2 text-xs transition-colors hover:bg-white/5"
                  style={{ color: language === l.code ? "#06B6D4" : MUTED }}>
                  {l.flag} {l.name}
                  {language === l.code && <span className="ml-auto">✓</span>}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto" style={{ scrollbarWidth: "none" }}>
        <div className="px-2 pb-2" style={{ color: MUTED, fontSize: "0.6rem", fontWeight: 600, letterSpacing: "0.08em", textTransform: "uppercase" }}>
          Navigation
        </div>
        {navItems.map(item => (
          <NavItem key={item.to} {...item} />
        ))}
      </nav>

      {/* Footer */}
      <div className="px-4 py-4 border-t" style={{ borderColor: BORDER }}>
        <div className="flex items-center gap-2 px-3 py-2 rounded-xl"
          style={{ backgroundColor: "rgba(255,255,255,0.03)", border: `1px solid ${BORDER}` }}>
          <div className="w-7 h-7 rounded-lg flex items-center justify-center text-sm flex-shrink-0"
            style={{ background: "linear-gradient(135deg, #4F46E5, #7C3AED)" }}>
            {roles.find(r => r.code === role)?.emoji}
          </div>
          <div>
            <div style={{ color: TEXT, fontSize: "0.75rem", fontWeight: 500 }}>
              {role === "student" ? "Arjun Patil" : role === "parent" ? "Priya Deshmukh" : "Ms. Kavita Joshi"}
            </div>
            <div style={{ color: MUTED, fontSize: "0.6rem" }}>Pune, Maharashtra</div>
          </div>
        </div>
        <div className="mt-2 text-center" style={{ color: MUTED, fontSize: "0.6rem" }}>
          MindMap v2.0 • Pune, Maharashtra 🇮🇳
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex h-screen overflow-hidden" style={{ backgroundColor: BG_DARK }}>
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex flex-col w-56 flex-shrink-0" style={{ borderRight: `1px solid ${BORDER}` }}>
        <SidebarContent />
      </aside>

      {/* Mobile Overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setSidebarOpen(false)} />
          <aside className="absolute left-0 top-0 bottom-0 w-64 z-10" style={{ borderRight: `1px solid ${BORDER}` }}>
            <button onClick={() => setSidebarOpen(false)}
              className="absolute top-4 right-4 p-1.5 rounded-lg z-20"
              style={{ backgroundColor: "rgba(255,255,255,0.07)", color: TEXT }}>
              <X className="w-4 h-4" />
            </button>
            <SidebarContent />
          </aside>
        </div>
      )}

      {/* Main Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Mobile Header */}
        <header className="lg:hidden flex items-center justify-between px-4 py-3 flex-shrink-0"
          style={{ backgroundColor: BG_CARD, borderBottom: `1px solid ${BORDER}` }}>
          <button onClick={() => setSidebarOpen(true)} className="p-2 rounded-xl"
            style={{ backgroundColor: "rgba(255,255,255,0.05)", color: TEXT }}>
            <Menu className="w-5 h-5" />
          </button>
          <div className="flex items-center gap-2">
            <span className="text-lg">🧠</span>
            <span style={{ color: TEXT, fontFamily: "Space Grotesk, sans-serif", fontWeight: 700 }}>MindMap</span>
          </div>
          <button onClick={() => setLangOpen(!langOpen)}
            className="p-2 rounded-xl text-xs"
            style={{ backgroundColor: "rgba(79,70,229,0.15)", color: "#A5B4FC" }}>
            {language.toUpperCase()}
          </button>
        </header>

        <main className="flex-1 overflow-y-auto" style={{ backgroundColor: BG_DARK }}>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
