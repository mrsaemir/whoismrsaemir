FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBEFFERED 1

WORKDIR /whois
COPY . /whois


EXPOSE 8000

RUN apt update && apt install -y curl cron python3-pip

RUN pip3 install -r whoismrsaemir/requirements.txt

RUN chmod +x ./whoismrsaemir/entrypoint.sh

CMD ["./whoismrsaemir/entrypoint.sh"]
