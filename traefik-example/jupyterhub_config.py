# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os

c = get_config()  # noqa

# We rely on environment variables to configure JupyterHub so that we
# avoid having to rebuild the JupyterHub container every time we change a
# configuration parameter.

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# Spawn containers from this image
c.DockerSpawner.image = os.environ["DOCKER_NOTEBOOK_IMAGE"]

# The public facing URL of the whole JupyterHub application.
# Set this to a name you have registered in DNS to point to the traefik server.
#
#          This is the address on which the traefik proxy will bind.
#          Sets protocol, ip, base_url
#  Default: 'http://:8000'
# (dev note) This will be copied to c.Proxy.public_url
#
# Set this to https in production!
c.JupyterHub.bind_url = "http://hub.localhost"

# Whether to clean up the jupyterhub-managed traefik configuration
# when the Hub shuts down.
c.JupyterHub.cleanup_proxy = True
c.JupyterHub.cleanup_servers = True

# The internal URL on which the Hub will listen.
#
# jupyterhub_traefik_proxy will configure the 'service' url in traefik, so this
# needs to be accessible from traefik. By default, jupyterhub will bind to
# 'localhost', but this will bind jupyterhub to its container name
c.JupyterHub.hub_bind_url = "http://hub:8000"

# This sets traefik's router rule for routing traffic to the jupyterhub
# instance. It can be a host, a path, or a host with path prefix.
#
# Typically, you'll want a traefik Host-based configuration rule, e.g.:-
#   traefik.http.routers.jupyterhub.rule=Host(`hub.example.com`)
#
# The corresponding `hub_routespec` for the above would be:-
#   c.JupyterHub.hub_routespec = 'hub.example.com'
#
# The default is to bind to everything, creating a path-based rule. i.e.
#   traefik.http.routers.jupyterhub.rule=PathPrefix(`/`)
#
# Default: = '/'
#
c.JupyterHub.hub_routespec = "hub.localhost"

# jupyterhub will only configure path-based routing by default. To stop
# traefik from routing all requests to jupyterhub, a subdomain host should be
# configured.
# That is, by default, jupyterhub will create a router rule of just PathPrefix(`/`).
# This could conflict with other traefik router rules, or just be too easily
# accessible.
#
# If a subdomain_host is configured, each user container will be accessible at:-
#   https://<user>.<subdomain_host>
#
# So a wildcard DNS entry should be configured for subdomains of the subdomain host.
#
# e.g. A user of "jbloggs", logging into a hub with a subdomain_host of
# "https://hub.example.com", will be redirected to their notebook at
# https://jbloggs.hub.example.com
#
# Set this to https in production!
c.JupyterHub.subdomain_host = "http://hub.localhost"

# Set the log level by value or name.
#  Choices: any of [0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']
#  Default: 30
#  See also: Application.log_level
c.JupyterHub.log_level = "DEBUG"

# Use jupyterhub_traefik_proxy's `TraefikFileProviderProxy` class
c.JupyterHub.proxy_class = "traefik_file"

# JupyterHub shouldn't start traefik, docker-compose will launch it
c.TraefikFileProviderProxy.should_start = False

# The configuration file jupyterhub will write to, and traefik will watch
c.TraefikFileProviderProxy.dynamic_config_file = "/var/run/traefik/jupyterhub.yaml"

# Don't try and configure traefik's API and dashboard router (already configured)
#c.TraefikFileProviderProxy.enable_setup_dynamic_config = False

# Settings jupyterhub_traefik_proxy will use to access the traefik API
# These must match traefik's dynamic configuration (check the labels in
# docker-compose.yaml).
#
# Currently, as of version 1.0.1, jupyterhub-traefik-proxy must manage the
# traefik API router and endpoint.
#
# [PR #210](https://github.com/jupyterhub/traefik-proxy/pull/210) addresses this,
# allowing pre-configured traefik API endpoints.
c.TraefikFileProviderProxy.traefik_api_url = "http://traefik:8080"
c.TraefikFileProviderProxy.traefik_api_validate_cert = False
c.TraefikFileProviderProxy.traefik_api_username = "admin"
c.TraefikFileProviderProxy.traefik_api_password = "password"
# The entry point must exist in the static configuration file (traefik.yaml),
# and correspond to the traefik_api_url, above.
# Default: auth_api
#c.TraefikFileProviderProxy.traefik_api_entrypoint = "websecure"

# Match the entrypoint to that listed in traefik.yaml.
# Use http for testing purposes only
#
# Default: "https"
c.TraefikFileProviderProxy.traefik_entrypoint = "web"

# Traefik can automatically retrieve certificates for each user container from
# an ACME provider (e.g. Let's Encrypt), For an example, read the comments in
# traefik's static configuraiton file, traefik.yaml, and refer to the
# reference documentation at:-
#   https://doc.traefik.io/traefik/https/acme/
# c.TraefikFileProviderProxy.traefik_cert_resolver = "leresolver"

# The class to use for spawning single-user servers.
#
# Launch each user's notebook server in a separate container.
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# Remove containers once they are stopped
c.DockerSpawner.remove = True

# The docker network name that single-user notebook containers should attach to
c.DockerSpawner.network_name = "traefik_internal"

# For jupyterhub to let traefik manage certificates, 'ssl_cert' needs a
# value. (This gets around a validate rule on 'proxy.bind_url', which
# forces redirects to 'http', unless there is a value in ssl_cert).
# Otherwise, when logging in, there will always be 302 redirects to http://
# c.JupyterHub.ssl_cert = "externally managed"

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/srv/jupyterhub/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////srv/jupyterhub/jupyterhub.sqlite"

# Allow cross-site requests. Set to False in production (the default).
#c.NotebookApp.disable_check_xsrf = True

# Authenticate users with Native Authenticator
c.JupyterHub.authenticator_class = "nativeauthenticator.NativeAuthenticator"

# Allow anyone to sign-up without approval
# Probably want to turn this off in production
c.NativeAuthenticator.open_signup = True

# Allowed admins
admin = os.environ.get("JUPYTERHUB_ADMIN")
if admin:
    c.Authenticator.admin_users = [admin]
