===
FAQ
===

What's the priority over env, role and node.
--------------------------------------------
The order of the priority is "node > role > env"


Can I change the context in the middle?
---------------------------------------
Yes, you can register again

.. code-block:: python

    import configoverloader as co
    co.register_context(env="OLD_ENV",)


The other call configoverloader.get_filesnames() with parameters
.. code-block:: python

    import configoverloader as co
    filename_list = co.get_filenames("example_a.ini", env="NEW_ENV")


What is default value of env, role and node ?
---------------------------------------------
env and role has no default value.  Node's default value is  :code:`socket.gethostname()` and :code:`socket.getfqdn`.
If you don't like this behavior, please set default value like this.
.. code-block:: python

    import configoverloader as co
    co.register_context(node="")


