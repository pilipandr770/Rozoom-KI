from typing import Callable, Iterable, Mapping, Sequence

from flask import current_app, g, request, url_for


SUPPORTED_LANGUAGES: Sequence[str] = ("en", "de", "uk")


def _t(en: str, de: str, ru: str | None = None, uk: str | None = None) -> dict[str, str]:
    data = {"en": en, "de": de}
    if uk is not None:
        data["uk"] = uk
    return data


OG_LOCALE_MAP = {
    "en": "en_US",
    "de": "de_DE",
    "uk": "uk_UA",
}

DEFAULT_SITE_DESCRIPTIONS = _t(
    "Rozoom-KI delivers multilingual AI assistants, automation and custom software for modern businesses.",
    "Rozoom-KI delivers multilingual AI assistants, automation and custom software for modern businesses.",
    "Rozoom-KI delivers multilingual AI assistants, automation and custom software for modern businesses.",
    "Rozoom-KI delivers multilingual AI assistants, automation and custom software for modern businesses.",
)

DEFAULT_KEYWORDS = _t(
    "AI solutions, chatbot development, business automation, Rozoom-KI",
    "AI solutions, chatbot development, business automation, Rozoom-KI",
    "AI solutions, chatbot development, business automation, Rozoom-KI",
    "AI solutions, chatbot development, business automation, Rozoom-KI",
)

DEFAULT_IMAGE_ALT = _t(
    "Rozoom-KI default social sharing illustration",
    "Rozoom-KI default social sharing illustration",
    "Rozoom-KI default social sharing illustration",
    "Rozoom-KI default social sharing illustration",
)

BLOG_LISTING_META = {
    "title": _t(
        "Rozoom-KI Blog - Insights on AI and Automation",
        "Rozoom-KI Blog - Insights on AI and Automation",
        "Rozoom-KI Blog - Insights on AI and Automation",
        "Rozoom-KI Blog - Insights on AI and Automation",
    ),
    "description": _t(
        "Articles and case studies on AI assistants, automation and digital transformation from the Rozoom-KI team.",
        "Articles and case studies on AI assistants, automation and digital transformation from the Rozoom-KI team.",
        "Articles and case studies on AI assistants, automation and digital transformation from the Rozoom-KI team.",
        "Articles and case studies on AI assistants, automation and digital transformation from the Rozoom-KI team.",
    ),
    "keywords": _t(
        "AI blog, automation insights, Rozoom-KI",
        "AI blog, automation insights, Rozoom-KI",
        "AI blog, automation insights, Rozoom-KI",
        "AI blog, automation insights, Rozoom-KI",
    ),
    "preserve_query": ["page"],
}

BLOG_CATEGORY_META = {
    "title": _t(
        "Rozoom-KI Blog - Category Insights",
        "Rozoom-KI Blog - Category Insights",
        "Rozoom-KI Blog - Category Insights",
        "Rozoom-KI Blog - Category Insights",
    ),
    "description": _t(
        "Browse curated AI and automation articles filtered by topic on the Rozoom-KI blog.",
        "Browse curated AI and automation articles filtered by topic on the Rozoom-KI blog.",
        "Browse curated AI and automation articles filtered by topic on the Rozoom-KI blog.",
        "Browse curated AI and automation articles filtered by topic on the Rozoom-KI blog.",
    ),
    "keywords": _t(
        "AI categories, automation topics, Rozoom-KI blog",
        "AI categories, automation topics, Rozoom-KI blog",
        "AI categories, automation topics, Rozoom-KI blog",
        "AI categories, automation topics, Rozoom-KI blog",
    ),
    "preserve_query": ["page"],
}

BLOG_TAG_META = {
    "title": _t(
        "Rozoom-KI Blog - Tagged Articles",
        "Rozoom-KI Blog - Tagged Articles",
        "Rozoom-KI Blog - Tagged Articles",
        "Rozoom-KI Blog - Tagged Articles",
    ),
    "description": _t(
        "Discover AI automation articles grouped by tag and technology focus.",
        "Discover AI automation articles grouped by tag and technology focus.",
        "Discover AI automation articles grouped by tag and technology focus.",
        "Discover AI automation articles grouped by tag and technology focus.",
    ),
    "keywords": _t(
        "AI tags, automation tags, Rozoom-KI",
        "AI tags, automation tags, Rozoom-KI",
        "AI tags, automation tags, Rozoom-KI",
        "AI tags, automation tags, Rozoom-KI",
    ),
    "preserve_query": ["page"],
}

