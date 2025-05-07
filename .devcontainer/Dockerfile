FROM mcr.microsoft.com/devcontainers/base:jammy

USER vscode

RUN curl -sSf https://rye.astral.sh/get | RYE_INSTALL_OPTION="--yes" bash \
	&& echo 'source "$HOME/.rye/env"' >> ~/.bashrc

# ENV FLASK_APP=server.py
# ENV FLASK_RUN_HOST=0.0.0.0

# CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]

# ENV PATH="$HOME/.rye/bin:$PATH"

ENV FLASK_APP=server.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["rye", "run", "python", "main.py"]
# CMD ["bash", "-c", "source $HOME/.rye/env && rye run python server.py"]