"""
Модуль содержит структурированную информацию о сайте Rozoom-KI
для использования в промптах чат-ассистентов
"""

# Структура сайта и назначение страниц
SITE_STRUCTURE = {
    "home": {
        "de": {
            "title": "Startseite",
            "path": "/",
            "description": "Hauptseite von Rozoom-KI mit Überblick über unsere KI-gestützten Entwicklungsdienstleistungen",
            "purpose": "Präsentation unserer Hauptdienstleistungen und Generierung von Kundenanfragen für Softwareentwicklungsprojekte",
            "key_elements": ["Hero-Banner", "Dienstleistungsübersicht", "Fallstudien", "Team", "Kontaktformular"]
        },
        "ru": {
            "title": "Главная",
            "path": "/",
            "description": "Главная страница Rozoom-KI с обзором наших услуг по разработке с использованием ИИ",
            "purpose": "Презентация наших основных услуг и генерация клиентских запросов на разработку программного обеспечения",
            "key_elements": ["Баннер", "Обзор услуг", "Примеры работ", "Команда", "Контактная форма"]
        },
        "en": {
            "title": "Homepage",
            "path": "/",
            "description": "Main page of Rozoom-KI with overview of our AI-powered development services",
            "purpose": "Presentation of our main services and generation of client inquiries for software development projects",
            "key_elements": ["Hero Banner", "Services Overview", "Case Studies", "Team", "Contact Form"]
        }
    },
    "services": {
        "de": {
            "title": "Dienstleistungen",
            "path": "/services",
            "description": "Detaillierte Übersicht unserer Dienstleistungen im Bereich Softwareentwicklung und KI-Integration",
            "purpose": "Potentiellen Kunden einen tieferen Einblick in unsere Entwicklungsdienstleistungen geben",
            "key_elements": ["Web-Entwicklung", "Mobile App-Entwicklung", "KI-Integration", "Datenanalyse", "UX/UI Design"]
        },
        "ru": {
            "title": "Услуги",
            "path": "/services",
            "description": "Подробный обзор наших услуг в области разработки ПО и интеграции ИИ",
            "purpose": "Предоставить потенциальным клиентам более глубокое понимание наших услуг по разработке",
            "key_elements": ["Веб-разработка", "Разработка мобильных приложений", "Интеграция ИИ", "Анализ данных", "UX/UI дизайн"]
        },
        "en": {
            "title": "Services",
            "path": "/services",
            "description": "Detailed overview of our software development and AI integration services",
            "purpose": "Provide potential clients with a deeper understanding of our development services",
            "key_elements": ["Web Development", "Mobile App Development", "AI Integration", "Data Analysis", "UX/UI Design"]
        }
    },
    "projects": {
        "de": {
            "title": "Projekte",
            "path": "/projects",
            "description": "Fallstudien und Beispielprojekte, die wir erfolgreich abgeschlossen haben",
            "purpose": "Demonstration unserer Erfahrung und Expertise in der Entwicklung verschiedener Arten von Software",
            "key_elements": ["Filterbarer Projektkatalog", "Detaillierte Fallstudien", "Technologie-Stack", "Kundenreferenzen"]
        },
        "ru": {
            "title": "Проекты",
            "path": "/projects",
            "description": "Примеры и кейсы проектов, которые мы успешно завершили",
            "purpose": "Демонстрация нашего опыта и экспертизы в разработке различных типов программного обеспечения",
            "key_elements": ["Фильтруемый каталог проектов", "Детальные кейсы", "Технологический стек", "Отзывы клиентов"]
        },
        "en": {
            "title": "Projects",
            "path": "/projects",
            "description": "Case studies and sample projects we have successfully completed",
            "purpose": "Demonstration of our experience and expertise in developing various types of software",
            "key_elements": ["Filterable Project Catalog", "Detailed Case Studies", "Technology Stack", "Client Testimonials"]
        }
    },
    "about": {
        "de": {
            "title": "Über uns",
            "path": "/about",
            "description": "Informationen über unser Team, unsere Geschichte und unsere Mission",
            "purpose": "Vertrauensaufbau durch Transparenz über unser Unternehmen und unser Team",
            "key_elements": ["Unternehmensgeschichte", "Team-Mitglieder", "Mission und Vision", "Arbeitskultur"]
        },
        "ru": {
            "title": "О нас",
            "path": "/about",
            "description": "Информация о нашей команде, истории и миссии",
            "purpose": "Построение доверия через прозрачность о нашей компании и команде",
            "key_elements": ["История компании", "Члены команды", "Миссия и видение", "Рабочая культура"]
        },
        "en": {
            "title": "About Us",
            "path": "/about",
            "description": "Information about our team, history, and mission",
            "purpose": "Building trust through transparency about our company and team",
            "key_elements": ["Company History", "Team Members", "Mission and Vision", "Work Culture"]
        }
    },
    "contact": {
        "de": {
            "title": "Kontakt",
            "path": "/contact",
            "description": "Kontaktformulare und Informationen für potentielle Kunden",
            "purpose": "Einfache Möglichkeit für Besucher, mit uns in Kontakt zu treten und Anfragen zu stellen",
            "key_elements": ["Kontaktformular", "Adresse", "E-Mail", "Telefon", "Karte"]
        },
        "ru": {
            "title": "Контакты",
            "path": "/contact",
            "description": "Контактные формы и информация для потенциальных клиентов",
            "purpose": "Простой способ для посетителей связаться с нами и задать вопросы",
            "key_elements": ["Контактная форма", "Адрес", "Email", "Телефон", "Карта"]
        },
        "en": {
            "title": "Contact",
            "path": "/contact",
            "description": "Contact forms and information for potential clients",
            "purpose": "Easy way for visitors to get in touch with us and make inquiries",
            "key_elements": ["Contact Form", "Address", "Email", "Phone", "Map"]
        }
    },
    "brief": {
        "de": {
            "title": "Projektanfrage",
            "path": "/brief",
            "description": "Ein strukturiertes Formular für Kunden, um ihre Projektanforderungen zu spezifizieren",
            "purpose": "Sammlung detaillierter Informationen über potentielle Projekte, um personalisierte Angebote erstellen zu können",
            "key_elements": ["15-Fragen-Formular", "Anforderungserfassung", "Budget-Schätzung", "Zeitplan-Erfassung"]
        },
        "ru": {
            "title": "Запрос проекта",
            "path": "/brief",
            "description": "Структурированная форма для клиентов для указания требований к проекту",
            "purpose": "Сбор подробной информации о потенциальных проектах для создания персонализированных предложений",
            "key_elements": ["Форма из 15 вопросов", "Сбор требований", "Оценка бюджета", "Фиксация сроков"]
        },
        "en": {
            "title": "Project Brief",
            "path": "/brief",
            "description": "A structured form for clients to specify their project requirements",
            "purpose": "Collection of detailed information about potential projects to create personalized offers",
            "key_elements": ["15-Question Form", "Requirements Gathering", "Budget Estimation", "Timeline Capture"]
        }
    },
    "blog": {
        "de": {
            "title": "Blog",
            "path": "/blog",
            "description": "Artikel über Softwareentwicklung, KI, Technologietrends und Branchennachrichten",
            "purpose": "Demonstration unserer Fachkompetenz und Verbesserung des SEO durch regelmäßige Inhaltsveröffentlichung",
            "key_elements": ["Artikel nach Kategorien", "KI-Trends", "Entwicklungstipps", "Branchennachrichten"]
        },
        "ru": {
            "title": "Блог",
            "path": "/blog",
            "description": "Статьи о разработке программного обеспечения, ИИ, технологических тенденциях и отраслевых новостях",
            "purpose": "Демонстрация нашей экспертизы и улучшение SEO через регулярные публикации контента",
            "key_elements": ["Статьи по категориям", "Тренды ИИ", "Советы по разработке", "Новости индустрии"]
        },
        "en": {
            "title": "Blog",
            "path": "/blog",
            "description": "Articles about software development, AI, technology trends, and industry news",
            "purpose": "Demonstration of our expertise and improvement of SEO through regular content publishing",
            "key_elements": ["Articles by Category", "AI Trends", "Development Tips", "Industry News"]
        }
    }
}

