# pp_cmd_pddf
Postprocessing command "pddf"
## Description
Commands invoke any pandas dataframe [functions](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) (except `eval`)


### Arguments
- function - positional argument, text, required, pandas function name.
- columns - positional infinite argument, text, not required. The names of the columns to be passed to the function. If not specified, the whole dataframe is used
- kwargs - infinite keyword arguments, any type, not required. Any keyword arguments to be passed to the function.
- subsearch_to_positional_list - keyword argument, not required, boolean. Makes all subsearches to a list and pass it to the function as first argument.
- subsearch_key - keyword argument, boolean, not required. If the pandas function accepts a dataframe as a keyword argument, it points to the name of the argument
- subsearches - subsearch, infinite argument. Pass subsearch dataframe as first argument to pandas function.

### Usage example
Using pandas `compare` function with subsearch:  
```
query: readFile a.csv 
   a   b   c
0  1   2   3
1  4   5   6
```
```
query: readFile b.csv
   a   b   c
0  1   2   3
1  4   5   7
```
```
readFile a.csv | pddf compare [readFile b.csv]
     c      
  self other
1  6.0   7.0
```
Using pandas `query` function:  
```
query: readFile a.csv  | pddf query, expr="a==1"
```
```
   a   b   c
0  1   2   3
```
Using `round` function:  
```
query: readFile d.csv 
         date         A          B           C           D
0  2013-01-01  1.075770  -0.109050    1.643563   -1.469388
1  2013-01-02  0.357021  -0.674600   -1.776904   -0.968914
2  2013-01-03 -1.294524   0.413738    0.276662   -0.472035
3  2013-01-04 -0.013960  -0.362543   -0.006154   -0.923061
4  2013-01-05  0.895717   0.805244   -1.206412    2.565646
```
```
readFile d.csv | pddf round, decimals=3
         date     A          B           C           D
0  2013-01-01  1.08      -0.11        1.64       -1.47
1  2013-01-02  0.36      -0.67       -1.78       -0.97
2  2013-01-03 -1.29       0.41        0.28       -0.47
3  2013-01-04 -0.01      -0.36       -0.01       -0.92
4  2013-01-05  0.90       0.81       -1.21        2.57

```
Use only selected columns:  
```
readFile d.csv | pddf round,A,B decimals=2
```
```
      A     B
0  1.08 -0.11
1  0.36 -0.67
2 -1.29  0.41
3 -0.01 -0.36
4  0.90  0.81

```

## Getting started
### Installing
1. Create virtual environment with post-processing sdk 
```bash
    make dev
```
That command  
- downloads [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- creates python virtual environment with [postprocessing_sdk](https://github.com/ISGNeuroTeam/postprocessing_sdk)
- creates link to current command in postprocessing `pp_cmd` directory 

2. Configure `otl_v1` command. Example:  
```bash
    vi ./venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/otl_v1/config.ini
```
Config example:  
```ini
[spark]
base_address = http://localhost
username = admin
password = 12345678

[caching]
# 24 hours in seconds
login_cache_ttl = 86400
# Command syntax defaults
default_request_cache_ttl = 100
default_job_timeout = 100
```

3. Configure storages for `readFile` and `writeFile` commands:  
```bash
   vi ./venv/lib/python3.9/site-packages/postprocessing_sdk/pp_cmd/readFile/config.ini
   
```
Config example:  
```ini
[storages]
lookups = /opt/otp/lookups
pp_shared = /opt/otp/shared_storage/persistent
```

### Run pddf
Use `pp` to run pddf command:  
```bash
pp
Storage directory is /tmp/pp_cmd_test/storage
Commmands directory is /tmp/pp_cmd_test/pp_cmd
query: | otl_v1 <# makeresults count=100 #> |  pddf 
```
## Deploy
Unpack archive `pp_cmd_pddf` to postprocessing commands directory