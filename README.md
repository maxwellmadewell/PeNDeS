# Max Coursey
#Vanderbilt CS 6388 - MiniProject
#Petri Net Design Studio

## Install & Run
First, install the following:
- [NodeJS](https://nodejs.org/en/) (LTS recommended)
- npm install jointjs
- npm install webgme-bindings
- [MongoDB](https://www.mongodb.com/)
- [Python3](https://www.python.org/downloads/)
- Python (required by plugin below) requires the additional packages
- pip/pip3 install webgme-bindings

Second, start mongodb locally by running the `mongod` executable in your mongodb installation (you may need to create a `data` directory or set `--dbpath`).

Last, run `webgme start` from the project root to start . Finally, navigate to `http://localhost:8888` to start using mc!


##Overview
This domain implenents a basic Petri Net model defined as a triple (P, T, F) where:
- P is a finite set of places
- T is a finite set of transitions (P ∩ T = ∅)
- F ⊆ (P x T) ∪ (T x P) is a set of arcs (flow relation) to describe an arc that connects a transition t to a place p
- Inplaces of a transition (*t) is a set of places where each element of a set is connected to the transition 
- Outplaces of a transition (t*) is a set of places that are connected to the transition by arcs where the places are the destinations and the transition is the source

A Petri net is a directed, weighted, bipartite graph consisting of two kinds of nodes(Places and Transitions) with arcs from a Place to a Transition or from a Transition to a Place. In the visualizer/graphical representation, Places are shown as circles, Transitions as bars/rectangles. Arcs are lines with multiple arcs allowed between nodes. A marking assigns to each Place p an nonnegative integer representing tokens.

Meta

![image](https://user-images.githubusercontent.com/49755125/116700466-cd53b080-a994-11eb-8b83-c8c3503ff60c.png)

Composition

![image](https://user-images.githubusercontent.com/49755125/116700517-dba1cc80-a994-11eb-83df-11ea1eeea983.png)

Visualizer

![image](https://user-images.githubusercontent.com/49755125/116700587-ef4d3300-a994-11eb-93af-cab01ac11820.png)

##Applications and Use Case
Petri Nets can be applied to many logical systems.  Systems that map flow of data such as vending machines are simple to understand.  Petri nets can be applied to such logical cases and most logical systems. Manufacturing, consumer product design, workflows, are just a few overarching applications.

##Design
When starting the application, the heirarchal tree on the right panel shows the Root, FCO, Meta Model, and Instance Model example (newName in initial startup).
Clicking on the newName instance example, there are three Visualizer Selectors:
1. PNViz - Is the generated visualizer show the implementation of the Composition model.
3. Composition - show the instation of a model.  Here the places, transitions, and arcs are added to form a model
4. Meta - Shows the meta node types, relationships, contraints, attributes, and aspects of the meta model


PNViz - This visualizer allows users to fire transitions using the sideways triangle, play, button located at the top of the screen.  Firing a transition moves a token from the curently selected place to the next place in the model.  If there exist two or more destinations, a selection is required.  The model can be reset to the initial node.  Also, the question mark button examines the current model and determines whether the model meets one or more of the following graph definitions:
- Free Choice Petri Net
- StateMachine Petri Net
- Marked Graph Petri Net
- Workflow Net 
