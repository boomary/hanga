# internal packages
import sys

# 3rd-party packages
import click
import botocore

# custom packages
from . import _session
from . import hanga_constants as const
from . import list_stacks
from . import describe_stack
from . import create_stack
from . import delete_stack
from . import protect_stack
from . import upload_object
from . import hanga_util as util


def _print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('hanga 0.01')
    ctx.exit()

def _init_profile(ctx, param, value):
    click.echo(value)
    ctx.exit()


@click.group()
@click.option(
    '--version',
    is_flag=True,
    callback=_print_version,
    expose_value=False,
    is_eager=True,
    help='Show hanga version'
)

@click.option(
    '--profile', '-p',
    required=True,
    default=const.DEFAULT_PROFILE,
    help='AWS CLI profile'
)

@click.option(
    '--region', '-r',
    help='Working region'
)

def cli(profile, region):
    try:
        _session._init_session(profile, region)  
    except:
        click.secho(const.ERM_PROFILE_NOTFOUND, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_PROFILE_NOTFOUND)

@click.command()
def describe():
    """
    Describe stack, resources, or events
    """
    pass

cli.add_command(describe_stack.describe_stack)
cli.add_command(list_stacks.list_stacks)
cli.add_command(create_stack.create_stack)
cli.add_command(delete_stack.delete_stack)
cli.add_command(protect_stack.protect_stack)
cli.add_command(upload_object.upload_object)






