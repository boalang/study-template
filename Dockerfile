FROM python:3.10-slim-bullseye

RUN set -e \
#
# update repos and install dependencies
#
&& apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --yes \
    make=4.3-4.1 \
#
# clean-up
#
&& rm --recursive --force \
    /usr/share/doc/* \
    /usr/share/man/* \
    /var/cache/apt/*.bin \
    /var/cache/apt/archives/*.deb \
    /var/cache/apt/archives/partial/*.deb \
    /var/cache/debconf/*.old \
    /var/lib/apt/lists/* \
    /var/lib/dpkg/info/* \
    /var/log/*.log \
    /var/log/apt

#
# install Python modules
#
COPY requirements.txt /
RUN pip3 install -r /requirements.txt ; rm -f /requirements.txt ; mkdir /study
WORKDIR /study

CMD ["/bin/bash"]
