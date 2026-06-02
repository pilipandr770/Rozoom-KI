# Phase 3 Execution Log (2026-06)

## Goal
Increase conversion and improve frontend performance while preserving existing business flows.

## Completed So Far
- Added CTA instrumentation in frontend (`data-cta-track`, `data-cta-form`) with Pixel custom event `CTA_Click`.
- Added hero CTA A/B experiment (`home_cta_order_v1`) with:
  - deterministic client-side variant assignment (A/B) via localStorage,
  - exposure tracking (`Experiment_Exposure`),
  - experiment conversion tracking (`Experiment_Conversion`).
- Tracked key conversion points:
  - Home hero and account CTA block.
  - Pricing purchase/contact CTAs.
  - Services questionnaire submit and aside contact CTA.
  - Contact form submit CTA.
- Added homepage impact metrics block with measurable proof statements.
- Added network preconnect hints for critical third-party domains.
- Moved Font Awesome CSS into head to stabilize icon rendering.
- Removed legacy Font Awesome stripping logic.
- Added conditional loading for visual effect scripts on pages with hero/visual sections.
- Removed debug-only footer click listeners and style mutations from global inline script.
- Switched blog media strategy to `loading=\"lazy\"` + `decoding=\"async\"` for list/search/category/tag and related images.
- Added semantic `autocomplete` attributes for lead-capture inputs in contact and services questionnaire forms.
- Added `rel=\"noopener noreferrer\"` for external share links in blog post page.
- Scoped heavy visual CSS bundles, particles/dark-background DOM, and visual effect script activation to homepage-only in base layout.
- Added semantic autofill/input hints in auth flow: login/register/forgot-password (`autocomplete`, `inputmode`, password context).
- Added autofill/input hints and form-level CTA tracking attributes on payment checkout form.
- Mirrored blog image lazy/async optimizations into `app/templates/blog/*` (blueprint-backed templates) to avoid split behavior between duplicate template sets.
- Added semantic autofill/input hints and `data-cta-form` tracking metadata on dashboard profile settings form.
- Added `data-cta-form` conversion metadata to dashboard message send/reply forms and added low-friction subject/content input hints.
- Added CTA click tracking metadata on project detail "Send Message" action.
- Applied global hardening for links opened in new tabs by adding `rel=\"noopener noreferrer\"` where missing across templates.
- Fixed duplicate element IDs in dashboard message reply modals by namespacing IDs with message id.
- Re-ran full diagnostics (no compile/lint template errors) and optimized remaining non-critical images in CV/client/admin templates with `loading=\"lazy\"` and/or `decoding=\"async\"`.
- Completed consistency hardening by normalizing `target=\"_blank\" rel=\"noopener\"` to `rel=\"noopener noreferrer\"` across templates and added `decoding=\"async\"` to CV project cards.
- Stabilized local PostgreSQL runtime on Windows by switching project venv to Python 3.13 and enabling SQLAlchemy URL fallback to `postgresql+psycopg://` when needed.
- Added startup schema bootstrap for configured project schemas (`POSTGRES_SCHEMA`, `POSTGRES_SCHEMA_CLIENTS`, `POSTGRES_SCHEMA_PROJECTS`, `POSTGRES_SCHEMA_SHOP`).
- Resolved local migration-history blocker by resetting stale `alembic_version` markers and stamping current heads (`add_image_data_field`, `002`) for this environment.
- Captured local HTTP baseline (5 requests/page average):
  - `/`: ~39.6 ms
  - `/services`: ~34.0 ms
  - `/pricing`: ~58.4 ms
  - `/contact`: ~14.8 ms
  - `/blog`: ~103.7 ms
- Optimized blog backend rendering path with eager loading (`joinedload`/`selectinload`) plus lightweight sidebar cache; post-pass `/blog` benchmark over 10 requests: avg ~101.6 ms, median ~101.0 ms.

## Expected Impact
- Better conversion visibility by CTA location and intent.
- Lower non-critical JS on non-hero pages.
- More stable first render for icon-dependent elements.
- Lower image decode/network pressure on blog discovery pages.
- Faster and less error-prone form filling on conversion-critical contact flows.
- Reduced non-critical CSS/DOM/script cost on inner pages (services/pricing/contact/dashboard/blog listings).
- Reduced authentication-form friction on mobile and desktop via better browser autofill behavior.
- Improved checkout form completion quality and analytics visibility for payment intent.
- Kept performance behavior consistent across both blog routing paths.
- Improved profile update and password-change form completion quality on mobile/desktop.
- Improved instrumentation coverage for in-cabinet communication actions.
- Reduced reverse-tabnabbing risk and improved DOM/accessibility correctness in modal reply flows.
- Reduced residual image decode/network overhead in secondary UI paths while preserving first-screen behavior.
- Removed remaining security-rel inconsistency for external links opened in a new tab.
- Unblocked next performance stage by ensuring production-like PostgreSQL schemas are migratable and runnable locally.

## Next Phase 3 Steps
- Establish baseline metrics for key pages (home, pricing, services, contact):
  - Lighthouse mobile (Performance, LCP, CLS, INP proxy).
  - Payload by JS/CSS transfer size.
- Apply optimization pass 3:
  - Reduce unnecessary above-the-fold animation work.
  - Prioritize critical media assets.
  - Tighten script loading gates if baseline indicates hotspots.
- Start conversion experiment v1:
  - Hero CTA ordering hypothesis and contact friction reduction hypothesis.
