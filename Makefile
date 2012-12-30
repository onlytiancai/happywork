VIRTUALENV?=virtualenv

init:
	rm webappbox -rf
	git clone git@github.com:onlytiancai/webappbox.git 
	rm webappbox/src/webapps/simpleApp -rf
	cp stuff/webappbox_config.py webappbox/src/config.py -rf
	cp todo/ webappbox/src/webapps/ -rf

start:
	cd webappbox/src/ && sh start.sh

stop:
	cd webappbox/src/ && sh stop.sh
