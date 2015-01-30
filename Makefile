SRC       =   $(addprefix ,       \
                Line.py           \
                OptionParser.py   \
                Screen.py         \
                Ransac.py         \
                Server.py         \
                Serializer.py     \
                Trigo.py          \
              )

doc:
	epydoc -v $(SRC)

rundoc: doc
	firefox html/index.html

cleandoc:
	rm -rf html/
