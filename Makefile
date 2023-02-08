.PHONY: doc
doc:
	python -m pdoc --html moodle -o doc
clean:
	rm -rf doc