<html>
<head>
	<title>PHP Form Test</title>
	<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
</head>
<body>
	<h2>Enter service and password here</h2>
	<form action="test.php" method="post">
	<select name="Team">
	<option value="1">Team 1</option>
	<option value="2">Team 2</option>
	<option value="3">Team 3</option>
	<option value="4">Team 4</option>
	<option value="5">Team 5</option>
	</select>
	<select name="Service">
	<option value="mail">Email</option>
	<option value="ssh">SSH</option>
	<option value="DHCP">DHCP</option>
	<option value="DNS">DNS</option>
	</select>
	Current Password: <input type="password" name="oldpass">
	New Password: <input type="password" name="newpass"/>
	<input type="submit" value="Submit">
	</form>
	<?php
		$team = $_POST['Team'];
		$service = $_POST['Service'];
		$old_pass = $_POST['oldpass'];
		$new_pass = $_POST['newpass'];
		$con = mysql_connect("localhost","whiteTeam","CCDC623");
		if(!$con)
		{
			die('Could not connect: ' . mysql_error());
		}
		mysql_select_db("CCDC",$con);
		$query_string = "SELECT * FROM passwords WHERE team_id ='".$team."' AND service='".$service."'";
		$result = mysql_query($query_string);
		while($row = mysql_fetch_array($result))
		{
			if($old_pass == $row['password'])
			{
				$update_string = "UPDATE passwords SET password='".$new_pass."' WHERE team_id = '".$team."'"." AND service='".$service."'";
				print "Password changed";
				$result=mysql_query($update_string);
			}
			else
			{
				print "Password mismatch";
			}
		}
		mysql_close($con);
	?>
</body>
</html>

