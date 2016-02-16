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
		<h1>Menu</h1>
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
		  //echo nl2br("Opened db successfully!\n\n");
		}
		?>
	</div>
	<div class="results">
		<table>
		  <tr>
		    <th>ID</th>
		    <th>Latest Value</th> 
		    <th>Unit</th>
		    <th>Description</th>
		    <th>Function</th>
		    <th>Timestamp</th>
		  </tr>
		  <?php
	    	$tablesquery = $db->query("SELECT name FROM sqlite_master WHERE type='table';");
		    while ($table = $tablesquery->fetchArray(SQLITE3_ASSOC)) {
		        // echo $table['name'] . '<br />';
			    $sql = "SELECT * FROM '".$table['name']."' ORDER BY unit_id ASC, datetime DESC";
				$results = $db->query($sql);
				while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
				    echo "<tr>";
                    echo "<td>" . $row['unit_id'] . "</td>";
				    echo "<td>" . $row['value'] . "</td>";
				    echo "<td>" . $row['unit'] . "</td>";
				    echo "<td>" . $row['description'] . "</td>";
				    echo "<td>" . $row['function'] . "</td>";
				    echo "<td>" . $row['datetime'] . "</td>";
				    echo "</tr>";
				    //echo nl2br(/*"Type = ". $row['type'] . "\n\n");
				}
			}
			?>
		</table>
	</div>
</div>
</body>
</html>