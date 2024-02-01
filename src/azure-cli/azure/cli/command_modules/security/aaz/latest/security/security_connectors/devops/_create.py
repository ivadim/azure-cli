# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "security security-connectors devops create",
    is_experimental=True,
)
class Create(AAZCommand):
    """Create a DevOps Configuration.

    :example: Configure access to DevOps SCM provider to onboard all existing and future organizations
        az security security-connectors devops create --name myConnector --resource-group myResourceGroup --auto-discovery Enabled --authorization-code MyAccessToken

    :example: Configure access to DevOps SCM provider to onboard all existing organizations
        az security security-connectors devops create --name myConnector --resource-group myResourceGroup --auto-discovery Disable --authorization-code $MY_ENVIRONMENT_VARIABLE_WITH_OAUTHTOKEN

    :example: Configure access to DevOps SCM provider to onboard specific organizations
        az security security-connectors devops create --name myConnector --resource-group myResourceGroup --auto-discovery Disable --top-level-inventory-list org1,org2 --authorization-code myOAuthToken
    """

    _aaz_info = {
        "version": "2023-09-01-preview",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.security/securityconnectors/{}/devops/default", "2023-09-01-preview"],
        ]
    }

    AZ_SUPPORT_NO_WAIT = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_lro_poller(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        _args_schema.security_connector_name = AAZStrArg(
            options=["-n", "--name", "--security-connector-name"],
            help="The security connector name.",
            required=True,
        )

        # define Arg Group "Authorization"

        _args_schema = cls._args_schema
        _args_schema.authorization_code = AAZStrArg(
            options=["--authorization-code"],
            arg_group="Authorization",
            help="Sets one-time OAuth code to exchange for refresh and access tokens.",
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.auto_discovery = AAZStrArg(
            options=["--auto-discovery"],
            arg_group="Properties",
            help="AutoDiscovery states.",
            enum={"Disabled": "Disabled", "Enabled": "Enabled", "NotApplicable": "NotApplicable"},
        )
        _args_schema.inventory_list = AAZListArg(
            options=["--inventory-list"],
            arg_group="Properties",
            help="List of top-level inventory to select when AutoDiscovery is disabled. This field is ignored when AutoDiscovery is enabled.",
        )

        inventory_list = cls._args_schema.inventory_list
        inventory_list.Element = AAZStrArg()
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        yield self.DevOpsConfigurationsCreateOrUpdate(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class DevOpsConfigurationsCreateOrUpdate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200, 201]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Security/securityConnectors/{securityConnectorName}/devops/default",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "securityConnectorName", self.ctx.args.security_connector_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2023-09-01-preview",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Content-Type", "application/json",
                ),
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content_builder(
                self.ctx.args,
                typ=AAZObjectType,
                typ_kwargs={"flags": {"required": True, "client_flatten": True}}
            )
            _builder.set_prop("properties", AAZObjectType)

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("authorization", AAZObjectType)
                properties.set_prop("autoDiscovery", AAZStrType, ".auto_discovery")
                properties.set_prop("topLevelInventoryList", AAZListType, ".inventory_list")

            authorization = _builder.get(".properties.authorization")
            if authorization is not None:
                authorization.set_prop("code", AAZStrType, ".authorization_code", typ_kwargs={"flags": {"secret": True}})

            top_level_inventory_list = _builder.get(".properties.topLevelInventoryList")
            if top_level_inventory_list is not None:
                top_level_inventory_list.set_elements(AAZStrType, ".")

            return self.serialize_content(_content_value)

        def on_200_201(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200_201
            )

        _schema_on_200_201 = None

        @classmethod
        def _build_schema_on_200_201(cls):
            if cls._schema_on_200_201 is not None:
                return cls._schema_on_200_201

            cls._schema_on_200_201 = AAZObjectType()
            _CreateHelper._build_schema_dev_ops_configuration_read(cls._schema_on_200_201)

            return cls._schema_on_200_201


class _CreateHelper:
    """Helper class for Create"""

    _schema_dev_ops_configuration_read = None

    @classmethod
    def _build_schema_dev_ops_configuration_read(cls, _schema):
        if cls._schema_dev_ops_configuration_read is not None:
            _schema.id = cls._schema_dev_ops_configuration_read.id
            _schema.name = cls._schema_dev_ops_configuration_read.name
            _schema.properties = cls._schema_dev_ops_configuration_read.properties
            _schema.system_data = cls._schema_dev_ops_configuration_read.system_data
            _schema.type = cls._schema_dev_ops_configuration_read.type
            return

        cls._schema_dev_ops_configuration_read = _schema_dev_ops_configuration_read = AAZObjectType()

        dev_ops_configuration_read = _schema_dev_ops_configuration_read
        dev_ops_configuration_read.id = AAZStrType(
            flags={"read_only": True},
        )
        dev_ops_configuration_read.name = AAZStrType(
            flags={"read_only": True},
        )
        dev_ops_configuration_read.properties = AAZObjectType()
        dev_ops_configuration_read.system_data = AAZObjectType(
            serialized_name="systemData",
            flags={"read_only": True},
        )
        dev_ops_configuration_read.type = AAZStrType(
            flags={"read_only": True},
        )

        properties = _schema_dev_ops_configuration_read.properties
        properties.authorization = AAZObjectType()
        properties.auto_discovery = AAZStrType(
            serialized_name="autoDiscovery",
        )
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
        )
        properties.provisioning_status_message = AAZStrType(
            serialized_name="provisioningStatusMessage",
            flags={"read_only": True},
        )
        properties.provisioning_status_update_time_utc = AAZStrType(
            serialized_name="provisioningStatusUpdateTimeUtc",
            flags={"read_only": True},
        )
        properties.top_level_inventory_list = AAZListType(
            serialized_name="topLevelInventoryList",
        )

        authorization = _schema_dev_ops_configuration_read.properties.authorization
        authorization.code = AAZStrType(
            flags={"secret": True},
        )

        top_level_inventory_list = _schema_dev_ops_configuration_read.properties.top_level_inventory_list
        top_level_inventory_list.Element = AAZStrType()

        system_data = _schema_dev_ops_configuration_read.system_data
        system_data.created_at = AAZStrType(
            serialized_name="createdAt",
        )
        system_data.created_by = AAZStrType(
            serialized_name="createdBy",
        )
        system_data.created_by_type = AAZStrType(
            serialized_name="createdByType",
        )
        system_data.last_modified_at = AAZStrType(
            serialized_name="lastModifiedAt",
        )
        system_data.last_modified_by = AAZStrType(
            serialized_name="lastModifiedBy",
        )
        system_data.last_modified_by_type = AAZStrType(
            serialized_name="lastModifiedByType",
        )

        _schema.id = cls._schema_dev_ops_configuration_read.id
        _schema.name = cls._schema_dev_ops_configuration_read.name
        _schema.properties = cls._schema_dev_ops_configuration_read.properties
        _schema.system_data = cls._schema_dev_ops_configuration_read.system_data
        _schema.type = cls._schema_dev_ops_configuration_read.type


__all__ = ["Create"]
