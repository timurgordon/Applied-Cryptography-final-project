# Applied-Cryptography-final-project
Partial Homomorphic Encryption for Statistical Queries on Music Stored in a Cloud Server

README.md

Project Type: 3
Project Title: Partial Homomorphic Encryption for Statistical Queries on Music Stored in Cloud Server
Timur Blair Gordon
May 13, 2020

1. Basic Information:

The software simulates interactions between a client and a cloud server. The first part of the code simulates these interactions without any encryption. The second part of the code simulates the same interactions in a symmetric encryption scheme, in order to check for encryption/decryption correction of the results of the queries. Alphabetical data is encrypted using AES encryption via the cryptography module in python (https://github.com/pyca/cryptography). Numerical data is encrypted using the PHE module in python (https://github.com/data61/python-paillier).

The client uploads a list of tracks to the cloud server and makes a number of queries. The performance of the encrypted and plain scheme are compared both in terms of upload speed and query response speed, across multiple datasets with varying size. In the third part the times for each implementation for each dataset is recorded for performance comparison.

2. Dataset:

The datasets consist of three separate Spotify playlists exported into csv.
The first playlist is the top 100 songs I listened to in 2019, created by Spotify. The second and third playlists are “Large Magic FM Playlist” by the Spotify user “thevictoriabararmagh” and “incredibly large playlist” by the Spotify user “Jordan Wickham”. The csv files don’t contain the song files themselves for storage purposes. The csv files were altered with the addition of an index column and a Play Count column for experimental purposes. Each dataset has the same columns: Index, Track Name, Artist Name, Album Name, Play Count, Track Duration (ms). 

The first dataset has 100 tracks, the second has 608 tracks, and the third has 1042 tracks. The datasets increase in size to better compare the performance of the encrypted and unencrypted schemes. 

3. Software Information:

The code is implemented in python 3. 
Path to main software file: Applied-Cryptography-final-project/code_folder/venv/main.py 
