<!DOCTYPE html>
<html lang="en">
<head>
	<link href="main.css" rel="stylesheet">
    <meta charset="UTF-8">
    <title>Meter Project</title>
</head>
<body>
<div class="top">
	<div class="logotype">
		<h1>Logo</h1>
	</div>
	<div class="menu">
		<h2>Menu Menu Menu</h2>
	</div>
</div>
<div class="main">
	<div class="header">
		<?php
		$db = new SQLite3('the_great_db.sqlite');
		if(!$db){
		  echo $db->lastErrorMsg();
		}
		else {
		  echo nl2br("Opened db successfully!\n\n");
		}

    	$tablesquery = $db->query("SELECT name FROM sqlite_master WHERE type='table';");

	    while ($table = $tablesquery->fetchArray(SQLITE3_ASSOC)) {
	        echo $table['name'] . '<br />';
	    }
		
		?>
	</div>
	<div class="results">
		<table>
		  <tr>
		    <th>ID</th>
		    <th>Latest Value</th> 
		    <th>Unit</th>
		    <th>Type</th>
		    <th>Timestamp</th>
		  </tr>		  
		  <?php		
			$results = $db->query('SELECT * FROM house001 WHERE 
				type = "Instantaneous  Volume" AND 
				value != 0 ORDER BY unit_id ASC, datetime DESC');
			while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
			    echo "<tr><td>" . $row['unit_id'] . "</td>";
			    echo "<td>" . $row['value'] . "</td>";
			    echo "<td>" . $row['unit'] . "</td>";
			    echo "<td>" . $row['type'] . "</td>";
			    echo "<td>" . $row['datetime'] . "</td></tr>";
			    //echo nl2br(/*"Type = ". $row['type'] . */"\n\n");
			}
			?>
		</table>
	</div>
</div>
</body>
</html>