import os
import git
import random
import yaml
from github import Github

def make_pr(yaml_data):
    # Local repository path
    repo_path = '/Users/edpozo/Git/iac-demo'

    # File path relative to the repository root
    file_path = 'README.md'

    # New line to add
    
    # Create a new branch
    repo = git.Repo(repo_path)

    # Checkout the main branch and pull the latest changes
    print("Checking out main branch")
    repo.git.checkout('main')
    print("Getting latest main")
    repo.git.pull()

    # Create a new branch
    random_number = random.randint(100, 999)
    new_branch = f'flask-branch-{random_number}'
    print("Branching")
    repo.git.checkout('HEAD', b=new_branch)

    # Modify the file
    print("Modifying DATA file")
    with open('napalm/data.yaml', 'r') as file:
        existing_data = yaml.safe_load(file)

    merged_data = existing_data.copy()
    for key, value in yaml_data.items():
        if key in merged_data:
            merged_data[key].append(value)
        else:
            merged_data[key] = value

    with open('napalm/data.yaml', 'w') as file:
        yaml.dump(merged_data, file)

    # Commit the changes
    print("Committing")
    repo.git.add(all=True)
    repo.git.commit('-m', 'Added a new line to README.md')

    # Push the new branch
    print("Pushing branch")
    repo.git.push('--set-upstream', 'origin', new_branch)

    # GitHub credentials
    github_token = os.getenv("DEMO_TOKEN")
    repository_name = 'edudppaz/iac-demo'
    base_branch = 'main'

    # Create a pull request
    print("New PR")
    g = Github(github_token)
    repo = g.get_repo(repository_name)
    head_branch = f'{repo.owner.login}:{new_branch}'
    repo.create_pull(title='New Automated Pull Request', body='Please review data changes', base=base_branch, head=head_branch)
    print("Done")

    # # Clean up - checkout main branch and delete the local branch
    print("Cleaning up")
    repo.git.checkout('main')
    repo.git.branch('-D', new_branch)
