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
@cmdList=("forward","reverse","left","right","nod","arm","camera", "cameraHS","cameraRF", "cameraRFHS","cameraVid","mast");
use Sys::Hostname;
my $hostname = hostname;
$|=1;
require "cgi_handlers.pl" ;
$htmlRoot = "/var/www/html";
$docRoot = "/curiosity/missions";
open FI, "$htmlRoot$docRoot/name.txt" || die "Cant open $htmlRoot$docRoot/name.txt";
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
    &html_header("Mission Task List Builder");
    $cnt = 1;
    $missionList = "";
    &display_sub_form;
}
sub display_sub_form{
    print <<EOF;
<H1>
Mission $currentMission Task List Builder on $hostname
</H1>
<a href="/"><img src=/littleman_small.jpg><br>home</a><br>
<form action="/cgi-bin/missionBuild.pl?post" method="post">
<select name="command">
EOF
foreach $cmd (@cmdList) {
    print "<option value=\"$cmd\">$cmd</option>\n"
}
    print <<EOF1;
</select>
    <input type="number" name="cnt" min="0.01" max="20" step=".01" value=$cnt> 
    <br>
    <input name="submit" type="submit" value="Add" />
<textarea name="missionList" rows="5" cols="50">
$missionList
</textarea>
    <input name="submit" type="submit" value="Run" />
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
EOF1
}

sub post{
    $cmd = $rqpairs{"command"};
    $cnt = $rqpairs{"cnt"};
    $opt = $rqpairs{"submit"};
    $ml = $rqpairs{"missionList"};
    $missionList = "$ml $cmd $cnt";
    $missionList =~ s/\n//g;
    if ($opt eq "Add" ) {
	&html_header("Build $currentMission Mission Task List");
#        print "opt = $opt, cmd = $cmd, cnt = $cnt, ml = $rqpairs{\"missionList\"} \n $missionList ";
	print "\n<br>\n";
	&display_sub_form;
    } else { # run
	&html_header("Running Mission Task List");
	print "<H1>Curiosity Running Mission $currentMisstion Task List on $hostname</H1>\n";
	print "\n<br>\n";
	print "<pre>\n";
	$output = system("sudo python /home/pi/curiosity/rover/python/taskRun.py $missionList");
	$output =~ s/\n/<br>\n/sg;
	print $output;
	print "</pre>\n";
    }
}
