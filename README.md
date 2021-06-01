# Jamie Gabriel


I set up this repo to hold links to my study notes, projects and templates, mostly in the area of math and computer science.


Setup:

If you just want to read what's in the various Jupyter Notebooks, just go to the associated Github Pages site at <a href='https://www.ladatavita.com/'>https://www.ladatavita.com/</a>. Once I complete them, I will post a html version.

If you want to run the notebooks, best bet is to create Jupyter-lab Docker container. TO do this:  

Install Docker on your machine by following the instructions at: https://www.docker.com/.

Open a shell/bash terminal on your machine. Run:
docker run -p 10000:8888 -e JUPYTER_ENABLE_LAB=yes --user root -v [location_you_want_to_keep_your_files_in]:/home/jovyan/work jupyter/datascience-notebook:33add21fab64 Remember to just replace [location_you_want_to_keep_your_files_in] with the absolute path where you are keeping your files. The -v command above just tells Docker that the container will be able to see and save files to some folder on your local machine that you specify. Wherever that is, go there and run pwd and include that in the above docker run command.

Docker will download the jupyter notebook container and run it (further details of the image you are downloading can also be found at: https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html. Once it has finished, it will provide some logs of a link that you can start your notebook. Note that the link it provides will say it should be running on port 8888. However, when you paste in the link, change the 8888 to 10000 as in the docker run command we have told Docker to reroute traffic on port 8888 of the container to port 10000 of our local machine

Note can can CTRL-c in the shell and it won't actually shut down the container (you can check with the command docker container ls and it will show the container running.

Now, still using the shell on your local machine and now go into the docker container’s bash shell by running:
docker exec -it [docker container ID] bash
Note you can get the ID of the Docker Container from running: docker container ls

Now you will be in the Docker container as the root user root. From here, just run two comands:
`apt-get update`
`apt-get install cmake`

Now, while you are still in the container's shell run:
git clone https://github.com/htm-community/htm . This will clone the htm.core repo into the docker container. You will notice it downloads to the \home folder in the Docker container which has been synced with your local folder you created with that -v command, so the cloned repo will appear in your local machine folder as well

Once its downloaded, just follow the instructions at https://github.com/htm-community/htm.core for the Python installation. This will involve cd’ing into the htm.core folder and running python setup.py install. Note that I have ommitted the flaggs --user and --force. This is because this image is based on an anaconda installation and these flags will prevent the htm package from registering in conda's site packages.

You can also compile the C++ code and the docs by following the instructions on the htm.core github repo. You should end up with everything installed, and when you go to localhost:1000 that Docker has spun up for you, you can check by things are ok by copying code from https://github.com/htm-community/htm.core/blob/master/py/htm/examples/hotgym.py into a notebook. Don't forget that when you go to the http://127.0.0.1:10000/lab/tree/ for the first time it might ask for a token, which you can get from the command in which you ran at step 2 of these instructions, (or just run docker container [CONTAINER ID] logs to get this.

Finally, note you can docker container stop [container-id] and docker container start [container-id] at any time to shut down the container, and it should come back to life if exactly the same way. You can also push an image of this container to DockerHub to keep a copy of the setup safe