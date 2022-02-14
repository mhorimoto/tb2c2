PYLIBD=/usr/local/lib/python3.9/dist-packages
#PYLIBD=/usr/local/lib/python3.8/dist-packages
#PYLIBD=/usr/local/lib/python3.6/dist-packages
EXECP=/usr/local/bin/tb2c2d.py
SCANP=/usr/local/bin/scanresponse.py
SYSCD=/etc/systemd/system/tb2c2.service
SCAND=/etc/systemd/system/scanresponse.service
WEBD=/etc/systemd/system/cgiserver.service
TARGD=/usr/local/bin
CFGFD=/etc/uecs
NTPDC=/etc/ntp.conf
CONFF=$(CFGFD)/config.ini
XMLFF=$(CFGFD)/tb2c2.xml
WD3INIT=wd3init.py
FWD3INIT=$(PYLIBD)/$(WD3INIT)
WD3RESET=wd3reset.py
FWD3RESET=$(PYLIBD)/$(WD3RESET)

$(EXECP): tb2c2d.py
	install $^ $(TARGD)

$(SCANP): scanresponse.py
	install $^ $(TARGD)

$(CONFF): config.ini
	cp $^ $(CONFF)

$(XMLFF): tb2c2.xml
	cp $^ $(XMLFF)

$(SYSCD): tb2c2.service
	cp $^ $(SYSCD)

$(SCAND): scanresponse.service
	cp $^ $(SCAND)

$(NTPDC): ntp.conf
	@mv $(NTPDC) $(NTPDC)-orig
	cp $^ $(NTPDC)

$(FWD3INIT): $(WD3INIT)
	cp $^ $(PYLIBD)

$(FWD3RESET): $(WD3RESET)
	cp $^ $(PYLIBD)


install: $(EXECP) $(SCANP) $(CONFF) $(XMLFF) $(SYSCD) $(SCAND) $(NTPDC) $(FWD3INIT) $(FWD3RESET)


