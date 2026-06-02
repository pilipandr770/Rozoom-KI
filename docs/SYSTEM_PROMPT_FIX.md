# РСЃРїСЂР°РІР»РµРЅРёРµ РѕС‚СЃСѓС‚СЃС‚РІСѓСЋС‰РµР№ С„СѓРЅРєС†РёРё get_system_prompt

## РћР±РЅР°СЂСѓР¶РµРЅРЅР°СЏ РїСЂРѕР±Р»РµРјР°

РџСЂРё Р·Р°РїСѓСЃРєРµ РїСЂРёР»РѕР¶РµРЅРёСЏ РІРѕР·РЅРёРєР°Р»Р° РѕС€РёР±РєР°:

```
NameError: name 'get_system_prompt' is not defined. Did you mean: 'get_greeter_prompt'?
```

## РџСЂРёС‡РёРЅР° РїСЂРѕР±Р»РµРјС‹

Р’ РјРѕРґСѓР»Рµ `app/agents/prompts.py` Р±С‹Р»Рё РѕРїСЂРµРґРµР»РµРЅС‹ Р°Р»РёР°СЃС‹ С„СѓРЅРєС†РёР№ РґР»СЏ РѕР±РµСЃРїРµС‡РµРЅРёСЏ РѕР±СЂР°С‚РЅРѕР№ СЃРѕРІРјРµСЃС‚РёРјРѕСЃС‚Рё СЃ `controller.py`, РѕРґРЅР°РєРѕ РѕС‚СЃСѓС‚СЃС‚РІРѕРІР°Р»Р° СЃР°РјР° С„СѓРЅРєС†РёСЏ `get_system_prompt`, РЅР° РєРѕС‚РѕСЂСѓСЋ СЃСЃС‹Р»Р°Р»РёСЃСЊ СЌС‚Рё Р°Р»РёР°СЃС‹:

```python
# РђР»РёР°СЃС‹ РґР»СЏ РѕР±РµСЃРїРµС‡РµРЅРёСЏ РѕР±СЂР°С‚РЅРѕР№ СЃРѕРІРјРµСЃС‚РёРјРѕСЃС‚Рё
# controller.py РёСЃРїРѕР»СЊР·СѓРµС‚ create_* РІРјРµСЃС‚Рѕ get_*
create_system_prompt = get_system_prompt  # РћС€РёР±РєР°: get_system_prompt РЅРµ РѕРїСЂРµРґРµР»РµРЅР°
create_greeter_prompt = get_greeter_prompt
create_completion_prompt = get_completion_prompt
create_portfolio_prompt = get_portfolio_prompt
```

## Р РµС€РµРЅРёРµ

Р’ РјРѕРґСѓР»СЊ `app/agents/prompts.py` РґРѕР±Р°РІР»РµРЅР° СЂРµР°Р»РёР·Р°С†РёСЏ РѕС‚СЃСѓС‚СЃС‚РІСѓСЋС‰РµР№ С„СѓРЅРєС†РёРё `get_system_prompt`:

```python
def get_system_prompt(lang='de'):
    """
    Р’РѕР·РІСЂР°С‰Р°РµС‚ СЃРёСЃС‚РµРјРЅС‹Р№ РїСЂРѕРјРїС‚
    
    Args:
        lang: РљРѕРґ СЏР·С‹РєР° ('de', 'ru', 'en')
        
    Returns:
        str: РЎРёСЃС‚РµРјРЅС‹Р№ РїСЂРѕРјРїС‚ РЅР° СѓРєР°Р·Р°РЅРЅРѕРј СЏР·С‹РєРµ
    """
    prompts = {
        'de': """Du bist ein KI-Assistent fГјr die Andrii-IT Website. Deine Hauptaufgabe ist es, Besuchern zu helfen, Fragen zu beantworten und sie durch die Website zu fГјhren.""",
        'ru': """РўС‹ РР-Р°СЃСЃРёСЃС‚РµРЅС‚ РґР»СЏ СЃР°Р№С‚Р° Andrii-IT. РўРІРѕСЏ РѕСЃРЅРѕРІРЅР°СЏ Р·Р°РґР°С‡Р° - РїРѕРјРѕРіР°С‚СЊ РїРѕСЃРµС‚РёС‚РµР»СЏРј, РѕС‚РІРµС‡Р°С‚СЊ РЅР° РІРѕРїСЂРѕСЃС‹ Рё РЅР°РїСЂР°РІР»СЏС‚СЊ РёС… РїРѕ СЃР°Р№С‚Сѓ.""",
        'en': """You are an AI assistant for the Andrii-IT website. Your main task is to help visitors, answer questions, and guide them through the website."""
    }
    return prompts.get(lang, prompts['de'])
```

РўРµРїРµСЂСЊ Р°Р»РёР°СЃС‹ РєРѕСЂСЂРµРєС‚РЅРѕ СЃСЃС‹Р»Р°СЋС‚СЃСЏ РЅР° СЃСѓС‰РµСЃС‚РІСѓСЋС‰СѓСЋ С„СѓРЅРєС†РёСЋ.

## РџСЂРѕРІРµСЂРєР°

РџРѕСЃР»Рµ РІРЅРµСЃРµРЅРёСЏ РёР·РјРµРЅРµРЅРёР№ РїСЂРѕРІРµРґРµРЅР° РїСЂРѕРІРµСЂРєР° РєРѕРјРїРёР»СЏС†РёРё РѕР±РѕРёС… С„Р°Р№Р»РѕРІ:

```
python -m py_compile app\agents\prompts.py
python -m py_compile app\agents\controller.py
```

РћР±Р° С„Р°Р№Р»Р° СѓСЃРїРµС€РЅРѕ СЃРєРѕРјРїРёР»РёСЂРѕРІР°Р»РёСЃСЊ, С‡С‚Рѕ РїРѕРґС‚РІРµСЂР¶РґР°РµС‚ СЂРµС€РµРЅРёРµ РїСЂРѕР±Р»РµРјС‹ СЃ РѕС‚СЃСѓС‚СЃС‚РІСѓСЋС‰РµР№ С„СѓРЅРєС†РёРµР№.

