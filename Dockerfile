FROM ubuntu:22.04
COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8
ENV JAVA_HOME /usr/local/openjdk-8
RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

# Install dependencies and needed executables
RUN  apt-get update && apt-get install -y --no-install-recommends \ 
    software-properties-common gpg gpg-agent git wget unzip \
    build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev \
    libsqlite3-dev libreadline-dev libffi-dev \ 
    libbz2-dev libarchive13 libcurl4-openssl-dev \
    # install python3.7
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install -y python3.7  \
    # install srcml and stanford tagger
    && wget --progress=dot:giga http://131.123.42.38/lmcrs/v1.0.0/srcml_1.0.0-1_ubuntu20.04.deb \
    && wget --progress=dot:giga https://nlp.stanford.edu/software/stanford-tagger-4.2.0.zip \
    && unzip stanford-tagger-4.2.0.zip -d stanford \
    && rm stanford-tagger-4.2.0.zip \
    # install libssl1.1 for srcml
    && wget --progress=dot:giga http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb \
    && dpkg -i ./libssl1.1_1.1.1f-1ubuntu2_amd64.deb \
    && apt update \
    && apt-get install -y --no-install-recommends libssl1.1 \
    && dpkg -i ./srcml_1.0.0-1_ubuntu20.04.deb \
    && apt install -f --no-install-recommends  \
    && rm srcml_1.0.0-1_ubuntu20.04.deb \
    # install pip
    && apt-get install -y python3-pip \
    && pip install --upgrade pip \
    && mkdir /app \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# copy source files into container
COPY src /app/src/
COPY requirements.txt /app/requirements.txt

WORKDIR /app

# 
RUN pip --no-cache-dir install -r  requirements.txt \
    && echo "import nltk" > download_nltk.py \
    && echo "nltk.download('wordnet')" >> download_nltk.py \
    && echo "nltk.download('punkt')" >> download_nltk.py \
    && echo "nltk.download('stopwords')" >> download_nltk.py \
    && echo "quit()" >> download_nltk.py \
    && python3 download_nltk.py \ 
    && rm download_nltk.py

COPY ./test /app/test/
COPY pytest.ini /app/pytest.ini
WORKDIR /app/

CMD ["pytest"]

