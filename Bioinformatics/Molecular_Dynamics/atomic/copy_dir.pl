#!/usr/bin/perl

use strict;
use warnings;

# The script that copies molecular dynamics bundle to the destination
# directory.

my $dest = shift @ARGV;

`cp * $dest`;
`cp -r amber94.ff $dest/amber94.ff`;
