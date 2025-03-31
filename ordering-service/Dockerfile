FROM python

WORKDIR /ordering-app
COPY requirements.txt /ordering-app
RUN pip install -r requirements.txt
COPY . /ordering-app
ENV PYTHONPATH=/ordering-app
CMD ["python", "-m", "src.main"]
