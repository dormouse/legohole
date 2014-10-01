Setup virtualenv
==================

install pip and virtualenvwrapper::

    $ sudo apt-get install python-pip
    $ sudo pip install virtualenvwrapper

add flowing to ~/.bashrc::

    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/project
    source /usr/local/bin/virtualenvwrapper.sh

reload .bashrc

creat virtualenv::

    $ cd project
    $ mkvirtualenv legohole

you should see somethine like::

    (legohole)dormouse@dormouse ~ $ 

usage::
    out virtualenv:deactivate
    in virtualenv:workon django_project

Setup django
==============

install django::

    $ pip install django

confirm install::

    $ which django-admin.py

should see:/home/dormouse/.virtualenvs/legohole/bin/django-admin.py

setup git
=========

install git::

    sudo apt-get install git

config git::

    git config --global user.name "Dormouse Young"
    git config --global user.email "dormouse.young@gmail.com"
    ssh-keygen -t rsa -C "dormouse.young@gmail.com"

Then add your new key to the ssh-agent::

    # start the ssh-agent in the background
    eval "$(ssh-agent -s)"
    # Agent pid XX566
    ssh-add ~/.ssh/id_rsa

Add the contents of the id_rsa.pub file to https://github.com/settings/ssh

test ssh::

    ssh -T git@github.com

should see "hi dormouse"

check befort push::

    git status

start project
=============

creat project::

    cd project
    django-admin.py startproject legohole

push to github::

    git init
    git add legohole
    git commit -m 'Initial commit of legohole'
    git remote add origin git@github.com:dormouse/legohole.git
    git push -u origin master

install south::

    pip install south


creat .gitignore file include::

    *.pyc
    .*swp

freeze requirements::

    pip freeze > requirements.txt





----
参考：http://www.jeffknupp.com/blog/2013/12/18/starting-a-django-16-project-the-right-way/




