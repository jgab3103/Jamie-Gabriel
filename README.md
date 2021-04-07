# Jamie Gabriel


I set up this repo to hold links to my study notes, projects and templates, mostly in the area of math and computer science.


Setup:

If you just want to read what's in the various Jupyter Notebooks, just go to the associated Github Pages site at <a href='https://www.ladatavita.com/'>https://www.ladatavita.com/</a>. Once I complete them, I will post a html version.

To run all the math notebooks in this repo, you can use a Sage Docker image. Just run <code>docker-compose up</code> in this directory and go to localhost:5000. This will work with no issues and Mac and Windows. I am in the process of moving many of my Sage notebooks to standard Python 3 notebooks so will update setup once this is done.

To run the HTM notebooks, I use Docker Data Science Jupyter Image (found <a href="https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html">here</a>). I am have amended it to include the compiled htm.core code base in python and C++.

To do this on Mac or Linux:

1. Download or clone this repo
2. cd into the Notebooks folder in the repo
3. Run the command: <code>docker run -p 8888:8888 --user root -v /Users/jamiegabriel/Desktop/Jamie-Gabriel/Notebooks:/home jupyter/datascience-notebook</code> where <code>"/Users/jamiegabriel/Desktop/Jamie-Gabriel/Notebooks"</code> gets replaced with the absolute path you are in (i.e. from running pwd)
4. This will start the container. Go into the container with <code> docker exec -it <YOUR CONTAINER ID> bash</code>
5. Run <code>apt-get update</code>
6. Run <code>apt-get install cmake </code>
7. Run <code git clone https://github.com/htm-community/htm </code>
8. Follow in the instructions at <a href="https://github.com/htm-community/htm">https://github.com/htm-community/htm</a> to install the Python release. Basically, just cd'ing into the relevant folder and running <code>python setup.py install --user --force</code>
9. Follow the instructions to compile the C++ release
10. Follow the instructions to compile the docs (just cd into the docs folder, and run doxygene - there are instructions inside this docs ReadME.md file)

Note that for this set up does not work on Windows (something do with more recent versions of running Docker Jupyter images which has permissions issues. I will get around to sorting this out)
