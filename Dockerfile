FROM python:3.12-bookworm
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /etc/local/app

COPY . ./

RUN pip install -r requirements.txt

RUN pip install uvicorn

CMD ["uvicorn", "app:app"]