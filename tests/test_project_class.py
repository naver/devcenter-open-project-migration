from migration.project import Project, InvalidProjectError
from migration.helper import get_random_string
import random
import unittest


class TestProject(unittest.TestCase):
    valid_projects = dict(
        d2coding=['okgosu','openapi'],
        nforge=['junoyoonkr','kss','nori','tiny657','리쯔','Piseth',
                  'chanraksmey','cheng900','darayong','manithnoun','rathapovkh',
                  'wkpark','졸린눈이'],
        asd=['xowns24']
    )

    naver_api_url = 'http://staging.dev.naver.com'

    project_name = random.choice(list(valid_projects.keys()))
    project = Project(project_name,naver_api_url)

    def test_constructor(self):
        try:
            project = Project(self.project_name,self.naver_api_url)
        except InvalidProjectError as e:
            self.fail(e)

        self.assertTrue(isinstance(project,Project))
        self.assertEqual(project._project_name,self.project_name)

    def test_invalid_project(self):
        with self.assertRaises(InvalidProjectError):
            project = Project(get_random_string(10),self.naver_api_url)

    def test_get_developers(self):
        self.assertEqual(sorted(self.project._developers),
                         sorted(self.valid_projects.get(
                             self.project._project_name)))

    def test_get_issues(self):
        pass

if __name__ == '__main__':
    unittest.main()
