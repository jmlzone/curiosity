#!/usr/bin/perl
#
# copyleft 201y James Lee jml@jmlzone.com
# This file is one of many created by or found by James Lee
# <jml@jmlzone.com> to help with the curiosity rover model for stellafane 2017.
# )c( 2017 for curiosity
# All the original files are CopyLeft 2017 James Lee permission is here
# by given to use these files for educational and non-commercial use.
# For commercial or other use please contact the author as indicated in
# the file or jml@jmlzone.com
#
@cmdList=("forward","reverse","left","right","mast","nod","widdle","cameraHR","cameraHS");
use Sys::Hostname;
my $hostname = hostname;
$|=1;
require "cgi_handlers.pl" ;
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
Mission Task List Builder on $hostname
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
    <input type="submit" value="Add" />
<textarea name="missionList" rows="5" cols="50">
$missionList
</textarea>
    <input type="submit" value="Run" />
</form>

<body>
<hr>
    <a href="/">home</a><br>
    Click to <a href="/cgi-bin/launch.sh">launch</a> a new mission<br>
    View <a href="/missions/mission.html">most recent mission</a><br>
    View all <a href="/missions/index.html">mission index</a><br>
    <a href="/cgi-bin/missionBuild.pl">Mission Task List Builder</a><br>
    <a href="/cgi-bin/motorCal.pl">Motor Calibration</a>

</body>
</html>
EOF1
}

sub post{
    $cmd = $rqpairs{"cmd"};
    $cnt = $rqpairs{"cnt"};
    $missionList = join( " ", $rqpairs{"missionList"}, $cmd, $cnt)
    &html_header("Build Mission Task List");
    print "<H1>Mission Task List Building on $hostname</H1>";
    #$output = system("sudo python /home/pi/curiosity/rover/python/motorCal.py $command $dur");
    #print $output;
    print "\n<br>\n";
    &display_sub_form;
}

