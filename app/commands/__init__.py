from flask import Blueprint

def register_commands(app):
    """Register Flask CLI commands."""
    # Temporarily disabled due to syntax error
    # from app.commands.seed_blog import seed_blog_command
    # app.cli.add_command(seed_blog_command)
    
    # Register category update command
    from app.commands.update_category import update_category_command
    app.cli.add_command(update_category_command)
    
    # Register schema update command
    from app.commands.update_schema import update_schema_command
    app.cli.add_command(update_schema_command)

    # Register pricing seed command
    from app.commands.seed_pricing import seed_pricing_command
    app.cli.add_command(seed_pricing_command)

    # Register admin reset command
    from app.commands.reset_admin import reset_admin_command
    app.cli.add_command(reset_admin_command)
