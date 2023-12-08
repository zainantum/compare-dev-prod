import os, glob, difflib, filecmp, argparse, sys, shutil, random
from pathlib import Path
from datetime import date

# development dir
source_dir = "/var/www/html/svn/web-accounting-trial"
# destination dir
dest_dir = "/var/www/html/svn/web-accounting-prod"

# target dir we want to compare between source_dir and dest_dir
target_dir = ["application", "assets"]
# don't compare this folder
exclude_dir = ["cache", "core", "helpers", "hooks", "language", "logs", "session", "third_party", "files", "font", "help", "img", "logs", "patch", "plugins", "report_schema"]

exclude_paths = ["browse", "custom"]

# specified file
sp_file = ["Syspage.php", "routes.php", "jmlib.js"]

global dir_today
dir_today = "diff/"+str(date.today())

def comparefile(source, dest, og):
    og = og.split('.')
    file_name = og[0]
    file_ext = og[1]
    f1_data = open(source, "r").readlines()
    f2_data = open(dest, "r").readlines()
    # create html diff 
    html_diff = difflib.HtmlDiff(wrapcolumn=65).make_file(f1_data, f2_data)
    # save html diff to dir and create symlink between source file and destination file
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
    # delete dir before compare
    if os.path.exists(dir_today):
        shutil.rmtree(dir_today)
        
    for main_dir in target_dir:
        # get all dir in target directory
        list_all_file = [d for f in os.scandir(source_dir+"/"+main_dir) if f.is_dir() and not f.name in exclude_dir for d in glob.glob(source_dir + '/'+main_dir+'/'+f.name+'/**/**/**', recursive = True) if os.path.isfile(d)]
        for source_path in set(list_all_file):
            head, tail = os.path.split(source_path)
            if len(sp_file) > 0 and not tail in sp_file:
                continue
                
            dest_path = source_path.replace(source_dir, dest_dir)
            get_exclude_path = os.path.split(os.path.dirname(source_path))
            if(get_exclude_path[1] not in exclude_paths):
                if os.path.exists(dest_path):
                    # compare between 2 source
                    res = filecmp.cmp(source_path, dest_path)
                    if res == False:
                        comparefile(source_path, dest_path, tail)
                else:
                    print("File not found in local production: "+dest_path)


main()