import os,re
from secrets import token_hex
from shutil import copytree
from multiprocessing import cpu_count

def already_exist(parent_path,relative_path,string_to_check):
  dst_path = os.path.join(parent_path, relative_path)
  with open(dst_path) as check_file:
    if string_to_check in check_file.read():
      return True
    else:
      return False

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
    except Exception:
      print("[e] Couldn't find the *viewport* to replace with.")


  with open(dst_path, 'r') as base_file:
    search_text = '<a href="https://ctfd.io" class="text-secondary">\n\t\t\t\t<small class="text-muted">Powered by CTFd</small>\n\t\t\t</a>\n'
    replace_text = '<script>const d=new Date();let year=d.getFullYear();document.write("{{ Configs.ctf_name }} - "+year);</script>\n'
    data = base_file.read()
    try:
      data = data.replace(search_text, replace_text)
      flag = 1
    except Exception:
      print("[e] Couldn't find the *Powered by CTFd* to replace with")
      flag = 0

  if flag == 1:
    with open(dst_path, 'w') as base_file:
      base_file.write(data)
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
    except Exception:
      print("[e] Couldn't find the *viewport* to replace with.")

def copy_plugin(parent_path):
  relative_path = "CTFd/CTFd/plugins/ctfd-auto-scoreboard"
  dst_path = os.path.join(parent_path, relative_path)
  src_path = "ctfd-auto-scoreboard"

  copytree(src_path,dst_path)
  print('[+] plugin copied to place.')

def patch_register_html(parent_path):
  relative_path = "CTFd/CTFd/themes/core/templates/register.html"
  dst_path = os.path.join(parent_path, relative_path)
  if os.path.exists(dst_path) == False:
    print("[e] Couldn't find the *register.html* to work with.")
    exit()

  with open(dst_path, 'r') as base_file:
    search_text = '\t\t\t{% endwith %}\n\t\t</div>\n\t</div>\n</div>\n'
    replace_text = '\t\t\t{% endwith %}\n\t\t</div>\n\t</div>\n</div>\n<script>\nvar newelement = \'<select class="form-control" id="fields[2]" name="fields[2]" required="" type="text" value=""><option disabled="" selected="" value=""> -- select an option -- </option><option value="January">January</option><option value="February">February</option><option value="March">March</option><option value="April">April</option><option value="May">May</option><option value="June">June</option><option value="July">July</option><option value="August">August</option><option value="September">September</option><option value="October">October</option><option value="November">November</option><option value="December">December</option></select>\';\nvar oldelement = document.getElementById(\'fields[2]\');\nif(oldelement.outerHTML) {\n\toldelement.outerHTML=newelement;\n}\nelse{\n\tvar tmpelement=document.createElement("div");\n\ttmpelement.innerHTML=\'<!--THIS DATA SHOULD BE REPLACED-->\';\n\tObjParent=oldelement.parentNode;\n\tObjParent.replaceChild(tmpelement,oldelement);\n\tObjParent.innerHTML=ObjParent.innerHTML.replace(\'<div><!--THIS DATA SHOULD BE REPLACED--></div>\',newelement);\n}\nconst element = document.getElementById("fields[3]").parentElement;\nelement.remove();</script>\n'
    data = base_file.read()
    try:
      data = data.replace(search_text, replace_text)
      flag = 1
    except Exception:
      print("[e] Couldn't find the element to replace with")
      flag = 0
  if flag == 1:
    with open(dst_path, 'w') as base_file:
      base_file.write(data)
  elif flag == 0:
    exit()

def patch_username_description(parent_path):
  relative_path = "CTFd/CTFd/themes/core/templates/register.html"
  dst_path = os.path.join(parent_path, relative_path)
  if os.path.exists(dst_path) == False:
    print("[e] Couldn't find the *register.html* to work with.")
    exit()

  with open(dst_path, 'r') as base_file:
    search_text = 'Your username on the site'
    replace_text = 'Your username on the site. It can be anything you want to be called.'
    data = base_file.read()
    try:
      data = data.replace(search_text, replace_text)
      flag = 1
    except Exception:
      print("[e] Couldn't find the element to replace with")
      flag = 0
  if flag == 1:
    with open(dst_path, 'w') as base_file:
      base_file.write(data)
  elif flag == 0:
    exit()

def patch_private_html(parent_path):
  relative_path = "CTFd/CTFd/themes/core/templates/users/private.html"
  dst_path = os.path.join(parent_path, relative_path)
  if os.path.exists(dst_path) == False:
    print("[e] Couldn't find the *users/private.html* to work with.")
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
    except Exception:
      print("[e] Couldn't find the *{{ user.name }}* to replace with.")

def create_secret(parent_path):
  relative_path = "CTFd/.ctfd_secret_key"
  dst_path = os.path.join(parent_path,relative_path)
  with open(dst_path, "w") as secret_file:
    secret_file.write(token_hex())

def patch_docker_compose(parent_path):
  relative_path = "CTFd/docker-compose.yml"
  dst_path = os.path.join(parent_path, relative_path)
  if os.path.exists(dst_path) == False:
    print("[e] Couldn't find the *docker-compose.yml* to work with.")
    exit()

  try:
    with open(dst_path, 'r+') as docker_compose_file:
      search_text = '(- WORKERS=\d*)'
      replace_text = '- WORKERS='+str(2*cpu_count()+1)
      data = docker_compose_file.read()

      data = re.sub(search_text,replace_text,data)
      docker_compose_file.seek(0)
      docker_compose_file.write(data)
      docker_compose_file.truncate()
      print("[+] docker-compose file patched.")
  except Exception:
    print("[e] Couldn't find the element to replace with")


