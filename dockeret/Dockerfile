FROM python:2.7-alpine

WORKDIR /install/

ADD setup.py /install/
ADD mailsort /install/mailsort
RUN python /install/setup.py install; rm -rf /install

WORKDIR /root/

RUN mkdir -p /root/.config/mailsort; ln -s /root/.config/mailsort/twiddle/machine/translucidus/_config/mailsort/filters /root/.config/mailsort/filters

COPY dockeret/cli.sh .

COPY dockeret/launcher.sh /
LABEL "com.github.sourcesimian.dockeret.launcher"="/launcher.sh"
