all: test_all release
#
# No practical reason for running separate remote integrated test
# This library does not perform any file i/o and is unlikely candidate for patching
# Remote integrated tests take too much time
#

release:
	cp -R ./src/* ~/$(CAIOS_VERSION)/
	
test_all:
	caios test run unit local
