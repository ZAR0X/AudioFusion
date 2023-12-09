import os

import soundfile
from pydub import AudioSegment
from pedalboard import (
    Pedalboard,
    Reverb,
)


class Fusion(AudioSegment):
    class InvalidMusicFileError(Exception):
        def __init__(self, file_name):
            self.file_name = file_name
            super().__init__(f"Invalid music file: {file_name}. File not found or not recognized as a valid music file.")

    @classmethod
    def loadSound(cls, inputFile: str):
        """
        Loads and returns the MP3 or WAV (whichever is found) source sound file.
        Stops program execution if file not found.
        """

        if os.path.isfile(inputFile) and inputFile.lower().endswith(('.mp3', '.wav', '.aac', '.ogg', '.flac', '.m4a')):
            return cls.from_file(inputFile, format=inputFile.split(".")[-1])
        else:
            raise cls.InvalidMusicFileError(inputFile)

    @classmethod
    def effect8D(
        cls,
        sound,
        panBoundary: int = 100,  # Perctange of dist from center that audio source can go
        jumpPercentage: int = 5,  # Percentage of dist b/w L-R to jump at a time
        timeLtoR: int = 10000,  # Time taken for audio source to move from left to right in ms
        volumeMultiplier: int = 6  # Max volume DB increase at edges
    ):
        """
        Generates the 8d sound effect by splitting the audio into multiple smaller pieces,
        pans each piece to make the sound source seem like it is moving from L to R and R to L in loop,
        decreases volume towards center position to make the movement sound like it is a circle
        instead of straight line.
        """
        piecesCtoR = panBoundary / jumpPercentage

        # Total pieces when audio source moves from extreme left to extreme right
        piecesLtoR = piecesCtoR * 2

        # Time length of each piece
        pieceTime = int(timeLtoR / piecesLtoR)

        pan = []
        left = -panBoundary  # Audio source to start from extreme left

        while left <= panBoundary:  # Until audio source position reaches extreme right
            pan.append(left)  # Append the position to pan array
            left += jumpPercentage  # Increment to next position

        # Above loop generates number in range -100 to 100, this converts it to -1.0 to 1.0 scale
        pan = [x / 100 for x in pan]

        sound8d = sound[0]  # Stores the 8d sound
        panIndex = 0  # Index of current pan position of pan array

        # We loop through the pan array forward once, and then in reverse (L to R, then R to L)
        iteratePanArrayForward = True

        # Loop through starting time of each piece
        for time in range(0, len(sound) - pieceTime, pieceTime):

            # time + pieceTime = ending time of piece
            piece = sound[time : time + pieceTime]

            # If at first element of pan array (Left) then iterate forward
            if panIndex == 0:
                iteratePanArrayForward = True

            # If at last element of pan array (Right) then iterate backward
            if panIndex == len(pan) - 1:
                iteratePanArrayForward = False

            # (panBoundary / 100) brings panBoundary to the same scale as elements of pan array i.e. -1.0 to 1.0
            # abs(pan[panIndex]) / (panBoundary / 100) = 1 for extreme left/right and 0 for center
            # abs(pan[panIndex]) / (panBoundary / 100) * volumeMultiplier = volumeMultiplier for extreme left/right and 0 for center
            # Hence, volAdjust = 0 for extreme left/right and volumeMultiplier for center
            volAdjust = volumeMultiplier - (
                abs(pan[panIndex]) / (panBoundary / 100) * volumeMultiplier
            )

            # Decrease piece volume by volAdjust i.e. max volume at extreme left/right and decreases towards center
            piece -= volAdjust

            # Pan the piece of sound according to the pan array element
            pannedPiece = piece.pan(pan[panIndex])

            # Iterates the pan array from left to right, then right to left, then left to right and so on..
            if iteratePanArrayForward:
                panIndex += 1
            else:
                panIndex -= 1

            # Add this panned piece of sound with adjusted volume to the 8d sound
            sound8d = sound8d + pannedPiece

        return sound8d

    @classmethod
    def effectSlowed(cls, sound, speedMultiplier: float = 0.92 ): # Slowdown audio, 1.0 means original speed, 0.5 half speed etc
        """
        Increases sound frame rate to slow it down.
        Returns slowed down version of the sound.
        """

        soundSlowedDown = sound._spawn(
            sound.raw_data,
            overrides={"frame_rate": int(sound.frame_rate * speedMultiplier)},
        )
        soundSlowedDown.set_frame_rate(sound.frame_rate)
        return soundSlowedDown


    @classmethod
    def effectReverb(
        cls,
        sound,
        roomSize: float = 0.8, 
        damping: float = 1,
        width : float = 0.5,
        wetLevel: float = 0.3,
        dryLevel: float= 0.8,
        tempFile: str = "tempWavFileForReverb"
    ):
        """
        Adds reverb effect to the sound.
        """
        outputFile = tempFile+".wav"
        # Convert the sound to a format usable by the pedalboard library
        with open(outputFile, "wb") as out_f:
            sound.export(out_f, format="wav")
        sound, sampleRate = soundfile.read(outputFile)

        # Define the reverb settings
        addReverb = Pedalboard(
            [Reverb(room_size=roomSize, damping=damping, width=width, wet_level=wetLevel, dry_level=dryLevel)]
        )

        # Add the reverb effect to the sound and return
        reverbedSound = addReverb(sound, sample_rate=sampleRate)
        with soundfile.SoundFile(outputFile, "w", samplerate=sampleRate, channels=sound.shape[1]) as f:
            f.write(sound)
        sound = cls.from_wav(outputFile)
        os.remove(outputFile)
        return sound

    @classmethod
    def saveSound(cls, sound, outputFile: str = "output"):
        """
        Save the sound in MP3 format.
        """
        sound.export(outputFile + ".mp3", format="mp3")
        return f"{outputFile}.mp3"


