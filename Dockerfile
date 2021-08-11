FROM python:3.9-alpine

WORKDIR /action_workspace

COPY requirements/run.txt /action_workspace/run.txt

ENV TERM "xterm-256color"
RUN pip install -r /action_workspace/run.txt

COPY . /action_workspace
ENV PYTHONPATH /action_workspace

ENTRYPOINT ["python", "-m", "action"]