# Структура формы ТЗ на странице «Услуги» (/services)
# Локализованные поля и краткие подсказки для ассистента-специфікатора
SERVICES_TZ_FORM = {
    "en": {
        "form_title": "Technical Specification (TZ) form",
        "path": "/services",
        "intro": "On the Services page you can fill a concise brief to kick off your tech spec.",
        "sections": [
            {
                "title": "Contact details",
                "fields": ["Name", "Email", "Phone (optional)"]
            },
            {
                "title": "Project basics",
                "fields": [
                    "Type (Website, Web App, Mobile App, Bot, Integration)",
                    "Main goal / business outcome",
                    "Target audience / users"
                ]
            },
            {
                "title": "Scope & features",
                "fields": [
                    "Key features (MVP)",
                    "Integrations (payments, CRM, AI, messengers)",
                    "Content/data specifics (languages, GDPR, PII)"
                ]
            },
            {
                "title": "Constraints",
                "fields": ["Budget range", "Timeline / milestones", "Tech preferences (if any)"]
            }
        ],
        "cta": "Open the Services page (/services), I’ll guide you step-by-step and prefill answers where possible."
    },
    "ru": {
        "form_title": "Форма технического задания (ТЗ)",
        "path": "/services",
        "intro": "На странице «Услуги» можно заполнить краткий бриф для старта ТЗ.",
        "sections": [
            {
                "title": "Контакты",
                "fields": ["Имя", "Email", "Телефон (необязательно)"]
            },
            {
                "title": "Базовая информация о проекте",
                "fields": [
                    "Тип (сайт, веб‑приложение, мобильное, бот, интеграции)",
                    "Главная цель / бизнес‑результат",
                    "Целевая аудитория / пользователи"
                ]
            },
            {
                "title": "Объем и функциональность",
                "fields": [
                    "Ключевые функции (MVP)",
                    "Интеграции (платежи, CRM, AI, мессенджеры)",
                    "Контент/данные (языки, GDPR, персональные данные)"
                ]
            },
            {
                "title": "Ограничения",
                "fields": ["Бюджет", "Сроки / этапы", "Технологические предпочтения (если есть)"]
            }
        ],
        "cta": "Откройте страницу /services — я помогу пройти форму и заполню черновик ТЗ."
    },
    "uk": {
        "form_title": "Форма технічного завдання (ТЗ)",
        "path": "/services",
        "intro": "На сторінці «Сервіси» можна заповнити короткий бриф для старту ТЗ.",
        "sections": [
            {
                "title": "Контакти",
                "fields": ["Ім’я", "Email", "Телефон (необов’язково)"]
            },
            {
                "title": "Базова інформація про проєкт",
                "fields": [
                    "Тип (сайт, веб‑додаток, мобільний, бот, інтеграції)",
                    "Головна ціль / бізнес‑результат",
                    "Цільова аудиторія / користувачі"
                ]
            },
            {
                "title": "Обсяг і функціональність",
                "fields": [
                    "Ключові функції (MVP)",
                    "Інтеграції (платежі, CRM, AI, месенджери)",
                    "Контент/дані (мови, GDPR, персональні дані)"
                ]
            },
            {
                "title": "Обмеження",
                "fields": ["Бюджет", "Терміни / етапи", "Технологічні вподобання (якщо є)"]
            }
        ],
        "cta": "Відкрийте сторінку /services — я проведу по формі та підготую чорновик ТЗ."
    },
    "de": {
        "form_title": "Technisches Aufgabenblatt (TZ) – Formular",
        "path": "/services",
        "intro": "Auf der Seite Dienstleistungen können Sie ein kurzes Briefing für das TZ ausfüllen.",
        "sections": [
            {
                "title": "Kontaktdaten",
                "fields": ["Name", "E‑Mail", "Telefon (optional)"]
            },
            {
                "title": "Projektgrundlagen",
                "fields": [
                    "Typ (Website, Web‑App, Mobile, Bot, Integrationen)",
                    "Hauptziel / Business‑Outcome",
                    "Zielgruppe / Nutzer"
                ]
            },
            {
                "title": "Umfang & Features",
                "fields": [
                    "Schlüsselfunktionen (MVP)",
                    "Integrationen (Zahlungen, CRM, KI, Messenger)",
                    "Inhalt/Daten (Sprachen, DSGVO, personenbezogene Daten)"
                ]
            },
            {
                "title": "Rahmenbedingungen",
                "fields": ["Budget", "Zeitplan / Meilensteine", "Tech‑Präferenzen (falls vorhanden)"]
            }
        ],
        "cta": "Öffnen Sie /services – ich führe Sie durch das Formular und erstelle einen TZ‑Entwurf."
    }
}

