import argparse
import yaml
from jinja2 import Environment, FileSystemLoader

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Network configuration management script')
parser.add_argument('--diff', action='store_true', help='Show configuration diff without applying the merge')
parser.add_argument('--op', action='store_true', help='Combine with --diff to prompt for operator confirmation before applying the merge')
parser.add_argument('--force', action='store_true', help='Combine with --diff to apply the merge without operator confirmation')
args = parser.parse_args()

# Load YAML data from file
with open('napalm/data.yaml') as file:
    data = yaml.safe_load(file)

# Jinja filter
def first_ip(ip):
    parts = ip.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    return '.'.join(parts)
def second_ip(ip):
    parts = ip.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    return '.'.join(parts)

# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
env.filters['first_ip'] = first_ip
env.filters['second_ip'] = second_ip

template = env.get_template('napalm/template.j2')

# Render template with data
config = template.render(data)

print(config)