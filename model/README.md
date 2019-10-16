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

### Session Players
* id
    * UUID
* session id
    * UUID of the session
* player id
    * UUID of the player
* score
    * int
* winner
    * boolean

### Session
* id
    * UUID
* date
    * date
* game
    * UUID of the game that was played
