# vcf-explorer
Tim Isonio
November 2015

A console based tool to view information from a large VCF file.


Offset File Format
------------------
[VCF file SHA256sum hash]
1    [byte offset]
...  [byte offset]
22   [byte offset]
X    [byte offset]
Y    [byte offset]
MT   [byte offset]
...