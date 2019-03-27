
def minify(input_file):
    import python_minifier

    with open(input_file, 'r') as handler:
        return python_minifier.minify(handler.read())
