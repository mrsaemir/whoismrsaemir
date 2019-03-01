FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBEFFERED 1

WORKDIR /whois
COPY . /whois


EXPOSE 8000

RUN pip install -r whoismrsaemir/requirements.txt

RUN chmod +x ./whoismrsaemir/entrypoint.sh

CMD ["./whoismrsaemir/entrypoint.sh"]
