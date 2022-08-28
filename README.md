# Recomendify
Python implementation of a music recommendation system using Graphs and different algorithms such as PageRank, Graph traversals (BFS, DFS, Etc) among other functionalities.

## Introduction and Objectives 
The main objective of Recomendify is to build a recommendation system using [Graphs](https://en.wikipedia.org/wiki/Graph_(abstract_data_type)#:~:text=A%20graph%20data%20structure%20consists,pairs%20for%20a%20directed%20graph.) for a music streaming service that could give song, playlists and user recommendation based on what a specific user enjoys and what others with similar taste are listenning. 

To achieve this, we used a processed .TSV file that was created from a larger dataset published by the [RecSys Challenge 2018](https://www.recsyschallenge.com/2018/) that had the following format:
```
ID	USER_ID	TRACK_NAME	ARTIST	PLAYLIST_ID	PLAYLIST_NAME	GENRES
1	sitevagalume	Eraser	Ed Sheeran	6736120	Ed Sheeran - Divide	Pop,Rock,Pop/Rock
2	sitevagalume	Castle On The Hill	Ed Sheeran	6736120	Ed Sheeran - Divide	Pop,Rock,Pop/Rock
3	sitevagalume	Dive	Ed Sheeran	6736120	Ed Sheeran - Divide	Pop,Rock,Pop/Rock
```

While processing each line, we created and populated 2 different graphs:
* An undirected bipartite graph that connected users and songs if a user liked a specific song.
* An undirected graph that connected songs between each other if they appeared in a playlist of a given user. 

## Commands and Usage
In order to use Recomendify, download both the code and the [processed .TSV file](https://drive.google.com/file/d/19piQbkrmO3GAt0ItekldWK4TbnMtAyGi/view?usp=sharing). Make sure the .TSV file into the same directory as the rest of the source code. 

To initiate the program on Unix based systems, run:
```
./recomendify spotify-procesado.tsv
```

Keep in mind that you could pass instructions from a file using for example a .TXT file:
```
./recomendify spotify-procesado.tsv < entrada.txt
```

In order to use the program, there are different commands that one could use:
 
### Shortest path
Prints a list that connects 2 songs with the least ammounts of songs in possible in between each other.

* Command: `camino`.
* Input Parameters: `origen` and `destino` (separated by `>>>>`). Origen and destino are songs. 
* Examples:
```
Input:
    
    camino Don't Go Away - Oasis >>>> Quitter - Eminem
    camino yarits >>>> Quitter - Eminem
    camino Oops!...I Did It Again - Britney Spears >>>> Love Story - Taylor Swift
    camino Mr. Brightside - The Killers >>>> Grow Old With Me - Tom Odell
    
Output:
    
    Don't Go Away - Oasis --> aparece en playlist --> misturo tudãao ;x --> de --> 8902446 --> tiene una playlist --> sóo nacionais' --> donde aparece --> Ela Vai Voltar (Todos Os Defeitos de Uma Mulher Perfeita) - Charlie Brown Jr --> aparece en playlist --> Playlist da Yara --> de --> yarits --> tiene una playlist --> Playlist da Yara --> donde aparece --> Quitter - Eminem
    Tanto el origen como el destino deben ser canciones
    Oops!...I Did It Again - Britney Spears --> aparece en playlist --> Britney Spears --> de --> aline_hdb --> tiene una playlist --> Só Antigas --> donde aparece --> I Will Always Love You - Whitney Houston --> aparece en playlist --> romaticas --> de --> joyce9224 --> tiene una playlist --> musicas --> donde aparece --> Love Story - Taylor Swift
    No se encontro recorrido
```

In case `origin` or `destino` are not valid songs, an error message is printed.

### Most important songs
Prints the `n` most important songs on the graph network by using the concept of centrality from the [PageRank algorithm](https://es.wikipedia.org/wiki/PageRank). The songs are sorted from most to least important.

* Command: `mas_importantes`.
* Input Parameters: `n`, amount of important songs requested.
* Example:
```
Input:

    mas_importantes 20
  
Output:
    
    Bad Romance - Lady Gaga; Poker Face - Lady Gaga; Telephone (feat. Beyoncé) - Lady Gaga; Paparazzi - Lady Gaga; Halo - Beyoncé; Viva La Vida - Coldplay; Single Ladies (Put a Ring on It) - Beyoncé; Decode - Paramore; In The End - Linkin Park; Levo Comigo - Restart; Leave Out All The Rest - Linkin Park; Broken-Hearted Girl - Beyoncé; Alejandro - Lady Gaga; If I Were A Boy - Beyoncé; I Gotta Feeling - Black Eyed Peas; Amo Noite E Dia - Jorge e Mateus; Sweet Dreams - Beyoncé; Smells Like Teen Spirit - Nirvana; Wonderwall - Oasis; Just Dance (feat. Colby O'Donis) - Lady Gaga
```

### Recommendation (Users o Songs)

Using the idea of a personalized PageRank that is seen as RandomWalks of various lenghts organized, and some ideas extracted from this [Stanford handout](https://web.archive.org/web/20201111231436/http://web.stanford.edu/class/msande233/handouts/lecture8.pdf), this command gives recommendations of either users with similar tastes of certain user or song recommendations based on a small song list given by the user.

* Command: `recomendacion`.
* Input Parameters: `usuarios/canciones`, the type of recommendation that we are requesting (either users or songs); `n`, the amount of users or songs to be recommended; `cancion1 >>>> cancion2 >>>> ... >>>> cancionK`, if we want a song recommendations, we need to provide a list of songs that we like.
* Examples:
```
Input:
    recomendacion canciones 10 Love Story - Taylor Swift >>>> Toxic - Britney Spears >>>> I Wanna Be Yours - Arctic Monkeys >>>> Hips Don't Lie (feat. Wyclef Jean) - Shakira >>>> Death Of A Martian - Red Hot Chili Peppers
    recomendacion usuarios 5 Love Story - Taylor Swift >>>> Toxic - Britney Spears >>>> I Wanna Be Yours - Arctic Monkeys >>>> Hips Don't Lie (feat. Wyclef Jean) - Shakira >>>> Death Of A Martian - Red Hot Chili Peppers
    
Output:
    
    Butterfly - Grimes; Cola - Lana Del Rey; In Time - FKA Twigs; Touch - Troye Sivan; Hurricane - 30 Seconds To Mars; Boring - The Pierces; Cut Your Teeth - Kyla La Grange; Earned It - The Weeknd; Player (Feat. Chris Brown) - Tinashe; If I Were A Boy - Beyoncé
    lorenafazion; naosoumodinha; hlovato906gmail; tiagogabbana19; extralouca
```    

### Cycle of N Songs
Prints a cicle of a certain lenght (with the songs of the graph) that starts with the requested song.

* Command: `ciclo`.
* Input Parameters: `n` and `cancion`.
* Examples:
```
Input:

    ciclo 7 By The Way - Red Hot Chili Peppers
    ciclo 15 Love Me Like You Do - Ellie Goulding
    
Output:
    
    By The Way - Red Hot Chili Peppers --> Fairy Tale - Shaman --> I Hate Everything About You - Three Days Grace --> Viva La Vida - Coldplay --> Under The Bridge - Red Hot Chili Peppers --> November Rain - Guns N' Roses --> Cryin' - Aerosmith --> By The Way - Red Hot Chili Peppers
    Love Me Like You Do - Ellie Goulding --> Uptown Funk (Feat. Bruno Mars) - Mark Ronson --> Thinking Out Loud - Ed Sheeran --> Ship To Wreck - Florence And The Machine --> Fourfiveseconds (feat. Kanye West, Paul Mccartney) - Rihanna --> Feeling Myself (Feat. Beyoncé) - Nicki Minaj --> Cheerleader (Felix Jaehn Remix) - Omi --> Ayo (Feat. Tyga) - Chris Brown --> Um Leão - Pitty --> I Know What You Did Last Summer (feat. Camila Cabello) - Shawn Mendes --> Hello - Adele --> Confident - Demi Lovato --> Hotline Bling - Drake --> My House - Flo Rida --> Alive - Sia --> Love Me Like You Do - Ellie Goulding
```
    
If a cycle of `n` lenght is not found, an error message is printed.


### All in range
Prints n amount of songs that are exactly at `n` distance of the song given by parameter.

* Command: `rango`.
* Input Parameters: `n` and `cancion`. 
* Examples:
```
Input:

    rango 8 Shots - Imagine Dragons
    rango 3 Shots - Imagine Dragons
    rango 2 After Dark - Asian Kung-fu Generation
    rango 4 I'm Yours - Jason Mraz
    
Output:
   
    0
    2171
    1059
    0
```
