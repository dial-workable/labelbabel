#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import labelbabel.lib.k8s as k8s


# @click.command()
# @click.option('--mode',
#               type=click.Choice(['server', 'k8s-contorler'], case_sensitive=False))
# def main(count, name):
#     """This is the main entry point to the application. It serves as the entry point to both application modes (i.e. k8s-contoller and
#     web-applicaiton."""
#     for x in range(count):
#         click.echo('Hello %s!' % name)

memory = {}


def handle(event, cluster_name: str, memory: dict):
    # {sum:{
    #     name: ...
    #     start_time: ...
    #     labels: ...
    # },
    # }
    # Handle ADD events
    # Handle MODIFY events
    # Handle DELETE events
    pass


def main():
    s = k8s.Scraper('test-cluster')
    for e in s.get_events():
        print(repr(e) + "\n")


if __name__ == '__main__':
    main()
