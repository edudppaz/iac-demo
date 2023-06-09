# Demo
Demo scripts used in Sopra Steria Network community presentation on 08/07/2023

Some extra info about each script:

## netmiko_example
Basic example to run a show command on a network device and output the text blob. The IP and user/password is hardcoded to a lab right now, so it needs to be changed for your environment

## netmiko_example2
Same script as the first example, but it now uses the genie parser to show the different on how genie makes it extremely easy to structure the text to a machine-readable formats. The commands that can be parsed with genie can be found at:

https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers

## napalm_example
An example script that uses jinja and yaml to generate a configuration file based on data input (yaml). It actually does not use napalm, but is the first step into generating the config to be used by napalm on the next example.
Template: napalm/templatev2.j2
Data: napalm/data.yaml

## napalm_example2
A script that builds further on the first example. This script, uses arguments and take the config generate by jinja+yaml and checks it against a live network device.

--diff : Connects into the network device, uploads the new config and does a compare() to get the diff. Obs: Right now the script is only using a compare_merge(), therefore it ONLY compares the lines included on the template. Lines not included on the template are not compared, thefore, for example, if you remove a customer from the template, is not removed from the configuration.
This arg used alone, does not make any change to the network device

--ops : When combined with diff, asks the operator to confirm if the configuration should be pushed to the device (after showing the diff). On Yes, it does a merge() on the config.

--force : Same as ops, but it just pushes after showing the diff. No questions asked. YOLO

## main_flask.py
Flask app to demostrate a web GUI to "order2 a new vlan/client. It imports functions on gittool.py to be able to create a new branch, do the changes, push to a PR.
The gittool.py functions have a hardcoded github repo and uses the "DEMO_TOKEN" to get the personal token to be used to authenticate to github. Both need to be changed for your environment.


## Workflows:
### PR.yml
Workflow to run the example2 script with a new PR is created (changed data, for example). It does a -diff and comments the output
Bug: It comes with some weird symbols, i have not had time to look at it.

### Merge.yml
If the PR is approved and merged, it runs the same example2 script but on --diff --force mode, so it pushes the config to the device.

