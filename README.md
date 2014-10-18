AskArbie
========
Ask Arbie is a web application for RBC customers that automatically groups investors based on their financial goals, risk profiles, and types of investments; it then compares your performance to others in your class, and provides personalized recommendations.

Ask Arbie automatically builds you a profile based on your investment history and your current investments, assessing your investment risks and average rate of return. Based on your profile, as well as the profiles of all other investors with RBC, you are placed in a category with similar investors (with similar financial interests, risk profile, annual income…). Based on this information, Ask Arbie identifies a benchmark of how well your investments are doing relative to the average of investors in your category, and recommends intelligent/realistic investment decisions based on successful investments made by others in your category.

The main idea behind Ask Arbie is that it empowers RBC customers to explore intelligent investment opportunities and set realistic financial goals for themselves. 

###Dependencies:
1. Python 3.3
2. Django 1.7.3
3. SciPy Stack

###For Ubuntu & Debian
1. sudo apt-get install python3.3
2. sudo apt-get install python-pip
3. (Optional) sudo pip install virtualenv
4. (Optional) virtualenv ENV
5. sudo pip install Django==1.7.3
6. sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose
7. change url.py appropriately
8. In settings.py, change DATABASES['NAME'], MEDIA_ROOT, STATIC_ROOT to match local paths
9. python manage.py syncdb
10. python manage.py runserver