PAGE_SEO_DATA = {
    "default": {
        "description": DEFAULT_SITE_DESCRIPTIONS,
        "keywords": DEFAULT_KEYWORDS,
        "image_alt": DEFAULT_IMAGE_ALT,
    },
    "pages.index": {
        "title": _t(
            "Rozoom-KI - AI Solutions, Chatbots and Automation",
            "Rozoom-KI - AI Solutions, Chatbots and Automation",
            "Rozoom-KI - AI Solutions, Chatbots and Automation",
            "Rozoom-KI - AI Solutions, Chatbots and Automation",
        ),
        "description": _t(
            "Rozoom-KI builds multilingual AI assistants, automation workflows and custom software for fast-growing companies.",
            "Rozoom-KI builds multilingual AI assistants, automation workflows and custom software for fast-growing companies.",
            "Rozoom-KI builds multilingual AI assistants, automation workflows and custom software for fast-growing companies.",
            "Rozoom-KI builds multilingual AI assistants, automation workflows and custom software for fast-growing companies.",
        ),
        "keywords": _t(
            "AI agency, chatbot development, automation services, Rozoom-KI",
            "AI agency, chatbot development, automation services, Rozoom-KI",
            "AI agency, chatbot development, automation services, Rozoom-KI",
            "AI agency, chatbot development, automation services, Rozoom-KI",
        ),
        "image_alt": _t(
            "Stylised illustration representing Rozoom-KI AI services",
            "Stylised illustration representing Rozoom-KI AI services",
            "Stylised illustration representing Rozoom-KI AI services",
            "Stylised illustration representing Rozoom-KI AI services",
        ),
        "structured_data": ["website", "organization"],
    },
    "pages.services": {
        "title": _t(
            "AI Services and Automation - Rozoom-KI",
            "AI Services and Automation - Rozoom-KI",
            "AI Services and Automation - Rozoom-KI",
            "AI Services and Automation - Rozoom-KI",
        ),
        "description": _t(
            "Explore Rozoom-KI services for AI assistants, machine learning integration and workflow automation tailored to your goals.",
            "Explore Rozoom-KI services for AI assistants, machine learning integration and workflow automation tailored to your goals.",
            "Explore Rozoom-KI services for AI assistants, machine learning integration and workflow automation tailored to your goals.",
            "Explore Rozoom-KI services for AI assistants, machine learning integration and workflow automation tailored to your goals.",
        ),
        "keywords": _t(
            "AI services, machine learning integration, workflow automation, Rozoom-KI",
            "AI services, machine learning integration, workflow automation, Rozoom-KI",
            "AI services, machine learning integration, workflow automation, Rozoom-KI",
            "AI services, machine learning integration, workflow automation, Rozoom-KI",
        ),
    },
    "pages.pricing": {
        "title": _t(
            "Pricing and Packages - Rozoom-KI",
            "Pricing and Packages - Rozoom-KI",
            "Pricing and Packages - Rozoom-KI",
            "Pricing and Packages - Rozoom-KI",
        ),
        "description": _t(
            "Review Rozoom-KI pricing packages for AI development, chatbot delivery and automation retainers.",
            "Review Rozoom-KI pricing packages for AI development, chatbot delivery and automation retainers.",
            "Review Rozoom-KI pricing packages for AI development, chatbot delivery and automation retainers.",
            "Review Rozoom-KI pricing packages for AI development, chatbot delivery and automation retainers.",
        ),
        "keywords": _t(
            "AI pricing, chatbot packages, automation retainers, Rozoom-KI",
            "AI pricing, chatbot packages, automation retainers, Rozoom-KI",
            "AI pricing, chatbot packages, automation retainers, Rozoom-KI",
            "AI pricing, chatbot packages, automation retainers, Rozoom-KI",
        ),
    },
    "pages.faq": {
        "title": _t(
            "FAQ - Rozoom-KI",
            "FAQ - Rozoom-KI",
            "FAQ - Rozoom-KI",
            "FAQ - Rozoom-KI",
        ),
        "description": _t(
            "Answers to frequent questions about Rozoom-KI AI solutions, onboarding and delivery timelines.",
            "Answers to frequent questions about Rozoom-KI AI solutions, onboarding and delivery timelines.",
            "Answers to frequent questions about Rozoom-KI AI solutions, onboarding and delivery timelines.",
            "Answers to frequent questions about Rozoom-KI AI solutions, onboarding and delivery timelines.",
        ),
    },
    "pages.about": {
        "title": _t(
            "About Rozoom-KI - AI Experts in Europe",
            "About Rozoom-KI - AI Experts in Europe",
            "About Rozoom-KI - AI Experts in Europe",
            "About Rozoom-KI - AI Experts in Europe",
        ),
        "description": _t(
            "Learn about Rozoom-KI's mission, team and experience delivering multilingual AI products across Europe.",
            "Learn about Rozoom-KI's mission, team and experience delivering multilingual AI products across Europe.",
            "Learn about Rozoom-KI's mission, team and experience delivering multilingual AI products across Europe.",
            "Learn about Rozoom-KI's mission, team and experience delivering multilingual AI products across Europe.",
        ),
    },
    "pages.contact": {
        "title": _t(
            "Contact Rozoom-KI - Start Your AI Project",
            "Contact Rozoom-KI - Start Your AI Project",
            "Contact Rozoom-KI - Start Your AI Project",
            "Contact Rozoom-KI - Start Your AI Project",
        ),
        "description": _t(
            "Reach out to Rozoom-KI for AI consulting, project estimates or partnership opportunities.",
            "Reach out to Rozoom-KI for AI consulting, project estimates or partnership opportunities.",
            "Reach out to Rozoom-KI for AI consulting, project estimates or partnership opportunities.",
            "Reach out to Rozoom-KI for AI consulting, project estimates or partnership opportunities.",
        ),
        "keywords": _t(
            "contact Rozoom-KI, AI consultation, start AI project",
            "contact Rozoom-KI, AI consultation, start AI project",
            "contact Rozoom-KI, AI consultation, start AI project",
            "contact Rozoom-KI, AI consultation, start AI project",
        ),
        "structured_data": ["contact_page"],
    },
    "pages.blog": BLOG_LISTING_META,
    "blog.index": BLOG_LISTING_META,
    "blog.category": BLOG_CATEGORY_META,
    "blog.tag": BLOG_TAG_META,
    "blog.search": {
        "title": _t(
            "Rozoom-KI Blog - Search Results",
            "Rozoom-KI Blog - Search Results",
            "Rozoom-KI Blog - Search Results",
            "Rozoom-KI Blog - Search Results",
        ),
        "description": _t(
            "Search AI and automation articles on the Rozoom-KI blog by keyword or topic.",
            "Search AI and automation articles on the Rozoom-KI blog by keyword or topic.",
            "Search AI and automation articles on the Rozoom-KI blog by keyword or topic.",
            "Search AI and automation articles on the Rozoom-KI blog by keyword or topic.",
        ),
        "keywords": _t(
            "search AI articles, Rozoom-KI blog",
            "search AI articles, Rozoom-KI blog",
            "search AI articles, Rozoom-KI blog",
            "search AI articles, Rozoom-KI blog",
        ),
        "preserve_query": ["q", "page"],
        "robots": _t("noindex, nofollow", "noindex, nofollow", "noindex, nofollow", "noindex, nofollow"),
    },
    "blog.post": {
        "og_type": _t("article", "article", "article", "article"),
    },
    "pages.impressum": {
        "title": _t(
            "Imprint - Rozoom-KI",
            "Imprint - Rozoom-KI",
            "Imprint - Rozoom-KI",
            "Imprint - Rozoom-KI",
        ),
        "description": _t(
            "Official company information and legal disclosure for Rozoom-KI.",
            "Official company information and legal disclosure for Rozoom-KI.",
            "Official company information and legal disclosure for Rozoom-KI.",
            "Official company information and legal disclosure for Rozoom-KI.",
        ),
    },
    "pages.privacy": {
        "title": _t(
            "Privacy Policy - Rozoom-KI",
            "Privacy Policy - Rozoom-KI",
            "Privacy Policy - Rozoom-KI",
            "Privacy Policy - Rozoom-KI",
        ),
        "description": _t(
            "Learn how Rozoom-KI collects, uses and protects personal data across our AI services.",
            "Learn how Rozoom-KI collects, uses and protects personal data across our AI services.",
            "Learn how Rozoom-KI collects, uses and protects personal data across our AI services.",
            "Learn how Rozoom-KI collects, uses and protects personal data across our AI services.",
        ),
    },
    "pages.terms": {
        "title": _t(
            "Terms of Service - Rozoom-KI",
            "Terms of Service - Rozoom-KI",
            "Terms of Service - Rozoom-KI",
            "Terms of Service - Rozoom-KI",
        ),
        "description": _t(
            "Review the terms governing access to Rozoom-KI platforms, AI assistants and managed services.",
            "Review the terms governing access to Rozoom-KI platforms, AI assistants and managed services.",
            "Review the terms governing access to Rozoom-KI platforms, AI assistants and managed services.",
            "Review the terms governing access to Rozoom-KI platforms, AI assistants and managed services.",
        ),
    },
}

