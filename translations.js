const translations = {
  en: {
    // Общие
    appName: 'DoubleW',
    saveWater: 'Save water. Save world.',
    
    // Навигация
    navHome: 'Home',
    navChat: 'Chat',
    navProfile: 'Profile',
    
    // Страница профиля (profile.html)
    profile: {
      title: 'Profile',
      subtitle: 'Manage your account settings',
      chooseAvatar: 'Choose your avatar',
      yourImpact: 'Your Impact',
      daysTracked: 'Days tracked',
      waterSaved: 'Water saved',
      appSettings: 'App Settings',
      privacy: 'Privacy and Security',
      help: 'Help',
      language: 'Language',
      signOut: 'Sign Out',
      farmer: 'Farmer'
    },
    
    // Страница чата (chat.html)
    chat: {
      title: 'Chat',
      subtitle: 'Connect with farmers and get AI assistance',
      farmerChat: 'Farmers community',
      aiAssistant: 'AI assistant',
      statusAI: 'Online',
      quickTips: 'Quick tips',
      share: '• Share your irrigation experiences with other farmers',
      ask:'• Ask the AI about optimal watering schedules',
      learn: '• Learn about water conservation techniques',
      onlineFarmers: 'Online farmers',
      welcomeMessage: "Hello! I'm your AI irrigation assistant. I can help you with questions about watering schedules, crop care, and water conservation. How can I help you today?",
      suggestedQuestions: "Suggested questions:",
      bestTimeToWater: "When is the best time to water?",
      saveWaterTips: "How can I save water?",
      typeMessage: "Ask me anything about irrigation...",
      errorMessage: "Sorry, something went wrong. Please try again later."
    },
    
    // frontend.html
    calculator: {
      title: 'Irrigation Calculator',
      subtitle: 'Calculate water needed for today',
      selectDate: 'Select date',
      calculate: 'Calculate',
      result: 'Result',
      waterNeeded: 'Water needed',
      phase: 'Growth phase',
      explanation: 'Explanation',
      wateringLog: 'Irrigation Calendar', //'Журнал полива'
      calculationDate: 'Calculation Date:', //'Дата расчета:'
      calculate: 'Calculate Irrigation', //'Рассчитать полив'
      recommendedWatering: 'Recommended Watering', //'Рекомендуемый полив'
      phase: 'Phase', //'Фаза'
      progress: 'Progress', //'Прогресс'
      daysFromSowing: 'Days from Sowing', //'Дней после посева'
      lastWatered: 'Last Watered', //'Последний полив'
      daysAgo: 'days ago', //'дней назад'
      noSowingDate: 'Please set sowing date in profile', //'Укажите дату посева в профиле'
      invalidSowingDate: 'Invalid sowing date format', //'Неверный формат даты посева'
      selectWateringDate: 'Please select at least one watering date', //'Выберите дату полива'
      pleaseLogin: 'Please log in', //'Войдите в аккаунт'
      sessionExpired: 'Session expired. Please login again.' //'Сессия истекла'
    },

    insights: {
      title: 'Insights',
      readMore: 'Read details'
    },

    
    
    // Страница логина (login.html)
    login: {
      title: 'Welcome Back',
      subtitle: 'Log in to manage your irrigation efficiently',
      email: 'Email',
      password: 'Password',
      remember: 'Remember me',
      forgot: 'Forgot password?',
      login: 'Log In',
      noAccount: "Don't have an account?",
      signUp: 'Sign up',
      info: 'By logging in, you agree to our smart irrigation practices<br>for a more sustainable future',
      fillFields: 'Please fill in email and password',
      loggingIn: 'Logging in...',
      success: 'Login successful!',
      invalid: 'Invalid email or password',
      connectionError: 'Could not connect to server. Please check your internet.'
    },

    register: {
      title: 'Create Account',
      subtitle: 'Join us in making irrigation smarter and more sustainable',
      fullName: 'Full Name',
      email: 'Email',
      password: 'Password',
      haveAccount: 'Already have an account?',
      login: 'Log in',
      signUp: 'Continue',
      fillFields: 'Please fill all fields',
      invalidEmail: 'Please enter a valid email address',
      passwordLength: 'Password must be at least 6 characters long',
      creating: 'Creating...',
      success: 'Account created successfully!',
      failed: 'Registration failed',
      serverError: 'Server error. Please try again later.'
    },
    
    // Страница календаря (calendar.html)
    calendar: {
      title: 'Last time you watered',
      subtitle: 'Select the date of your most recent irrigation',
      complete: 'Complete Registration'
    }
  },
  
  ru: {
    saveWater: 'Экономьте воду. Спасите мир.',
    
    // Навигация
    navHome: 'Главная',
    navChat: 'Чат',
    navProfile: 'Профиль',
    
    // Страница профиля
    profile: {
      title: 'Профиль',
      subtitle: 'Управление настройками аккаунта',
      yourImpact: 'Ваш вклад',
      daysTracked: 'Дней отслежено',
      waterSaved: 'Воды сохранено',
      appSettings: 'Настройки приложения',
      privacy: 'Конфиденциальность',
      help: 'Помощь',
      language: 'Язык',
      signOut: 'Выйти',
      farmer: 'Фермер',
      chooseAvatar: 'Выберите аватар'
    },
    
    // Страница чата
    chat: {

      title: 'Чат сообщества',
      subtitle: 'Общайтесь с другими фермерами',
      farmerChat: 'Чат фермеров',
      aiAssistant: 'ИИ Помощник',
      onlineFarmers: 'Фермеры онлайн',
      statusAI: 'В сети',
      quickTips: 'Краткие советы',
      share: '• Поделитесь своим опытом в области орошения с другими фермерами',
      ask:'• Спросите у ИИ об оптимальном графике полива.',
      learn: '• Узнайте о методах экономии воды.',
      welcomeMessage: "Здравствуйте! Я ваш AI-помощник по поливу. Я могу помочь с вопросами о графике полива, уходе за культурами и экономии воды. Чем я могу помочь вам сегодня?",
      suggestedQuestions: "Рекомендуемые вопросы:",
      bestTimeToWater: "Когда лучше всего поливать?",
      saveWaterTips: "Как экономить воду?",
      typeMessage: "Спросите меня о поливе...",
      errorMessage: "Извините, что-то пошло не так. Пожалуйста, попробуйте позже."
    },
    
    // Страница калькулятора
    calculator: {
      title: 'Калькулятор полива',
      subtitle: 'Рассчитайте необходимое количество воды на сегодня',
      selectDate: 'Выберите дату',
      result: 'Результат',
      waterNeeded: 'Необходимо воды',
      phase: 'Фаза роста',
      explanation: 'Объяснение',
      wateringLog: 'Журнал полива',
      calculationDate: 'Дата расчета:',
      calculate: 'Рассчитать полив',
      recommendedWatering: 'Рекомендуемый полив',
      progress: 'Прогресс',
      daysFromSowing: 'Дней после посева',
      lastWatered: 'Последний полив',
      daysAgo: 'дней назад',
      noSowingDate: 'Укажите дату посева в профиле',
      invalidSowingDate: 'Неверный формат даты посева',
      selectWateringDate: 'Выберите дату полива',
      pleaseLogin: 'Войдите в аккаунт',
      sessionExpired: 'Сессия истекла. Пожалуйста, войдите заново.'
    },

    insights: {
      title: 'Статьи и советы',
      readMore: 'Подробнее'
    },
    
    // Страница логина
    login: {
      title: 'С возвращением',
      subtitle: 'Войдите для эффективного управления поливом',
      email: 'Эл. почта',
      password: 'Пароль',
      remember: 'Запомнить меня',
      forgot: 'Забыли пароль?',
      login: 'Войти',
      noAccount: 'Нет аккаунта?',
      signUp: 'Регистрация',
      info: 'Входя в систему, вы соглашаетесь с нашими методами умного полива<br>для устойчивого будущего',
      fillFields: 'Пожалуйста, заполните email и пароль',
      loggingIn: 'Вход...',
      success: 'Вход выполнен успешно!',
      invalid: 'Неверный email или пароль',
      connectionError: 'Не удалось подключиться к серверу. Проверьте интернет.'
    },

    register: {
      title: 'Создать аккаунт',
      subtitle: 'Присоединяйтесь к нам, чтобы сделать полив умнее и устойчивее',
      fullName: 'Полное имя',
      email: 'Эл. почта',
      password: 'Пароль',
      haveAccount: 'Уже есть аккаунт?',
      login: 'Войти',
      signUp: 'Продолжить',
      fillFields: 'Пожалуйста, заполните все поля',
      invalidEmail: 'Введите корректный email адрес',
      passwordLength: 'Пароль должен содержать минимум 6 символов',
      creating: 'Создание...',
      success: 'Аккаунт успешно создан!',
      failed: 'Ошибка регистрации',
      serverError: 'Ошибка сервера. Пожалуйста, попробуйте позже.'
    },
    
    // Страница календаря
    calendar: {
      title: 'Последний полив',
      subtitle: 'Выберите дату последнего полива',
      complete: 'Завершить регистрацию'
    }
  },
  
  kz: {
    saveWater: 'Суды үнемде. Әлемді сақта.',
    
    // Страница профиля
    profile: {
      title: 'Профиль',
      subtitle: 'Парақша параметрлерін басқару',
      yourImpact: 'Сіздің үлесіңіз',
      daysTracked: 'Бақыланған күндер',
      waterSaved: 'Үнемделген су',
      appSettings: 'Қолданба параметрлері',
      privacy: 'Құпиялылық',
      help: 'Көмек',
      language: 'Тіл',
      signOut: 'Шығу',
      farmer: 'Фермер',
      chooseAvatar: 'Аватарды таңдаңыз'
    },
    
    // Страница чата
    chat: {
      quickTips: 'Пайдалы кеңестер',
      share: '• Суару тәжірибеңізбен басқа фермерлермен бөлісіңіз',
      ask: '• Жасанды интеллектен оңтайлы суару кестесі туралы сұраңыз',
      learn: '• Суды үнемдеу әдістері туралы біліңіз',
      title: 'Қауымдастық чаты',
      subtitle: 'Басқа фермерлермен байланысыңыз',
      farmerChat: 'Фермерлер чаты',
      aiAssistant: 'AI Көмекші',
      typeMessage: 'Хабарламаңызды жазыңыз...',
      send: 'Жіберу',
      onlineFarmers: 'Желідегі фермерлер',
      welcomeMessage: "Сәлеметсіз бе! Мен сіздің AI суару көмекшіңізбін. Мен суару кестесі, дақылдарға күтім жасау және суды үнемдеу туралы сұрақтарға көмектесе аламын. Бүгін сізге қалай көмектесе аламын?",
      suggestedQuestions: "Ұсынылатын сұрақтар:",
      bestTimeToWater: "Суарудың ең жақсы уақыты қашан?",
      saveWaterTips: "Суды қалай үнемдеуге болады?",
      typeMessage: "Суару туралы сұраңыз...",
      errorMessage: "Кешіріңіз, қате шықты. Кейінірек қайталап көріңіз."
    },
    
    // Страница калькулятора
    calculator: {
      title: 'Суару калькуляторы',
      subtitle: 'Бүгінгі қажетті су мөлшерін есептеу',
      selectDate: 'Күнді таңдаңыз',
      result: 'Нәтиже',
      waterNeeded: 'Қажет су',
      phase: 'Өсу кезеңі',
      explanation: 'Түсіндірме',
      wateringLog: 'Суару журналы',
      calculationDate: 'Есептеу күні:',
      calculate: 'Суаруды есептеу',
      recommendedWatering: 'Ұсынылатын суару',
      progress: 'Прогресс',
      daysFromSowing: 'Егілгеннен бері күн',
      lastWatered: 'Соңғы суару',
      daysAgo: 'күн бұрын',
      noSowingDate: 'Профильде егілген күнді көрсетіңіз',
      invalidSowingDate: 'Егілген күннің форматы дұрыс емес',
      selectWateringDate: 'Кемінде бір суару күнін таңдаңыз',
      pleaseLogin: 'Парақшаңызға кіріңіз',
      sessionExpired: 'Сессия аяқталды. Қайта кіріңіз.'
    },

    insights: {
      title: 'Мақалалар мен кеңестер',
      readMore: 'Толығырақ'
    },
    
    // Страница логина
    login: {
      title: 'Қайта оралу',
      subtitle: 'Суаруды басқару үшін кіріңіз',
      email: 'Эл. пошта',
      password: 'Құпия сөз',
      remember: 'Мені есте сақта',
      forgot: 'Құпия сөзді ұмыттыңыз ба?',
      login: 'Кіру',
      noAccount: 'Аккаунтыңыз жоқ па?',
      signUp: 'Тіркелу',
      info: 'Жүйеге кіру арқылы сіз біздің ақылды суару тәжірибемізбен келісесіз<br>тұрақты болашақ үшін',
      fillFields: 'Эл. пошта мен құпия сөзді толтырыңыз',
      loggingIn: 'Кіру...',
      success: 'Кіру сәтті аяқталды!',
      invalid: 'Қате email немесе құпия сөз',
      connectionError: 'Серверге қосылу мүмкін емес. Интернетті тексеріңіз.'
    },

    register: {
      title: 'Аккаунт құру',
      subtitle: 'Суаруды ақылды және тұрақты ету үшін бізге қосылыңыз',
      fullName: 'Толық аты-жөні',
      email: 'Эл. пошта',
      password: 'Құпия сөз',
      haveAccount: 'Аккаунтыңыз бар ма?',
      login: 'Кіру',
      signUp: 'Жалғастыру',
      fillFields: 'Барлық өрістерді толтырыңыз',
      invalidEmail: 'Жарамды email мекенжайын енгізіңіз',
      passwordLength: 'Құпия сөз кемінде 6 таңбадан тұруы керек',
      creating: 'Құрылуда...',
      success: 'Аккаунт сәтті құрылды!',
      failed: 'Тіркеу сәтсіз аяқталды',
      serverError: 'Сервер қатесі. Кейінірек қайталап көріңіз.'
    },
    
    // Страница календаря
    calendar: {
      title: 'Соңғы суару',
      subtitle: 'Соңғы суару күнін таңдаңыз',
      complete: 'Тіркелуді аяқтау'
    }
  }
};