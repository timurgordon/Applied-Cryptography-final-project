
import pandas as pd
import time
from phe import paillier
from cryptography.fernet import Fernet

class Cloud:
    def __init__(self):
        # creates database of songs stored on the HomomorphicCloud object
        self.database = pd.DataFrame()

    def __repr__(self):
        repr = ""
        return repr

    def displayDatabase(self):
        if (not self.database.empty):
            print(self.database.to_string(index=False))
        else:
            print("There are no songs stored in the cloud server!")

    def downloadSongs(self, songs):
        self.database = songs

    def indexQuery(self, index):
        return self.database.loc[index - 1, : ]

    def nameQuery(self, name):
        for index, row in self.database.iterrows():
            if row["Track Name"] == name:
                return row

    def statQuery(self, column, stat_type):
        if stat_type == "average":
            total = 0
            for index, row in self.database.iterrows():
                total += row[column]
            return (total / len(self.database.index))
        if stat_type == "sum":
            total = 0
            for index, row in self.database.iterrows():
                total += row[column]
            return total

class Client:
    def __init__(self, filename):
        self.songs = pd.read_csv(filename)
        self.songs.set_index("Index")
        self.cloud = Cloud()

    def displaySongs(self):
        if (not self.songs.empty):
            print(self.songs.to_string(index=False))
        else:
            print("There are no songs stored in the client object!")

    def uploadSongs(self):
        songs = self.songs
        self.songs = pd.DataFrame()
        self.cloud.downloadSongs(songs)

    def querySongByIndex(self, index):
        return self.cloud.indexQuery(index)

    def querySongByName(self, name):
        return self.cloud.nameQuery(name)

    def queryStats(self, column, stat_type):
        return self.cloud.statQuery(column, stat_type)

class HomomorphicCloud:
    def __init__(self):
        # creates database of songs stored on the HomomorphicCloud object
        self.database = pd.DataFrame()
        self.size_cipher = None
        self.inverse_size = None

    def __repr__(self):
        repr = ""
        return repr

    def displayDatabase(self):
        if (not self.database.empty):
            print(self.database.to_string(index=False))
        else:
            print("There are no songs stored in the cloud server!")

    def downloadSongs(self, songs):
        self.database = songs

    def statQuery(self, column, stat_type, zero_cipher):
        if stat_type == "average":
            total = zero_cipher
            for index, row in self.database.iterrows():
                total += row[column]
            return (total * self.inverse_size)
        if stat_type == "sum":
            total = zero_cipher
            for index, row in self.database.iterrows():
                total += row[column]
            return total

    def setSize(self, size_cipher):
        self.size_cipher = size_cipher

    def setInverseSize(self, inverse_size):
        self.inverse_size = inverse_size


class HomomorphicClient:
    def __init__(self, filename):
        self.songs = pd.read_csv(filename)
        self.songs.set_index("Index")
        self.cloud = HomomorphicCloud()
        self.public_key, self.private_key = paillier.generate_paillier_keypair()
        self.aes_key = Fernet.generate_key()
        self.fernet = Fernet(self.aes_key)

    def displaySongs(self):
        if (not self.songs.empty):
            print(self.songs.to_string(index=False))
        else:
            print("There are no songs stored in the client object!")

    def uploadSongs(self):
        for index, row in self.songs.iterrows():
            for column in self.songs.keys():
                if isinstance(row[column], int):
                    self.songs.at[index, column] = self.public_key.encrypt(row[column])
                else:
                    self.songs.at[index, column] = self.fernet.encrypt(row[column].encode())
        songs = self.songs
        self.cloud.downloadSongs(songs)
        self.cloud.setSize(self.public_key.encrypt(len(songs.index)))
        self.cloud.setInverseSize(1 / len(songs.index))
        self.songs = pd.DataFrame()

    def queryStats(self, column, stat_type):
        encrypted_response = self.cloud.statQuery(column, stat_type, self.public_key.encrypt(0))
        return self.private_key.decrypt(encrypted_response)

