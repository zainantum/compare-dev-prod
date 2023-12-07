import os, glob, difflib, filecmp, argparse, sys, shutil, random
from pathlib import Path
from datetime import date

source_dir = "/var/www/html/svn/web-accounting-trial"
dest_dir = "/var/www/html/svn/web-accounting-prod"

target_dir = ["application", "assets"]
exclude_dir = ["cache", "core", "helpers", "hooks", "language", "logs", "session", "third_party", "files", "font", "help", "img", "logs", "patch", "plugins", "report_schema"]

exclude_paths = ["browse", "custom"]

global dir_today
dir_today = "diff/"+str(date.today())

def comparefile(source, dest, og):
    og = og.split('.')
    file_name = og[0]
    file_ext = og[1]
    f1_data = open(source, "r").readlines()
    f2_data = open(dest, "r").readlines()
    html_diff = difflib.HtmlDiff(wrapcolumn=65).make_file(f1_data, f2_data)
    if not os.path.exists(dir_today):
        os.mkdir(dir_today)
        
    if not os.path.exists(dir_today+"/"+file_name):
        os.mkdir(dir_today+"/"+file_name)
    else:
        file_name = file_name + str(random.randint(1000, 9999))
        os.mkdir(dir_today+"/"+file_name)
        
    Path('diff/'+str(date.today())+"/"+file_name+"/"+file_name+'.html').write_text(html_diff)
    os.symlink(source, dir_today+"/"+file_name+"/src_"+file_name+'.'+file_ext) 
    os.symlink(dest, dir_today+"/"+file_name+"/dest_"+file_name+'.'+file_ext) 
    

def main():
    if os.path.exists(dir_today):
        shutil.rmtree(dir_today)
        
    for main_dir in target_dir:
        list_all_file = [d for f in os.scandir(source_dir+"/"+main_dir) if f.is_dir() and not f.name in exclude_dir for d in glob.glob(source_dir + '/'+main_dir+'/'+f.name+'/**/**/**', recursive = True) if os.path.isfile(d)]
        for source_path in set(list_all_file):
            dest_path = source_path.replace(source_dir, dest_dir)
            get_exclude_path = os.path.split(os.path.dirname(source_path))
            if(get_exclude_path[1] not in exclude_paths):
                if os.path.exists(dest_path):
                    res = filecmp.cmp(source_path, dest_path)
                    if res == False:
                        head, tail = os.path.split(source_path)
                        comparefile(source_path, dest_path, tail)
                else:
                    print("File not found in local production: "+dest_path)


main()