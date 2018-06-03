FROM continuumio/miniconda3

COPY . /app
WORKDIR /app
RUN conda update -n base conda
RUN conda config --add channels conda-forge
RUN conda install -y plotly flask dash dash-core-components dash-html-components dash-renderer
RUN conda install numpy hdf5 pandas pytables
RUN pip install flask-caching redis

#ENTRYPOINT ["python"]
#CMD ["run.py"]