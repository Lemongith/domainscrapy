FROM python:3
RUN pip install pystrich && pip install requests && pip install bs4 && pip install pytz
CMD [ "python", "./code.py" ]
