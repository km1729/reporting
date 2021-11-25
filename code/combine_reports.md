File name: combine_reports.py

# Background 


# Issues  


# Flow-chart 

``` mermaid
graph TD
A[start] -->|scan dir| B(read file name)
B --> C{if 'Project' in the file name}
C -->|yes| D[open & readlines the file name]
C -->|no| J[END]
D --> |get data:project names, usage per use|E{if 'project' in the file}
E --> |yes| F(copy the line)
F --> G(change the format)
G --> H(get date from the file name)
H --> I(Save data into the total usage file )
E --> |no| J[END]


```




