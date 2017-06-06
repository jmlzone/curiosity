#!/usr/bin/perl
#
# copyleft 2017 James Lee jml@jmlzone.com
# This file is one of many created by or found by James Lee
# <jml@jmlzone.com> to help with the curiosity rover model for stellafane 2017.
# )c( 2017 for curiosity
# All the original files are CopyLeft 2017 James Lee permission is here
# by given to use these files for educational and non-commercial use.
# For commercial or other use please contact the author as indicated in
# the file or jml@jmlzone.com
#
use Sys::Hostname;
my $hostname = hostname;
$|=1;
require "cgi_handlers.pl" ;
$htmlRoot = "/var/www/html";
$docRoot = "/curiosity/missions";
open FI, "{$htmlRoot}${docRoot}/name.txt" || die "Cant open ${htmlRoot}${docRoot}/name.txt";
$currentMission = <FI>;
close(FI);

($mode = $ARGV[0]) =~ s/:.*$//;
&get_request;
if($mode =~ /^post$/){
  &post;
} else {
    &display_full_form;
}
sub display_full_form{
    &html_header("Start a new mission");
    &display_sub_form;
}
sub display_sub_form{
    print <<EOF;
<H1>
Start a new mission on $hostname
</H1>
<a href="/"><img src=/littleman_small.jpg><br>home</a><br>
<form action="/cgi-bin/newMission.pl?post" method="post">
    <input type="text" name="missionName" value="curiosity"> 
    <br>
    Pressing submit will finalize the $currentMission mission and start a new mission
<br> 
    <input name="submit" type="submit" value="submit" />
    <input name="cancel" type="submit" value="cancel" />
</form>

<body>
<hr>
    <a href="/">home</a><br>
    View <a href="$docRoot/mission.html">most recent mission</a><br>
    View all <a href="$docRoot/index.html">Mission Index</a><br>
    <a href="/cgi-bin/motorCal.pl">Motor Calibration</a><br>
    <a href="/cgi-bin/missionBuild.pl">Mission Builder</a><br>
    <a href="/cgi-bin/newMission.pl">Start New Mission</a><br>
    <br>
    <img src=/curiosity.jpg>

</body>
</html>
EOF
}

sub post{
    $missionName = $rqpairs{"missionName"};
    $opt = $rqpairs{"submit"};
    $htmlLog = "${missionName}_log.html";
    if ($opt eq "submit" ) {
	&html_header("Start New Mission");
	if( -e "${htmlRoot}${docRoot}/${htmlLog}") {
	    print "Error a mission with the name $missionName exists on this rover pick another name!\n<br>";
	} else {
	    print "Creating new mission log for $missionName.\n<br>";
	    open(FO, ">${htmlRoot}${docRoot}/name.txt" ) || die "cant open mission name ${htmlRoot}${docRoot}/name.txt\n";
	    print FO "$missionName\n";
	    close(FO);
	    
	    open(FO, ">${htmlRoot}${docRoot}/${htmlLog}" ) || die "cant open mission log ${htmlRoot}${docRoot}/${htmlLog}\n";
	    print FO "Content-type: text/html\n\n";
	    print FO "<html><head>\n";
	    print FO "<title>Curiosity $missionName log</title>\n";
	    print FO "</head>\n<body>\n";
	    print FO "<H1>Curiosity $missionName log</H1>\n";
	    close(FO);
	    unlink("${htmlRoot}${docRoot}/mission.html") if (-e "${htmlRoot}${docRoot}/mission.html");
	    symlink("${htmlRoot}${docRoot}/${htmlLog}", "${htmlRoot}${docRoot}/mission.html");
	    unlink("${htmlRoot}${docRoot}/sequence.txt");
	    if(! -e "${htmlRoot}${docRoot}/index.html") {
		open(FO, ">${htmlRoot}${docRoot}/index.html" ) || die "can't open mission index ${htmlRoot}${docRoot}/$index.html\n";
		print FO <<EOF2;
Content-type: text/html\n\n
<html><head>\n
<title>Curiosity $hostname missions</title>\n
</head>\n<body>\n
<H1>Curiosity $hostname missions</H1>\n
<img src="/curiosity.jpg">
<a href="/">home</a><br>
View <a href="$docRoot/mission.html">most recent mission</a><br>
View all <a href="$docRoot/index.html">Mission Index</a><br>
<a href="/cgi-bin/motorCal.pl">Motor Calibration</a><br>
<a href="/cgi-bin/missionBuild.pl">Mission Builder</a><br>
<a href="/cgi-bin/newMission.pl">Start New Mission</a><br>
<br>
<hr>
<ul>
<li><a href=\"${docRoot}/${htmlLog}\"> Mission ${missionName} mission log</a></li>

EOF2
		    close(FO);
	} else {
	    open(FO, ">>${htmlRoot}${docRoot}/index.html" ) || die "can't open mission index ${htmlRoot}${docRoot}/$index.html\n";
	    print FO "<li><a href=\"${docRoot}/${htmlLog}\"> Mission ${missionName} mission log</a></li>\n";
	    close(FO);
	}
	}
    } else { # run
	&html_header("Cancelled");
    }
    &display_sub_form;
}
