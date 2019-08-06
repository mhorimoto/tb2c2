TARGD=/etc/uecs/html
CGID=$(TARGD)/cgi-bin

install: $(TARGD)/cgiserver.py $(TARGD)/index.html $(CGID)/test.py $(CGID)/querytest.py $(CGID)/index.py

$(TARGD)/cgiserver.py : cgiserver.py
	install $^ $(TARGD)

$(TARGD)/httpserver.py : httpserver.py
	install $^ $(TARGD)

$(CGID)/test.py: cgi-bin/test.py
	install $^ $(CGID)

$(CGID)/index.py: cgi-bin/index.py
	install $^ $(CGID)

$(CGID)/querytest.py: cgi-bin/querytest.py
	install $^ $(CGID)

$(TARGD)/index.html : index.html
	cp $^ $(TARGD)
