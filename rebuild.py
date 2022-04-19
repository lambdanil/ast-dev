import sys
import os

def main():
    args = list(sys.argv)
    if len(args) > 2:
        fromsnap = args[1]
        tosnap = args[2]
        print(f"please chroot into snapshot {tosnap} in another console, then press enter")
        input("")
        os.system(f"rm -rf /.overlays/overlay-chr{tosnap}/usr/share/ast/*")
        os.system(f"cp -r /.overlays/overlay-{fromsnap}/usr/share/ast/* /.overlays/overlay-chr{tosnap}/usr/share/ast/")
        os.system(f"chroot /.overlays/overlay-chr{tosnap} /var/astpk/redownload")
        os.system(f"umount /.overlays/overlay-chr{tosnap}/etc/resolv.conf")
        os.system(f"chroot /.overlays/overlay-chr{tosnap} /var/astpk/reinstall")
        os.system(f"cp -r /.etc/etc-{fromsnap}/* /.overlays/overlay-chr{tosnap}/etc/")
        print("please exit chroot shell now with 'exit'")
    else:
        fromsnap = args[1]
        print(f"please chroot into snapshot {tosnap} in another console, then press enter")
        input("")
        os.system(f"chroot /.overlays/overlay-chr{tosnap} /var/astpk/redownload")
        os.system(f"umount /.overlays/overlay-chr{tosnap}/etc/resolv.conf")
        os.system(f"chroot /.overlays/overlay-chr{tosnap} /var/astpk/reinstall")
        print("please exit chroot shell now with 'exit'")

if __name__=="__main__":
    main()
