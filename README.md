# NLP-Linguistic-Repair-Project

Speech to Speech Machine Translation (SSMT) faces several challenges. There exist many key differences between written and spoken language; during SSMT these differences must be handled before the translation can be done, in order to avoid inaccuracies. Since oral communication (speech) is transient, many sentence constructions are not strictly grammatical. These errors in speech are referred to as disfluencies. Dealing with the disfluencies (in speech transcripts) is referred to as the process of linguistic repair.
The objective of this project is to devise a set of rules and create a system to identify instances of repetition disfluencies in speech transcription, as a precursor to the larger task of SSMT.

The dataset used is the speech transcripts from NPTEL (National Programme on Technology Enhanced Learning) lecture videos of 20-30 minutes each, that have been transcribed by human annotators. The video series selected was the course titled ‘NOC: Natural Language Processing’ (Course ID: 106105158). For each video lecture, files in the following format were provided: <no>_text.txt, <no>_nltk.txt and <no>.srt. The task of repetition identification was performed on the tokenized and preprocessed <no>_nltk.txt files.

'report_final.pdf' lays out the problem with detailed insights and explains our proposed algorithm. Do give it a read.
