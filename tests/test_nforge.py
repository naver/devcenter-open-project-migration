from github_migration import GitHubSession
from migration.nforge_parser import NforgeParser

gh = GitHubSession('fd7afb7372aef5c3a05f9f5a32aa5f115588364c', False, 'test')
parser = NforgeParser(gh, '../Nforge/open_project/d2coding')

print(parser.make_issue_json())
