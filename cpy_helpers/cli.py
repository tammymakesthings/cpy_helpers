# SPDX-FileCopyrightText: 2022 Tammy Cravit
#
# SPDX-License-Identifier: MIT

"""
Click CLI interface for the `cpy_helpers` tool.

* Author: Tammy Cravit <tammy@tammymakesthings.com>
"""

import os
import os.path
import click
from probe_blinka import ProbeBlinka


class CLIHelpers:
    """
    CLI Helper Methods.
    """

    def __init__(self):
        pass

    # pylint: disable=no-self-use
    def environment_variable_def(self,
                                 var_name: str = 'VAR',
                                 var_value: str = '1',
                                 the_shell: str =
                                 os.path.basename(os.getenv('SHELL'))) -> str:
        """
        Helper to return a shell environment variable definition for a given
        environment variable and shell.
        """

        if the_shell in ('sh', 'ksh'):
            return f'{var_name}={var_value}; export {var_name}'
        if the_shell in ('csh', 'tcsh'):
            return f'setenv {var_name}={var_value}'
        if the_shell == 'bash':
            return f'export {var_name}={var_value}'
        if the_shell == 'fish':
            return f'set -gx {var_name} {var_value}'
        return None

    @staticmethod
    def blinka_environment_variable(the_board: str, the_shell: str) -> str:
        """
        Returns the appropriate shell command to set the BLINKA environment
        variable for the specified board.
        """

        if not the_board.lower() in ['mcp2221', 'ft232h', 'u2if']:
            raise ValueError(f"Unknown board '{the_board.lower()}'")
        if not the_shell.lower() in ['sh', 'csh', 'bash', 'fish']:
            raise ValueError(f"Unknown shell '{the_shell.lower()}'")

        var_name: str = f'BLINKA_{the_board.upper()}'
        return CLIHelpers().environment_variable_def(var_name=var_name,
                                                     var_value='1',
                                                     the_shell=the_shell)


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    """
    Provide the CLI for the cpy_helpers tool.
    """

    ctx.ensure_object(dict)
    click.echo(f"Debug mode is{'on' if debug else 'off'}")
    ctx.obj['_debug'] = debug


@cli.command()
@click.pass_context
@click.option(
    '--prefer', '-p',
    default='u2if',
    help='the preferred board to use if multiple are found',
    type=click.Choice(['mcp2221', 'u2if', 'ft232h'], case_sensitive=False)
)
@click.option(
    '--shell', '-s',
    default=os.path.basename(os.getenv('SHELL')),
    help='the shell to use for the environment variable output',
    type=click.Choice(
        ['sh', 'ksh', 'bash', 'csh', 'tcsh', 'fish'],
        case_sensitive=False
    )
)
def probe(ctx, prefer: str, shell: str) -> None:
    """
    Probe for a CircuitPython board and print out an environment variable
    definition for the preferred shell.
    """
    the_board: str = ProbeBlinka(preferred_board=prefer).available_board()

    if the_board:
        click.echo(CLIHelpers.blinka_environment_variable(the_board, shell))
    elif ctx['_debug']:
        click.echo('warning: No blinka-compatible boards found.')


if __name__ == '__main__':
    cli(obj = {})     # noqa
