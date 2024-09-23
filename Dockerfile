FROM python
WORKDIR /test_project/
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir "logs"
ENV ENV=dev
CMD python -m pytest -s --alluredir=test_results/ /tests_project/tests/