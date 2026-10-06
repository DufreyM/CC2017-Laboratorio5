FROM continuumio/miniconda3:latest

WORKDIR /workspace

COPY environment.yml .

RUN conda env create -f environment.yml && conda clean -afy

SHELL ["conda", "run", "--no-capture-output", "-n", "lab5", "/bin/bash", "-c"]

RUN python -m ipykernel install --user --name=lab5 --display-name "Python (Lab5)"

EXPOSE 8888

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "lab5"]
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=", "--NotebookApp.password="]
