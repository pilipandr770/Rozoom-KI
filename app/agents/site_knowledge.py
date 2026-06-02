"""
РњРѕРґСѓР»СЊ СЃРѕРґРµСЂР¶РёС‚ СЃС‚СЂСѓРєС‚СѓСЂРёСЂРѕРІР°РЅРЅСѓСЋ РёРЅС„РѕСЂРјР°С†РёСЋ Рѕ СЃР°Р№С‚Рµ Andrii-IT
РґР»СЏ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ РІ РїСЂРѕРјРїС‚Р°С… С‡Р°С‚-Р°СЃСЃРёСЃС‚РµРЅС‚РѕРІ
"""

# РЎС‚СЂСѓРєС‚СѓСЂР° СЃР°Р№С‚Р° Рё РЅР°Р·РЅР°С‡РµРЅРёРµ СЃС‚СЂР°РЅРёС†
SITE_STRUCTURE = {
    "home": {
        "de": {
            "title": "Startseite",
            "path": "/",
            "description": "Hauptseite von Andrii-IT mit Гњberblick Гјber unsere KI-gestГјtzten Entwicklungsdienstleistungen",
            "purpose": "PrГ¤sentation unserer Hauptdienstleistungen und Generierung von Kundenanfragen fГјr Softwareentwicklungsprojekte",
            "key_elements": ["Hero-Banner", "DienstleistungsГјbersicht", "Fallstudien", "Team", "Kontaktformular"]
        },
        "ru": {
            "title": "Р“Р»Р°РІРЅР°СЏ",
            "path": "/",
            "description": "Р“Р»Р°РІРЅР°СЏ СЃС‚СЂР°РЅРёС†Р° Andrii-IT СЃ РѕР±Р·РѕСЂРѕРј РЅР°С€РёС… СѓСЃР»СѓРі РїРѕ СЂР°Р·СЂР°Р±РѕС‚РєРµ СЃ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј РР",
            "purpose": "РџСЂРµР·РµРЅС‚Р°С†РёСЏ РЅР°С€РёС… РѕСЃРЅРѕРІРЅС‹С… СѓСЃР»СѓРі Рё РіРµРЅРµСЂР°С†РёСЏ РєР»РёРµРЅС‚СЃРєРёС… Р·Р°РїСЂРѕСЃРѕРІ РЅР° СЂР°Р·СЂР°Р±РѕС‚РєСѓ РїСЂРѕРіСЂР°РјРјРЅРѕРіРѕ РѕР±РµСЃРїРµС‡РµРЅРёСЏ",
            "key_elements": ["Р‘Р°РЅРЅРµСЂ", "РћР±Р·РѕСЂ СѓСЃР»СѓРі", "РџСЂРёРјРµСЂС‹ СЂР°Р±РѕС‚", "РљРѕРјР°РЅРґР°", "РљРѕРЅС‚Р°РєС‚РЅР°СЏ С„РѕСЂРјР°"]
        },
        "en": {
            "title": "Homepage",
            "path": "/",
            "description": "Main page of Andrii-IT with overview of our AI-powered development services",
            "purpose": "Presentation of our main services and generation of client inquiries for software development projects",
            "key_elements": ["Hero Banner", "Services Overview", "Case Studies", "Team", "Contact Form"]
        }
    },
    "services": {
        "de": {
            "title": "Dienstleistungen",
            "path": "/services",
            "description": "Detaillierte Гњbersicht unserer Dienstleistungen im Bereich Softwareentwicklung und KI-Integration",
            "purpose": "Potentiellen Kunden einen tieferen Einblick in unsere Entwicklungsdienstleistungen geben",
            "key_elements": ["Web-Entwicklung", "Mobile App-Entwicklung", "KI-Integration", "Datenanalyse", "UX/UI Design"]
        },
        "ru": {
            "title": "РЈСЃР»СѓРіРё",
            "path": "/services",
            "description": "РџРѕРґСЂРѕР±РЅС‹Р№ РѕР±Р·РѕСЂ РЅР°С€РёС… СѓСЃР»СѓРі РІ РѕР±Р»Р°СЃС‚Рё СЂР°Р·СЂР°Р±РѕС‚РєРё РџРћ Рё РёРЅС‚РµРіСЂР°С†РёРё РР",
            "purpose": "РџСЂРµРґРѕСЃС‚Р°РІРёС‚СЊ РїРѕС‚РµРЅС†РёР°Р»СЊРЅС‹Рј РєР»РёРµРЅС‚Р°Рј Р±РѕР»РµРµ РіР»СѓР±РѕРєРѕРµ РїРѕРЅРёРјР°РЅРёРµ РЅР°С€РёС… СѓСЃР»СѓРі РїРѕ СЂР°Р·СЂР°Р±РѕС‚РєРµ",
            "key_elements": ["Р’РµР±-СЂР°Р·СЂР°Р±РѕС‚РєР°", "Р Р°Р·СЂР°Р±РѕС‚РєР° РјРѕР±РёР»СЊРЅС‹С… РїСЂРёР»РѕР¶РµРЅРёР№", "РРЅС‚РµРіСЂР°С†РёСЏ РР", "РђРЅР°Р»РёР· РґР°РЅРЅС‹С…", "UX/UI РґРёР·Р°Р№РЅ"]
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
            "title": "РџСЂРѕРµРєС‚С‹",
            "path": "/projects",
            "description": "РџСЂРёРјРµСЂС‹ Рё РєРµР№СЃС‹ РїСЂРѕРµРєС‚РѕРІ, РєРѕС‚РѕСЂС‹Рµ РјС‹ СѓСЃРїРµС€РЅРѕ Р·Р°РІРµСЂС€РёР»Рё",
            "purpose": "Р”РµРјРѕРЅСЃС‚СЂР°С†РёСЏ РЅР°С€РµРіРѕ РѕРїС‹С‚Р° Рё СЌРєСЃРїРµСЂС‚РёР·С‹ РІ СЂР°Р·СЂР°Р±РѕС‚РєРµ СЂР°Р·Р»РёС‡РЅС‹С… С‚РёРїРѕРІ РїСЂРѕРіСЂР°РјРјРЅРѕРіРѕ РѕР±РµСЃРїРµС‡РµРЅРёСЏ",
            "key_elements": ["Р¤РёР»СЊС‚СЂСѓРµРјС‹Р№ РєР°С‚Р°Р»РѕРі РїСЂРѕРµРєС‚РѕРІ", "Р”РµС‚Р°Р»СЊРЅС‹Рµ РєРµР№СЃС‹", "РўРµС…РЅРѕР»РѕРіРёС‡РµСЃРєРёР№ СЃС‚РµРє", "РћС‚Р·С‹РІС‹ РєР»РёРµРЅС‚РѕРІ"]
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
            "title": "Гњber uns",
            "path": "/about",
            "description": "Informationen Гјber unser Team, unsere Geschichte und unsere Mission",
            "purpose": "Vertrauensaufbau durch Transparenz Гјber unser Unternehmen und unser Team",
            "key_elements": ["Unternehmensgeschichte", "Team-Mitglieder", "Mission und Vision", "Arbeitskultur"]
        },
        "ru": {
            "title": "Рћ РЅР°СЃ",
            "path": "/about",
            "description": "РРЅС„РѕСЂРјР°С†РёСЏ Рѕ РЅР°С€РµР№ РєРѕРјР°РЅРґРµ, РёСЃС‚РѕСЂРёРё Рё РјРёСЃСЃРёРё",
            "purpose": "РџРѕСЃС‚СЂРѕРµРЅРёРµ РґРѕРІРµСЂРёСЏ С‡РµСЂРµР· РїСЂРѕР·СЂР°С‡РЅРѕСЃС‚СЊ Рѕ РЅР°С€РµР№ РєРѕРјРїР°РЅРёРё Рё РєРѕРјР°РЅРґРµ",
            "key_elements": ["РСЃС‚РѕСЂРёСЏ РєРѕРјРїР°РЅРёРё", "Р§Р»РµРЅС‹ РєРѕРјР°РЅРґС‹", "РњРёСЃСЃРёСЏ Рё РІРёРґРµРЅРёРµ", "Р Р°Р±РѕС‡Р°СЏ РєСѓР»СЊС‚СѓСЂР°"]
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
            "description": "Kontaktformulare und Informationen fГјr potentielle Kunden",
            "purpose": "Einfache MГ¶glichkeit fГјr Besucher, mit uns in Kontakt zu treten und Anfragen zu stellen",
            "key_elements": ["Kontaktformular", "Adresse", "E-Mail", "Telefon", "Karte"]
        },
        "ru": {
            "title": "РљРѕРЅС‚Р°РєС‚С‹",
            "path": "/contact",
            "description": "РљРѕРЅС‚Р°РєС‚РЅС‹Рµ С„РѕСЂРјС‹ Рё РёРЅС„РѕСЂРјР°С†РёСЏ РґР»СЏ РїРѕС‚РµРЅС†РёР°Р»СЊРЅС‹С… РєР»РёРµРЅС‚РѕРІ",
            "purpose": "РџСЂРѕСЃС‚РѕР№ СЃРїРѕСЃРѕР± РґР»СЏ РїРѕСЃРµС‚РёС‚РµР»РµР№ СЃРІСЏР·Р°С‚СЊСЃСЏ СЃ РЅР°РјРё Рё Р·Р°РґР°С‚СЊ РІРѕРїСЂРѕСЃС‹",
            "key_elements": ["РљРѕРЅС‚Р°РєС‚РЅР°СЏ С„РѕСЂРјР°", "РђРґСЂРµСЃ", "Email", "РўРµР»РµС„РѕРЅ", "РљР°СЂС‚Р°"]
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
            "description": "Ein strukturiertes Formular fГјr Kunden, um ihre Projektanforderungen zu spezifizieren",
            "purpose": "Sammlung detaillierter Informationen Гјber potentielle Projekte, um personalisierte Angebote erstellen zu kГ¶nnen",
            "key_elements": ["15-Fragen-Formular", "Anforderungserfassung", "Budget-SchГ¤tzung", "Zeitplan-Erfassung"]
        },
        "ru": {
            "title": "Р—Р°РїСЂРѕСЃ РїСЂРѕРµРєС‚Р°",
            "path": "/brief",
            "description": "РЎС‚СЂСѓРєС‚СѓСЂРёСЂРѕРІР°РЅРЅР°СЏ С„РѕСЂРјР° РґР»СЏ РєР»РёРµРЅС‚РѕРІ РґР»СЏ СѓРєР°Р·Р°РЅРёСЏ С‚СЂРµР±РѕРІР°РЅРёР№ Рє РїСЂРѕРµРєС‚Сѓ",
            "purpose": "РЎР±РѕСЂ РїРѕРґСЂРѕР±РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё Рѕ РїРѕС‚РµРЅС†РёР°Р»СЊРЅС‹С… РїСЂРѕРµРєС‚Р°С… РґР»СЏ СЃРѕР·РґР°РЅРёСЏ РїРµСЂСЃРѕРЅР°Р»РёР·РёСЂРѕРІР°РЅРЅС‹С… РїСЂРµРґР»РѕР¶РµРЅРёР№",
            "key_elements": ["Р¤РѕСЂРјР° РёР· 15 РІРѕРїСЂРѕСЃРѕРІ", "РЎР±РѕСЂ С‚СЂРµР±РѕРІР°РЅРёР№", "РћС†РµРЅРєР° Р±СЋРґР¶РµС‚Р°", "Р¤РёРєСЃР°С†РёСЏ СЃСЂРѕРєРѕРІ"]
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
            "description": "Artikel Гјber Softwareentwicklung, KI, Technologietrends und Branchennachrichten",
            "purpose": "Demonstration unserer Fachkompetenz und Verbesserung des SEO durch regelmГ¤Гџige InhaltsverГ¶ffentlichung",
            "key_elements": ["Artikel nach Kategorien", "KI-Trends", "Entwicklungstipps", "Branchennachrichten"]
        },
        "ru": {
            "title": "Р‘Р»РѕРі",
            "path": "/blog",
            "description": "РЎС‚Р°С‚СЊРё Рѕ СЂР°Р·СЂР°Р±РѕС‚РєРµ РїСЂРѕРіСЂР°РјРјРЅРѕРіРѕ РѕР±РµСЃРїРµС‡РµРЅРёСЏ, РР, С‚РµС…РЅРѕР»РѕРіРёС‡РµСЃРєРёС… С‚РµРЅРґРµРЅС†РёСЏС… Рё РѕС‚СЂР°СЃР»РµРІС‹С… РЅРѕРІРѕСЃС‚СЏС…",
            "purpose": "Р”РµРјРѕРЅСЃС‚СЂР°С†РёСЏ РЅР°С€РµР№ СЌРєСЃРїРµСЂС‚РёР·С‹ Рё СѓР»СѓС‡С€РµРЅРёРµ SEO С‡РµСЂРµР· СЂРµРіСѓР»СЏСЂРЅС‹Рµ РїСѓР±Р»РёРєР°С†РёРё РєРѕРЅС‚РµРЅС‚Р°",
            "key_elements": ["РЎС‚Р°С‚СЊРё РїРѕ РєР°С‚РµРіРѕСЂРёСЏРј", "РўСЂРµРЅРґС‹ РР", "РЎРѕРІРµС‚С‹ РїРѕ СЂР°Р·СЂР°Р±РѕС‚РєРµ", "РќРѕРІРѕСЃС‚Рё РёРЅРґСѓСЃС‚СЂРёРё"]
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

# РЎС‚СЂСѓРєС‚СѓСЂР° С„РѕСЂРјС‹ РўР— РЅР° СЃС‚СЂР°РЅРёС†Рµ В«РЈСЃР»СѓРіРёВ» (/services)
# Р›РѕРєР°Р»РёР·РѕРІР°РЅРЅС‹Рµ РїРѕР»СЏ Рё РєСЂР°С‚РєРёРµ РїРѕРґСЃРєР°Р·РєРё РґР»СЏ Р°СЃСЃРёСЃС‚РµРЅС‚Р°-СЃРїРµС†РёС„С–РєР°С‚РѕСЂР°
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
        "cta": "Open the Services page (/services), IвЂ™ll guide you step-by-step and prefill answers where possible."
    },
    "ru": {
        "form_title": "Р¤РѕСЂРјР° С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ Р·Р°РґР°РЅРёСЏ (РўР—)",
        "path": "/services",
        "intro": "РќР° СЃС‚СЂР°РЅРёС†Рµ В«РЈСЃР»СѓРіРёВ» РјРѕР¶РЅРѕ Р·Р°РїРѕР»РЅРёС‚СЊ РєСЂР°С‚РєРёР№ Р±СЂРёС„ РґР»СЏ СЃС‚Р°СЂС‚Р° РўР—.",
        "sections": [
            {
                "title": "РљРѕРЅС‚Р°РєС‚С‹",
                "fields": ["РРјСЏ", "Email", "РўРµР»РµС„РѕРЅ (РЅРµРѕР±СЏР·Р°С‚РµР»СЊРЅРѕ)"]
            },
            {
                "title": "Р‘Р°Р·РѕРІР°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ Рѕ РїСЂРѕРµРєС‚Рµ",
                "fields": [
                    "РўРёРї (СЃР°Р№С‚, РІРµР±вЂ‘РїСЂРёР»РѕР¶РµРЅРёРµ, РјРѕР±РёР»СЊРЅРѕРµ, Р±РѕС‚, РёРЅС‚РµРіСЂР°С†РёРё)",
                    "Р“Р»Р°РІРЅР°СЏ С†РµР»СЊ / Р±РёР·РЅРµСЃвЂ‘СЂРµР·СѓР»СЊС‚Р°С‚",
                    "Р¦РµР»РµРІР°СЏ Р°СѓРґРёС‚РѕСЂРёСЏ / РїРѕР»СЊР·РѕРІР°С‚РµР»Рё"
                ]
            },
            {
                "title": "РћР±СЉРµРј Рё С„СѓРЅРєС†РёРѕРЅР°Р»СЊРЅРѕСЃС‚СЊ",
                "fields": [
                    "РљР»СЋС‡РµРІС‹Рµ С„СѓРЅРєС†РёРё (MVP)",
                    "РРЅС‚РµРіСЂР°С†РёРё (РїР»Р°С‚РµР¶Рё, CRM, AI, РјРµСЃСЃРµРЅРґР¶РµСЂС‹)",
                    "РљРѕРЅС‚РµРЅС‚/РґР°РЅРЅС‹Рµ (СЏР·С‹РєРё, GDPR, РїРµСЂСЃРѕРЅР°Р»СЊРЅС‹Рµ РґР°РЅРЅС‹Рµ)"
                ]
            },
            {
                "title": "РћРіСЂР°РЅРёС‡РµРЅРёСЏ",
                "fields": ["Р‘СЋРґР¶РµС‚", "РЎСЂРѕРєРё / СЌС‚Р°РїС‹", "РўРµС…РЅРѕР»РѕРіРёС‡РµСЃРєРёРµ РїСЂРµРґРїРѕС‡С‚РµРЅРёСЏ (РµСЃР»Рё РµСЃС‚СЊ)"]
            }
        ],
        "cta": "РћС‚РєСЂРѕР№С‚Рµ СЃС‚СЂР°РЅРёС†Сѓ /services — СЏ РїРѕРјРѕРіСѓ РїСЂРѕР№С‚Рё С„РѕСЂРјСѓ Рё Р·Р°РїРѕР»РЅСЋ С‡РµСЂРЅРѕРІРёРє РўР—."
    },
    "uk": {
        "form_title": "Р¤РѕСЂРјР° С‚РµС…РЅС–С‡РЅРѕРіРѕ Р·Р°РІРґР°РЅРЅСЏ (РўР—)",
        "path": "/services",
        "intro": "РќР° СЃС‚РѕСЂС–РЅС†С– В«РЎРµСЂРІС–СЃРёВ» РјРѕР¶РЅР° Р·Р°РїРѕРІРЅРёС‚Рё РєРѕСЂРѕС‚РєРёР№ Р±СЂРёС„ РґР»СЏ СЃС‚Р°СЂС‚Сѓ РўР—.",
        "sections": [
            {
                "title": "РљРѕРЅС‚Р°РєС‚Рё",
                "fields": ["Р†РјвЂ™СЏ", "Email", "РўРµР»РµС„РѕРЅ (РЅРµРѕР±РѕРІвЂ™СЏР·РєРѕРІРѕ)"]
            },
            {
                "title": "Р‘Р°Р·РѕРІР° С–РЅС„РѕСЂРјР°С†С–СЏ РїСЂРѕ РїСЂРѕС”РєС‚",
                "fields": [
                    "РўРёРї (СЃР°Р№С‚, РІРµР±вЂ‘РґРѕРґР°С‚РѕРє, РјРѕР±С–Р»СЊРЅРёР№, Р±РѕС‚, С–РЅС‚РµРіСЂР°С†С–С—)",
                    "Р“РѕР»РѕРІРЅР° С†С–Р»СЊ / Р±С–Р·РЅРµСЃвЂ‘СЂРµР·СѓР»СЊС‚Р°С‚",
                    "Р¦С–Р»СЊРѕРІР° Р°СѓРґРёС‚РѕСЂС–СЏ / РєРѕСЂРёСЃС‚СѓРІР°С‡С–"
                ]
            },
            {
                "title": "РћР±СЃСЏРі С– С„СѓРЅРєС†С–РѕРЅР°Р»СЊРЅС–СЃС‚СЊ",
                "fields": [
                    "РљР»СЋС‡РѕРІС– С„СѓРЅРєС†С–С— (MVP)",
                    "Р†РЅС‚РµРіСЂР°С†С–С— (РїР»Р°С‚РµР¶С–, CRM, AI, РјРµСЃРµРЅРґР¶РµСЂРё)",
                    "РљРѕРЅС‚РµРЅС‚/РґР°РЅС– (РјРѕРІРё, GDPR, РїРµСЂСЃРѕРЅР°Р»СЊРЅС– РґР°РЅС–)"
                ]
            },
            {
                "title": "РћР±РјРµР¶РµРЅРЅСЏ",
                "fields": ["Р‘СЋРґР¶РµС‚", "РўРµСЂРјС–РЅРё / РµС‚Р°РїРё", "РўРµС…РЅРѕР»РѕРіС–С‡РЅС– РІРїРѕРґРѕР±Р°РЅРЅСЏ (СЏРєС‰Рѕ С”)"]
            }
        ],
        "cta": "Р’С–РґРєСЂРёР№С‚Рµ СЃС‚РѕСЂС–РЅРєСѓ /services — СЏ РїСЂРѕРІРµРґСѓ РїРѕ С„РѕСЂРјС– С‚Р° РїС–РґРіРѕС‚СѓСЋ С‡РѕСЂРЅРѕРІРёРє РўР—."
    },
    "de": {
        "form_title": "Technisches Aufgabenblatt (TZ) вЂ“ Formular",
        "path": "/services",
        "intro": "Auf der Seite Dienstleistungen kГ¶nnen Sie ein kurzes Briefing fГјr das TZ ausfГјllen.",
        "sections": [
            {
                "title": "Kontaktdaten",
                "fields": ["Name", "EвЂ‘Mail", "Telefon (optional)"]
            },
            {
                "title": "Projektgrundlagen",
                "fields": [
                    "Typ (Website, WebвЂ‘App, Mobile, Bot, Integrationen)",
                    "Hauptziel / BusinessвЂ‘Outcome",
                    "Zielgruppe / Nutzer"
                ]
            },
            {
                "title": "Umfang & Features",
                "fields": [
                    "SchlГјsselfunktionen (MVP)",
                    "Integrationen (Zahlungen, CRM, KI, Messenger)",
                    "Inhalt/Daten (Sprachen, DSGVO, personenbezogene Daten)"
                ]
            },
            {
                "title": "Rahmenbedingungen",
                "fields": ["Budget", "Zeitplan / Meilensteine", "TechвЂ‘PrГ¤ferenzen (falls vorhanden)"]
            }
        ],
        "cta": "Г–ffnen Sie /services вЂ“ ich fГјhre Sie durch das Formular und erstelle einen TZвЂ‘Entwurf."
    }
}

# РџРѕРґСЂРѕР±РЅРѕСЃС‚Рё Рѕ С‚РµС…РЅРёС‡РµСЃРєРёС… Р·Р°РґР°РЅРёСЏС… Рё С„РѕСЂРјРµ Р±СЂРёС„-Р·Р°РїСЂРѕСЃР°
BRIEF_FORM_INFO = {
    "de": {
        "form_title": "Projektanfrage - Technisches Aufgabenblatt",
        "description": "Ein kostenloses, unverbindliches Formular mit 15 Fragen, das Ihnen hilft, Ihre Projektanforderungen klar zu definieren.",
        "purpose": "Sammlung ausreichender Informationen, um ein personalisiertes Angebot fГјr Ihr Projekt zu erstellen.",
        "questions": [
            "Art des Projekts (Website, Mobile App, Desktop-Anwendung, etc.)",
            "Hauptziel des Projekts",
            "Zielgruppe",
            "GewГјnschte Funktionen",
            "Design-Vorlieben",
            "Bestehende Referenzen oder Beispiele",
            "Technische Anforderungen",
            "IntegrationsbedГјrfnisse",
            "Inhaltsanforderungen",
            "Zeitrahmen",
            "Budget-Bereich",
            "Nach Fertigstellung benГ¶tigte Dienste",
            "Wie haben Sie von uns erfahren?",
            "Bevorzugte Kommunikationsmethode",
            "ZusГ¤tzliche Informationen"
        ],
        "benefits": [
            "Kostenlose Projektberatung",
            "Personalisiertes Angebot",
            "Klarheit Гјber Projektumfang",
            "Bessere Budget- und ZeitplanschГ¤tzungen",
            "Unverbindliche Anfrage"
        ]
    },
    "ru": {
        "form_title": "Р—Р°РїСЂРѕСЃ РїСЂРѕРµРєС‚Р° - РўРµС…РЅРёС‡РµСЃРєРѕРµ Р·Р°РґР°РЅРёРµ",
        "description": "Р‘РµСЃРїР»Р°С‚РЅР°СЏ, РЅРё Рє С‡РµРјСѓ РЅРµ РѕР±СЏР·С‹РІР°СЋС‰Р°СЏ С„РѕСЂРјР° РёР· 15 РІРѕРїСЂРѕСЃРѕРІ, РєРѕС‚РѕСЂР°СЏ РїРѕРјРѕР¶РµС‚ РІР°Рј С‡РµС‚РєРѕ РѕРїСЂРµРґРµР»РёС‚СЊ С‚СЂРµР±РѕРІР°РЅРёСЏ Рє РїСЂРѕРµРєС‚Сѓ.",
        "purpose": "РЎР±РѕСЂ РґРѕСЃС‚Р°С‚РѕС‡РЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё РґР»СЏ СЃРѕР·РґР°РЅРёСЏ РїРµСЂСЃРѕРЅР°Р»РёР·РёСЂРѕРІР°РЅРЅРѕРіРѕ РїСЂРµРґР»РѕР¶РµРЅРёСЏ РґР»СЏ РІР°С€РµРіРѕ РїСЂРѕРµРєС‚Р°.",
        "questions": [
            "РўРёРї РїСЂРѕРµРєС‚Р° (РІРµР±-СЃР°Р№С‚, РјРѕР±РёР»СЊРЅРѕРµ РїСЂРёР»РѕР¶РµРЅРёРµ, РґРµСЃРєС‚РѕРїРЅРѕРµ РїСЂРёР»РѕР¶РµРЅРёРµ Рё С‚.Рґ.)",
            "РћСЃРЅРѕРІРЅР°СЏ С†РµР»СЊ РїСЂРѕРµРєС‚Р°",
            "Р¦РµР»РµРІР°СЏ Р°СѓРґРёС‚РѕСЂРёСЏ",
            "Р–РµР»Р°РµРјС‹Рµ С„СѓРЅРєС†РёРё",
            "РџСЂРµРґРїРѕС‡С‚РµРЅРёСЏ РїРѕ РґРёР·Р°Р№РЅСѓ",
            "РЎСѓС‰РµСЃС‚РІСѓСЋС‰РёРµ СЂРµС„РµСЂРµРЅСЃС‹ РёР»Рё РїСЂРёРјРµСЂС‹",
            "РўРµС…РЅРёС‡РµСЃРєРёРµ С‚СЂРµР±РѕРІР°РЅРёСЏ",
            "РџРѕС‚СЂРµР±РЅРѕСЃС‚Рё РІ РёРЅС‚РµРіСЂР°С†РёРё",
            "РўСЂРµР±РѕРІР°РЅРёСЏ Рє РєРѕРЅС‚РµРЅС‚Сѓ",
            "Р’СЂРµРјРµРЅРЅС‹Рµ СЂР°РјРєРё",
            "Р”РёР°РїР°Р·РѕРЅ Р±СЋРґР¶РµС‚Р°",
            "РќРµРѕР±С…РѕРґРёРјС‹Рµ СѓСЃР»СѓРіРё РїРѕСЃР»Рµ Р·Р°РІРµСЂС€РµРЅРёСЏ",
            "РљР°Рє РІС‹ Рѕ РЅР°СЃ СѓР·РЅР°Р»Рё?",
            "РџСЂРµРґРїРѕС‡С‚РёС‚РµР»СЊРЅС‹Р№ РјРµС‚РѕРґ СЃРІСЏР·Рё",
            "Р”РѕРїРѕР»РЅРёС‚РµР»СЊРЅР°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ"
        ],
        "benefits": [
            "Р‘РµСЃРїР»Р°С‚РЅР°СЏ РєРѕРЅСЃСѓР»СЊС‚Р°С†РёСЏ РїРѕ РїСЂРѕРµРєС‚Сѓ",
            "РџРµСЂСЃРѕРЅР°Р»РёР·РёСЂРѕРІР°РЅРЅРѕРµ РїСЂРµРґР»РѕР¶РµРЅРёРµ",
            "РЇСЃРЅРѕСЃС‚СЊ РѕС‚РЅРѕСЃРёС‚РµР»СЊРЅРѕ РѕР±СЉРµРјР° РїСЂРѕРµРєС‚Р°",
            "Р›СѓС‡С€РёРµ РѕС†РµРЅРєРё Р±СЋРґР¶РµС‚Р° Рё СЃСЂРѕРєРѕРІ",
            "РќРµРѕР±СЏР·С‹РІР°СЋС‰РёР№ Р·Р°РїСЂРѕСЃ"
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

# РРЅС„РѕСЂРјР°С†РёСЏ Рѕ РєРѕРјРїР°РЅРёРё
COMPANY_INFO = {
    "de": {
        "name": "Andrii-IT",
        "location": "Frankfurt am Main, Deutschland",
        "specialization": "KI-gestГјtzte Softwareentwicklung und DigitallГ¶sungen",
        "unique_selling_points": [
            "KI-Integration in bestehende Systeme",
            "MaГџgeschneiderte Softwareentwicklung",
            "Automatisierung von GeschГ¤ftsprozessen",
            "Datenanalyse und Vorhersagemodelle",
            "Mehrsprachiger Support (Deutsch, Englisch, Russisch)"
        ]
    },
    "ru": {
        "name": "Andrii-IT",
        "location": "Р¤СЂР°РЅРєС„СѓСЂС‚-РЅР°-РњР°Р№РЅРµ, Р“РµСЂРјР°РЅРёСЏ",
        "specialization": "Р Р°Р·СЂР°Р±РѕС‚РєР° РїСЂРѕРіСЂР°РјРјРЅРѕРіРѕ РѕР±РµСЃРїРµС‡РµРЅРёСЏ СЃ РР Рё С†РёС„СЂРѕРІС‹Рµ СЂРµС€РµРЅРёСЏ",
        "unique_selling_points": [
            "РРЅС‚РµРіСЂР°С†РёСЏ РР РІ СЃСѓС‰РµСЃС‚РІСѓСЋС‰РёРµ СЃРёСЃС‚РµРјС‹",
            "РРЅРґРёРІРёРґСѓР°Р»СЊРЅР°СЏ СЂР°Р·СЂР°Р±РѕС‚РєР° РїСЂРѕРіСЂР°РјРјРЅРѕРіРѕ РѕР±РµСЃРїРµС‡РµРЅРёСЏ",
            "РђРІС‚РѕРјР°С‚РёР·Р°С†РёСЏ Р±РёР·РЅРµСЃ-РїСЂРѕС†РµСЃСЃРѕРІ",
            "РђРЅР°Р»РёР· РґР°РЅРЅС‹С… Рё РїСЂРµРґРёРєС‚РёРІРЅС‹Рµ РјРѕРґРµР»Рё",
            "РњРЅРѕРіРѕСЏР·С‹С‡РЅР°СЏ РїРѕРґРґРµСЂР¶РєР° (РЅРµРјРµС†РєРёР№, Р°РЅРіР»РёР№СЃРєРёР№, СЂСѓСЃСЃРєРёР№)"
        ]
    },
    "en": {
        "name": "Andrii-IT",
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

# Р РѕР»Рё Р°СЃСЃРёСЃС‚РµРЅС‚РѕРІ
ASSISTANT_ROLES = {
    "de": {
        "greeter": {
            "role": "BegrГјГџungs-Assistent",
            "description": "BegrГјГџt Besucher, erklГ¤rt die Website und hilft bei der Navigation",
            "goals": [
                "Besucher willkommen heiГџen",
                "Website-Funktionen erklГ¤ren",
                "Zu relevanten Seiten navigieren helfen",
                "HГ¤ufig gestellte Fragen beantworten"
            ]
        },
        "project_consultant": {
            "role": "Projekt-Berater",
            "description": "Hilft Besuchern, ihre Projektanforderungen zu definieren und fГјhrt sie zum TZ-Formular",
            "goals": [
                "Besucher ermutigen, das kostenlose TZ-Formular auszufГјllen",
                "Die Vorteile eines detaillierten technischen Aufgabenblatts erklГ¤ren",
                "Bei Fragen zum Projektumfang helfen",
                "Kontaktdaten sammeln fГјr ein personalisiertes Angebot"
            ]
        },
        "technical_advisor": {
            "role": "Technischer Berater",
            "description": "Beantwortet technische Fragen und gibt Einblicke in unsere Entwicklungsmethoden",
            "goals": [
                "Technische Fragen zu unseren Entwicklungsprozessen beantworten",
                "Verwendete Technologien erklГ¤ren",
                "Projektmachbarkeit bewerten",
                "Technische Aspekte verschiedener LГ¶sungen erlГ¤utern"
            ]
        }
    },
    "ru": {
        "greeter": {
            "role": "РџСЂРёРІРµС‚СЃС‚РІСѓСЋС‰РёР№ Р°СЃСЃРёСЃС‚РµРЅС‚",
            "description": "РџСЂРёРІРµС‚СЃС‚РІСѓРµС‚ РїРѕСЃРµС‚РёС‚РµР»РµР№, РѕР±СЉСЏСЃРЅСЏРµС‚ С„СѓРЅРєС†РёРё СЃР°Р№С‚Р° Рё РїРѕРјРѕРіР°РµС‚ СЃ РЅР°РІРёРіР°С†РёРµР№",
            "goals": [
                "РџРѕРїСЂРёРІРµС‚СЃС‚РІРѕРІР°С‚СЊ РїРѕСЃРµС‚РёС‚РµР»РµР№",
                "РћР±СЉСЏСЃРЅРёС‚СЊ С„СѓРЅРєС†РёРё СЃР°Р№С‚Р°",
                "РџРѕРјРѕС‡СЊ СЃ РЅР°РІРёРіР°С†РёРµР№ РїРѕ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РёРј СЃС‚СЂР°РЅРёС†Р°Рј",
                "РћС‚РІРµС‚РёС‚СЊ РЅР° С‡Р°СЃС‚Рѕ Р·Р°РґР°РІР°РµРјС‹Рµ РІРѕРїСЂРѕСЃС‹"
            ]
        },
        "project_consultant": {
            "role": "РљРѕРЅСЃСѓР»СЊС‚Р°РЅС‚ РїРѕ РїСЂРѕРµРєС‚Р°Рј",
            "description": "РџРѕРјРѕРіР°РµС‚ РїРѕСЃРµС‚РёС‚РµР»СЏРј РѕРїСЂРµРґРµР»РёС‚СЊ С‚СЂРµР±РѕРІР°РЅРёСЏ Рє РїСЂРѕРµРєС‚Сѓ Рё РЅР°РїСЂР°РІР»СЏРµС‚ РёС… Рє С„РѕСЂРјРµ РўР—",
            "goals": [
                "РџРѕРѕС‰СЂСЏС‚СЊ РїРѕСЃРµС‚РёС‚РµР»РµР№ Р·Р°РїРѕР»РЅРёС‚СЊ Р±РµСЃРїР»Р°С‚РЅСѓСЋ С„РѕСЂРјСѓ РўР—",
                "РћР±СЉСЏСЃРЅРёС‚СЊ РїСЂРµРёРјСѓС‰РµСЃС‚РІР° РїРѕРґСЂРѕР±РЅРѕРіРѕ С‚РµС…РЅРёС‡РµСЃРєРѕРіРѕ Р·Р°РґР°РЅРёСЏ",
                "РџРѕРјРѕС‡СЊ СЃ РІРѕРїСЂРѕСЃР°РјРё РѕР± РѕР±СЉРµРјРµ РїСЂРѕРµРєС‚Р°",
                "РЎРѕР±СЂР°С‚СЊ РєРѕРЅС‚Р°РєС‚РЅС‹Рµ РґР°РЅРЅС‹Рµ РґР»СЏ РїРµСЂСЃРѕРЅР°Р»РёР·РёСЂРѕРІР°РЅРЅРѕРіРѕ РїСЂРµРґР»РѕР¶РµРЅРёСЏ"
            ]
        },
        "technical_advisor": {
            "role": "РўРµС…РЅРёС‡РµСЃРєРёР№ РєРѕРЅСЃСѓР»СЊС‚Р°РЅС‚",
            "description": "РћС‚РІРµС‡Р°РµС‚ РЅР° С‚РµС…РЅРёС‡РµСЃРєРёРµ РІРѕРїСЂРѕСЃС‹ Рё РґР°РµС‚ РїСЂРµРґСЃС‚Р°РІР»РµРЅРёРµ Рѕ РЅР°С€РёС… РјРµС‚РѕРґР°С… СЂР°Р·СЂР°Р±РѕС‚РєРё",
            "goals": [
                "РћС‚РІРµС‚РёС‚СЊ РЅР° С‚РµС…РЅРёС‡РµСЃРєРёРµ РІРѕРїСЂРѕСЃС‹ Рѕ РЅР°С€РёС… РїСЂРѕС†РµСЃСЃР°С… СЂР°Р·СЂР°Р±РѕС‚РєРё",
                "РћР±СЉСЏСЃРЅРёС‚СЊ РёСЃРїРѕР»СЊР·СѓРµРјС‹Рµ С‚РµС…РЅРѕР»РѕРіРёРё",
                "РћС†РµРЅРёС‚СЊ РІС‹РїРѕР»РЅРёРјРѕСЃС‚СЊ РїСЂРѕРµРєС‚Р°",
                "РћР±СЉСЏСЃРЅРёС‚СЊ С‚РµС…РЅРёС‡РµСЃРєРёРµ Р°СЃРїРµРєС‚С‹ СЂР°Р·Р»РёС‡РЅС‹С… СЂРµС€РµРЅРёР№"
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
    """Р‘РµР·РѕРїР°СЃРЅРѕ РІС‹Р±РёСЂР°РµС‚ Р»РѕРєР°Р»РёР·Р°С†РёСЋ: СЃРЅР°С‡Р°Р»Р° lang, Р·Р°С‚РµРј РїРѕ РїРѕСЂСЏРґРєСѓ РёР· fallbacks."""
    if lang in d:
        return d[lang]
    for fb in fallbacks:
        if fb in d:
            return d[fb]
    # РєР°Рє РїРѕСЃР»РµРґРЅРёР№ РІР°СЂРёР°РЅС‚ — Р±РµСЂРµРј Р»СЋР±РѕР№
    return next(iter(d.values()))


def get_site_info(lang='en'):
    """Р’РѕР·РІСЂР°С‰Р°РµС‚ СЃРІРѕРґРЅСѓСЋ РёРЅС„РѕСЂРјР°С†РёСЋ Рѕ СЃР°Р№С‚Рµ Рё Р±СЂРёС„-С„РѕСЂРјР°С… РґР»СЏ Р°СЃСЃРёСЃС‚РµРЅС‚РѕРІ."""
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
    """РћС‚РґР°РµС‚ СЃС‚СЂСѓРєС‚СѓСЂСѓ С„РѕСЂРјС‹ РўР— РЅР° СЃС‚СЂР°РЅРёС†Рµ /services РґР»СЏ СѓРєР°Р·Р°РЅРЅРѕРіРѕ СЏР·С‹РєР° (СЃ Р±РµР·РѕРїР°СЃРЅС‹Рј С„РѕР»Р±СЌРєРѕРј)."""
    return _pick_lang(SERVICES_TZ_FORM, lang)


def spec_agent_context(lang='en') -> str:
    """РљРѕСЂРѕС‚РєРёР№ С‚РµРєСЃС‚-РєРѕРЅС‚РµРєСЃС‚ РґР»СЏ Р°СЃСЃРёСЃС‚РµРЅС‚Р° SPEC: РіРґРµ С„РѕСЂРјР° РўР— Рё С‡С‚Рѕ РІ РЅРµР№ Р·Р°РїРѕР»РЅСЏС‚СЊ."""
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
        lines.append(f"вЂў {sec.get('title')}:")
        for f in sec.get('fields', []):
            lines.append(f"  вЂ“ {f}")
    cta = info.get("cta")
    if cta:
        lines.append("")
        lines.append(cta)
    return "\n".join(lines)

