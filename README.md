<br>
<div align="center">
<h1>AudioFusion</h1>
<i>A package that allows to edit your music file however you want with effects like slowed reverb and 8d.</i>
</div>

<br><hr><br>
More effects and method will be added soon<br>
PR in [github repository](https://github.com/MineisZarox/AudioFusion) beta branch are always welcome.

For more immersive usage and possibilities check out [pydub](https://github.com/jiaaro/pydub)<br>
Working Web application based on this library - [AudioFuser](https://huggingface.co/spaces/zarox/AudioFusion)

## Installation:

```bash
>>> python3 -m pip install AudioFusion
```

## Usage:

```python
>>> from AudioFusion import Fusion
>>> # from AudioFusion.async import Fusion

>>> # Load your music file
>>> music = Fusion.loadSound("/path/to/your/music.mp3")

>>> # Add effects
>>> music = Fusion.effect8D(music)
>>> music = Fusion.effectSlowed(music)
>>> music = Fusion.effectReverb(music)

>>> # Save your edited music file
>>> Fusion.saveSound(music, "finalMusic")


```


<h2>Advanced Usage:</h2>

```python
>>> from AudioFusion import Fusion


>>> # Load your music file
>>> music = Fusion.loadSound("/path/to/your/music.mp3")

>>> # Add effects
>>> music = Fusion.effect8D(
        music,
        panBoundary = 100,  # Perctange of dist from center that audio source can go
        jumpPercentage = 5,  # Percentage of dist b/w L-R to jump at a time
        timeLtoR = 10000,  # Time taken for audio source to move from left to right in ms
        volumeMultiplier = 6  # Max volume DB increase at edges
)

>>> music = Fusion.effectSlowed(music, speedMultiplier: float = 0.92 ): # Slowdown audio, 1.0 means original speed, 0.5 half speed etc

>>> music = Fusion.effectReverb(
        music,
        roomSize = 0.8, 
        damping = 1,
        width = 0.5,
        wetLevel = 0.3,
        dryLevel = 0.8,
        tempFile = "tempWavFileForReverb"
    )

>>> # Save your edited music file
>>> Fusion.saveSound(music, "finalMusic")

```

## Todo

\# Acapella Extractor<br>
\# Karoke Maker<br>
\# Bass Booster<br>
\# Volume Booster<br>


## Inspiration & Credits

- Special thanks to [Jiaaro](https://github.com/jiaaro) for pydub. AudioFusion is mainly wrapped around pydub
- Thanks to [Rohan](https://github.com/dashroshan) for his [8d-slow-reverb](https://github.com/dashroshan/8d-slow-reverb) repository

- My Soundscapes of Serenity - [Because](https://t.me/bcuzwhynot)