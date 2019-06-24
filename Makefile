EXECP=/usr/local/bin/tb2c2d.py
SCANP=/usr/local/bin/scanresponse.py
SYSCD=/etc/systemd/system/tb2c2.service
SCAND=/etc/systemd/system/scanresponse.service
TARGD=/usr/local/bin
CFGFD=/etc/uecs
NTPDC=/etc/ntp.conf
CONFF=$(CFGFD)/config.ini
XMLFF=$(CFGFD)/tb2c2.xml

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

install: $(EXECP) $(SCANP) $(CONFF) $(XMLFF) $(SYSCD) $(SCAND) $(NTPDC)


