from Bio import SeqIO

k = 10
kmeri = []
for record in SeqIO.parse("prova.fa", "fasta"):
    sequence = str(record.seq) 
    print(len(sequence))
    for x in range(1, len(sequence)-k):
       kmeri.append(sequence[x:x+k])
    print(kmeri)