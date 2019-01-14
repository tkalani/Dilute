<?php

if (($_POST["flag"] == 0 || $_POST["flag"] == 1) && $_POST["actuator_id"]) {
	$flag = $_POST["flag"];
	$act_id = $_POST["actuator_id"];
	echo $flag, " ", $act_id;
	$out = shell_exec("python /home/pi/Desktop/actuator.py $flag $act_id 2>&1");
	echo "<pre>$out</pre>";
}
else {
	echo "GET REQUEST TO ACTUATOR SERVER";
}
?>
