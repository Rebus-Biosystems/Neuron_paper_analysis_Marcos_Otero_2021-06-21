# Analysis_Marcos_Otero_2021-06-21
Starting from segmented Nuclei and IF marker images the goal is to measure the fluorescence intensity in the total IF+ region, in the IF+/Nuclei+ region and in the IF+/Nuclei- region. The segmented nuclei and IF images come from different rounds of imaging.

Marcos provided a testing dataset located at [Data](https://netorg4154883-my.sharepoint.com/:f:/g/personal/motero_rebusbio_com/EmZGXtpqt_pNv74XcoKlTL8BKlVtAPLjvQSVPYq_dLYf8w?e=vUNkWA)


# Instruction

1) Build the docker image 
2) Run the docker image 
    - map container port 8080 to local 8081
    - Select the volume host path and map to `/data` in the container path
3) Go to the browser and enter `localhost:8081`to access the jupyter lab 


