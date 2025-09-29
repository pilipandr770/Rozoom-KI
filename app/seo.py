from flask import request, url_for


def init_app(app):
    @app.context_processor
    def inject_seo_defaults():
        """Provide site-wide SEO defaults and helpers to templates.

        Exposes:
        - site_name: site title
        - default_description: fallback description
        - default_image: absolute URL to default social image (if any)
        - canonical_url: request.url by default
        """
        site_name = app.config.get('SITE_NAME', 'Rozoom-KI')
        default_description = app.config.get('SITE_DESCRIPTION', '')

        # Resolve SITE_IMAGE if provided; otherwise fall back to static default
        site_image_cfg = app.config.get('SITE_IMAGE', '')
        if site_image_cfg:
            if site_image_cfg.startswith('http'):
                default_image = site_image_cfg
            else:
                # Allow values like '/static/img/og-default.svg' or 'img/og-default.svg' or 'static/img/..'
                fname = site_image_cfg.lstrip('/')
                if fname.startswith('static/'):
                    fname = fname[len('static/'):]
                default_image = url_for('static', filename=fname, _external=True)
        else:
            default_image = url_for('static', filename='img/og-default.png', _external=True)

        canonical_url = request.url if request else ''

        return dict(
            site_name=site_name,
            default_description=default_description,
            default_image=default_image,
            canonical_url=canonical_url,
        )
