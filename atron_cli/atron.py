import click
import time
import platform
import os
from minifier import minify
from .board import Board, BoardException, DirectoryExistsError
from .board import PyboardError

_board = None


@click.group()
@click.option(
    "--port",
    "-p",
    envvar="ATRON_PORT",
    default="",
    type=click.STRING,
    help="Name of serial port for connected board.  Can optionally specify with ATRON_PORT environment variable.",
    metavar="PORT",
)
@click.option(
    "--baud",
    "-b",
    envvar="ATRON_BAUD",
    default=115200,
    type=click.INT,
    help="Baud rate for the serial connection (default 115200).  Can optionally specify with ATRON_BAUD environment variable.",
    metavar="BAUD",
)
@click.version_option()
def cli(port, baud):
    global _board
    if platform.system() == "Windows":
        if port == '':
            click.secho('you have to choose a COM port.', bold=True, fg='red')
            return

        if not re.match("^COM(\d+)$", port):
            click.secho('invalid port {}'.format(port), fg='red')
            return
    else:
        if port == '':
            port = '/dev/ttyUSB0'

    seconds = 1
    while True:
        try:
            _board = Board(port, baud)
            break
        except BoardException as error:
            click.secho(str(error), bold=True, fg='yellow')
            click.secho(
                'reonnecting to board after {} seconds. press ctrl+c to cancel'.format(seconds), fg='green')
            time.sleep(seconds)
            seconds *= 2


@cli.command()
@click.option(
    "-h",
    "--hard",
    "hard",
    is_flag=True,
    default=False,
    help="Perform a hard reboot, including running init.py",
)
def reset(hard):
    if not hard:
        _board.soft_reset()
        return
    # TODO: Hard reset is not implemented.


@cli.command()
def raw_command():
    click.secho(
        'the raw-command is under construction and may have some bugs.', fg='yellow')
    click.secho('entering raw-command mode ...', fg='green')
    _board.soft_reset()
    time.sleep(1)

    _board.board.enter_raw_repl()
    try:
        while True:
            command = raw_input(">>> ")
            result = _board.board.exec_raw(command)
            if result[0]:
                print(result[0])
    finally:
        _board.board.exit_raw_repl()
        _board.soft_reset()


@cli.command()
@click.argument("remote_folder")
def rmdir(remote_folder):
    _board.files.rmdir(remote_folder)


@cli.command()
@click.argument(
    "local",
    default="main.py",
)
@click.argument(
    "remote",
    default="main.py",
)
def upload(local, remote):
    if remote is None:
        remote = os.path.basename(os.path.abspath(local))
    _board.files.put(remote, minify(local))


@cli.command()
@click.argument(
    "local",
    default="main.py",
)
@click.argument(
    "remote",
    required=False,
)
def put(local, remote):
    if remote is None:
        remote = os.path.basename(os.path.abspath(local))
    if os.path.isdir(local):
        board_files = _board.files
        for parent, child_dirs, child_files in os.walk(local):
            remote_parent = posixpath.normpath(
                posixpath.join(remote, os.path.relpath(parent, local))
            )
            try:
                board_files.mkdir(remote_parent)
                for filename in child_files:
                    with open(os.path.join(parent, filename), "rb") as infile:
                        remote_filename = posixpath.join(
                            remote_parent, filename)
                        board_files.put(remote_filename, infile.read())
            except DirectoryExistsError:
                pass
    else:
        with open(local, "rb") as infile:
            _board.files.put(remote, infile.read())


@cli.command()
@click.argument("remote_file")
def rm(remote_file):
    _board.files.rm(remote_file)


@cli.command()
@click.argument("local_file")
@click.option(
    "--no-output",
    "-n",
    is_flag=True,
    help="Run the code without waiting for it to finish and print output.  Use this when running code with main loops that never return.",
)
def run(local_file, no_output):
    try:
        output = _board.files.run(local_file, not no_output)
        if output is not None:
            click.secho(output.decode("utf-8"))
    except IOError:
        click.echo(
            "Failed to find or read input file: {0}".format(local_file), err=True
        )


@cli.command()
@click.argument("directory", default="/")
@click.option(
    "--long_format",
    "-l",
    is_flag=True,
    help="Print long format info including size of files.  Note the size of directories is not supported and will show 0 values.",
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="recursively list all files and (empty) directories.",
)
def ls(directory, long_format, recursive):    
    try:
        files = _board.files.ls(directory, long_format=long_format, recursive=recursive)
    except PyboardError as err:
        click.secho('PyBoard Exception.', fg='red')
        click.secho(str(err), fg='yellow')
        return
    
    for f in files:
        if not long_format:
            click.secho(
                f,
                fg='green' if os.path.splitext(f)[1].lower() == '.py' else 'white',
            )
        else:
            click.echo(f)


if __name__ == '__main__':
    try:
        cli()
    finally:
        if _board is not None:
            try:
                _board.close()
            except:
                pass
