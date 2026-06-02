# UI/UX Roadmap (June 2026)

## Context
Goal: refresh visual quality, improve trust perception, and increase lead conversion without breaking existing platform functionality.

## SWOT (Current State)

### Strengths
- Strong functional core: multilingual content, AI chat, blog, payment flow, client dashboard.
- Good SEO foundation in base template (meta, OG, hreflang, structured data).
- Clear commercial funnel elements (services, pricing, contact, CTA blocks).

### Weaknesses
- Fragmented visual system: many CSS layers and patch files are loaded globally.
- Inconsistent style language between pages (dark/glass + white cards + inline page styles).
- Homepage uses inline animation delays and decorative noise that can hurt clarity.
- Placeholder social links on contact page reduce trust.

### Opportunities
- Conversion lift from cleaner hierarchy and stronger first-screen value proposition.
- Faster future delivery after introducing design tokens and componentized styles.
- Better mobile UX and loading speed can improve both SEO and lead quality.

### Threats
- Outdated visual perception vs. competitors can reduce trust and response rates.
- Effects-heavy rendering can hurt performance and first impressions.
- Ongoing patch-based styling increases maintenance and regression risk.

## Work Plan

### Phase 1 (1-2 weeks): Quick Wins
- Define one visual direction (typography, color, spacing, button/card standards).
- Simplify homepage hero and reduce decorative noise.
- Replace/clean trust-breaking UI details (placeholder social links, inconsistent accents).
- Add a final UI override layer for safe incremental modernization.

### Phase 2 (3-5 weeks): Systematization
- Build design tokens and shared components (hero, card, section, CTA, form).
- Refactor CSS structure into predictable layers (base/components/pages/utilities).
- Unify key commercial pages: home, services, pricing, contact.

### Phase 3 (6-8 weeks): Conversion and Performance
- Optimize Core Web Vitals (LCP/CLS/INP) and reduce non-critical visual payload.
- Run conversion experiments on hero copy, CTA ordering, and form friction.
- Add stronger proof blocks (case outcomes, process, guarantees, delivery clarity).

## KPI Tracking
- Primary: lead conversion rate to contact/request/payment.
- Secondary: CTA click-through, form completion rate, bounce rate, mobile Lighthouse.

