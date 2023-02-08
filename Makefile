.PHONY: doc
doc:
	python -m pdoc --html moodle -o doc
	mv doc/moodle/*.html doc
	rm -rf doc/moodle
clean:
	rm -rf doc