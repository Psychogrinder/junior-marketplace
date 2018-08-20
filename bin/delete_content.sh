#!/bin/bash
export DIR="$(pwd)" 
cd $DIR/marketplace.app/marketplace/content
export FLASK_APP=data_app.py
gnome_terminal 'flask run --port=9999'
python3 delete_content.py
cd $DIR
fuser -n tcp -k 9999
export FLASK_APP=runserver.py
exec bash

