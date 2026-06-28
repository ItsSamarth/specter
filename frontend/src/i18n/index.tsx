import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { loadUiPreferences, subscribeUiPreferences, type UiPreferences } from "../utils/preferences";
import en from "./en.json";
import zh from "./zh.json";

type Lang = "zh-CN" | "en-US";
type Translations = Record<string, string>;
export type TFunction = (key: string, params?: Record<string, string>, fallback?: string) => string;

const TRANSLATIONS: Record<Lang, Translations> = {
  "en-US": en as Translations,
  "zh-CN": zh as Translations,
};

/* ── Global singleton (for non-React code such as taskLabels) ── */

let _currentLang: Lang = resolveInitialLang();
let _currentTranslations: Translations = TRANSLATIONS[_currentLang];

function resolveInitialLang(): Lang {
  try {
    const preferences = loadUiPreferences();
    return preferences.language === "zh-CN" ? "zh-CN" : "en-US";
  } catch {
    return "en-US";
  }
}

/**
 * Global translation function — callable outside React components.
 *   t("key")                -> translated text
 *   t("key", {a:"1"})       -> substitute the {a} placeholder
 *   t("key", {}, "fallback") -> use fallback when the key is missing
 *
 * Fallback chain: current language → English → the key itself (or fallback)
 */
export function t(key: string, params?: Record<string, string>, fallback?: string): string {
  let text = _currentTranslations[key];
  if (text === undefined) {
    text = TRANSLATIONS["en-US"][key];
  }
  if (text === undefined) {
    text = fallback ?? key;
  }
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      text = text.replace(`{${k}}`, String(v));
    }
  }
  return text;
}

/* ── React Context ── */

interface I18nContextValue {
  lang: Lang;
  t: (key: string, params?: Record<string, string>, fallback?: string) => string;
}

const I18nContext = createContext<I18nContextValue>({
  lang: _currentLang,
  t,
});

/**
 * React Hook — components call `const { t, lang } = useT()` to get the
 * translation function. Re-renders automatically when the language changes.
 */
export function useT(): I18nContextValue {
  return useContext(I18nContext);
}

/**
 * I18nProvider — wraps <App /> in main.tsx.
 * Watches preference changes and updates the Context and global singleton
 * whenever the language switches.
 */
export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLang] = useState<Lang>(_currentLang);

  useEffect(() => {
    const unsubscribe = subscribeUiPreferences((preferences: UiPreferences) => {
      const nextLang: Lang = preferences.language === "zh-CN" ? "zh-CN" : "en-US";
      if (nextLang !== _currentLang) {
        _currentLang = nextLang;
        _currentTranslations = TRANSLATIONS[nextLang];
        setLang(nextLang);
      }
    });
    return unsubscribe;
  }, []);

  const value = useMemo<I18nContextValue>(() => {
    const tFn: TFunction = (key, params, fallback) => {
      let text = TRANSLATIONS[lang][key];
      if (text === undefined) text = TRANSLATIONS["en-US"][key];
      if (text === undefined) text = fallback ?? key;
      if (params) {
        for (const [k, v] of Object.entries(params)) text = text.replace(`{${k}}`, String(v));
      }
      return text;
    };
    return { lang, t: tFn };
  }, [lang]);

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}
