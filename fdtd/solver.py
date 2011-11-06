import numpy
from constants import constants
from material import material
import grid as gr

class solver:
    """Solves FDTD equations on given grid, with given materials and ports"""
    def __init__(self, grid, mode='TMz', ports=None):
        # save arguments
        self.grid = grid
        self.mode = mode
        self.ports = ports

        # create memory grid
        self.memoryGrid = gr.grid(self.grid.xSize, self.grid.ySize, self.grid.deltaX, self.grid.deltaY)
        
        # create material
        self.material = {}
        self.material['epsilon'] = numpy.ones((grid.xSize/grid.deltaX, grid.ySize/grid.deltaY))
        self.material['mu'] = numpy.ones((grid.xSize/grid.deltaX, grid.ySize/grid.deltaY))
        self.material['sigma'] = numpy.zeros((grid.xSize/grid.deltaX, grid.ySize/grid.deltaY))

    def iterate(self, deltaT, time, starttime=0.0):
        """Iterates the FDTD algorithm in respect of the pre-defined ports"""
        # create constants
        c1 = deltaT/self.grid.deltaX
        c2 = deltaT/self.grid.deltaY
        c3 = constants.permit
        c4 = constants.permea

        # shortcut materials
        m1 = self.material['epsilon']
        m2 = self.material['mu']
        m3 = self.material['sigma']
        m4 = numpy.zeros(self.material['sigma'].shape)

        if self.mode == 'TEz':
            c1, c2, c3, c4 = -c1, -c2, c4, c3
            m1, m2, m3, m4 = m2, m1, m4, m3

        # iterate
        for t in numpy.arange(starttime, starttime + time, deltaT):
            # update ports
            for port in self.ports:
                port.update(self.grid, t)

            # calc odd Grid
            xshape, yshape = self.grid.oddGrid['field'].shape
            for x in range(0, xshape-1, 1):
                for y in range(0, yshape-1, 1):
                    # calc flux density
                    self.grid.oddGrid['flux'][x, y] += c1*(self.grid.evenGridY['field'][x+1, y] - self.grid.evenGridY['field'][x, y]) 
                    self.grid.oddGrid['flux'][x, y] -= c2*(self.grid.evenGridX['field'][x, y+1] - self.grid.evenGridX['field'][x, y])
                    
            # calc field
            self.grid.oddGrid['field'] = (1.0/(c3*m1 + m3))*(self.grid.oddGrid['flux'] - self.memoryGrid.oddGrid['flux'])
            # integrate field
            self.memoryGrid.oddGrid['flux'] += m3*self.grid.oddGrid['field']*deltaT

            # calc even Grid
            for x in range(0, xshape-1, 1):
                for y in range(1, yshape-1, 1):
                    # calc flux density
                    self.grid.evenGridX['flux'][x, y] -= c2*(self.grid.oddGrid['field'][x, y] - self.grid.oddGrid['field'][x, y-1])

            # calc field
            self.grid.evenGridX['field'] = (1.0/(c4*m2 + m4))*(self.grid.evenGridX['flux'] - self.memoryGrid.evenGridX['flux'])
            # integrate field
            self.memoryGrid.evenGridX['flux'] += m4*self.grid.evenGridX['field']*deltaT

            for x in range(1, xshape-1, 1):
                for y in range(0, yshape-1, 1):
                    # calc flux density
                    self.grid.evenGridY['flux'][x, y] += c1*(self.grid.oddGrid['field'][x, y] - self.grid.oddGrid['field'][x-1, y])

            # calc field
            self.grid.evenGridY['field'] = (1.0/(c4*m2 + m4))*(self.grid.evenGridY['flux'] - self.memoryGrid.evenGridY['flux'])
            # integrate field
            self.memoryGrid.evenGridY['flux'] += m4*self.grid.evenGridY['field']*deltaT

            if t/deltaT % 100 == 0:
                print "{}%".format((t-starttime)*100/time)
