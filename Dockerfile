FROM vionel-aux

RUN pip install numpy
RUN apt-get install -y python-scipy

COPY . /source_code

WORKDIR /source_code
CMD python mfcc_similarity.py
