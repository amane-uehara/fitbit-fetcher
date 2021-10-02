#!/bin/sh

SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd ${SCRIPT_DIR}

git clone https://github.com/orcasgit/python-fitbit.git
cd ${SCRIPT_DIR}/python-fitbit

pip3 install -r requirements/base.txt
pip3 install -r requirements/dev.txt
pip3 install -r requirements/test.txt
pip3 install cherrypy
pip3 install fitbit

cd ${SCRIPT_DIR}
