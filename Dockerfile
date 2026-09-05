FROM python:latest
LABEL Maintainer="m-ue-d"

WORDKIR /bot/src

COPY bot.py .

CMD ["python", "bot.py"]
