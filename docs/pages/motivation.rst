
Motivation
----------
I often use different config files depend not only on "*env*", but also "*role*", "*node*"
I save each config in each repository. But I found it frustrating because the most part is the same.
It should be saved 1 repository.

Idea
----
As the name says, "overloading" is main idea.
Originally python's ConfigParser has overloading function.
This library just helps to glob files based on directory and file name rules.