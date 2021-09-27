FROM python:3.8

ADD main.py /
ADD functions.py /
ADD pharmacies_data.json /
ADD pharmacies_manager.py /
ADD pharmacy.py /
ADD README.md /

RUN pip install bs4 colorama cloudscraper tqdm

CMD [ "python", "./main.py"]
