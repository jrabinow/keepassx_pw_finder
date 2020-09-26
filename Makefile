all:
	pex -o ./build/keepassx_pw_finder -D ./src -r requirements.txt -e keepassx_pw_finder:main

typecheck:
	mypy src/

docs:
	cd docs && sphinx-apidoc -f -o . ../src/ && $(MAKE) html

clean:
	$(RM) pykeepass_socket
	$(RM) -r ./build/ .mypy_cache ./src/__pycache__ ./src/*.pyc
	cd docs && $(MAKE) clean

.PHONY: clean docs
