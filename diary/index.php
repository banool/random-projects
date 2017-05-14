<?php
echo "<b>Entries</b></br></br>";
$path = "./entries";
$dh = opendir($path);
$files = array();
while(false != ($file = readdir($dh))) {
    if($file != "." && $file != ".." && $file != "index.php" && $file != "github-markdown.css" && $file != ".htaccess" && $file != "error_log" && $file != "cgi-bin") {
        $files[] = $file;
    }
}

natsort($files);

foreach($files as $file) {
    $withoutExt = preg_replace('/\\.[^.\\s]{3,4}$/', '', $file);
    echo "<a href='$path/$file'>$withoutExt</a><br /><br />";
}
closedir($dh);
?> 

