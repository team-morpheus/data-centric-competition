FROM continuumio/miniconda3:4.10.3

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install useful commands
RUN apt-get update && apt-get install -y \
      software-properties-common \
      cmake \
      git \
      curl wget \
      ca-certificates \
      nano vim \
      openssh-server

COPY environment.yml /tmp/environment.yml
ENV PATH /opt/conda/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false

# Install dc_comp environment
RUN conda env create -f /tmp/environment.yml && conda clean -ya

# Init conda environment
ENV CONDA_DEFAULT_ENV=dc_comp
ENV CONDA_PREFIX=/opt/conda/envs/$CONDA_DEFAULT_ENV
ENV PATH $CONDA_PREFIX/bin:$PATH
# Other configs
# jupytertheme config to dark mode - Optional, seems to mess up some UI elements in 8.8.20
#RUN $CONDA_PREFIX/bin/jt -t onedork -fs 95 -altp -tfs 11 -nfs 115 -lineh 140 -cellw 1200 -T

# Install requirements for noxfile.py
COPY .github/workflows/constraints.txt /tmp
RUN $CONDA_PREFIX/bin/pip install --constraint=/tmp/constraints.txt nox toml

# copy source code
COPY ../.. /code
WORKDIR /code

# Start running
USER root

CMD ["/bin/bash"]