# Подробности о технических заданиях и форме бриф-запроса
BRIEF_FORM_INFO = {
    "de": {
        "form_title": "Projektanfrage - Technisches Aufgabenblatt",
        "description": "Ein kostenloses, unverbindliches Formular mit 15 Fragen, das Ihnen hilft, Ihre Projektanforderungen klar zu definieren.",
        "purpose": "Sammlung ausreichender Informationen, um ein personalisiertes Angebot für Ihr Projekt zu erstellen.",
        "questions": [
            "Art des Projekts (Website, Mobile App, Desktop-Anwendung, etc.)",
            "Hauptziel des Projekts",
            "Zielgruppe",
            "Gewünschte Funktionen",
            "Design-Vorlieben",
            "Bestehende Referenzen oder Beispiele",
            "Technische Anforderungen",
            "Integrationsbedürfnisse",
            "Inhaltsanforderungen",
            "Zeitrahmen",
            "Budget-Bereich",
            "Nach Fertigstellung benötigte Dienste",
            "Wie haben Sie von uns erfahren?",
            "Bevorzugte Kommunikationsmethode",
            "Zusätzliche Informationen"
        ],
        "benefits": [
            "Kostenlose Projektberatung",
            "Personalisiertes Angebot",
            "Klarheit über Projektumfang",
            "Bessere Budget- und Zeitplanschätzungen",
            "Unverbindliche Anfrage"
        ]
    },
    "ru": {
        "form_title": "Запрос проекта - Техническое задание",
        "description": "Бесплатная, ни к чему не обязывающая форма из 15 вопросов, которая поможет вам четко определить требования к проекту.",
        "purpose": "Сбор достаточной информации для создания персонализированного предложения для вашего проекта.",
        "questions": [
            "Тип проекта (веб-сайт, мобильное приложение, десктопное приложение и т.д.)",
            "Основная цель проекта",
            "Целевая аудитория",
            "Желаемые функции",
            "Предпочтения по дизайну",
            "Существующие референсы или примеры",
            "Технические требования",
            "Потребности в интеграции",
            "Требования к контенту",
            "Временные рамки",
            "Диапазон бюджета",
            "Необходимые услуги после завершения",
            "Как вы о нас узнали?",
            "Предпочтительный метод связи",
            "Дополнительная информация"
        ],
        "benefits": [
            "Бесплатная консультация по проекту",
            "Персонализированное предложение",
            "Ясность относительно объема проекта",
            "Лучшие оценки бюджета и сроков",
            "Необязывающий запрос"
        ]
    },
    "en": {
        "form_title": "Project Request - Technical Specification",
        "description": "A free, non-binding form with 15 questions that helps you clearly define your project requirements.",
        "purpose": "Collection of sufficient information to create a personalized offer for your project.",
        "questions": [
            "Type of project (website, mobile app, desktop application, etc.)",
            "Main goal of the project",
            "Target audience",
            "Desired features",
            "Design preferences",
            "Existing references or examples",
            "Technical requirements",
            "Integration needs",
            "Content requirements",
            "Timeline",
            "Budget range",
            "Services needed after completion",
            "How did you hear about us?",
            "Preferred method of communication",
            "Additional information"
        ],
        "benefits": [
            "Free project consultation",
            "Personalized offer",
            "Clarity on project scope",
            "Better budget and timeline estimates",
            "Non-binding inquiry"
        ]
    }
}