## Implementation Log
- 2026-06-02: Roadmap documented.
- 2026-06-02: Phase 1 implementation started (homepage visual refresh + modern override layer).
- 2026-06-02: Contact trust quick win completed (placeholder social links replaced with real contact actions).
- 2026-06-02: Services and Pricing pages aligned to modern refresh layer; inline pricing style block removed.
- 2026-06-02: Mobile visual noise reduced (particles/background effects softened or disabled on small screens and reduced-motion preference).
- 2026-06-02: About and FAQ upgraded from placeholders to structured conversion-ready pages with unified design language.
- 2026-06-02: Performance quick win: heavy particles scripts now load conditionally (desktop + no reduced motion) and non-critical scripts use defer.
- 2026-06-02: Blog page refreshed (cleaner header copy + locale-aware internal navigation links).
- 2026-06-02: Blog detail/category/tag/search templates unified; malformed category template fixed; locale-aware routing applied across blog views.
- 2026-06-02: Header/navigation modernization completed (new brand bar, responsive mobile menu, accessible toggle behavior, improved nav spacing and hierarchy).
- 2026-06-02: Accessibility quick win: skip link + improved keyboard navigation path to main content.
- 2026-06-02: Frontend cleanup: removed duplicate flash close listeners from base inline scripts.
- 2026-06-02: Cabinet mobile UX pass: dashboard/client buttons aligned and stacked predictably; action groups made responsive; float-based button layout removed.
- 2026-06-02: Deep mobile polish for dashboard Messages/Invoices: responsive card-mode tables with data labels + stable action button alignment.
- 2026-06-02: Final mobile completion pass: Projects/Tasks/Submissions tables adapted to card-mode; cabinet tabs and modal footers optimized for touch-friendly full-width buttons.
- 2026-06-02: Ultra-small breakpoint hardening (420/390/360): overflow-safe buttons/badges/headings, status-badge overlap fix, toolbar resilience.
- 2026-06-02: Phase 2 started: introduced global design tokens and shared component primitives, wired into base layer and bridged with modern-refresh.
- 2026-06-02: Phase 2 continuation: extracted repeated glass surfaces/proof pills/accordion contrast patterns into shared component layer and reduced duplicate rules in modern-refresh.
- 2026-06-02: Phase 2 template adoption: about/faq/blog/pricing views now use shared component classes (surface, kicker, accordion contrast) for consistent visual contracts.
- 2026-06-02: Phase 2 services migration: services/questionnaire/aside blocks moved to shared component classes; services-specific CSS reduced to layout-only concerns.
- 2026-06-02: Phase 2 blog completion: blog post/search detail surfaces switched to explicit shared surface classes for consistent component-driven styling.
- 2026-06-02: Phase 2 legacy blog alignment: blog blueprint post view and sidebar sections aligned with shared surface component classes.
- 2026-06-02: Phase 2 legacy blog lists aligned: index/category/tag/search blueprint views moved to explicit shared surface classes; heavy surface fallback bridge removed from ui-components.
- 2026-06-02: Phase 2 bridge reduction: homepage hero kicker switched to explicit ui-kicker; redundant kicker and accordion fallback bridges removed from ui-components.
- 2026-06-02: Phase 2 proof migration: hero/about/services/pricing proof chips moved to explicit ui-proof-pill; proof-row fallback bridges removed.
- 2026-06-02: Phase 2 refresh cleanup: duplicate visual styles removed from modern-refresh kicker rules; ui-kicker now acts as the primary visual contract.
- 2026-06-02: Phase 2 cleanup polish: removed obsolete faq/questionnaire legacy classes from templates and finalized ui-components as a clean primitive layer.
- 2026-06-02: Phase 2 mobile cohesion: consolidated mobile surface radius override to shared ui-surface-soft selector.
- 2026-06-02: Phase 2 kicker completion: public templates migrated to explicit ui-kicker + spacing utilities; legacy kicker selectors removed from modern-refresh.
- 2026-06-02: Phase 2 final report published (`docs/PHASE2_FINAL_REPORT_2026-06.md`).
- 2026-06-02: Phase 3 started: CTA conversion tracking hooks added (click + form submit) with Pixel custom event `CTA_Click`.
- 2026-06-02: Phase 3 conversion: homepage strengthened with measurable outcomes block (impact metrics).
- 2026-06-02: Phase 3 performance: preconnect hints added for critical CDNs; Font Awesome stylesheet moved to head and legacy stripping logic removed.
- 2026-06-02: Phase 3 performance pass 2: visual effect scripts (animations/background/dark-background) switched to conditional loading based on hero/visual block presence and motion/viewport constraints.
- 2026-06-02: Phase 3 conversion pass 2: key CTA links/forms on home, pricing, services, and contact now include explicit data tracking attributes.
- 2026-06-02: Phase 3 conversion pass 3: homepage hero CTA A/B experiment (`home_cta_order_v1`) added with exposure/conversion tracking.
- 2026-06-02: Phase 3 performance pass 3: removed debug footer listeners/style mutations from global inline script to reduce unnecessary runtime work.
- 2026-06-02: Phase 3 performance pass 4: blog media switched to lazy/async image loading strategy (list/search/category/tag + related images).
- 2026-06-02: Phase 3 conversion pass 4: contact and services lead forms improved with semantic autocomplete attributes.
- 2026-06-02: Phase 3 performance pass 5: moved heavy visual CSS/background DOM and visual script activation in base layout to homepage-only scope.
- 2026-06-02: Phase 3 conversion pass 5: auth flow forms (login/register/forgot-password) enriched with autocomplete/inputmode attributes for faster mobile completion.
- 2026-06-02: Phase 3 conversion pass 6: payment checkout form enriched with semantic autofill/input hints and CTA-form tracking metadata.
- 2026-06-02: Phase 3 performance pass 6: synchronized lazy/async image strategy in `app/templates/blog/*` templates used by blog blueprint routes.
- 2026-06-02: Phase 3 conversion pass 7: dashboard profile form improved with semantic autofill/input hints and form-level CTA tracking metadata.
- 2026-06-02: Phase 3 conversion pass 8: dashboard messaging flows enriched with form-level CTA tracking and low-friction subject/message input hints.
- 2026-06-02: Phase 3 hardening pass 9: project-wide `target=\"_blank\"` links normalized with `rel=\"noopener noreferrer\"`; dashboard reply modal fields switched to unique IDs to prevent duplicate-id collisions.
- 2026-06-02: Phase 3 audit pass 10: full workspace diagnostics re-checked (`get_errors` clean), plus residual media optimization on CV/client/admin templates (lazy/async or async decoding).
- 2026-06-02: Phase 3 hardening pass 11: normalized remaining `target=\"_blank\" rel=\"noopener\"` links to `noopener noreferrer` and added async decoding for CV project card images.
- 2026-06-02: Phase 3 infra pass 12: PostgreSQL runtime stabilized for local work (Python 3.13 venv, psycopg fallback support, schema auto-create for `rozoom_ki_*` schemas).
- 2026-06-02: Phase 3 migration pass 12: stale Alembic pointer cleared and DB stamped to current multi-head state (`add_image_data_field`, `002`) for clean local evolution.
- 2026-06-02: Phase 3 baseline pass 12: local response baseline captured (home/services/pricing/contact/blog), then blog route optimized with eager loading + sidebar cache.
