FROM python:3.10.6-buster



# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY data /data
COPY api /api
COPY models/final_model.py /models/final_model.py
COPY models/base_model_fulldata_2.h5 /models/base_model_fulldata_2.h5
COPY main.py /main.py
#COPY samsung_ecg.pdf /samsung_ecg.pdf
#RUN pip install .

#COPY Makefile /Makefile
#RUN make reset_local_files

CMD uvicorn api.fast:app --host 0.0.0.0
#--port $PORT
