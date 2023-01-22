#!/usr/bin/env python3

from argparse import ArgumentParser
from sys import exit

from peewee_migrate import Router

from db import db

router = Router(db)

parser = ArgumentParser(description='Peewee migration wrapper')

parser.add_argument('action', metavar='action', type=str,
                    help='migrate / create')

parser.add_argument('name', default=None, metavar='migration name', type=str)

args = parser.parse_args()

if args.action == 'create':
    if args.name:
        try:
            router.create(args.name)
        except Exception:
            print('Can`t create migration "{0}". Exiting'.format(args.name))
            exit(1)
    else:
        ArgumentParser.error()

elif args.action == 'migrate':
    if args.name == 'all':
        try:
            router.run()
        except Exception as e:
            print('Can`t apply migrations. Exiting')
            print(e)
            exit(1)
    else:
        try:
            router.run(args.name)
        except Exception as e:
            print('Can`t apply migration "{0}". Exiting'.format(args.name))
            print(e)
            exit(1)
else:
    ArgumentParser.error()
