# Models

## Description
Holds the database related files 

## Design
### Game
* id
    * UUID
* name
    * string
* scoring
    * for now, likely always "score-based", eventually an enum as we add methods
    
### Player
* id 
    * UUID
* name
    * string
    
### Session
* id
    * UUID
* date
    * date
* game
    * UUID of the game that was played
* players
    * JSON array of:
        * player 
            * uuid
        * score
            * int
        * winner
            * boolean
