+=============================================+

--== [ Documentation Readme: ] ==--

This readme contains some important info 
for writing and correcting capy docs!

--== [ Goals: ] ==--

We have the following goals for the docs:

    * Ensure spelling and grammatical correctness
    * Ensure text is understandable
        (As long as the reader has a simple understanding of what I am trying to say, then i’m calling that a success)
    * Ensure text is free of excessive rambling
    * Ensure text does not get repetitive or ‘copy-paste’ like
        (I know, this is a technical documentation and it is not supposed to be interesting)

Please keep these goals in mind!

--== [ Doc Status: ] ==--

Here you will find the status of documentation.
We will list each file that needs to be checked.
Please refrain from editing files that are sill being written!

Ready for checking:

collec_simp.rst
into_stip.rst

Being written:

index.rst
install.rst
usage.rst
curse_inst.rst

Completed:

--== [ Using Git: ] ==--

We use git for version control.
Here are some common operations you will need to know:

Commit - Save all changes you made locally

Push - Push all local changes to remote

Pull - 'Update' your files with changes from remote

If you want a primer on git, have a look here:

https://git-scm.com/docs/gittutorial

--== [ Doc Writing Introduction: ] ==--

The capy docs are separated into 'pages',
much like a website. Each page
contains info on a certain topic.
This is to ensure the documentation
remains maintainable,
as putting everything in one file
would make maintainability difficult.

The docs are built using a service called Sphinx 
that will render the content, and link them together.
You can read more about sphinx here:

https://www.sphinx-doc.org/en/master/

--== [ Locating the Docs: ] ==--

The docs can be found here:

docs/source/

Any file with an extension with '.rst' are
docs files that should be checked!
Have a list at the top of this file 
for doc status.
You can ignore 'conf.py'.

--== [ Doc Syntax: ] ==--

Content in these pages are written in a
markup language called ReStructuredText.
RT should look like normal text,
but with some minor syntax changes.

For example, here is text rendered as a header:

Header
======

Normal text 

The 'Header' text will be rendered in large and bold, acting a header.
Any text with '=' below it will act as a header.
Any text with '-' beneath it will act as a sub-header.

You might also see text like this:

    * Value 1
    * Value 2

This will render the content as a list.

You will definitely see something like this:

.. [SOME NAME]::

	Content!

The ‘.. [SOME NAME]::’ is what's called a directive. 
This tells the computer to format the indented text in a special way. 
For example, text might be rendered in red to act as a warning.
In my docs, I use the ‘Code-Block’ directive a lot. 
This essentially tells the computer to do some syntax highlighting, 
and separate it from the rest of the text. Here is an example of the ‘Code-Block’ directive:

.. Code-Block:: python

	# We are python code!
	# We are probably going to be highlighted in some special way!

	print(“Rocking in the CyberSpace!”)

You do not have to worry about content in these code block sections,
as they are code examples. The only thing you should look at are the comments,
which are preceded by a hashtag(#).

Any other directives like 'note' and 'warning' should be checked!

Don’t worry about syntax errors or indentation, I can correct that at a later date. 
Please have a look at the primer tutorial if you want a deeper understanding of RT:

https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html


--== [ Manually Building Docs: ] ==--

Your IDE should automatically build the docs for 
you in the preview pane.
If you want to build the docs yourself, 
then follow these steps:

    1. Open a command prompt in the root directory 
    2. Navigate to 'docs/' by using this command:
        cd docs/
    3. Run this command to build:
        make html

After the docs are built, navigate to 'docs/build/html'
and you will find the HTML pages for each page.
You can open the HTML files with your favorite web browser.

--== [ Conclusion: ] ==--

Thank you for helping out, 
I really do appreciate it!

If you have any questions, 
please don't hesitated to contact me.