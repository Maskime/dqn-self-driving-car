#Self Driving Car with DQN
This project was created to demonstrate the usage of a DQN for a "Self driving car".

The starting point is what was provided by the the [Udemy](https://www.udemy.com/) online course 
[Artificial Intelligence A to Z](https://www.udemy.com/artificial-intelligence-az/).
It was then modified in great extend to provide a GUI that allows various modifications about the DQN settings and get
feedback in real-time.

## Installation
  * Clone this repository
  * Python version : 2.7
  * PyTorch version : 0.1.12 `pip install http://download.pytorch.org/whl/cu80/torch-0.1.12.post2-cp27-none-linux_x86_64.whl`
  * Kivy version : 1.0.9 [Information](https://kivy.org/#download) `pip install cython kivy`
  * Kivy Garden : [Information](https://kivy.org/doc/stable/api-kivy.garden.html)
  * Matplotlib : 2.2.3 `pip install matplotlib==2.2.3`
  * Kivy Garden Matplotlib : [Information](https://github.com/kivy-garden/garden.matplotlib) `garden install matplotlib`
  
Once you've installed the previously mentioned packages you should be good to go.
"cd" into your installation directory and to launch the application : `python map.py`

If any error shows up, please fill an issue in this repository with your stack trace.

## GUI
Once started you should have something like that:
![GUI Main screen](https://i.imgur.com/KtTtgig.png)

### GUI features
  * Allow pausing the car
  * Allow creating obstacle to verify that the car effectively learn not to go through obstacles
  * Access to a configuration panel that allows following settings:
    * DQN Configuration:
      * Gamma parameter (or discount factor)
      * NB Hidden neurons
      * Learning rate
      * Temperature applied to the softmax function
      * Sample size to get from the Replay Memory
    * Rewards configuration:
      * Decay reward (living penalty)
      * Distance reward (when the distance to the current objective is decreasing)
  * Save :
    * Current Brain : Save the current NN state
    * Current Map : Save the map (you then put the name of the file, and it will be save in the
    `maps/` directory provided in this repository)
  * Load : 
    * Last brain : When saving the current brain, it will create a last_brain.pth file which 
    will be the one loaded when clicking this item
    * Map... : You must type the name of the file you created when your saved map.
    
_Please keep in mind that this is a research/prototype application and that it's perfectly possible to
do a better job when it comes to its usability :)_

#### Main screen components
##### Realtime graph
In the top left corner.

This graph shows the current score average, if it goes down, not good, if it goes up, good.
It only shows the last 1000 average to help with the readability of the graph.

##### Current Stats
In the top right corner.

Various information about the current state of the environment:
  * Car sensors : Sensors are here to report the density of sand they encounter : 0 no sand, 1 the whole captor is in sand.
    * R : Red sensor
    * B : Blue sensor
    * Y : Yellow sensor
  * Destination : The car objective is to make round trip between top left (1) and bottom right (2).
  This field simply tells where the car is supposed to go.
  * Distance btw Goals : Current distance between the 2 destinations
  * Steps : Number of iteration that we currently made
  * Last rewards : Currently provided reward
  * Distance to dest : Distance between the car (car front, signaled with a red square) and the current destination

##### "Road"
Bottom

This is where the car is moving, its objective it to make round trips between 1 and 2.

You can draw obstacles on it by simply left-clicking and drawing your obstacles.

## Credits
Credits to [SuperDataScience](https://www.superdatascience.com) for providing this great introduction to
the Reinforcement Learning principles. 