if [ -f "/etc/arch-release" ]; then
  pacman -Sy python-pip
  pacman -Sy python-flask python-pyMySQL python-argon2_cffi

elif [ -f "/etc/debian-version" ]; then
  apt install python3 python3-pip
  apt install python-flask python-pyMySQL python-argon2_cffi
fi

python3 app.py