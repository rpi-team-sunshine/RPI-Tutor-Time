Team-Sunshine
=============

Authors:

Thomas Chestna
Adam DeRusha
Sheena McNeil
Zhenzheng Zhou

INSTALLATION:

Step 1: You need django 1.4 and python 2.7. If you don't have them go out and install them. Google should have helpful directions.
Step 2: Navigate from the folder containing this file to RPI\_tutor\_time.
Step 3: Edit the settings.py setting to your particular environment. The only thing that should need to be changed is CAMPUS\_EMAIL\_ENDING which is at the bottom.
Step 4: Run 'python manage.py syncdb'. When prompted about a super user, type yes and follow the instructions. This super user can promote tutees to tutors.
Step 5: Run 'python manage.py runserver'. This will start the server. You can now navigate to '127.0.0.1:8000' in your web browswer to view the site.