# Информация о компании
COMPANY_INFO = {
    "de": {
        "name": "Rozoom-KI",
        "location": "Frankfurt am Main, Deutschland",
        "specialization": "KI-gestützte Softwareentwicklung und Digitallösungen",
        "unique_selling_points": [
            "KI-Integration in bestehende Systeme",
            "Maßgeschneiderte Softwareentwicklung",
            "Automatisierung von Geschäftsprozessen",
            "Datenanalyse und Vorhersagemodelle",
            "Mehrsprachiger Support (Deutsch, Englisch, Russisch)"
        ]
    },
    "ru": {
        "name": "Rozoom-KI",
        "location": "Франкфурт-на-Майне, Германия",
        "specialization": "Разработка программного обеспечения с ИИ и цифровые решения",
        "unique_selling_points": [
            "Интеграция ИИ в существующие системы",
            "Индивидуальная разработка программного обеспечения",
            "Автоматизация бизнес-процессов",
            "Анализ данных и предиктивные модели",
            "Многоязычная поддержка (немецкий, английский, русский)"
        ]
    },
    "en": {
        "name": "Rozoom-KI",
        "location": "Frankfurt am Main, Germany",
        "specialization": "AI-powered software development and digital solutions",
        "unique_selling_points": [
            "AI integration into existing systems",
            "Custom software development",
            "Business process automation",
            "Data analysis and predictive models",
            "Multilingual support (German, English, Russian)"
        ]
    }
}