if __name__=="__main__":
#   change parent path of CTFd after clone
  current_path=os.getcwd()
  parent_path = os.path.dirname(current_path)+"/"
  if os.path.isfile(os.path.join(parent_path,"CTFd/.ctfd_secret_key")) == False:
    create_secret(parent_path)
    print("[+] .ctfd_secret_key file created.")
  else:
    print("[e] .ctfd_secret_key exist! No need to have another .ctfd_secret_key file. Skipped.")

  patch_docker_compose(parent_path)

  if os.path.isfile(os.path.join(parent_path,"CTFd/CTFd/plugins/ctfd-auto-scoreboard/assets/auto-scoreboard.js")) == False:
    copy_plugin(parent_path)
  else:
    print("[e] Plugin already exist. Skipped.")

  print("[i] patching base.html ...")
  if already_exist(parent_path, 'CTFd/CTFd/themes/core/templates/base.html', '{{ ctf_starts_in() }}') == False and already_exist(parent_path, 'CTFd/CTFd/themes/core/templates/base.html', 'year=d.getFullYear()') == False:
    patch_base_html(parent_path)
    print("[+] Done")
  elif already_exist(parent_path, 'CTFd/CTFd/themes/core/templates/base.html', '{{ ctf_starts_in() }}') == True and already_exist(parent_path, 'CTFd/CTFd/themes/core/templates/base.html', 'year=d.getFullYear()') == True:
    print('[e] base.html already patched, skipped.')
    pass
  elif already_exist(parent_path, 'CTFd/CTFd/themes/core/templates/base.html', '{{ ctf_starts_in() }}') == True and already_exist(parent_path, 'CTFd/CTFd/themes/core/templates/base.html', 'year=d.getFullYear()') == False:
    print("[e] Something's wrong, for some reason, ony the first half of base.html is patched. Skipped")
    pass
  elif already_exist(parent_path, 'CTFd/CTFd/themes/core/templates/base.html', '{{ ctf_starts_in() }}') == False and already_exist(parent_path, 'CTFd/CTFd/themes/core/templates/base.html', 'year=d.getFullYear()') == True:
    print("[e] Something's wrong, for some reason, the base file is half patched. Skipped")
    pass
  else:
    print("[e] Something's wrong please check if base.html esixts.")
    pass

  print("[i] Patching challenges.html ...")
  if already_exist(parent_path, 'CTFd/CTFd/themes/core/templates/challenges.html','class="ctfd-auto-scoreboard"') == False:
    patch_challenges_html(parent_path)
    print("[+] Done")
  elif already_exist(parent_path, 'CTFd/CTFd/themes/core/templates/challenges.html','class="ctfd-auto-scoreboard"') == True:
    print('[e] challenges.html already patched. Skipped')
    pass
  else:
    print("[e] Something's wrong please check if challenges.html esixts.")
    pass

  print("[i] Patching register.html ...")
  if already_exist(parent_path, "CTFd/CTFd/themes/core/templates/register.html", '<option value="May">May</option>') == False and already_exist(parent_path, "CTFd/CTFd/themes/core/templates/register.html", 'It can be anything you want to be called.') == False:
    patch_register_html(parent_path)
    patch_username_description(parent_path)
    print("[+] Done")
  elif already_exist(parent_path, "CTFd/CTFd/themes/core/templates/register.html", '<option value="May">May</option>') == True and already_exist(parent_path, "CTFd/CTFd/themes/core/templates/register.html", 'It can be anything you want to be called.') == True:
    print("[e] register.html already patched, skipped.")
    pass
  elif already_exist(parent_path, "CTFd/CTFd/themes/core/templates/register.html", '<option value="May">May</option>') == True and already_exist(parent_path, "CTFd/CTFd/themes/core/templates/register.html", 'It can be anything you want to be called.') == False:
    print("[e] Something's wrong, for some reason, ony the first half of base.html is patched. Skipped")
    pass
  elif already_exist(parent_path, "CTFd/CTFd/themes/core/templates/register.html", '<option value="May">May</option>') == False and already_exist(parent_path, "CTFd/CTFd/themes/core/templates/register.html", 'It can be anything you want to be called.') == True:
    print("[e] Something's wrong, for some reason, the base file is half patched. Skipped")
    pass
  else:
    print("[e] Something's wrong please check if register.html esixts.")
    pass

  print("[i] Patching private.html ...")
  if already_exist(parent_path, "CTFd/CTFd/themes/core/templates/users/private.html", '<h5 class="d-block">\n\t\t\t\t\t{{ field.name }}: {{ field.value }}') == False:
    patch_private_html(parent_path)
    print("[+] Done")
  elif already_exist(parent_path, "CTFd/CTFd/themes/core/templates/users/private.html", '<h5 class="d-block">\n\t\t\t\t\t{{ field.name }}: {{ field.value }}') == True:
    print("[e] private.html already patched, skipped.")
    pass
  else:
    print("[e] Something's wrong please check if private.html esixts.")
    pass
