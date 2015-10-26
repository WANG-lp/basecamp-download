# basecamp-download
This script downloads all the files  from basecamphq(classical version)


##BEFORE RUN IT

Before you use this script, you should modify it properly.

Here is the things you should fill into this script:

* line 11:        'authorization'
* line 12:        'User-Agent'
* line 54:        'url'
* line 85,86:     your projects' id and name
* line 89:        the directory you want to store your files
* 

##RUN IT

for example:

```>./python download.py 0 3```

will download your projects of the index 0,1,2 in project_id array in your script.

you can use this script to download many projects on the same time by setting different range of your projects_id 

at last, you can run many times of this script to check if you download all files completely. 


