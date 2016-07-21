#!env python
# -*- coding: utf-8 -*-
import threading


def issue_migration(**kwargs):
    project = kwargs.get('project')

    print(threading.current_thread().name)

