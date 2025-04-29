# Traffic Modelling

This project aims to model traffic dynamics for a system of cars moving along a road and through an intersection through an agent-based approach, where each car is an actor with certain attributes and allowed actions based on its position with respect to other cars and the road environment.

## Four-way stop model 

Cars that will turn left are plotted in blue, while cars that will turn right are plotted in red. Cars that will continue straight through the intersection are shown in white. The environment is implemented with periodic boundary conditions, so that when a car exits the environment at one edge, it immediately reenters at the opposite edge. Whenever a car passes through one edge and reenters through the opposite edge, it is randomly assigned new navigation data and its color changes to reflect this update to whether it will turn in one direction or the other.

## Even vs. uneven density in each direction

When there is significantly higher car density in one direction compared to another, the four-way stop model becomes much less efficient. While cars moving in the direction with lower traffic density pass through the intersection without having to wait, buildup occurs in the direction with higher traffic density, with most cars spending most of their time waiting in line to get to the intersection.

## Simple Freeway Models

Based on how the model is initialized, stop and go traffic may or may not occur in the model, even if the number of cars and size of the environment remain the same.
