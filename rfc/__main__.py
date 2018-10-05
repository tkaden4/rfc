import click
from . import index
from os import path

index_file = None


def update_full_index(index_file):
    index.update_index(index_file, index.get_available_rfcs())


@click.group()
@click.option("-f", "--file", default=path.expanduser("~/.rfc-index"), help="Index file to use")
def cli(file):
    global index_file
    index_file = file


@cli.command("read")
@click.argument("number", type=int)
def read(number):
    have_rfc = index.index_contains(index_file, number)
    if not have_rfc:
        print("RFC not available")
    else:
        import requests as rq
        print(rq.get(index.rfc_url(number)).text)


@cli.command("update-index")
def update_index():
    update_full_index(index_file)


cli(prog_name="rfc")
