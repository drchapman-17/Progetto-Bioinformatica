from Bio import SeqIO

records = SeqIO.parse("H3K4me1_chr21.fq", "fastq")
count = SeqIO.write(records, "prova_output_fasta", "fasta")
print("Converted %i records" % count)