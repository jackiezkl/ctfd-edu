def main():
  with open('/home/ctfd/Desktop/test/CTFd/CTFd/themes/core/templates/base.html', 'r+') as f: 
    lines = f.readlines()
    for i, line in enumerate(lines):
      if line.startswith('\t<meta name="viewport"'):
        lines[i] = lines[i].strip() + '\n\t<meta name="starts_in" content="{{ ctf_starts_in() }}">\n\t<meta name="ends_in" content="{{ ctf_ends_in() }}">'
    f.seek(0)
    for line in lines:
      f.write(line)
    f.close()
    
  with open(('/home/ctfd/Desktop/test/CTFd/CTFd/themes/core/templates/base.html', 'r+') as file:
    search_text1 = '<a href="https://ctfd.io" class="text-secondary">\n\t\t\t\t<small class="text-muted">Powered by CTFd</small>\n\t\t\t</a>\n'
    replace_text = '<script>const d=new Date();let year=d.getFullYear();document.write("CTF - "+year);</script>'

    data = file.read()
  
    data = data.replace(search_text, replace_text)
  
    file.write(data)

if __name__=="__main__":
  main()
