def patch_base_html():
  with open('/home/ctfd/Desktop/test/CTFd/CTFd/themes/core/templates/base.html', 'r+') as f: 
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

  with open('/home/ctfd/Desktop/test/CTFd/CTFd/themes/core/templates/base.html', 'r') as base_file:
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
    with open('/home/ctfd/Desktop/test/CTFd/CTFd/themes/core/templates/base.html', 'w') as base_file:
      base_file.write(data)
      base_file.close()
  elif flag == 0:
    exit()

def patch_challenges_html():
  with open('/home/ctfd/Desktop/test/CTFd/CTFd/themes/core/templates/challenges.html', 'r+') as challenges_file: 
    lines = challenges_file.readlines()
    try:
      for i, line in enumerate(lines):
        if line.startswith('<div class="modal fade" id="challenge-window"'):
          lines[i] = '<span class="ctfd-auto-scoreboard" style="position: relative; float: right; top: 0px; right: 0px; min-width: 20%;">&nbsp;</span>\n' + lines[i]
      challenges_file.seek(0)
      for line in lines:
        challenges_file.write(line)
      challenges_file.close()
    except Exception:
      print("[+] Couldn't find the *viewport* to replace with.")
      challenges_file.close()

if __name__=="__main__":
  patch_base_html()
  patch_challenges_html()

  
  
