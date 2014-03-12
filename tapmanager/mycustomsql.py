from django.db import connection

def my_custom_sql():
	cursor = connection.cursor()
	cursor.execute("""
	SELECT firstname, lastname, username, userid AS id, CASE WHEN sum(pr*amount) IS NULL THEN 0.00 ELSE round(sum(pr*amount),2) END AS totalsum FROM
		(SELECT tap.firstname AS firstname, tap.lastname AS lastname, tap.username AS username, tap.id AS userid, tap.amount AS amount, type.name AS typename, CASE WHEN type.price IS NULL THEN 1 ELSE type.price END AS pr FROM
			(SELECT tap.taptype_id, tap.user_id, tap.amount, userr.username, userr.id, userr.firstname, userr.lastname FROM
				(SELECT * FROM tapmanager_tap WHERE active=True) AS tap
				RIGHT JOIN
				(SELECT auth_user.first_name AS firstname, auth_user.last_name AS lastname, auth_user.username, auth_user.id FROM auth_user_groups, auth_user 
					WHERE auth_user_groups.user_id = auth_user.id AND auth_user_groups.group_id = (SELECT id FROM auth_group WHERE name='tapmanager')) AS userr
					ON userr.id = tap.user_id) AS tap
			LEFT JOIN
			(SELECT id, name, CASE WHEN type.price IS NULL THEN 1 ELSE type.price END AS price FROM tapmanager_taptype AS type WHERE active=True) AS type
				ON tap.taptype_id = type.id) AS final GROUP BY userid, username, firstname, lastname ORDER BY username;
""")
	desc = cursor.description
	return [ dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall() ]




