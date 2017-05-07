#!/usr/bin/perl
#
# copyleft 2016 James Lee jml@jmlzone.com
# This file is one of many created by or found by James Lee
# <jml@jmlzone.com> to help with the new horizon model for stellafane 2016.
# )c( 2017 for curiosity
# All the original files are CopyLeft 2016 James Lee permission is here
# by given to use these files for educational and non-commercial use.
# For commercial or other use please contact the author as indicated in
# the file or jml@jmlzone.com
#
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
    &html_header("Motor Calibration");
    $dur = 0.50;
    $commmand = "forward";
    &display_sub_form;
}
sub display_sub_form{
    if($command eq "forward") {
	$forwardChecked = "checked";
	$reverseChecked = "";
	$leftChecked = "";
	$rightChecked = "";
    }elsif($command eq "reverse") {
	$forwardChecked = "";
	$reverseChecked = "checked";
	$leftChecked = "";
	$rightChecked = "";
    }elsif($command eq "left") {
	$forwardChecked = "";
	$reverseChecked = "";
	$leftChecked = "checked";
	$rightChecked = "";
    }else{
	$forwardChecked = "";
	$reverseChecked = "";
	$leftChecked = "";
	$rightChecked = "checked";
    }
print <<EOF;
<H1>
Motor Calibration on $hostname
</H1>
<a href="/"><img src=/littleman_small.jpg><br>home</a><br>
<form action="/cgi-bin/motorCal.pl?post" method="post">
Motor duration (between 0.01 and 20) Seconds:
    <input type="number" name="dur" min="0.01" max="20" step=".01" value=$dur> 
    <input type="radio" name="command" value="forward" $forwardChecked> forward
    <input type="radio" name="command" value="reverse" $reverseChecked> reverse
    <input type="radio" name="command" value="left" $leftChecked> left
    <input type="radio" name="command" value="right" $rightChecked> right
    <br>
    <input type="submit"value="Go" />
</form>

<body>
<hr>
    <a href="/">home</a><br>
    Click to <a href="/cgi-bin/launch.sh">launch</a> a new mission<br>
    View <a href="/missions/mission.html">most recent mission</a><br>
    View all <a href="/missions/index.html">mission index</a><br>
    <a href="/cgi-bin/missionParams.pl">Edit Mission Parameters</a><br>
    <a href="/cgi-bin/motorCal.pl">Motor Calibration</a>

</body>
</html>
EOF
}

sub post{
    $dur = $rqpairs{"dur"};
    $command = $rqpairs{"command"};
    &html_header("Motor Calibration Results");
    print "<H1>Motor Calibration Results from $hostname</H1>";
    $output = system("sudo python /home/pi/curiosity/rover/python/motorCal.py $command $dur");
    print $output;
    print "\n<br>\n";
    &display_sub_form;
}
