from Bio import SeqIO

def read_fasta(filename, k):
   kmer = []
   for record in SeqIO.parse(filename, "fasta"):
      sequence = str(record.seq) 
      for x in range(0, len(sequence)-k+1):
        kmer.append(sequence[x:x+k])

   return(kmer)