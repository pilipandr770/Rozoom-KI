import click
from flask.cli import with_appcontext
from app import db
from app.models.pricing import PricePackage


DEFAULT_PACKAGES = [
    {
        'name': 'Starter',
        'hours': 5,
        'price_per_hour': 50.0,
        'description': 'Perfect for small tasks and fixes.',
        'is_active': True,
    },
    {
        'name': 'Basic',
        'hours': 10,
        'price_per_hour': 45.0,
        'description': 'Ideal for small features and improvements.',
        'is_active': True,
    },
    {
        'name': 'Standard',
        'hours': 20,
        'price_per_hour': 40.0,
        'description': 'Best value for medium-sized projects.',
        'is_active': True,
    },
    {
        'name': 'Professional',
        'hours': 40,
        'price_per_hour': 35.0,
        'description': 'For larger features and ongoing development.',
        'is_active': True,
    },
    {
        'name': 'Enterprise',
        'hours': 80,
        'price_per_hour': 30.0,
        'description': 'Maximum value for long-term projects.',
        'is_active': True,
    },
]


@click.command('seed-pricing')
@with_appcontext
def seed_pricing_command():
    """Seed the database with default pricing packages."""
    seed_pricing()
    click.echo('Pricing packages seeded successfully.')


def seed_pricing():
    """Insert default pricing packages if the table is empty."""
    existing = PricePackage.query.count()
    if existing > 0:
        click.echo(f'Skipping seed: {existing} package(s) already exist.')
        return

    for data in DEFAULT_PACKAGES:
        pkg = PricePackage(**data)
        db.session.add(pkg)

    db.session.commit()
    click.echo(f'Inserted {len(DEFAULT_PACKAGES)} default pricing packages.')
