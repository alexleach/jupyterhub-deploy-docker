FROM jupyterhub/jupyterhub

# Add DockerSpawner and OAuthenticator classes to JupyterHub
# hadolint ignore=DL3008,DL3013
RUN apt-get update && \
    apt-get install -y git --no-install-recommends && \
    python3 -m pip install -U --no-cache-dir \
        dockerspawner \
        oauthenticator \
        git+https://github.com/jupyterhub/traefik-proxy.git && \
    apt-get remove -y git && \
    rm -rf /var/lib/apt/lists

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
WORKDIR /srv/jupyterhub
