# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from collections import OrderedDict
import os
import re
from typing import (
    Dict,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from google.cloud.spanner_admin_database_v1 import gapic_version as package_version

from google.api_core import client_options as client_options_lib
from google.api_core import exceptions as core_exceptions
from google.api_core import gapic_v1
from google.api_core import retry as retries
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore

from google.api_core import operation  # type: ignore
from google.api_core import operation_async  # type: ignore
from google.cloud.spanner_admin_database_v1.services.database_admin import pagers
from google.cloud.spanner_admin_database_v1.types import backup
from google.cloud.spanner_admin_database_v1.types import backup as gsad_backup
from google.cloud.spanner_admin_database_v1.types import common
from google.cloud.spanner_admin_database_v1.types import spanner_database_admin
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from .transports.base import DatabaseAdminTransport, DEFAULT_CLIENT_INFO
from .transports.grpc import DatabaseAdminGrpcTransport
from .transports.grpc_asyncio import DatabaseAdminGrpcAsyncIOTransport
from .transports.rest import DatabaseAdminRestTransport


class DatabaseAdminClientMeta(type):
    """Metaclass for the DatabaseAdmin client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[DatabaseAdminTransport]]
    _transport_registry["grpc"] = DatabaseAdminGrpcTransport
    _transport_registry["grpc_asyncio"] = DatabaseAdminGrpcAsyncIOTransport
    _transport_registry["rest"] = DatabaseAdminRestTransport

    def get_transport_class(
        cls,
        label: Optional[str] = None,
    ) -> Type[DatabaseAdminTransport]:
        """Returns an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class DatabaseAdminClient(metaclass=DatabaseAdminClientMeta):
    """Cloud Spanner Database Admin API

    The Cloud Spanner Database Admin API can be used to:

    -  create, drop, and list databases
    -  update the schema of pre-existing databases
    -  create, delete and list backups for a database
    -  restore a database from an existing backup
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Converts api endpoint to mTLS endpoint.

        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "spanner.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DatabaseAdminClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_info(info)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            DatabaseAdminClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> DatabaseAdminTransport:
        """Returns the transport used by the client instance.

        Returns:
            DatabaseAdminTransport: The transport used by the client
                instance.
        """
        return self._transport

    @staticmethod
    def backup_path(
        project: str,
        instance: str,
        backup: str,
    ) -> str:
        """Returns a fully-qualified backup string."""
        return "projects/{project}/instances/{instance}/backups/{backup}".format(
            project=project,
            instance=instance,
            backup=backup,
        )

    @staticmethod
    def parse_backup_path(path: str) -> Dict[str, str]:
        """Parses a backup path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/instances/(?P<instance>.+?)/backups/(?P<backup>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def crypto_key_path(
        project: str,
        location: str,
        key_ring: str,
        crypto_key: str,
    ) -> str:
        """Returns a fully-qualified crypto_key string."""
        return "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}".format(
            project=project,
            location=location,
            key_ring=key_ring,
            crypto_key=crypto_key,
        )

    @staticmethod
    def parse_crypto_key_path(path: str) -> Dict[str, str]:
        """Parses a crypto_key path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/keyRings/(?P<key_ring>.+?)/cryptoKeys/(?P<crypto_key>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def crypto_key_version_path(
        project: str,
        location: str,
        key_ring: str,
        crypto_key: str,
        crypto_key_version: str,
    ) -> str:
        """Returns a fully-qualified crypto_key_version string."""
        return "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{crypto_key_version}".format(
            project=project,
            location=location,
            key_ring=key_ring,
            crypto_key=crypto_key,
            crypto_key_version=crypto_key_version,
        )

    @staticmethod
    def parse_crypto_key_version_path(path: str) -> Dict[str, str]:
        """Parses a crypto_key_version path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)/keyRings/(?P<key_ring>.+?)/cryptoKeys/(?P<crypto_key>.+?)/cryptoKeyVersions/(?P<crypto_key_version>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def database_path(
        project: str,
        instance: str,
        database: str,
    ) -> str:
        """Returns a fully-qualified database string."""
        return "projects/{project}/instances/{instance}/databases/{database}".format(
            project=project,
            instance=instance,
            database=database,
        )

    @staticmethod
    def parse_database_path(path: str) -> Dict[str, str]:
        """Parses a database path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/instances/(?P<instance>.+?)/databases/(?P<database>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def database_role_path(
        project: str,
        instance: str,
        database: str,
        role: str,
    ) -> str:
        """Returns a fully-qualified database_role string."""
        return "projects/{project}/instances/{instance}/databases/{database}/databaseRoles/{role}".format(
            project=project,
            instance=instance,
            database=database,
            role=role,
        )

    @staticmethod
    def parse_database_role_path(path: str) -> Dict[str, str]:
        """Parses a database_role path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/instances/(?P<instance>.+?)/databases/(?P<database>.+?)/databaseRoles/(?P<role>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def instance_path(
        project: str,
        instance: str,
    ) -> str:
        """Returns a fully-qualified instance string."""
        return "projects/{project}/instances/{instance}".format(
            project=project,
            instance=instance,
        )

    @staticmethod
    def parse_instance_path(path: str) -> Dict[str, str]:
        """Parses a instance path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/instances/(?P<instance>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_billing_account_path(
        billing_account: str,
    ) -> str:
        """Returns a fully-qualified billing_account string."""
        return "billingAccounts/{billing_account}".format(
            billing_account=billing_account,
        )

    @staticmethod
    def parse_common_billing_account_path(path: str) -> Dict[str, str]:
        """Parse a billing_account path into its component segments."""
        m = re.match(r"^billingAccounts/(?P<billing_account>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_folder_path(
        folder: str,
    ) -> str:
        """Returns a fully-qualified folder string."""
        return "folders/{folder}".format(
            folder=folder,
        )

    @staticmethod
    def parse_common_folder_path(path: str) -> Dict[str, str]:
        """Parse a folder path into its component segments."""
        m = re.match(r"^folders/(?P<folder>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_organization_path(
        organization: str,
    ) -> str:
        """Returns a fully-qualified organization string."""
        return "organizations/{organization}".format(
            organization=organization,
        )

    @staticmethod
    def parse_common_organization_path(path: str) -> Dict[str, str]:
        """Parse a organization path into its component segments."""
        m = re.match(r"^organizations/(?P<organization>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_project_path(
        project: str,
    ) -> str:
        """Returns a fully-qualified project string."""
        return "projects/{project}".format(
            project=project,
        )

    @staticmethod
    def parse_common_project_path(path: str) -> Dict[str, str]:
        """Parse a project path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)$", path)
        return m.groupdict() if m else {}

    @staticmethod
    def common_location_path(
        project: str,
        location: str,
    ) -> str:
        """Returns a fully-qualified location string."""
        return "projects/{project}/locations/{location}".format(
            project=project,
            location=location,
        )

    @staticmethod
    def parse_common_location_path(path: str) -> Dict[str, str]:
        """Parse a location path into its component segments."""
        m = re.match(r"^projects/(?P<project>.+?)/locations/(?P<location>.+?)$", path)
        return m.groupdict() if m else {}

    @classmethod
    def get_mtls_endpoint_and_cert_source(
        cls, client_options: Optional[client_options_lib.ClientOptions] = None
    ):
        """Return the API endpoint and client cert source for mutual TLS.

        The client cert source is determined in the following order:
        (1) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is not "true", the
        client cert source is None.
        (2) if `client_options.client_cert_source` is provided, use the provided one; if the
        default client cert source exists, use the default one; otherwise the client cert
        source is None.

        The API endpoint is determined in the following order:
        (1) if `client_options.api_endpoint` if provided, use the provided one.
        (2) if `GOOGLE_API_USE_CLIENT_CERTIFICATE` environment variable is "always", use the
        default mTLS endpoint; if the environment variable is "never", use the default API
        endpoint; otherwise if client cert source exists, use the default mTLS endpoint, otherwise
        use the default API endpoint.

        More details can be found at https://google.aip.dev/auth/4114.

        Args:
            client_options (google.api_core.client_options.ClientOptions): Custom options for the
                client. Only the `api_endpoint` and `client_cert_source` properties may be used
                in this method.

        Returns:
            Tuple[str, Callable[[], Tuple[bytes, bytes]]]: returns the API endpoint and the
                client cert source to use.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If any errors happen.
        """
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        use_client_cert = os.getenv("GOOGLE_API_USE_CLIENT_CERTIFICATE", "false")
        use_mtls_endpoint = os.getenv("GOOGLE_API_USE_MTLS_ENDPOINT", "auto")
        if use_client_cert not in ("true", "false"):
            raise ValueError(
                "Environment variable `GOOGLE_API_USE_CLIENT_CERTIFICATE` must be either `true` or `false`"
            )
        if use_mtls_endpoint not in ("auto", "never", "always"):
            raise MutualTLSChannelError(
                "Environment variable `GOOGLE_API_USE_MTLS_ENDPOINT` must be `never`, `auto` or `always`"
            )

        # Figure out the client cert source to use.
        client_cert_source = None
        if use_client_cert == "true":
            if client_options.client_cert_source:
                client_cert_source = client_options.client_cert_source
            elif mtls.has_default_client_cert_source():
                client_cert_source = mtls.default_client_cert_source()

        # Figure out which api endpoint to use.
        if client_options.api_endpoint is not None:
            api_endpoint = client_options.api_endpoint
        elif use_mtls_endpoint == "always" or (
            use_mtls_endpoint == "auto" and client_cert_source
        ):
            api_endpoint = cls.DEFAULT_MTLS_ENDPOINT
        else:
            api_endpoint = cls.DEFAULT_ENDPOINT

        return api_endpoint, client_cert_source

    def __init__(
        self,
        *,
        credentials: Optional[ga_credentials.Credentials] = None,
        transport: Optional[Union[str, DatabaseAdminTransport]] = None,
        client_options: Optional[Union[client_options_lib.ClientOptions, dict]] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the database admin client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, DatabaseAdminTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (Optional[Union[google.api_core.client_options.ClientOptions, dict]]): Custom options for the
                client. It won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = client_options_lib.from_dict(client_options)
        if client_options is None:
            client_options = client_options_lib.ClientOptions()
        client_options = cast(client_options_lib.ClientOptions, client_options)

        api_endpoint, client_cert_source_func = self.get_mtls_endpoint_and_cert_source(
            client_options
        )

        api_key_value = getattr(client_options, "api_key", None)
        if api_key_value and credentials:
            raise ValueError(
                "client_options.api_key and credentials are mutually exclusive"
            )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, DatabaseAdminTransport):
            # transport is a DatabaseAdminTransport instance.
            if credentials or client_options.credentials_file or api_key_value:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, provide its scopes "
                    "directly."
                )
            self._transport = transport
        else:
            import google.auth._default  # type: ignore

            if api_key_value and hasattr(
                google.auth._default, "get_api_key_credentials"
            ):
                credentials = google.auth._default.get_api_key_credentials(
                    api_key_value
                )

            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=api_endpoint,
                scopes=client_options.scopes,
                client_cert_source_for_mtls=client_cert_source_func,
                quota_project_id=client_options.quota_project_id,
                client_info=client_info,
                always_use_jwt_access=True,
                api_audience=client_options.api_audience,
            )

    def list_databases(
        self,
        request: Optional[
            Union[spanner_database_admin.ListDatabasesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDatabasesPager:
        r"""Lists Cloud Spanner databases.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_list_databases():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.ListDatabasesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_databases(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.ListDatabasesRequest, dict]):
                The request object. The request for
                [ListDatabases][google.spanner.admin.database.v1.DatabaseAdmin.ListDatabases].
            parent (str):
                Required. The instance whose databases should be listed.
                Values are of the form
                ``projects/<project>/instances/<instance>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.spanner_admin_database_v1.services.database_admin.pagers.ListDatabasesPager:
                The response for
                [ListDatabases][google.spanner.admin.database.v1.DatabaseAdmin.ListDatabases].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a spanner_database_admin.ListDatabasesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, spanner_database_admin.ListDatabasesRequest):
            request = spanner_database_admin.ListDatabasesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_databases]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDatabasesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_database(
        self,
        request: Optional[
            Union[spanner_database_admin.CreateDatabaseRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        create_statement: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Creates a new Cloud Spanner database and starts to prepare it
        for serving. The returned [long-running
        operation][google.longrunning.Operation] will have a name of the
        format ``<database_name>/operations/<operation_id>`` and can be
        used to track preparation of the database. The
        [metadata][google.longrunning.Operation.metadata] field type is
        [CreateDatabaseMetadata][google.spanner.admin.database.v1.CreateDatabaseMetadata].
        The [response][google.longrunning.Operation.response] field type
        is [Database][google.spanner.admin.database.v1.Database], if
        successful.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_create_database():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.CreateDatabaseRequest(
                    parent="parent_value",
                    create_statement="create_statement_value",
                )

                # Make the request
                operation = client.create_database(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.CreateDatabaseRequest, dict]):
                The request object. The request for
                [CreateDatabase][google.spanner.admin.database.v1.DatabaseAdmin.CreateDatabase].
            parent (str):
                Required. The name of the instance that will serve the
                new database. Values are of the form
                ``projects/<project>/instances/<instance>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            create_statement (str):
                Required. A ``CREATE DATABASE`` statement, which
                specifies the ID of the new database. The database ID
                must conform to the regular expression
                ``[a-z][a-z0-9_\-]*[a-z0-9]`` and be between 2 and 30
                characters in length. If the database ID is a reserved
                word or if it contains a hyphen, the database ID must be
                enclosed in backticks (:literal:`\``).

                This corresponds to the ``create_statement`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.spanner_admin_database_v1.types.Database`
                A Cloud Spanner database.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, create_statement])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a spanner_database_admin.CreateDatabaseRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, spanner_database_admin.CreateDatabaseRequest):
            request = spanner_database_admin.CreateDatabaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if create_statement is not None:
                request.create_statement = create_statement

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_database]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            spanner_database_admin.Database,
            metadata_type=spanner_database_admin.CreateDatabaseMetadata,
        )

        # Done; return the response.
        return response

    def get_database(
        self,
        request: Optional[
            Union[spanner_database_admin.GetDatabaseRequest, dict]
        ] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> spanner_database_admin.Database:
        r"""Gets the state of a Cloud Spanner database.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_get_database():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.GetDatabaseRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_database(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.GetDatabaseRequest, dict]):
                The request object. The request for
                [GetDatabase][google.spanner.admin.database.v1.DatabaseAdmin.GetDatabase].
            name (str):
                Required. The name of the requested database. Values are
                of the form
                ``projects/<project>/instances/<instance>/databases/<database>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.spanner_admin_database_v1.types.Database:
                A Cloud Spanner database.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a spanner_database_admin.GetDatabaseRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, spanner_database_admin.GetDatabaseRequest):
            request = spanner_database_admin.GetDatabaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_database]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_database_ddl(
        self,
        request: Optional[
            Union[spanner_database_admin.UpdateDatabaseDdlRequest, dict]
        ] = None,
        *,
        database: Optional[str] = None,
        statements: Optional[MutableSequence[str]] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Updates the schema of a Cloud Spanner database by
        creating/altering/dropping tables, columns, indexes, etc. The
        returned [long-running operation][google.longrunning.Operation]
        will have a name of the format
        ``<database_name>/operations/<operation_id>`` and can be used to
        track execution of the schema change(s). The
        [metadata][google.longrunning.Operation.metadata] field type is
        [UpdateDatabaseDdlMetadata][google.spanner.admin.database.v1.UpdateDatabaseDdlMetadata].
        The operation has no response.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_update_database_ddl():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.UpdateDatabaseDdlRequest(
                    database="database_value",
                    statements=['statements_value1', 'statements_value2'],
                )

                # Make the request
                operation = client.update_database_ddl(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.UpdateDatabaseDdlRequest, dict]):
                The request object. Enqueues the given DDL statements to be applied, in
                order but not necessarily all at once, to the database
                schema at some point (or points) in the future. The
                server checks that the statements are executable
                (syntactically valid, name tables that exist, etc.)
                before enqueueing them, but they may still fail upon
                later execution (e.g., if a statement from another batch
                of statements is applied first and it conflicts in some
                way, or if there is some data-related problem like a
                ``NULL`` value in a column to which ``NOT NULL`` would
                be added). If a statement fails, all subsequent
                statements in the batch are automatically cancelled.

                Each batch of statements is assigned a name which can be
                used with the
                [Operations][google.longrunning.Operations] API to
                monitor progress. See the
                [operation_id][google.spanner.admin.database.v1.UpdateDatabaseDdlRequest.operation_id]
                field for more details.
            database (str):
                Required. The database to update.
                This corresponds to the ``database`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            statements (MutableSequence[str]):
                Required. DDL statements to be
                applied to the database.

                This corresponds to the ``statements`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be :class:`google.protobuf.empty_pb2.Empty` A generic empty message that you can re-use to avoid defining duplicated
                   empty messages in your APIs. A typical example is to
                   use it as the request or the response type of an API
                   method. For instance:

                      service Foo {
                         rpc Bar(google.protobuf.Empty) returns
                         (google.protobuf.Empty);

                      }

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([database, statements])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a spanner_database_admin.UpdateDatabaseDdlRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, spanner_database_admin.UpdateDatabaseDdlRequest):
            request = spanner_database_admin.UpdateDatabaseDdlRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if database is not None:
                request.database = database
            if statements is not None:
                request.statements = statements

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_database_ddl]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("database", request.database),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            empty_pb2.Empty,
            metadata_type=spanner_database_admin.UpdateDatabaseDdlMetadata,
        )

        # Done; return the response.
        return response

    def drop_database(
        self,
        request: Optional[
            Union[spanner_database_admin.DropDatabaseRequest, dict]
        ] = None,
        *,
        database: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Drops (aka deletes) a Cloud Spanner database. Completed backups
        for the database will be retained according to their
        ``expire_time``. Note: Cloud Spanner might continue to accept
        requests for a few seconds after the database has been deleted.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_drop_database():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.DropDatabaseRequest(
                    database="database_value",
                )

                # Make the request
                client.drop_database(request=request)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.DropDatabaseRequest, dict]):
                The request object. The request for
                [DropDatabase][google.spanner.admin.database.v1.DatabaseAdmin.DropDatabase].
            database (str):
                Required. The database to be dropped.
                This corresponds to the ``database`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([database])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a spanner_database_admin.DropDatabaseRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, spanner_database_admin.DropDatabaseRequest):
            request = spanner_database_admin.DropDatabaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if database is not None:
                request.database = database

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.drop_database]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("database", request.database),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def get_database_ddl(
        self,
        request: Optional[
            Union[spanner_database_admin.GetDatabaseDdlRequest, dict]
        ] = None,
        *,
        database: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> spanner_database_admin.GetDatabaseDdlResponse:
        r"""Returns the schema of a Cloud Spanner database as a list of
        formatted DDL statements. This method does not show pending
        schema updates, those may be queried using the
        [Operations][google.longrunning.Operations] API.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_get_database_ddl():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.GetDatabaseDdlRequest(
                    database="database_value",
                )

                # Make the request
                response = client.get_database_ddl(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.GetDatabaseDdlRequest, dict]):
                The request object. The request for
                [GetDatabaseDdl][google.spanner.admin.database.v1.DatabaseAdmin.GetDatabaseDdl].
            database (str):
                Required. The database whose schema we wish to get.
                Values are of the form
                ``projects/<project>/instances/<instance>/databases/<database>``

                This corresponds to the ``database`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.spanner_admin_database_v1.types.GetDatabaseDdlResponse:
                The response for
                [GetDatabaseDdl][google.spanner.admin.database.v1.DatabaseAdmin.GetDatabaseDdl].

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([database])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a spanner_database_admin.GetDatabaseDdlRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, spanner_database_admin.GetDatabaseDdlRequest):
            request = spanner_database_admin.GetDatabaseDdlRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if database is not None:
                request.database = database

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_database_ddl]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("database", request.database),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def set_iam_policy(
        self,
        request: Optional[Union[iam_policy_pb2.SetIamPolicyRequest, dict]] = None,
        *,
        resource: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Sets the access control policy on a database or backup resource.
        Replaces any existing policy.

        Authorization requires ``spanner.databases.setIamPolicy``
        permission on
        [resource][google.iam.v1.SetIamPolicyRequest.resource]. For
        backups, authorization requires ``spanner.backups.setIamPolicy``
        permission on
        [resource][google.iam.v1.SetIamPolicyRequest.resource].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_set_iam_policy():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.SetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = client.set_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.SetIamPolicyRequest, dict]):
                The request object. Request message for ``SetIamPolicy`` method.
            resource (str):
                REQUIRED: The resource for which the
                policy is being specified. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": [ "user:eve@example.com" ],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ], "etag": "BwWWja0YfJA=", "version": 3

                      }

                   **YAML example:**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z') etag:
                      BwWWja0YfJA= version: 3

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.SetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.SetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.set_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_iam_policy(
        self,
        request: Optional[Union[iam_policy_pb2.GetIamPolicyRequest, dict]] = None,
        *,
        resource: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> policy_pb2.Policy:
        r"""Gets the access control policy for a database or backup
        resource. Returns an empty policy if a database or backup exists
        but does not have a policy set.

        Authorization requires ``spanner.databases.getIamPolicy``
        permission on
        [resource][google.iam.v1.GetIamPolicyRequest.resource]. For
        backups, authorization requires ``spanner.backups.getIamPolicy``
        permission on
        [resource][google.iam.v1.GetIamPolicyRequest.resource].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_get_iam_policy():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.GetIamPolicyRequest(
                    resource="resource_value",
                )

                # Make the request
                response = client.get_iam_policy(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.GetIamPolicyRequest, dict]):
                The request object. Request message for ``GetIamPolicy`` method.
            resource (str):
                REQUIRED: The resource for which the
                policy is being requested. See the
                operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.policy_pb2.Policy:
                An Identity and Access Management (IAM) policy, which specifies access
                   controls for Google Cloud resources.

                   A Policy is a collection of bindings. A binding binds
                   one or more members, or principals, to a single role.
                   Principals can be user accounts, service accounts,
                   Google groups, and domains (such as G Suite). A role
                   is a named list of permissions; each role can be an
                   IAM predefined role or a user-created custom role.

                   For some types of Google Cloud resources, a binding
                   can also specify a condition, which is a logical
                   expression that allows access to a resource only if
                   the expression evaluates to true. A condition can add
                   constraints based on attributes of the request, the
                   resource, or both. To learn which resources support
                   conditions in their IAM policies, see the [IAM
                   documentation](\ https://cloud.google.com/iam/help/conditions/resource-policies).

                   **JSON example:**

                      {
                         "bindings": [
                            {
                               "role":
                               "roles/resourcemanager.organizationAdmin",
                               "members": [ "user:mike@example.com",
                               "group:admins@example.com",
                               "domain:google.com",
                               "serviceAccount:my-project-id@appspot.gserviceaccount.com"
                               ]

                            }, { "role":
                            "roles/resourcemanager.organizationViewer",
                            "members": [ "user:eve@example.com" ],
                            "condition": { "title": "expirable access",
                            "description": "Does not grant access after
                            Sep 2020", "expression": "request.time <
                            timestamp('2020-10-01T00:00:00.000Z')", } }

                         ], "etag": "BwWWja0YfJA=", "version": 3

                      }

                   **YAML example:**

                      bindings: - members: - user:\ mike@example.com -
                      group:\ admins@example.com - domain:google.com -
                      serviceAccount:\ my-project-id@appspot.gserviceaccount.com
                      role: roles/resourcemanager.organizationAdmin -
                      members: - user:\ eve@example.com role:
                      roles/resourcemanager.organizationViewer
                      condition: title: expirable access description:
                      Does not grant access after Sep 2020 expression:
                      request.time <
                      timestamp('2020-10-01T00:00:00.000Z') etag:
                      BwWWja0YfJA= version: 3

                   For a description of IAM and its features, see the
                   [IAM
                   documentation](\ https://cloud.google.com/iam/docs/).

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.GetIamPolicyRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.GetIamPolicyRequest()
            if resource is not None:
                request.resource = resource

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_iam_policy]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def test_iam_permissions(
        self,
        request: Optional[Union[iam_policy_pb2.TestIamPermissionsRequest, dict]] = None,
        *,
        resource: Optional[str] = None,
        permissions: Optional[MutableSequence[str]] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        r"""Returns permissions that the caller has on the specified
        database or backup resource.

        Attempting this RPC on a non-existent Cloud Spanner database
        will result in a NOT_FOUND error if the user has
        ``spanner.databases.list`` permission on the containing Cloud
        Spanner instance. Otherwise returns an empty set of permissions.
        Calling this method on a backup that does not exist will result
        in a NOT_FOUND error if the user has ``spanner.backups.list``
        permission on the containing instance.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1
            from google.iam.v1 import iam_policy_pb2  # type: ignore

            def sample_test_iam_permissions():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = iam_policy_pb2.TestIamPermissionsRequest(
                    resource="resource_value",
                    permissions=['permissions_value1', 'permissions_value2'],
                )

                # Make the request
                response = client.test_iam_permissions(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.iam.v1.iam_policy_pb2.TestIamPermissionsRequest, dict]):
                The request object. Request message for ``TestIamPermissions`` method.
            resource (str):
                REQUIRED: The resource for which the
                policy detail is being requested. See
                the operation documentation for the
                appropriate value for this field.

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            permissions (MutableSequence[str]):
                The set of permissions to check for the ``resource``.
                Permissions with wildcards (such as '*' or 'storage.*')
                are not allowed. For more information see `IAM
                Overview <https://cloud.google.com/iam/docs/overview#permissions>`__.

                This corresponds to the ``permissions`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.iam.v1.iam_policy_pb2.TestIamPermissionsResponse:
                Response message for TestIamPermissions method.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource, permissions])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        if isinstance(request, dict):
            # The request isn't a proto-plus wrapped type,
            # so it must be constructed via keyword expansion.
            request = iam_policy_pb2.TestIamPermissionsRequest(**request)
        elif not request:
            # Null request, just make one.
            request = iam_policy_pb2.TestIamPermissionsRequest()
            if resource is not None:
                request.resource = resource
            if permissions:
                request.permissions.extend(permissions)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.test_iam_permissions]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("resource", request.resource),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def create_backup(
        self,
        request: Optional[Union[gsad_backup.CreateBackupRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        backup: Optional[gsad_backup.Backup] = None,
        backup_id: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Starts creating a new Cloud Spanner Backup. The returned backup
        [long-running operation][google.longrunning.Operation] will have
        a name of the format
        ``projects/<project>/instances/<instance>/backups/<backup>/operations/<operation_id>``
        and can be used to track creation of the backup. The
        [metadata][google.longrunning.Operation.metadata] field type is
        [CreateBackupMetadata][google.spanner.admin.database.v1.CreateBackupMetadata].
        The [response][google.longrunning.Operation.response] field type
        is [Backup][google.spanner.admin.database.v1.Backup], if
        successful. Cancelling the returned operation will stop the
        creation and delete the backup. There can be only one pending
        backup creation per database. Backup creation of different
        databases can run concurrently.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_create_backup():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.CreateBackupRequest(
                    parent="parent_value",
                    backup_id="backup_id_value",
                )

                # Make the request
                operation = client.create_backup(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.CreateBackupRequest, dict]):
                The request object. The request for
                [CreateBackup][google.spanner.admin.database.v1.DatabaseAdmin.CreateBackup].
            parent (str):
                Required. The name of the instance in which the backup
                will be created. This must be the same instance that
                contains the database the backup will be created from.
                The backup will be stored in the location(s) specified
                in the instance configuration of this instance. Values
                are of the form
                ``projects/<project>/instances/<instance>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup (google.cloud.spanner_admin_database_v1.types.Backup):
                Required. The backup to create.
                This corresponds to the ``backup`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup_id (str):
                Required. The id of the backup to be created. The
                ``backup_id`` appended to ``parent`` forms the full
                backup name of the form
                ``projects/<project>/instances/<instance>/backups/<backup_id>``.

                This corresponds to the ``backup_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.spanner_admin_database_v1.types.Backup`
                A backup of a Cloud Spanner database.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, backup, backup_id])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gsad_backup.CreateBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gsad_backup.CreateBackupRequest):
            request = gsad_backup.CreateBackupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if backup is not None:
                request.backup = backup
            if backup_id is not None:
                request.backup_id = backup_id

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_backup]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            gsad_backup.Backup,
            metadata_type=gsad_backup.CreateBackupMetadata,
        )

        # Done; return the response.
        return response

    def copy_backup(
        self,
        request: Optional[Union[backup.CopyBackupRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        backup_id: Optional[str] = None,
        source_backup: Optional[str] = None,
        expire_time: Optional[timestamp_pb2.Timestamp] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Starts copying a Cloud Spanner Backup. The returned backup
        [long-running operation][google.longrunning.Operation] will have
        a name of the format
        ``projects/<project>/instances/<instance>/backups/<backup>/operations/<operation_id>``
        and can be used to track copying of the backup. The operation is
        associated with the destination backup. The
        [metadata][google.longrunning.Operation.metadata] field type is
        [CopyBackupMetadata][google.spanner.admin.database.v1.CopyBackupMetadata].
        The [response][google.longrunning.Operation.response] field type
        is [Backup][google.spanner.admin.database.v1.Backup], if
        successful. Cancelling the returned operation will stop the
        copying and delete the backup. Concurrent CopyBackup requests
        can run on the same source backup.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_copy_backup():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.CopyBackupRequest(
                    parent="parent_value",
                    backup_id="backup_id_value",
                    source_backup="source_backup_value",
                )

                # Make the request
                operation = client.copy_backup(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.CopyBackupRequest, dict]):
                The request object. The request for
                [CopyBackup][google.spanner.admin.database.v1.DatabaseAdmin.CopyBackup].
            parent (str):
                Required. The name of the destination instance that will
                contain the backup copy. Values are of the form:
                ``projects/<project>/instances/<instance>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup_id (str):
                Required. The id of the backup copy. The ``backup_id``
                appended to ``parent`` forms the full backup_uri of the
                form
                ``projects/<project>/instances/<instance>/backups/<backup>``.

                This corresponds to the ``backup_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            source_backup (str):
                Required. The source backup to be copied. The source
                backup needs to be in READY state for it to be copied.
                Once CopyBackup is in progress, the source backup cannot
                be deleted or cleaned up on expiration until CopyBackup
                is finished. Values are of the form:
                ``projects/<project>/instances/<instance>/backups/<backup>``.

                This corresponds to the ``source_backup`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            expire_time (google.protobuf.timestamp_pb2.Timestamp):
                Required. The expiration time of the backup in
                microsecond granularity. The expiration time must be at
                least 6 hours and at most 366 days from the
                ``create_time`` of the source backup. Once the
                ``expire_time`` has passed, the backup is eligible to be
                automatically deleted by Cloud Spanner to free the
                resources used by the backup.

                This corresponds to the ``expire_time`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.spanner_admin_database_v1.types.Backup`
                A backup of a Cloud Spanner database.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, backup_id, source_backup, expire_time])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a backup.CopyBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, backup.CopyBackupRequest):
            request = backup.CopyBackupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if backup_id is not None:
                request.backup_id = backup_id
            if source_backup is not None:
                request.source_backup = source_backup
            if expire_time is not None:
                request.expire_time = expire_time

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.copy_backup]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            backup.Backup,
            metadata_type=backup.CopyBackupMetadata,
        )

        # Done; return the response.
        return response

    def get_backup(
        self,
        request: Optional[Union[backup.GetBackupRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> backup.Backup:
        r"""Gets metadata on a pending or completed
        [Backup][google.spanner.admin.database.v1.Backup].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_get_backup():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.GetBackupRequest(
                    name="name_value",
                )

                # Make the request
                response = client.get_backup(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.GetBackupRequest, dict]):
                The request object. The request for
                [GetBackup][google.spanner.admin.database.v1.DatabaseAdmin.GetBackup].
            name (str):
                Required. Name of the backup. Values are of the form
                ``projects/<project>/instances/<instance>/backups/<backup>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.spanner_admin_database_v1.types.Backup:
                A backup of a Cloud Spanner database.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a backup.GetBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, backup.GetBackupRequest):
            request = backup.GetBackupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_backup]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def update_backup(
        self,
        request: Optional[Union[gsad_backup.UpdateBackupRequest, dict]] = None,
        *,
        backup: Optional[gsad_backup.Backup] = None,
        update_mask: Optional[field_mask_pb2.FieldMask] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> gsad_backup.Backup:
        r"""Updates a pending or completed
        [Backup][google.spanner.admin.database.v1.Backup].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_update_backup():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.UpdateBackupRequest(
                )

                # Make the request
                response = client.update_backup(request=request)

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.UpdateBackupRequest, dict]):
                The request object. The request for
                [UpdateBackup][google.spanner.admin.database.v1.DatabaseAdmin.UpdateBackup].
            backup (google.cloud.spanner_admin_database_v1.types.Backup):
                Required. The backup to update. ``backup.name``, and the
                fields to be updated as specified by ``update_mask`` are
                required. Other fields are ignored. Update is only
                supported for the following fields:

                -  ``backup.expire_time``.

                This corresponds to the ``backup`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (google.protobuf.field_mask_pb2.FieldMask):
                Required. A mask specifying which fields (e.g.
                ``expire_time``) in the Backup resource should be
                updated. This mask is relative to the Backup resource,
                not to the request message. The field mask must always
                be specified; this prevents any future fields from being
                erased accidentally by clients that do not know about
                them.

                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.spanner_admin_database_v1.types.Backup:
                A backup of a Cloud Spanner database.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([backup, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a gsad_backup.UpdateBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, gsad_backup.UpdateBackupRequest):
            request = gsad_backup.UpdateBackupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if backup is not None:
                request.backup = backup
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_backup]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata(
                (("backup.name", request.backup.name),)
            ),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_backup(
        self,
        request: Optional[Union[backup.DeleteBackupRequest, dict]] = None,
        *,
        name: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a pending or completed
        [Backup][google.spanner.admin.database.v1.Backup].

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_delete_backup():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.DeleteBackupRequest(
                    name="name_value",
                )

                # Make the request
                client.delete_backup(request=request)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.DeleteBackupRequest, dict]):
                The request object. The request for
                [DeleteBackup][google.spanner.admin.database.v1.DatabaseAdmin.DeleteBackup].
            name (str):
                Required. Name of the backup to delete. Values are of
                the form
                ``projects/<project>/instances/<instance>/backups/<backup>``.

                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a backup.DeleteBackupRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, backup.DeleteBackupRequest):
            request = backup.DeleteBackupRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_backup]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def list_backups(
        self,
        request: Optional[Union[backup.ListBackupsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBackupsPager:
        r"""Lists completed and pending backups. Backups returned are
        ordered by ``create_time`` in descending order, starting from
        the most recent ``create_time``.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_list_backups():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.ListBackupsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_backups(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.ListBackupsRequest, dict]):
                The request object. The request for
                [ListBackups][google.spanner.admin.database.v1.DatabaseAdmin.ListBackups].
            parent (str):
                Required. The instance to list backups from. Values are
                of the form ``projects/<project>/instances/<instance>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.spanner_admin_database_v1.services.database_admin.pagers.ListBackupsPager:
                The response for
                [ListBackups][google.spanner.admin.database.v1.DatabaseAdmin.ListBackups].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a backup.ListBackupsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, backup.ListBackupsRequest):
            request = backup.ListBackupsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_backups]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListBackupsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def restore_database(
        self,
        request: Optional[
            Union[spanner_database_admin.RestoreDatabaseRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        database_id: Optional[str] = None,
        backup: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operation.Operation:
        r"""Create a new database by restoring from a completed backup. The
        new database must be in the same project and in an instance with
        the same instance configuration as the instance containing the
        backup. The returned database [long-running
        operation][google.longrunning.Operation] has a name of the
        format
        ``projects/<project>/instances/<instance>/databases/<database>/operations/<operation_id>``,
        and can be used to track the progress of the operation, and to
        cancel it. The [metadata][google.longrunning.Operation.metadata]
        field type is
        [RestoreDatabaseMetadata][google.spanner.admin.database.v1.RestoreDatabaseMetadata].
        The [response][google.longrunning.Operation.response] type is
        [Database][google.spanner.admin.database.v1.Database], if
        successful. Cancelling the returned operation will stop the
        restore and delete the database. There can be only one database
        being restored into an instance at a time. Once the restore
        operation completes, a new restore operation can be initiated,
        without waiting for the optimize operation associated with the
        first restore to complete.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_restore_database():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.RestoreDatabaseRequest(
                    backup="backup_value",
                    parent="parent_value",
                    database_id="database_id_value",
                )

                # Make the request
                operation = client.restore_database(request=request)

                print("Waiting for operation to complete...")

                response = operation.result()

                # Handle the response
                print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.RestoreDatabaseRequest, dict]):
                The request object. The request for
                [RestoreDatabase][google.spanner.admin.database.v1.DatabaseAdmin.RestoreDatabase].
            parent (str):
                Required. The name of the instance in which to create
                the restored database. This instance must be in the same
                project and have the same instance configuration as the
                instance containing the source backup. Values are of the
                form ``projects/<project>/instances/<instance>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            database_id (str):
                Required. The id of the database to create and restore
                to. This database must not already exist. The
                ``database_id`` appended to ``parent`` forms the full
                database name of the form
                ``projects/<project>/instances/<instance>/databases/<database_id>``.

                This corresponds to the ``database_id`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            backup (str):
                Name of the backup from which to restore. Values are of
                the form
                ``projects/<project>/instances/<instance>/backups/<backup>``.

                This corresponds to the ``backup`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.api_core.operation.Operation:
                An object representing a long-running operation.

                The result type for the operation will be
                :class:`google.cloud.spanner_admin_database_v1.types.Database`
                A Cloud Spanner database.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, database_id, backup])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a spanner_database_admin.RestoreDatabaseRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, spanner_database_admin.RestoreDatabaseRequest):
            request = spanner_database_admin.RestoreDatabaseRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent
            if database_id is not None:
                request.database_id = database_id
            if backup is not None:
                request.backup = backup

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.restore_database]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Wrap the response in an operation future.
        response = operation.from_gapic(
            response,
            self._transport.operations_client,
            spanner_database_admin.Database,
            metadata_type=spanner_database_admin.RestoreDatabaseMetadata,
        )

        # Done; return the response.
        return response

    def list_database_operations(
        self,
        request: Optional[
            Union[spanner_database_admin.ListDatabaseOperationsRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDatabaseOperationsPager:
        r"""Lists database
        [longrunning-operations][google.longrunning.Operation]. A
        database operation has a name of the form
        ``projects/<project>/instances/<instance>/databases/<database>/operations/<operation>``.
        The long-running operation
        [metadata][google.longrunning.Operation.metadata] field type
        ``metadata.type_url`` describes the type of the metadata.
        Operations returned include those that have
        completed/failed/canceled within the last 7 days, and pending
        operations.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_list_database_operations():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.ListDatabaseOperationsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_database_operations(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.ListDatabaseOperationsRequest, dict]):
                The request object. The request for
                [ListDatabaseOperations][google.spanner.admin.database.v1.DatabaseAdmin.ListDatabaseOperations].
            parent (str):
                Required. The instance of the database operations.
                Values are of the form
                ``projects/<project>/instances/<instance>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.spanner_admin_database_v1.services.database_admin.pagers.ListDatabaseOperationsPager:
                The response for
                   [ListDatabaseOperations][google.spanner.admin.database.v1.DatabaseAdmin.ListDatabaseOperations].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a spanner_database_admin.ListDatabaseOperationsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(
            request, spanner_database_admin.ListDatabaseOperationsRequest
        ):
            request = spanner_database_admin.ListDatabaseOperationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_database_operations]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDatabaseOperationsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_backup_operations(
        self,
        request: Optional[Union[backup.ListBackupOperationsRequest, dict]] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListBackupOperationsPager:
        r"""Lists the backup [long-running
        operations][google.longrunning.Operation] in the given instance.
        A backup operation has a name of the form
        ``projects/<project>/instances/<instance>/backups/<backup>/operations/<operation>``.
        The long-running operation
        [metadata][google.longrunning.Operation.metadata] field type
        ``metadata.type_url`` describes the type of the metadata.
        Operations returned include those that have
        completed/failed/canceled within the last 7 days, and pending
        operations. Operations returned are ordered by
        ``operation.metadata.value.progress.start_time`` in descending
        order starting from the most recently started operation.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_list_backup_operations():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.ListBackupOperationsRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_backup_operations(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.ListBackupOperationsRequest, dict]):
                The request object. The request for
                [ListBackupOperations][google.spanner.admin.database.v1.DatabaseAdmin.ListBackupOperations].
            parent (str):
                Required. The instance of the backup operations. Values
                are of the form
                ``projects/<project>/instances/<instance>``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.spanner_admin_database_v1.services.database_admin.pagers.ListBackupOperationsPager:
                The response for
                   [ListBackupOperations][google.spanner.admin.database.v1.DatabaseAdmin.ListBackupOperations].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a backup.ListBackupOperationsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, backup.ListBackupOperationsRequest):
            request = backup.ListBackupOperationsRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_backup_operations]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListBackupOperationsPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def list_database_roles(
        self,
        request: Optional[
            Union[spanner_database_admin.ListDatabaseRolesRequest, dict]
        ] = None,
        *,
        parent: Optional[str] = None,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDatabaseRolesPager:
        r"""Lists Cloud Spanner database roles.

        .. code-block:: python

            # This snippet has been automatically generated and should be regarded as a
            # code template only.
            # It will require modifications to work:
            # - It may require correct/in-range values for request initialization.
            # - It may require specifying regional endpoints when creating the service
            #   client as shown in:
            #   https://googleapis.dev/python/google-api-core/latest/client_options.html
            from google.cloud import spanner_admin_database_v1

            def sample_list_database_roles():
                # Create a client
                client = spanner_admin_database_v1.DatabaseAdminClient()

                # Initialize request argument(s)
                request = spanner_admin_database_v1.ListDatabaseRolesRequest(
                    parent="parent_value",
                )

                # Make the request
                page_result = client.list_database_roles(request=request)

                # Handle the response
                for response in page_result:
                    print(response)

        Args:
            request (Union[google.cloud.spanner_admin_database_v1.types.ListDatabaseRolesRequest, dict]):
                The request object. The request for
                [ListDatabaseRoles][google.spanner.admin.database.v1.DatabaseAdmin.ListDatabaseRoles].
            parent (str):
                Required. The database whose roles should be listed.
                Values are of the form
                ``projects/<project>/instances/<instance>/databases/<database>/databaseRoles``.

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.spanner_admin_database_v1.services.database_admin.pagers.ListDatabaseRolesPager:
                The response for
                [ListDatabaseRoles][google.spanner.admin.database.v1.DatabaseAdmin.ListDatabaseRoles].

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Quick check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a spanner_database_admin.ListDatabaseRolesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, spanner_database_admin.ListDatabaseRolesRequest):
            request = spanner_database_admin.ListDatabaseRolesRequest(request)
            # If we have keyword arguments corresponding to fields on the
            # request, apply these.
            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_database_roles]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDatabaseRolesPager(
            method=rpc,
            request=request,
            response=response,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def __enter__(self) -> "DatabaseAdminClient":
        return self

    def __exit__(self, type, value, traceback):
        """Releases underlying transport's resources.

        .. warning::
            ONLY use as a context manager if the transport is NOT shared
            with other clients! Exiting the with block will CLOSE the transport
            and may cause errors in other clients!
        """
        self.transport.close()

    def list_operations(
        self,
        request: Optional[operations_pb2.ListOperationsRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.ListOperationsResponse:
        r"""Lists operations that match the specified filter in the request.

        Args:
            request (:class:`~.operations_pb2.ListOperationsRequest`):
                The request object. Request message for
                `ListOperations` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.ListOperationsResponse:
                Response message for ``ListOperations`` method.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.ListOperationsRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.list_operations,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_operation(
        self,
        request: Optional[operations_pb2.GetOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> operations_pb2.Operation:
        r"""Gets the latest state of a long-running operation.

        Args:
            request (:class:`~.operations_pb2.GetOperationRequest`):
                The request object. Request message for
                `GetOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            ~.operations_pb2.Operation:
                An ``Operation`` object.
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.GetOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.get_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_operation(
        self,
        request: Optional[operations_pb2.DeleteOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a long-running operation.

        This method indicates that the client is no longer interested
        in the operation result. It does not cancel the operation.
        If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.DeleteOperationRequest`):
                The request object. Request message for
                `DeleteOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.DeleteOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.delete_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )

    def cancel_operation(
        self,
        request: Optional[operations_pb2.CancelOperationRequest] = None,
        *,
        retry: OptionalRetry = gapic_v1.method.DEFAULT,
        timeout: Union[float, object] = gapic_v1.method.DEFAULT,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running operation.

        The server makes a best effort to cancel the operation, but success
        is not guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.

        Args:
            request (:class:`~.operations_pb2.CancelOperationRequest`):
                The request object. Request message for
                `CancelOperation` method.
            retry (google.api_core.retry.Retry): Designation of what errors,
                    if any, should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        Returns:
            None
        """
        # Create or coerce a protobuf request object.
        # The request isn't a proto-plus wrapped type,
        # so it must be constructed via keyword expansion.
        if isinstance(request, dict):
            request = operations_pb2.CancelOperationRequest(**request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method.wrap_method(
            self._transport.cancel_operation,
            default_timeout=None,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request,
            retry=retry,
            timeout=timeout,
            metadata=metadata,
        )


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=package_version.__version__
)


__all__ = ("DatabaseAdminClient",)
