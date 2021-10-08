#!/usr/bin/perl

use strict;
use warnings;
use Getopt::Long;

# Script that extracts sequences that share the same TaxID from two MSA files.

# Input: two MSA (.a3m) files, linker, boolean option to enlong linker

# Prolonged linker has 10 glycine residues on both sides.

# Output: one MSA file (.a3m) for fusion protein modelling

# Example run:
# ./GenFusMSA.pl -i1 A3M/4CL_fullQT.a3m -i2 A3M/CHS_fullQT.a3m -l EAAAK -n 1
# After running this command the prolonged MSA when linker is EAAAK is printed
# to the terminal window.

# Subroutine that prints the usage message
sub usage( ) {
    my $EOF = "$0 extracts sequences that share the same TaxID ".
        "from two MSA files.\n".
        "usage: $0 -i1 file -i2 file -l str [-n int] [p int] [-h]\n".
        "positional arguments\n".
        "\t-i1 file\t: first input .a3m file\n".
        "\t-i2 file\t: second input .a3m file\n".
        "\t-l str\t\t: peptide linker\n".
        "optional arguments\n".
        "\t-n int\t\t: how many repeats of linker (default: 1)\n".
        "\t-p int\t\t: boolean whether to extend the linker (default: 0)\n".
        "\t-h\t\t: this (help) message\n".
        "example: $0 -i1 4CL_fullQT.a3m -i2 CHS_fullQT.a3m -l EAAAK\n";
    print STDERR "$EOF";
    exit;
}

# Subroutine that reads the first input file
sub get_max_length( % ) {
    my %matched = @_;
    my $max_length = 0;
    for my $id ( keys( %matched ) ){
        if( length( $matched{$id} ) > $max_length ) {
            $max_length = length( $matched{$id} )
        }
    }
    return $max_length;
}


# Collecting options
GetOptions(
    'i1=s' => \my $in1,
    'i2=s' => \my $in2,
    'linker=s' => \my $linker,
    'n=s' => \my $n,
    'prolonged=s' => \my $prolonged,
    'help=s' => \my $help
) or usage( );

# Checking if all positional arguments are present or help is called
if((!defined($in1))|(!defined($in2))|(!defined($linker))|(defined($help))) {
    usage();
}

my %taxid_1 = ( );
my %matched = ( );

my $num1 = 0;
my $num2 = 0;

# Reading the first input .a3m file
open(my $inp, '<', $in1) || die "$in1 file not found\n";
$/ = "\n>";
while( <$inp> ) {
    /^>?([^\n]*)\n([^>]*)/;
    my( $header, $sequence ) = ( $1, $2 );
    $sequence =~ s/\s//g;
    if( $sequence ){
        $num1 += 1;
        if( $num1 == 1 ){
            my $taxid = 'query';
            $taxid_1{$taxid} = $sequence;
        }else{
            my @split_header = split(' ', $header);
            $header =~ /TaxID=([[:digit:]]+)/;
            my $taxid = $1;
            $taxid_1{$taxid} = $sequence if($taxid);
        }
    }
}
close($inp);

# Reading the second input .a3m file
open(my $inp, '<', $in2) || die "$in2 file not found\n";;
while( <$inp> ) {
    /^>?([^\n]*)\n([^>]*)/;
    my( $header, $sequence ) = ( $1, $2 );
    $sequence =~ s/\s//g;
    if($sequence){
        $num2 += 1;
        if($num2 == 1){
            my $taxid = 'query';
            $matched{$taxid} = $taxid_1{$taxid} . $sequence;
        }else{
            my @split_header = split(' ', $header);
            $header =~ /TaxID=([[:digit:]]+)/;
            my $taxid = $1;
            if($taxid && exists($taxid_1{$taxid})){
                # Merging sequences that have got matching TaxIDs
                # in both input MSA
                my $merged_seq = $taxid_1{$taxid};
                $merged_seq .= $sequence;
                # Adding merged sequence to the array for the result
                $matched{$taxid} = $merged_seq;
            }
        }
    }
}
close($inp);

# Determining the length of the longest construct
my $max_length = get_max_length( %matched );

# Adding the linker to the output MSA
for my $id ( reverse sort keys(%matched) ){
    my $fusion = substr($matched{$id}, 0, length($taxid_1{$id}));
    if($prolonged){
        $fusion .= 'G' x 10;
        $fusion .= $linker x $n;
        $fusion .= 'G' x 10;
    }else{
        $fusion .= $linker x $n;
    }

    $fusion .= substr($matched{$id}, length($taxid_1{$id}), length($matched{$id}));

    $matched{$id} = $fusion;

    # Printing output MSA
    print '>', $id, "\n", $matched{$id}, "\n";
}
