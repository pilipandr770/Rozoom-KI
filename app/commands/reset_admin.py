import click
from flask.cli import with_appcontext
from app import db
from app.auth import AdminUser


@click.command('reset-admin')
@click.option('--username', default='admin', help='Admin username (default: admin)')
@click.option('--password', default='admin', help='New password (default: admin)')
@click.option('--email', default=None, help='Admin email')
@with_appcontext
def reset_admin_command(username, password, email):
    """Create or reset the admin user password."""
    admin = AdminUser.query.filter_by(username=username).first()

    if admin:
        admin.set_password(password)
        if email:
            admin.email = email
        db.session.commit()
        click.echo(f"Password for admin '{username}' has been reset.")
    else:
        admin = AdminUser(
            username=username,
            email=email or f'{username}@rozoom-ki.com',
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        click.echo(f"Admin user '{username}' created with the given password.")

    click.echo(f"Login at /admin/login  →  username: {username}  password: {password}")
