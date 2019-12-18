#!/usr/bin/env python3

import os

import yaml
from aws_cdk import core

from nginx_ec2.nginx_ec2_stack import NginxEc2Stack

app = core.App()

with open(f"config/{os.environ.get('ENVIRONMENT')}/nginx-ec2.yaml") as f:
    config = yaml.safe_load(f)

if os.environ.get("ENVIRONMENT") == "dev":
    stack_suffix = os.environ.get("CI_COMMIT_SHA", default="dev")
elif os.environ.get("ENVIRONMENT") == "prod":
    stack_suffix = os.environ.get("CI_COMMIT_TAG", default="dev")
else:
    stack_suffix = "dev"

NginxEc2Stack(app, f"{os.environ.get('NGINX_STACK_PREFIX')}-{stack_suffix}", config)

app.synth()
