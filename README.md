# CSV to JSON

![Pipeline status](https://gitlab.com/fhightower/csv-to-json/badges/master/build.svg)

Convert CSV to JSON. There is a testing/debugging interface [here](https://hub.mybinder.org/user/fhightower-csv-to-json-hkqr8zl5/tree).

This:

```
"foo,bar\n1,2"
```

becomes:

```
[{'a': 'foo', 'b': 'bar'}, {'a': '1', 'b': '2'}]
```

or (depending on how you want the output):

```
[{'foo': '1', 'bar': '2'}]
```

## Usage

The basic interface is:

```python
import csv_to_json

csv_string = "foo,bar\n1,2"

output_json = csv_to_json.convert(csv_string)
print(output_json) # [{'a': 'foo', 'b': 'bar'}, {'a': '1', 'b': '2'}]
```

You can also pass the following arguments into the `csv_to_json.convert()` function:

- `delimiter` (default: ','): This sets the delimiter to be used on the csv_string
- `comment_character` (default: '#'): csv_to_json will ignore all lines that start with this character
- `heading_row` (default: None): If a heading_row is set (it takes an integer), the json result will use the values at that row for the keys of the json (see the example below for more details on how this works)
- `debug` (default: None): If this is set, there will be output given as the script converts CSV to JSON to help you debug if anything goes wrong

Here is an example using the `heading_row`

```python
import csv_to_json

csv_string = "foo,bar\n1,2"

output_json = csv_to_json.convert(csv_string, heading_row=0)
print(output_json) #  [{'foo': '1', 'bar': '2'}]
```

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and fhightower's [Python project template](https://github.com/fhightower-templates/python-project-template).