STRUCTURED_DATA_BUILDERS: dict[str, Callable[..., dict | None]] = {}


def _localized(value, locale):
    if isinstance(value, Mapping):
        return value.get(locale) or value.get("en") or next(iter(value.values()), None)
    return value


def _get_locale() -> str:
    locale = getattr(g, "locale", None)
    if not locale:
        locale = current_app.config.get("BABEL_DEFAULT_LOCALE", "en")
    if locale not in SUPPORTED_LANGUAGES:
        locale = "en"
    return locale


def _resolve_image(image_value: str | None, fallback: str | None) -> str | None:
    if not image_value:
        return fallback
    if image_value.startswith("http"):
        return image_value
    fname = image_value.lstrip("/")
    if fname.startswith("static/"):
        fname = fname[len("static/"):]
    try:
        return url_for("static", filename=fname, _external=True)
    except Exception:
        return fallback


def _ensure_absolute_url(url_value: str | None) -> str | None:
    if not url_value:
        return None
    if url_value.startswith("http"):
        return url_value
    base = request.url_root.rstrip("/")
    if not url_value.startswith("/"):
        url_value = f"/{url_value}"
    return f"{base}{url_value}"


def _collect_preserved_query(keys: Iterable[str]) -> dict[str, str]:
    preserved: dict[str, str] = {}
    for key in keys:
        if key == "lang":
            continue
        if key not in request.args:
            continue
        value = request.args.get(key)
        if value is None or value == "":
            continue
        if key == "page" and value in {"1", 1}:
            continue
        preserved[key] = str(value)
    return preserved


