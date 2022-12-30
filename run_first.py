import shutil,os

def patch_base_html(parent_path):
  relative_path = "CTFd/CTFd/themes/core/templates/base.html"
  dst_path = os.path.join(parent_path, relative_path)

  with open(dst_path, 'r+') as f: 
    lines = f.readlines()
    try:
      for i, line in enumerate(lines):
        if line.startswith('\t<meta name="viewport"'):
          lines[i] = lines[i] + '\t<meta name="starts_in" content="{{ ctf_starts_in() }}">\n\t<meta name="ends_in" content="{{ ctf_ends_in() }}">\n'
      f.seek(0)
      for line in lines:
        f.write(line)
      f.close()
    except Exception:
      print("[+] Couldn't find the *viewport* to replace with.")
      f.close()

  with open(dst_path, 'r') as base_file:
    search_text = '<a href="https://ctfd.io" class="text-secondary">\n\t\t\t\t<small class="text-muted">Powered by CTFd</small>\n\t\t\t</a>\n'
    replace_text = '<script>const d=new Date();let year=d.getFullYear();document.write("CTF - "+year);</script>\n'
    data = base_file.read()
    try:
      data = data.replace(search_text, replace_text)
      flag = 1
    except Exception:
      print("[+] Couldn't find the *Powered by CTFd* to replace with")
      flag = 0
  if flag == 1:
    with open(dst_path, 'w') as base_file:
      base_file.write(data)
      base_file.close()
  elif flag == 0:
    exit()

def patch_challenges_html(parent_path):
  relative_path = "CTFd/CTFd/themes/core/templates/challenges.html"
  dst_path = os.path.join(parent_path, relative_path)

  with open(dst_path, 'r+') as challenges_file: 
    lines = challenges_file.readlines()
    try:
      for i, line in enumerate(lines):
        if line.startswith('<div class="modal fade" id="challenge-window"'):
          lines[i] = '<span class="ctfd-auto-scoreboard" style="position: relative; float: right; top: 0px; right: 0px; min-width: 20%;">&nbsp;</span>\n\n' + lines[i]
      challenges_file.seek(0)
      for line in lines:
        challenges_file.write(line)
      challenges_file.close()
    except Exception:
      print("[+] Couldn't find the *viewport* to replace with.")
      challenges_file.close()

def copy_plugin(parent_path):
  relative_path = "CTFd/CTFd/plugins/auto-scoreboard"
  dst_path = os.path.join(parent_path, relative_path)

  os.mkdir(dst_path)
  src_path = "auto-scoreboard"

  files=os.listdir(src_path)
  for file_name in files:
    shutil.copy2(os.path.join(src_path,file_name), dst_path)


if __name__=="__main__":
#   change parent path of CTFd after clone
  parent_path = "/home/ctfd/Desktop/test/"

  patch_base_html(parent_path)
  patch_challenges_html(parent_path)
  copy_plugin(parent_path)
