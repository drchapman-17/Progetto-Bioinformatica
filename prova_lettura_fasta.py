from Bio import SeqIO

def read_fasta():
   k = 10
   kmer = []
   for record in SeqIO.parse("prova.fa", "fasta"):
      sequence = str(record.seq) 
      for x in range(1, len(sequence)-k):
        kmer.append(sequence[x:x+k])
   return(kmer)