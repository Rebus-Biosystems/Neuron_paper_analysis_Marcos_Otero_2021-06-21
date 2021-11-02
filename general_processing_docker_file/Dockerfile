# Create the miniconda environment
FROM continuumio/miniconda3:latest

# Add some metadata to the image        
LABEL maintainer="simone.codeluppi@gmail.com"
LABEL version='1.0'
LABEL description=" This image is used to set up my standard developing \
        and prototyping environment"


COPY general-env-requirements.txt ./requirements.txt
COPY start_commands.sh ./start_commands.sh

# In alpine linux apk is the equivalent of apk
# RUN apk update && \
#     apk upgrade -U && \ 
#     apk add --no-cache libc-dev gcc
    
# Update conda and anaconda and create working env
RUN /bin/bash -c "yes | conda update -n base conda && \
                conda create --name general-env python=3.6 pip gcc_linux-64 gxx_linux-64"


#RUN  ["/bin/bash", "-c", "yes | conda update -n base conda"]

# Create the working environment
#RUN ["/bin/bash", "-c", "yes | conda create --name general-env python=3 pip"]

# # Activate the commands for conda init
# RUN ["/bin/bash", "conda init bash"]
# RUN ["/bin/bash", "source ~/.bashrc"]

# Activate the processing enviroment and install some packages
# RUN ["/bin/bash", "conda activate general-env"]
# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "general-env", "/bin/bash", "-c"]
#RUN /bin/bash -c "source activate general-env"


RUN /bin/bash -c "pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m ipykernel install --user --name general-env --display-name 'general-env'"

EXPOSE 8080

CMD sh start_commands.sh




# ENTRYPOINT ["jupyter", "lab --port=8080 --ip=0.0.0.0 --no-browser --allow-root"]



# # Source the changes in the bashrc
# RUN ["/bin/bash","source ~/.bashrc"]

