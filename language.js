// language.js
class LanguageManager {
  constructor() {
    this.currentLang = localStorage.getItem('appLanguage') || 'en';
    this.observers = [];
  }

  // Получить перевод
  t(key) {
    const keys = key.split('.');
    let value = translations[this.currentLang];
    
    for (const k of keys) {
      if (value && value[k]) {
        value = value[k];
      } else {
        console.warn(`Translation missing for key: ${key} in ${this.currentLang}`);
        return key;
      }
    }
    
    return value;
  }

  // Сменить язык
  setLanguage(lang) {
    if (translations[lang]) {
      this.currentLang = lang;
      localStorage.setItem('appLanguage', lang);
      this.notifyObservers();
      this.updateHtmlLang();
      return true;
    }
    return false;
  }

  // Обновить атрибут lang в HTML
  updateHtmlLang() {
    document.documentElement.lang = this.currentLang;
  }

  // Подписаться на изменения языка
  subscribe(callback) {
    this.observers.push(callback);
  }

  // Уведомить всех подписчиков
  notifyObservers() {
    this.observers.forEach(callback => callback(this.currentLang));
  }

  getCurrentLang() {
    return this.currentLang;
  }

  getLangName(lang = this.currentLang) {
    const names = {
      'en': 'English',
      'ru': 'Русский',
      'kz': 'Қазақша'
    };
    return names[lang] || lang;
  }
}

// Создаем глобальный экземпляр
window.langManager = new LanguageManager();

// Функция-помощник для перевода
function __(key) {
  return window.langManager.t(key);
}