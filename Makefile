init:
    pip install -r requirements.txt

test:
    py.test ./gdal2scidb/tests

.PHONY: init test
