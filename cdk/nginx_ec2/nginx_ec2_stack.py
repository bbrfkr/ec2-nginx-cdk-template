import base64
import os

from aws_cdk import core
from aws_cdk.aws_ec2 import CfnInstance
from aws_cdk.aws_elasticloadbalancingv2 import CfnTargetGroup
from aws_cdk.core import CfnCreationPolicy, CfnOutput, CfnResourceSignal
from jinja2 import Template


class NginxEc2Stack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        with open(f"config/{os.environ.get('ENVIRONMENT')}/user_data.txt.j2", "r") as f:
            template = Template(f.read())
            user_data = base64.encodestring(
                template.render(env=os.environ, config=config, stack=id).encode("utf8")
            ).decode("ascii")

        nginx_ec2 = CfnInstance(
            self,
            "NginxEc2",
            block_device_mappings=config.get("block_device_mappings"),
            iam_instance_profile=config.get("iam_instance_profile"),
            image_id=config.get("image_id"),
            instance_type=config.get("instance_type"),
            key_name=config.get("key_name"),
            network_interfaces=config.get("network_interfaces"),
            user_data=user_data,
            tags=config.get("tags"),
        )

        nginx_ec2.cfn_options.creation_policy = CfnCreationPolicy(
            resource_signal=CfnResourceSignal(count=1, timeout="PT5M")
        )

        nginx_targetgroup = CfnTargetGroup(
            self,
            "NginxTargetGroup",
            vpc_id=config.get("tg_vpc_id"),
            protocol=config.get("tg_protocol"),
            port=config.get("tg_port"),
            health_check_enabled=True,
            health_check_protocol=config.get("tg_healthcheck_protocol"),
            health_check_port=config.get("tg_health_check_port"),
            health_check_path=config.get("tg_healthcheck_path"),
            health_check_timeout_seconds=config.get("tg_health_check_timeout_seconds"),
            health_check_interval_seconds=config.get(
                "tg_health_check_interval_seconds"
            ),
            healthy_threshold_count=config.get("tg_healthy_threshold_count"),
            unhealthy_threshold_count=config.get("tg_unhealthy_threshold_count"),
            matcher=config.get("tg_matcher"),
            tags=config.get("tg_tags"),
            target_group_attributes=config.get("tg_target_group_attributes"),
            targets=[
                CfnTargetGroup.TargetDescriptionProperty(
                    id=nginx_ec2.ref, port=config.get("tg_target_port")
                )
            ],
        )

        CfnOutput(self, "NginxInstanceId", value=nginx_ec2.ref)
        CfnOutput(self, "NginxTargetGroupArn", value=nginx_targetgroup.ref)
