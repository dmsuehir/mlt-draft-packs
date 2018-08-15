# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: EPL-2.0
#

FROM python:3.6

ENV CONDA_DIR /opt/anaconda3
RUN mkdir -p $CONDA_DIR

# Download and Install Miniconda
ARG CONDA_VERSION="3-4.5.4"
RUN \
    wget -q --no-check-certificate https://repo.continuum.io/miniconda/Miniconda${CONDA_VERSION}-Linux-x86_64.sh -P $CONDA_DIR && \
    bash $CONDA_DIR/Miniconda${CONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm -rf $CONDA_DIR/Miniconda${CONDA_VERSION}*x86_64.sh

#Add conda binaries to path
ENV PATH $CONDA_DIR/bin:$PATH

ARG TF_VERSION="1.8.0"
RUN conda install -c anaconda tensorflow==$TF_VERSION && \
    conda install pip && \
    conda clean --all

ADD requirements.txt /src/deps/requirements.txt
RUN pip install -r /src/deps/requirements.txt

WORKDIR /src/app
ADD . /src/app

RUN pycodestyle -v .

# debug wrapper, followed by the model training script to execute
ENTRYPOINT [ "python", "kubernetes_debug_wrapper.py", "main.py" ]
