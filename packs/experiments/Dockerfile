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

ADD requirements.txt /src/deps/requirements.txt
RUN pip install -r /src/deps/requirements.txt

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.9.0/bin/linux/amd64/kubectl
RUN mv ./kubectl /usr/local/bin/kubectl && chmod +x /usr/local/bin/kubectl

# Get the experiments version file
ADD EXPERIMENTS_VERSION.txt /src/deps/EXPERIMENTS_VERSION.txt

# Clone the experiments repo, and grab the specified git version
WORKDIR /src/app
RUN git clone https://github.com/IntelAI/experiments.git
WORKDIR /src/app/experiments
RUN git pull
RUN EXPERIMENTS_VERISON=$(cat /src/deps/EXPERIMENTS_VERSION.txt) && git checkout $EXPERIMENTS_VERISON

ADD . /src/app/experiments

RUN pycodestyle -v .

CMD ["python3"]
