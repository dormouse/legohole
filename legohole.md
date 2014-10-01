install virtualenv
==================
$ sudo apt-get install python-pip
$ sudo pip install virtualenvwrapper

add flowing to .bashrc

export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/project
source /usr/local/bin/virtualenvwrapper.sh

reload .bashrc

$ cd project
$ mkvirtualenv legohole

shuld see:(legohole)dormouse@dormouse-OptiPlex-360 ~ $ 

out virtualenv:deactivate
in virtualenv:workon django_project

install django
==============

$ pip install django

confirm install

$ which django-admin.py
should see:/home/dormouse/.virtualenvs/legohole/bin/django-admin.py


setup git
=========
sudo apt-get install git
git config --global user.name "Dormouse Young"
git config --global user.email "dormouse.young@gmail.com"
ssh-keygen -t rsa -C "dormouse.young@gmail.com"

Then add your new key to the ssh-agent:

# start the ssh-agent in the background
eval "$(ssh-agent -s)"
# Agent pid 59566
ssh-add ~/.ssh/id_rsa

Copies the contents of the id_rsa.pub file to your clipboard

add to https://github.com/settings/ssh

test ssh::

    ssh -T git@github.com

should see hi dormouse

git usage::

    …or create a new repository on the command line

    touch README.md
    git init
    git add README.md
    git commit -m "first commit"
    git remote add origin git@github.com:dormouse/legohole.git
    git push -u origin master

    …or push an existing repository from the command line

    git remote add origin git@github.com:dormouse/legohole.git
    git push -u origin master

start project
=============

cd project

django-admin.py startproject legohole

git init
git add django_project
git commit -m 'Initial commit of legohole'


pip install south


creat .gitignore::

*.pyc
.*swp

pip freeze > requirements.txt

check befort push::

    git status




参考：http://www.jeffknupp.com/blog/2013/12/18/starting-a-django-16-project-the-right-way/




