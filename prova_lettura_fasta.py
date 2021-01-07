from Bio import SeqIO

def read_fasta():
   k = 15
   kmer = []
   for record in SeqIO.parse("prova.fa", "fasta"):
      sequence = str(record.seq) 
      for x in range(0, len(sequence)-k+1):
        kmer.append(sequence[x:x+k])

   return(kmer)