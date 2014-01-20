===========
Tab manager
===========

This is simple django app for managing tab:s.

Users can register and add items to eace others tab:s.

Quick start
-----------
1. Add "tapmanager to your INSTALLED_APPS settings like this::

	INSTALLED_APPS = (
		...
		'tapmanager',
	)

2. Include the polls URLconf in your project urls.py like this::
		
	url(r'^tapmanager/', include('tapmanager.urls')),

3. You need to configure LOGIN_URL in your settings file also becouse this app handels login and registration also.

4. Run 'python manage.py syncdb' to create models.

5. You are ready to test it´.

