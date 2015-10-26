__author__ = 'will'
import requests
import xml.etree.cElementTree as ET
import os, sys, time
from urllib import unquote

#you can use postman to generate this part :)
headers = {
    'content-type': "application/xml",
    'accept': "application/xml",
    'authorization': "Basic your_basic_auth_code_should_be_here",
    'user-agent': "your name,email, basecamp server checks this field, if not set up properly, you will be limited to send the request very slowly",
    'cache-control': "no-cache",
}

err_list = []
succ_list = []


#fetch the file, store it to the path dir
def download_files(urls, path):
    url = urls['url']
    size = urls['size']
    fid = urls['id']

    filename = fid + '_' + unquote(url).split('/')[-1]

    if os.path.exists(path + '/' + filename):
        if os.path.getsize(path + '/' + filename) == size:
            succ_list.append(url)
            return

    print "Downloading... :" + filename + "\tsize: " + str(size/1024.0) + "KB"
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200:
        time.sleep(3)
        response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        time.sleep(3)
        response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        print "ERROR", url
        err_list.append(url)
        return

    with open(path + "/" + filename, "wb+") as f:
        f.write(response.content)
    succ_list.append(url)

#fetch all the files' url of your project
def download_urls(project, count=0):
    url = "https://your_domain_should_be_here.basecamphq.com/projects/%s/attachments?n=%s" % (project, count)
    response = requests.request("GET", url, headers=headers)

    while response.status_code != 200:
        time.sleep(3)
        response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        print "ERROR:", project
        return '', []
    # print(response.text)
    print response.status_code

    tree = ET.fromstring(response.text)

    files = []

    attas = tree.findall('attachment')

    for att in attas:
        f = {}
        f['size'] = int(att.find('byte-size').text)
        f['id'] = att.find('id').text
        f['url'] = att.find('download-url').text

        files.append(f)

    return response.text, files


#your project_id and name, this program save them in separate folders
projects_id = ['0000001', '180201']
projects_name = ['project_name1', 'This is example']

#save files to this directory
BASE_DIR = '/Volumes/WILL-U-DISK/'

if len(sys.argv) < 3:
    raise RuntimeError("args error!")

start = int(sys.argv[1])
end = int(sys.argv[2])
if len(projects_name) < end:
    end = len(projects_name)

print "[%d, %d)" % (start, end)
for i in range(start ,end):

    path = BASE_DIR + projects_name[i]
    if not os.path.isdir(path):
        os.mkdir(path)
    finished = False
    count = 0
    err_list = []
    succ_list = []
    while (not finished):
        response_t, urls = download_urls(projects_id[i], count)
        count += len(urls)
        time.sleep(1)
        if len(urls) == 0:
            finished = True
            break
        with open(BASE_DIR + projects_name[i] + '_' + str(count) + '.xml', 'wb+') as f:
            f.write(response_t)
        for u in urls:
            download_files(u, path)
    with open(path + '/' + "a_succ.txt", "wb+") as f:
        f.write("Successful Download file count: " + str(len(succ_list)) + "\n")
        for succ in succ_list:
            f.write(succ + "\n")
    with open(path + '/' + "a_failed.txt", "wb+") as f:
        f.write("Failed Download file count: " + str(len(err_list)) + "\n")
        for err in err_list:
            f.write(err + "\n")
