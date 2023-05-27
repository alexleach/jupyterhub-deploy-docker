# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
ARG JUPYTERHUB_VERSION
FROM jupyterhub/jupyterhub:$JUPYTERHUB_VERSION

# Add DockerSpawner and OAuthenticator classes to JupyterHub
# hadolint ignore=DL3008,DL3013
RUN apt-get update && \
    apt-get install -y git --no-install-recommends && \
    python3 -m pip install -U --no-cache-dir \
        dockerspawner \
        jupyterhub-nativeauthenticator \
        git+https://github.com/jupyterhub/traefik-proxy.git && \
    apt-get remove -y git && \
    rm -rf /var/lib/apt/lists

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
WORKDIR /srv/jupyterhub