def _build_url_for_lang(endpoint: str, view_args: Mapping[str, object], query_args: Mapping[str, str], lang_code: str | None) -> str:
    if not endpoint:
        return ""
    args = dict(view_args or {})
    query = dict(query_args or {})
    if lang_code:
        query["lang"] = lang_code
    else:
        query.pop("lang", None)
    try:
        return url_for(endpoint, _external=True, **args, **query)
    except Exception:
        return ""


def _structured_website(locale: str, site_name: str, site_url: str, canonical_url: str | None, default_image: str | None):
    data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site_name,
        "url": site_url,
        "inLanguage": locale,
    }
    try:
        search_url = url_for("blog.search", _external=True)
    except Exception:
        search_url = ""
    if search_url:
        target = f"{search_url}?q={{search_term_string}}"
        data["potentialAction"] = {
            "@type": "SearchAction",
            "target": target,
            "query-input": "required name=search_term_string",
        }
    return data


def _structured_organization(locale: str, site_name: str, site_url: str, canonical_url: str | None, default_image: str | None):
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": site_name,
        "url": site_url,
        "inLanguage": locale,
    }
    if default_image:
        data["logo"] = default_image
    return data


def _structured_contact_page(locale: str, site_name: str, site_url: str, canonical_url: str | None, default_image: str | None):
    if not canonical_url:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "name": f"Contact {site_name}",
        "url": canonical_url,
        "inLanguage": locale,
        "mainEntityOfPage": canonical_url,
    }


STRUCTURED_DATA_BUILDERS.update(
    {
        "website": _structured_website,
        "organization": _structured_organization,
        "contact_page": _structured_contact_page,
    }
)


def _build_structured_data(keys: Iterable[str], locale: str, site_name: str, site_url: str, canonical_url: str | None, default_image: str | None) -> list[dict]:
    data: list[dict] = []
    for key in keys:
        builder = STRUCTURED_DATA_BUILDERS.get(key)
        if not builder:
            continue
        item = builder(locale, site_name, site_url, canonical_url, default_image)
        if item:
            data.append(item)
    return data


