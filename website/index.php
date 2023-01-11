<?php
//index.php
$depart = '';
$arrive = '';

function clean_text($string)
{
	$string = trim($string);
	$string = stripslashes($string);
	$string = htmlspecialchars($string);
	
	return $string;
}


if(isset($_POST["submit"]))
{
	if(empty($_POST["depart"]))
	{
		$error .= '<p><label class = "text-danger"> Error, Must contain something. </label></p>';
	}
	else
	{
		$depart = clean_text($_POST["depart"]);
		
		if(!preg_match("/^[a-zA-Z]*$/", $depart))
		{
			$error .= '<p><label class = "text-danger"> Error </label> </p>';
		}
	}
	
	if(empty($_POST["arrive"]))
	{
		$error .= '<p><label class = "text-danger"> Error, Must contain something. </label></p>';
	}
	else
	{
		$arrive = clean_text($_POST["arrive"]);
		if(!preg_match("/^[a-zA-Z]*$/", $arrive))
		{
			$error .= '<p><label class = "text-danger"> Error </label> </p>';
		}
		
	}
	
	if($error == '')
	{
		$file_open = fopen("ticket_data.csv", "a");
		$no_rows = count(file("ticket_data.csv"));
		
		if($no_rows > 1)
		{
			$no_rows = ($no_rows - 1) + 1;
		}
		$form_data = array(
		
		'sr_no' 	  => $no_rows,
		'departInput' => $depart,
		'arriveInput' => $arrive
		
		);
		fputcsv($file_open, $form_data);
		$error = '<label class = "text-success"> Input Accepted </label>';

		$depart = '';
		$arrive = '';
	}


}



?>
