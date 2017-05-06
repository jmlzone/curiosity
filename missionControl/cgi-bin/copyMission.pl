#!/usr/bin/perl
#
# copyleft 2016 James Lee jml@jmlzone.com
# This file is one of many created by or found by James Lee
# <jml@jmlzone.com> to help with the new horizon model for stellafane 2016.
#
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
    &html_header("Copy Mission");
    $rhost = "nh1";
    $mission = "1";
    &display_sub_form;
}
sub display_sub_form{

print <<EOF;
<H1>
Downoad Mission to Mission Control
</H1>
<form action="/cgi-bin/copyMission.pl?post" method="post">
Copy from :
    <input type="text" name="rhost" size="8" value=$rhost> 
    <input type="number" name="mission" value=$mission> 
    <input type="submit"value="Copy" />
</form>

<body>
<hr>
    <a href="/">home</a><br>
    <a href="/missions">Local Mission Copies</a><br>
</body>
</html>
EOF
}

sub post{
    $rhost = $rqpairs{"rhost"};
    $mission = $rqpairs{"mission"};
    &html_header("Copy Results");
    print "<H1>Copy Results</H1>";
    $output = system("cd /var/www/html/missions; wget -nd -nH -r ${rhost}/missions/mission${mission}.html --reject-regex index -np -l 1 -P ${rhost} -X cgi-bin -k
");
    print $output;
    print "\n<br>\n";
    open(OUT, ">>/var/www/html/missions/index.html") || die "error appending to index";
    print OUT "<a href=\"/missions/${rhost}/mission${mission}.html\"> ${rhost} Mission ${mission}</a><br>\n";
    close(OUT);
    &display_sub_form;
}
