<?php
echo '<meta name="robots" content="noindex,nofollow">';
echo "<b>Entries</b></br></br>";
$path = "./entries";
$dh = opendir($path);
$files = array();
$others = array();
while(false != ($file = readdir($dh))) {
    if($file != "." && $file != ".." && $file != "index.php" && $file != "github-markdown.css" && $file != ".htaccess" && $file != "error_log" && $file != "cgi-bin") {
        if(ereg("^[0-9]{4}-[0-9]{2}-[0-9]{2}.html$", $file)){
            $files[] = $file;
        } else {
            $others[] = $file;
        }
    }
}

natsort($files);
natsort($others);

foreach($files as $file) {
    $withoutExt = preg_replace('/\\.[^.\\s]{3,4}$/', '', $file);
    echo "<a href='$path/$file'>$withoutExt</a><br /><br />";
}

echo "<b>Others</b></br></br>";
foreach($others as $file) {
    $withoutExt = preg_replace('/\\.[^.\\s]{3,4}$/', '', $file);
    echo "<a href='$path/$file'>$withoutExt</a><br /><br />";
}
closedir($dh);
?> 

