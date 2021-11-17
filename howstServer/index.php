<?php
$data=explode("\n",file_get_contents("php://input"));
$arPrev=file("data.csv",FILE_SKIP_EMPTY_LINES);
$af=array_merge($arPrev,$data);
for($i=0;$i<count($af);$i++){
	$af[$i]=trim($af[$i])."\n";
}
function normalizeDate($a){
	 $aL = explode(";",$a);
     $aL[0] = str_replace("\"","",$aL[0]);
     $aL[1] = str_replace("\"","",$aL[1]);
     $d = explode("/",$aL[0]);
     $t = explode(":",$aL[1]);
     return 86400*($d[0]+$d[1]*30+$d[2]*365)+$t[0]*3600+$t[1]*60;
}
function cmp($a, $b)
{
	return normalizeDate($a) <=> normalizeDate($b);
}

usort($af, "cmp");
$af = array_unique($af);
file_put_contents("data.csv",implode("",$af));