def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    files = ["your_top_songs_2019_2.csv", "large_magic_fm_playlist.csv", "incredibly_large_playlist.csv"]

    print("Creating client and cloud objects...")
    testClient = Client("your_top_songs_2019.csv")

    print("Before uploading to cloud, all songs are stored in the client object:\n")
    testClient.displaySongs()
    testClient.cloud.displayDatabase()

    print("Client is uploading songs to cloud server...")
    testClient.uploadSongs()

    print("After uploading to cloud, all songs are stored in the cloud object.\n")
    testClient.displaySongs()
    testClient.cloud.displayDatabase()

    print("Client is making queries to cloud server...")

    print("Client is querying the song stored at index 6...")
    print(testClient.querySongByIndex(6))

    print("Client is querying the song stored at index 6...")
    print(testClient.querySongByIndex(6))

    print("Client is querying the song stored at index 12...")
    print(testClient.querySongByIndex(12))

    print("Client is querying the song named \"Sisters of Arequipa\"....")
    print(testClient.querySongByName("Sisters of Arequipa"))

    print("Client is querying for average length of songs in the playlist...")
    print(testClient.queryStats("Track Duration (ms)", "average"))

    print("Client is querying for average play count for songs in the playlist...")
    print(testClient.queryStats("Play Count", "average"))

    print("Client is querying for the total length of the tracks in playlist...")
    print(testClient.queryStats("Track Duration (ms)", "sum"))

    print("Client is querying for the total play count of the playlist...")
    print(testClient.queryStats("Play Count", "sum"))

    print("=================================================================================================\n")
    print("HOMOMORPHIC CLIENT-CLOUD")
    print("=================================================================================================\n")

    print("Creating homomorphic client and cloud objects...")
    testCryptoClient = HomomorphicClient("your_top_songs_2019.csv")

    print("Before uploading to homomorphic cloud, all songs are stored in the homomorphic client object:\n")
    testCryptoClient.displaySongs()
    testCryptoClient.cloud.displayDatabase()

    print("Client is uploading homomorphically encrypted songs to cloud server...")
    testCryptoClient.uploadSongs()

    print("After uploading to cloud, all songs are stored in the cloud object with homomorphic encryption.\n")
    testCryptoClient.displaySongs()
    testCryptoClient.cloud.displayDatabase()

    print("Client is querying for average length of songs in the playlist...")
    print(testCryptoClient.queryStats("Track Duration (ms)", "average"))

    print("Client is querying for average play count for songs in the playlist...")
    print(testCryptoClient.queryStats("Play Count", "average"))

    print("Client is querying for the total length of the tracks in playlist...")
    print(testCryptoClient.queryStats("Track Duration (ms)", "sum"))

    print("Client is querying for the total play count of the playlist...")
    print(testCryptoClient.queryStats("Play Count", "sum"))

    print("=================================================================================================\n")
    print("UNENCRYPTED vs. ENCRYPTED SHEMES PERFORMANCE")
    print("=================================================================================================\n")

    time_data = {}
    secure_time_data = {}

    for filename in files:
        client = Client(filename)

        start_upload = time.perf_counter()
        print("Measuring upload speed...")
        client.uploadSongs()
        end_upload = time.perf_counter()
        upload_duration = end_upload - start_upload

        start_query = time.perf_counter()
        print("Measuring query speed...")
        client.queryStats("Track Duration (ms)", "average")
        client.queryStats("Play Count", "average")
        client.queryStats("Track Duration (ms)", "sum")
        client.queryStats("Play Count", "sum")
        end_query = time.perf_counter()
        query_duration = end_query - start_query

        time_data[filename] = [upload_duration, query_duration]

    for filename in files:
        secure_client = HomomorphicClient(filename)

        start_upload = time.perf_counter()
        print("Measuring upload speed...")
        secure_client.uploadSongs()
        end_upload = time.perf_counter()
        upload_duration = end_upload - start_upload

        start_query = time.perf_counter()
        print("Measuring query speed...")
        secure_client.queryStats("Track Duration (ms)", "average")
        secure_client.queryStats("Play Count", "average")
        secure_client.queryStats("Track Duration (ms)", "sum")
        secure_client.queryStats("Play Count", "sum")
        end_query = time.perf_counter()
        query_duration = end_query - start_query

        secure_time_data[filename] = [upload_duration, query_duration]

    print(time_data)
    print(secure_time_data)

main()