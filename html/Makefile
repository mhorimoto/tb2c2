TARGD=/etc/uecs/html
CGID=$(TARGD)/cgi-bin
WEBD=/etc/systemd/system/cgiserver.service

install: $(TARGD)/cgiserver.py $(TARGD)/index.html $(CGID)/test.py $(CGID)/querytest.py $(CGID)/index.py $(WEBD) $(TARGD)/httpd.sh

$(TARGD)/cgiserver.py : cgiserver.py
	install $^ $(TARGD)

$(CGID)/index.py: cgi-bin/index.py
	install $^ $(CGID)

$(TARGD)/httpd.sh : httpd.sh
	install $^ $(TARGD)

$(TARGD)/index.html : index.html
	cp $^ $(TARGD)

$(WEBD): cgiserver.service
	cp $^ $(WEBD)
