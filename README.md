# Quickstart
* `git clone git@github.com:incuna/incuna-project`
* `sudo pip install -U django`
* `python django-admin.py startproject --template=incuna-project <new_project>`
* `cd <new_project>`
* Create your virtualenv (and activate)
* `git setup .`
* `git create -p incuna/<new_project>`
* `git push -u origin master`


# Template project

This is the introduction section which explains what this project is all about!
This project is just the starting project which is used as a template for the
start script. You should explain here succinctly what sort of website this is,
who the client is and any other super important information, such as any
external services you rely on. If the text in this section is getting long and
complicated then you probably want to pass some of it off to the wiki.

## Setup

    git clone -p incuna/project_name
    cd project_name
    # Make your virutalenv
    pip install -r dev_requirements.txt
    cp project_name/local_settings{.example,}.py
    python manage.py runserver

## Applications

Here you should list the major django applications in the app with a brief
description of their purpose. Here's the stuff which is included by default.

- **FeinCMS** is used for administrator-managed content using the sites
  framework. Ideally everything else we do should be integrated with Fein as it
  allows the admin to move things around the site easier. This means defining
  content types and application content.
- **Crispy forms** is used for form layout.
- **South** is used for database migrations.
