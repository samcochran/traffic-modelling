import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation 


def animate(road, snapshots, filename, filetype, nSeconds, endPause=3):
    lastFrame = np.copy(snapshots[-1])
    framesAdded = int(np.ceil(endPause/nSeconds*len(snapshots)))
    for _ in range(framesAdded):
        snapshots.append(lastFrame)
    k = len(snapshots)
    nSeconds += endPause
    fps = k/nSeconds
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    fig.patch.set_facecolor('black')
    road.plotRoad()
    # line = ax.plot([], [], marker='D', color='w', linestyle='')[0]
    lines = [ax.plot([], [], marker='D', color='w', linestyle='')[0] for car in snapshots[0]]

    def animate_func(i):
        # occupied = np.where(snapshots[i] == 1)
        # line.set_data(occupied[0] + .5, occupied[1] + .5)
        for line, car in zip(lines, snapshots[i]):
            if car.lane == 0 or car.lane == 1:
                line.set_data([car.road.laneLocs[car.lane] + .5], [car.road.roadLen - car.loc - .5])
            elif car.lane == 2 or car.lane ==3:
                line.set_data([car.loc + .5], [car.road.roadLen - car.road.laneLocs[car.lane] - .5]) 
            if car.nav == 'straight': line.set_color('white')
            elif car.nav == 'left': line.set_color('steelblue')
            elif car.nav == 'right': line.set_color('sandybrown')
        return lines

    anim = animation.FuncAnimation(fig, 
                                   animate_func, 
                                   frames = list(range(k)),
                                   interval = 1000/fps)
    
    anim.save(f'./animations/{filename}.{filetype}', fps=fps, writer='ffmpeg', dpi=400)
