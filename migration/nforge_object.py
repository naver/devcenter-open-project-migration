# -*- coding: utf-8 -*-
import json

import time


class NforgeObject:
    tags = ()

    def __init__(self, soup):
        self.result = None
        self.soup = soup
        assert self.tags

        for tag in self.tags:
            self.__dict__[tag] = self.soup.find(tag)

    def __str__(self):
        return self.result

    def make_result(self):
        pass


class Milestone(NforgeObject):
    tags = ('id', 'group_artifact_id', 'features', 'due_date', 'status')

    def __init__(self, soup):
        super(Milestone, self).__init__(soup)
        self.status_str = 'open' if self.status is 'PROGRESS' else 'closed'
        self.result = self.make_result()

    def make_result(self):
        return json.dumps(
            dict(
                title=self.features,
                state=self.status_str,
                description=self.features,
                due_on=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(int(self.due_date)))
            )
        )