def init_app(app):
    @app.context_processor
    def inject_seo_defaults():
        '''Provide site-wide SEO defaults and helpers to templates.'''
        locale = _get_locale()
        site_name = app.config.get("SITE_NAME", "Rozoom-KI")

        site_description = _localized(DEFAULT_SITE_DESCRIPTIONS, locale) or app.config.get("SITE_DESCRIPTION", "")
        site_keywords = _localized(DEFAULT_KEYWORDS, locale)

        site_image_cfg = app.config.get("SITE_IMAGE", "img/og-default.svg")
        default_image = _resolve_image(site_image_cfg, None)
        if not default_image:
            default_image = url_for("static", filename="img/og-default.png", _external=True)

        endpoint = request.endpoint or ""
        base_config = PAGE_SEO_DATA.get("default", {})
        page_config = PAGE_SEO_DATA.get(endpoint, {})

        seo_meta: dict[str, object] = {}

        def merge_config(config: Mapping[str, object]):
            for key, value in (config or {}).items():
                if key in {"structured_data", "preserve_query", "add_lang_param"}:
                    continue
                localized_value = _localized(value, locale)
                if localized_value:
                    seo_meta[key] = localized_value

        merge_config(base_config)
        merge_config(page_config)

        if "description" not in seo_meta and site_description:
            seo_meta["description"] = site_description
        if "keywords" not in seo_meta and site_keywords:
            seo_meta["keywords"] = site_keywords
        if "title" not in seo_meta:
            seo_meta["title"] = site_name

        image_override = seo_meta.get("image") if isinstance(seo_meta.get("image"), str) else None
        seo_meta["image"] = _resolve_image(image_override, default_image)

        if "image_alt" not in seo_meta:
            image_alt = _localized(base_config.get("image_alt"), locale)
            if image_alt:
                seo_meta["image_alt"] = image_alt

        seo_meta.setdefault("og_title", seo_meta.get("title"))
        seo_meta.setdefault("twitter_title", seo_meta.get("title"))
        seo_meta.setdefault("og_description", seo_meta.get("description"))
        seo_meta.setdefault("twitter_description", seo_meta.get("description"))
        seo_meta.setdefault("og_type", "website")
        seo_meta.setdefault("twitter_card", "summary_large_image")
        seo_meta.setdefault("robots", "index,follow")
        seo_meta.setdefault("twitter_image", seo_meta.get("image"))

        preserve_query: list[str] = []
        for key in base_config.get("preserve_query", []):
            if key not in preserve_query:
                preserve_query.append(key)
        for key in page_config.get("preserve_query", []):
            if key not in preserve_query:
                preserve_query.append(key)

        add_lang_param = page_config.get("add_lang_param")
        if add_lang_param is None:
            add_lang_param = True

        view_args = dict(request.view_args or {})
        query_args = _collect_preserved_query(preserve_query)

        canonical_override = _localized(page_config.get("canonical"), locale)
        canonical_url = _ensure_absolute_url(canonical_override) if canonical_override else ""
        if not canonical_url:
            lang_for_canonical = locale if add_lang_param else None
            canonical_url = _build_url_for_lang(endpoint, view_args, query_args, lang_for_canonical)
        if not canonical_url:
            canonical_url = request.url
        seo_meta["canonical"] = canonical_url

        site_url = request.url_root.rstrip("/")

        supported_langs = [lang for lang in current_app.config.get("LANGUAGES", SUPPORTED_LANGUAGES) if lang in SUPPORTED_LANGUAGES]
        alternate_hreflangs: list[dict[str, str]] = []
        seen: set[tuple[str, str]] = set()
        if endpoint:
            for lang_code in supported_langs:
                lang_param = lang_code if add_lang_param else None
                href = _build_url_for_lang(endpoint, view_args, query_args, lang_param)
                if not href:
                    continue
                key = (lang_code, href)
                if key in seen:
                    continue
                alternate_hreflangs.append({"lang": lang_code, "href": href})
                seen.add(key)
            x_default_href = _build_url_for_lang(endpoint, view_args, query_args, None)
            if x_default_href and ("x-default", x_default_href) not in seen:
                alternate_hreflangs.append({"lang": "x-default", "href": x_default_href})

        og_locale = OG_LOCALE_MAP.get(locale)
        if og_locale:
            seo_meta["og_locale"] = og_locale
            alt_locales = [OG_LOCALE_MAP.get(code) for code in supported_langs if code != locale and OG_LOCALE_MAP.get(code)]
            seo_meta["og_locale_alternates"] = alt_locales
        else:
            seo_meta["og_locale_alternates"] = []

        structured_keys: list[str] = []
        for key in base_config.get("structured_data", []):
            if key not in structured_keys:
                structured_keys.append(key)
        for key in page_config.get("structured_data", []):
            if key not in structured_keys:
                structured_keys.append(key)
        structured_data = _build_structured_data(structured_keys, locale, site_name, site_url, canonical_url, seo_meta.get("image"))
        seo_meta["structured_data"] = structured_data

        default_description = seo_meta.get("description", site_description)

        return dict(
            site_name=site_name,
            default_description=default_description,
            default_image=default_image,
            canonical_url=canonical_url,
            seo_meta=seo_meta,
            alternate_hreflangs=alternate_hreflangs,
        )

    return app


