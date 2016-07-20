#!env python
# -*- coding: utf-8 -*-
import json

import time


class Milestone:
    """
     <milestone>
        <id>676</id>
        <group_artifact_id>143</group_artifact_id>
        <element_id>71587</element_id>
        <features>미뤄둘 일들</features>
        <duedate>1609426799</duedate>
        <status>PROGRESS</status>
    </milestone>
    """

    def __init__(self, milestone):
        self.id = milestone.id.get_text()
        self.group_artifact_id = milestone.group_artifact_id.get_text()
        self.features = milestone.element_id.get_text()
        self.due_date = milestone.duedate.get_text()
        self.status = milestone.status.get_text()

    def __str__(self):
        status = 'open' if self.status is 'PROGRESS' else 'closed'

        return json.dumps(
            dict(
                title=self.features,
                state=status,
                description=self.features,
                due_on=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(int(self.due_date)))
            )
        )
