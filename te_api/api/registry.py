# Auto-generated registry file. Do not edit manually.
from . import audit
from . import autoprovisioning
from . import companies
from . import billing
from . import bot_mitigation
from . import core
from . import inventory
from . import logs
from . import media
from . import notifications
from . import authentication
from . import security
from . import statistics
from . import storage
from . import users

def register_api_commands(cli):
    cli.add_command(audit.cli, name='audit')
    cli.add_command(autoprovisioning.cli, name='autoprovisioning')
    cli.add_command(companies.cli, name='companies')
    cli.add_command(billing.cli, name='billing')
    cli.add_command(bot_mitigation.cli, name='bot-mitigation')
    cli.add_command(core.cli, name='core')
    cli.add_command(inventory.cli, name='inventory')
    cli.add_command(logs.cli, name='logs')
    cli.add_command(media.cli, name='media')
    cli.add_command(notifications.cli, name='notifications')
    cli.add_command(authentication.cli, name='authentication')
    cli.add_command(security.cli, name='security')
    cli.add_command(statistics.cli, name='statistics')
    cli.add_command(storage.cli, name='storage')
    cli.add_command(users.cli, name='users')