# Роли ассистентов
ASSISTANT_ROLES = {
    "de": {
        "greeter": {
            "role": "Begrüßungs-Assistent",
            "description": "Begrüßt Besucher, erklärt die Website und hilft bei der Navigation",
            "goals": [
                "Besucher willkommen heißen",
                "Website-Funktionen erklären",
                "Zu relevanten Seiten navigieren helfen",
                "Häufig gestellte Fragen beantworten"
            ]
        },
        "project_consultant": {
            "role": "Projekt-Berater",
            "description": "Hilft Besuchern, ihre Projektanforderungen zu definieren und führt sie zum TZ-Formular",
            "goals": [
                "Besucher ermutigen, das kostenlose TZ-Formular auszufüllen",
                "Die Vorteile eines detaillierten technischen Aufgabenblatts erklären",
                "Bei Fragen zum Projektumfang helfen",
                "Kontaktdaten sammeln für ein personalisiertes Angebot"
            ]
        },
        "technical_advisor": {
            "role": "Technischer Berater",
            "description": "Beantwortet technische Fragen und gibt Einblicke in unsere Entwicklungsmethoden",
            "goals": [
                "Technische Fragen zu unseren Entwicklungsprozessen beantworten",
                "Verwendete Technologien erklären",
                "Projektmachbarkeit bewerten",
                "Technische Aspekte verschiedener Lösungen erläutern"
            ]
        }
    },
    "ru": {
        "greeter": {
            "role": "Приветствующий ассистент",
            "description": "Приветствует посетителей, объясняет функции сайта и помогает с навигацией",
            "goals": [
                "Поприветствовать посетителей",
                "Объяснить функции сайта",
                "Помочь с навигацией по соответствующим страницам",
                "Ответить на часто задаваемые вопросы"
            ]
        },
        "project_consultant": {
            "role": "Консультант по проектам",
            "description": "Помогает посетителям определить требования к проекту и направляет их к форме ТЗ",
            "goals": [
                "Поощрять посетителей заполнить бесплатную форму ТЗ",
                "Объяснить преимущества подробного технического задания",
                "Помочь с вопросами об объеме проекта",
                "Собрать контактные данные для персонализированного предложения"
            ]
        },
        "technical_advisor": {
            "role": "Технический консультант",
            "description": "Отвечает на технические вопросы и дает представление о наших методах разработки",
            "goals": [
                "Ответить на технические вопросы о наших процессах разработки",
                "Объяснить используемые технологии",
                "Оценить выполнимость проекта",
                "Объяснить технические аспекты различных решений"
            ]
        }
    },
    "en": {
        "greeter": {
            "role": "Greeting Assistant",
            "description": "Greets visitors, explains the website features, and helps with navigation",
            "goals": [
                "Welcome visitors",
                "Explain website features",
                "Help navigate to relevant pages",
                "Answer frequently asked questions"
            ]
        },
        "project_consultant": {
            "role": "Project Consultant",
            "description": "Helps visitors define their project requirements and guides them to the brief form",
            "goals": [
                "Encourage visitors to fill out the free brief form",
                "Explain the benefits of a detailed technical specification",
                "Help with questions about project scope",
                "Collect contact details for a personalized offer"
            ]
        },
        "technical_advisor": {
            "role": "Technical Advisor",
            "description": "Answers technical questions and provides insights into our development methods",
            "goals": [
                "Answer technical questions about our development processes",
                "Explain technologies used",
                "Assess project feasibility",
                "Explain technical aspects of different solutions"
            ]
        }
    }
}

