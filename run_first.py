import os
from shutil import copytree

def patch_base_html(parent_path):
  relative_path = "CTFd/CTFd/themes/core/templates/base.html"
  dst_path = os.path.join(parent_path, relative_path)
  try:
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
  except Exception:
    print("[+] Could't find base.html file to work with.")
    exit()

def patch_challenges_html(parent_path):
  relative_path = "CTFd/CTFd/themes/core/templates/challenges.html"
  dst_path = os.path.join(parent_path, relative_path)

  try:
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
  except Exception:
    print("[+] Couldn't find the challenges.html to work with.")
    exit()

def copy_plugin(parent_path):
  relative_path = "CTFd/CTFd/plugins/auto-scoreboard"
  dst_path = os.path.join(parent_path, relative_path)
  src_path = "auto-scoreboard"

  copytree(src_path,dst_path)

def patch_register_html(parent_path):
  relative_path = "CTFd/CTFd/themes/core/templates/register.html"
  dst_path = os.path.join(parent_path, relative_path)
  if os.path.exists(dst_path) == False:
    print("[+] Couldn't find the *register.html* to work with.")
    exit()

  with open(dst_path, 'r+') as f:
    lines = f.readlines()
    try:
      for i, line in enumerate(lines):
        if line.startswith('\t\t\t{% endwith %}\n\t\t</div>\n\t</div>\n</div>\n'):
          lines[i] = lines[i] + '<script>var newelement = \'<select class="form-control" id="fields[2]" name="fields[2]" required="" type="text" value=""><option disabled="" selected="" value=""> -- select an option -- </option><option value="January">January</option><option value="February">February</option><option value="March">March</option><option value="April">April</option><option value="May">May</option><option value="June">June</option><option value="July">July</option><option value="August">August</option><option value="September">September</option><option value="October">October</option><option value="November">November</option><option value="December">December</option></select>\';var oldelement = document.getElementById(\'fields[2]\');if(oldelement.outerHTML) {oldelement.outerHTML=newelement;}else {var tmpelement=document.createElement("div");tmpelement.innerHTML=\'<!--THIS DATA SHOULD BE REPLACED-->\';ObjParent=oldelement.parentNode;ObjParent.replaceChild(tmpelement,oldelement);ObjParent.innerHTML=ObjParent.innerHTML.replace(\'<div><!--THIS DATA SHOULD BE REPLACED--></div>\',newelement);}const element = document.getElementById("fields[3]").parentElement;element.remove();</script>\n'
      f.seek(0)
      for line in lines:
        f.write(line)
      f.close()
    except Exception:
      print("[+] Couldn't find the *{% end with %}* to replace with.")
      f.close()

def patch_private_html(parent_path):
  relative_path = "CTFd/CTFd/themes/core/templates/users/private.html"
  dst_path = os.path.join(parent_path, relative_path)
  if os.path.exists(dst_path) == False:
    print("[+] Couldn't find the *users/private.html* to work with.")
    exit()

  with open(dst_path, 'r+') as f:
    lines = f.readlines()
    try:
      for i, line in enumerate(lines):
        if line.startswith('\t\t\t<h1>{{ user.name }}</h1>\n'):
          lines[i] = lines[i] + '\t\t\t{% for field in user.get_fields(admin=true) %}\n\t\t\t\t<h5 class="d-block">\n\t\t\t\t\t{{ field.name }}: {{ field.value }}\n\t\t\t\t</h5>\n\t\t\t{% endfor %}\n'
      f.seek(0)
      for line in lines:
        f.write(line)
      f.close()
    except Exception:
      print("[+] Couldn't find the *{{ user.name }}* to replace with.")
      f.close()


if __name__=="__main__":
#   change parent path of CTFd after clone
  current_path=os.getcwd()
  parent_path = current_path+"/"

  patch_base_html(parent_path)
  patch_challenges_html(parent_path)
  copy_plugin(parent_path)
  patch_register_html(parent_path)
  patch_private_html(parent_path)
