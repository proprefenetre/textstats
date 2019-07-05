# Textstats

This is an example of a service for use in the [CLARIAH WP3 Virtual Research
Environment](https://github.com/meertensinstituut/clariah-wp3-vre) that is currently under development.

It provides basic statistics and key word/sentence extraction for TEI-encoded documents.

# Request

~~~
curl -X POST -F file=@{filename} -F layer={div-type} http://{domain}:{port}
~~~

By default, the service analyzes the first `div` in a `text` element. If `layer` is provided, the service analyzes all
divs with type `div-type` (e.g. 'chapter').
