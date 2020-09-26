all:
	pex -o ./build/keepassx_pw_finder -D ./src -r requirements.txt -e keepassx_pw_finder:main

typecheck:
	mypy src/

clean:
	$(RM) pykeepass_socket
	$(RM) -r ./build/ .mypy_cache
