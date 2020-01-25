# internal packages
import sys

# 3rd-party packages
import click

# custom packages
from . import _session
from . import hanga_constants as const
from . import create
from . import dryrun
from . import delete
from . import list_stacks


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
    '--profile',
    required=True,
    default=const.DEF_PROFILE,
    help='AWS CLI profile'
)

def cli(profile):
    try:
        _session._init_session(profile)
    except:
        click.secho(const.ERM_PROFILE_NOTFOUND, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_PROFILE_NOTFOUND)

@click.command()
def describe():
    """
    Describe stack, resources, or events
    """
    pass

cli.add_command(describe)
cli.add_command(create.create)
cli.add_command(dryrun.dryrun)
cli.add_command(delete.delete)
cli.add_command(list_stacks.list_stacks)





