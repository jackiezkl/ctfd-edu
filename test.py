import os
from secrets import token_hex
from shutil import copytree
from multiprocessing import cpu_count

def already_replaced(path_to_file,string_to_check):
  with open(path_to_file) as file:
    if string_to_check in file.read():
      return True
    else:
      return False




if __name__=="__main__":
#   change parent path of CTFd after clone
  current_path=os.getcwd()
  parent_path = os.path.dirname(current_path)+"/"

  relative_path = "CTFd/CTFd/themes/core/templates/base.html"
  dst_path = os.path.join(parent_path, relative_path)

  if already_replaced(dst_path,'\t<meta name="starts_in" content="{{ ctf_starts_in() }}">\n\t<meta name="ends_in" content="{{ ctf_ends_in() }}">\n') == True:
    print("Yes")

