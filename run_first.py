if __name__=="__main__":
  with open('CTFd/themes/core/templates/base.html', 'r+') as f: 
    lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('<meta name="viewport"'):
            lines[i] = lines[i].strip() + '\n<meta name="starts_in" content="{{ ctf_starts_in() }}">\n<meta name="ends_in" content="{{ ctf_ends_in() }}">'
    f.seek(0)
    for line in lines:
        f.write(line)
