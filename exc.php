<html>
<body>

 


Welcome
<?php echo $_GET["name"]; 
    $username=$_GET["name"];
	echo ('<br>');
    $tmp = shell_exec("python script.py $username");
	echo $tmp;
    

?>

</body>
</html>