-------------
Usage
-------------
Here is basic example.
If your directory structure is like this

directory structure::

    ├── example_a.ini
    ├── env
    │   └── production
    │       └── example_a.ini
    ├── role
    │   └── read_api
    │       └── example_a.ini
    └── node
        └── xxx101
            └── example_a.ini


.. code-block:: python

    import configoverloader as co
    from ConfigParser import ConfigParser

    # register context
    co.register_context(
        env="production",
        role="read_api",
        node="xxx101")

    # get files
    path_list = co.get_filenames( "YOUR_BASE_DIR/example_a.ini")
    print(path_list)
    # Output:
    # [ 'YOUR_BASE_DIR/example_a.ini',
    #   'YOUR_BASE_DIR/env/production/example_a.ini',
    #   'YOUR_BASE_DIR/env/production/example_a.ini',
    #   'YOUR_BASE_DIR/node/xxx101/example_a.ini']
    #
    # then you can call ConfigParser.read()
    cfg = ConfigParser()
    cfg.read(path_list)


You can pass stream instead of filename like this

.. code-block:: python

    with open( "YOUR_BASE_DIR/example_a.ini") as fp:
        path_list = co.get_filenames(fp)

