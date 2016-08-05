# -*- coding: utf-8 -*-
import json

import time


class Milestone:
    def __init__(self, milestone):
        self.id = milestone.id.get_text()
        self.group_artifact_id = milestone.group_artifact_id.get_text()
        self.features = milestone.features.get_text()
        self.due_date = milestone.duedate.get_text()
        self.status = milestone.status.get_text()

        status = 'open' if self.status is 'PROGRESS' else 'closed'

        self.json = json.dumps(
            dict(
                title=self.features,
                state=status,
                description=self.features,
                due_on=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(int(self.due_date)))
            )
        )

    def __str__(self):
        return self.json