def _pick_lang(d: dict, lang: str, fallbacks=("uk", "de", "en", "ru")):
    """Безопасно выбирает локализацию: сначала lang, затем по порядку из fallbacks."""
    if lang in d:
        return d[lang]
    for fb in fallbacks:
        if fb in d:
            return d[fb]
    # как последний вариант — берем любой
    return next(iter(d.values()))


def get_site_info(lang='en'):
    """Возвращает сводную информацию о сайте и бриф-формах для ассистентов."""
    site_structure = {page: _pick_lang(data, lang) for page, data in SITE_STRUCTURE.items()}
    brief_form = _pick_lang(BRIEF_FORM_INFO, lang)
    company_info = _pick_lang(COMPANY_INFO, lang)
    assistant_roles = _pick_lang(ASSISTANT_ROLES, lang)
    services_form = _pick_lang(SERVICES_TZ_FORM, lang)

    return {
        "site_structure": site_structure,
        "brief_form": brief_form,
        "company_info": company_info,
        "assistant_roles": assistant_roles,
        "services_tz_form": services_form,
    }


def get_services_form_info(lang='en'):
    """Отдает структуру формы ТЗ на странице /services для указанного языка (с безопасным фолбэком)."""
    return _pick_lang(SERVICES_TZ_FORM, lang)


def spec_agent_context(lang='en') -> str:
    """Короткий текст-контекст для ассистента SPEC: где форма ТЗ и что в ней заполнять."""
    info = get_services_form_info(lang)
    title = info.get("form_title")
    path = info.get("path", "/services")
    intro = info.get("intro")
    sections = info.get("sections", [])
    lines = []
    lines.append(f"{title} — {path}.")
    if intro:
        lines.append(intro)
    lines.append("")
    for sec in sections:
        lines.append(f"• {sec.get('title')}:")
        for f in sec.get('fields', []):
            lines.append(f"  – {f}")
    cta = info.get("cta")
    if cta:
        lines.append("")
        lines.append(cta)
    return "\n".join(lines)
