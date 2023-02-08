.PHONY: doc
doc:
	mkdir -p doc
	pydoc -w moodle
	pydoc -w `find moodle -name '*.py'`
	mv *.html doc
clean:
	rm -rf doc 2>/dev/null