// language-switcher.js
class LanguageSwitcher {
  constructor() {
    this.init();
  }

  init() {
    // Создаем HTML для переключателя
    const switcherHTML = `
      <div class="language-switcher" id="globalLanguageSwitcher">
        <div class="current-lang" onclick="toggleLangDropdown()">
          <i class='bx bx-globe'></i>
          <span id="currentLangDisplay">${window.langManager.getLangName()}</span>
          <i class='bx bx-chevron-down' id="langArrow"></i>
        </div>
        <div class="lang-dropdown" id="langDropdown">
          <div class="lang-option" data-lang="en" onclick="changeGlobalLanguage('en')">
            <span>🇬🇧 English</span>
          </div>
          <div class="lang-option" data-lang="ru" onclick="changeGlobalLanguage('ru')">
            <span>🇷🇺 Русский</span>
          </div>
          <div class="lang-option" data-lang="kz" onclick="changeGlobalLanguage('kz')">
            <span>🇰🇿 Қазақша</span>
          </div>
        </div>
      </div>
    `;

    // Добавляем стили
    this.addStyles();

    // Вставляем переключатель в нужное место (например, в header)
    document.addEventListener('DOMContentLoaded', () => {
      const header = document.querySelector('header');
      
      if (header && !document.getElementById('globalLanguageSwitcher')) {
        header.insertAdjacentHTML('afterbegin', switcherHTML);
      }
    });
  }
  addStyles() {
    const styles = `
      .language-switcher {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
      }
      
      .current-lang {
        background: white;
        padding: 8px 16px;
        border-radius: 30px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border: 1px solid #86efac;
      }
      
      .lang-dropdown {
        position: absolute;
        top: 100%;
        right: 0;
        margin-top: 5px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        border: 1px solid #e5e7eb;
        opacity: 0;
        visibility: hidden;
        transform: translateY(-10px);
        transition: all 0.2s;
      }
      
      .lang-dropdown.show {
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
      }
      
      .lang-option {
        padding: 10px 20px;
        cursor: pointer;
        white-space: nowrap;
      }
      
      .lang-option:hover {
        background: #f3f4f6;
      }
      
      .lang-option:first-child {
        border-radius: 12px 12px 0 0;
      }
      
      .lang-option:last-child {
        border-radius: 0 0 12px 12px;
      }
    `;

    const styleSheet = document.createElement("style");
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);
  }
}

// Глобальные функции для переключателя
window.toggleLangDropdown = function() {
  const dropdown = document.getElementById('langDropdown');
  const arrow = document.getElementById('langArrow');
  dropdown.classList.toggle('show');
  arrow.classList.toggle('bx-chevron-up');
};

window.changeGlobalLanguage = function(lang) {
  window.langManager.setLanguage(lang);
  document.getElementById('currentLangDisplay').textContent = window.langManager.getLangName();
  document.getElementById('langDropdown').classList.remove('show');
  
  // Перезагружаем страницу для применения переводов
  // (или обновляем контент динамически)
  location.reload();
};

// Закрытие дропдауна при клике вне
document.addEventListener('click', function(event) {
  const switcher = document.getElementById('globalLanguageSwitcher');
  if (switcher && !switcher.contains(event.target)) {
    const dropdown = document.getElementById('langDropdown');
    const arrow = document.getElementById('langArrow');
    if (dropdown) {
      dropdown.classList.remove('show');
      if (arrow) arrow.classList.remove('bx-chevron-up');
    }
  }
});

// Инициализация
new LanguageSwitcher();