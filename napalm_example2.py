import argparse
import yaml
from jinja2 import Environment, FileSystemLoader
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure, napalm_validate
from nornir_utils.plugins.functions import print_result
import napalm
import json 

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Network configuration management script')
parser.add_argument('--diff', action='store_true', help='Show configuration diff without applying the merge')
parser.add_argument('--show', action='store_true', help='Show configuration diff without applying the merge')
parser.add_argument('--op', action='store_true', help='Combine with --diff to prompt for operator confirmation before applying the merge')
parser.add_argument('--force', action='store_true', help='Combine with --diff to apply the merge without operator confirmation')
args = parser.parse_args()

# Load YAML data from file
with open('napalm/data.yaml') as file:
    data = yaml.safe_load(file)

# Load YAML dict from file
with open('napalm/hosts.yaml') as file:
    inv = yaml.safe_load(file)

# Jinja filter
def first_ip(ip):
    parts = ip.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    return '.'.join(parts)
def second_ip(ip):
    parts = ip.split('.')
    parts[-1] = str(int(parts[-1]) + 2)
    return '.'.join(parts)

# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True )
env.filters['first_ip'] = first_ip
env.filters['second_ip'] = second_ip

template = env.get_template('napalm/templatev2.j2')


# Define the task for merging the configuration
def main():
    # Render template with data
    config = template.render(data)
    if args.show:
        print(config)
        exit()
    if args.diff:
        # Create a NAPALM connection
        for k, v in inv.items():
            driver = napalm.get_network_driver(v['platform'])
            connection = driver(hostname=v['hostname'], username=v['username'], password=v['password'])
            connection.open()

            # Load merge candidate
            connection.load_merge_candidate(config=config)
            # Calculate the config diff
            diff = connection.compare_config()
            print(f"Configuration diff for {k}:")
            print(diff)
            if diff == '':
                print('==== No diff =====\n')

            if args.force:
                # Apply the merged configuration without operator confirmation
                if diff == '':
                    print(f"Nothing to apply to R1, exiting... ")
                    connection.discard_config()
                else:
                    connection.commit_config()
                    print(f"Configuration diff applied to {k}")
                    
            elif args.op:
                # Prompt for operator approval
                if diff != '':
                    approval = input(f"Apply configuration diff to {k}? (yes/no): ")
                    if approval.lower() == 'yes':
                        # Apply the merged configuration
                        connection.commit_config()
                        print(f"Configuration applied to {k}")
                else:
                    print(f"Nothing to apply to R1, exiting... ")
                    connection.discard_config()
            # Close the NAPALM connection
            else:
                connection.discard_config()
                print(f"Configuration not applied to {k}, diff-only mode")
            connection.close()

if __name__ == '__main__':
    main()