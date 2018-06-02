
# coding: utf-8

# In[1]:


import vtk

from vtk import *

import numpy as np


# In[2]:


with open('atoms-radius.txt') as f:
    radiusDataset = f.read().splitlines()
f.close()

with open('atoms-coordinates.txt') as f:
    atomsCoordinatesDataset = f.read().splitlines()
f.close()

with open('atoms-connections.txt') as f:
    atomsConnectionsDataset = f.read().splitlines()
f.close()


# In[3]:


del radiusDataset[0]
print(len(radiusDataset))


# In[4]:


del atomsCoordinatesDataset[0]
print(len(atomsCoordinatesDataset))


# In[5]:


del atomsConnectionsDataset[0]
print(len(atomsConnectionsDataset))


# In[6]:


points = vtk.vtkPoints()
print(points.GetNumberOfPoints())
for coord in atomsCoordinatesDataset:
    pointData = coord.split(' ')
    numPointData = [float(pointData[0]), float(pointData[1]), float(pointData[2])]
    points.InsertNextPoint(numPointData[:])
#print(pointData[0])
#points.addPoint(0, pointData[0], pointData[1], pointData[2])
print(points.GetNumberOfPoints())


# In[7]:


#Parse atoms connections
'''connections = []
for i in range(0, len(atomsCoordinatesDataset)):
    connections.append([])
    
print(len(connections))

lines = vtk.vtkCellArray()
for line in atomsConnectionsDataset:
    stringList = line.split(' ')
    position = int(stringList[0])
    value = int(stringList[1])
    connections[position].append(value)
    
for connection in connections:
    if connection != []:
        #print(connection)
        lines.InsertNextCell(len(connection))
        for index in connection:
            lines.InsertCellPoint(index)
            
print(lines)
'''

#connections = []
#for i in range(0, len(atomsCoordinatesDataset)):
#    connections.append([])

#print(len(connections))

lines = vtk.vtkCellArray()
for line in atomsConnectionsDataset:
    stringList = line.split(' ')
    position = int(stringList[0])
    value = int(stringList[1])
    #connections[position].append(value)

    lines.InsertNextCell(2)
    lines.InsertCellPoint(position)
    lines.InsertCellPoint(value)



print(lines)


'''lines = vtk.vtkCellArray()
file = open('atoms-connections.txt')
line = file.readline()
line = file.readline()

while line:
    data = str.split(line)
    if data:
        a, b = int(data[0]), int(data[1])
        lines.InsertNextCell(2)
        lines.InsertCellPoint(a)
        lines.InsertCellPoint(b)
    line = file.readline()
'''

# In[8]:


scalars = vtk.vtkFloatArray()


# In[9]:


'''for valueStr in radiusDataset:
    value = float(valueStr)
    #scalars.InsertTuple1(value,value)
    scalars.InsertTuple(i, value)
    i = i + 1
    print(valueStr)
'''
for valueStr in radiusDataset:
    value = float(valueStr)
    scalars.InsertNextValue(value)
    
print(scalars)


# In[10]:


renderer = vtk.vtkRenderer()

#elev = vtk.vtkElevationFilter()
#elev.SetLowPoint(-2,-2,0)
#elev.SetHighPoint(2,2,0)
glyph = vtk.vtkGlyph3D()
#glyph.SetInputConnection(elev.GetOutputPort())

mapper = vtk.vtkPolyDataMapper()
#mapper.SetInputConnection(glyph.GetOutputPort())

#polydata.GetCellData().SetScalars(scalars);
'''for i in range(0, points.GetNumberOfPoints()):
    point = points.GetPoint(i)
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(scalars.GetValue(i))
    print(scalars.GetValue(i))
    #sphere.SetRadius(1)
    glyph.SetInputData(i, sphere.GetOutput())
    mapper.SetInputConnection(sphere.GetOutputPort())
    sphereActor = vtk.vtkActor()
    sphereActor.SetPosition(point)
    radiiValue = scalars.GetValue(i)
    if radiiValue < 0.4:
        sphereActor.GetProperty().SetColor(scalars.GetValue(i), 0, 0)
    elif radiiValue < 0.7: 
        sphereActor.GetProperty().SetColor(0, 0, scalars.GetValue(i))
    else:
        sphereActor.GetProperty().SetColor(0, scalars.GetValue(i), 0)
    sphereActor.SetMapper(mapper)
    renderer.AddActor(sphereActor)
    
'''

for i in range(0, points.GetNumberOfPoints()):
    point = points.GetPoint(i)
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(scalars.GetValue(i) / 2)
    #sphere.SetRadius(1)
    #print(scalars.GetValue(i))

    glyph.SetInputConnection(sphere.GetOutputPort())
    #glyph.SetVectorModeToUseNormal()
    #glyph.SetScaleModeToScaleByVector()
    glyph.SetScaleFactor(0.1)

    #apd = vtk.vtkAppendPolyData()
    #apd.AddInputConnection(glyph.GetOutputPort())
    #apd.AddInputConnection(sphere.GetOutputPort())

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphere.GetOutputPort())
    
    mapper.SetColorModeToMapScalars();
    #mapper.SetScalarModeToUsePointFieldData()
    #mapper.SetColorModeToMapScalars()
    #mapper.ScalarVisibilityOn()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetPosition(point)
    actor.VisibilityOn()
    
    radiiValue = scalars.GetValue(i)
    
    lut = vtkColorTransferFunction()
    #lut.SetNumberOfTableValues(4)
    lut.SetColorSpaceToRGB()
    lut.AddRGBPoint(0.3,1,1,1)
    lut.AddRGBPoint(0.7,1,0,0)
    lut.AddRGBPoint(0.78,0,0,1)
    lut.AddRGBPoint(2,0,1,0)
    lut.SetScaleToLinear()
    
    
    print(lut.GetColor(0))
    actor.GetProperty().SetColor(lut.GetColor(scalars.GetValue(i)))
    print(lut)
    
    '''if radiiValue > 1.5:
        actor.GetProperty().SetColor(0, scalars.GetValue(i) * 0.5, 0) 
    elif radiiValue > 0.745:
        
        actor.GetProperty().SetColor(0, 0, scalars.GetValue(i))   
    elif radiiValue > 0.4: 
        
        actor.GetProperty().SetColor(scalars.GetValue(i), 0, 0) 
    else:
        actor.GetProperty().SetColor(1, 1, 1)
    '''
    
    mapper.SetLookupTable(lut)
    renderer.AddActor(actor)

#print(actor.GetMapper())
#glyph.Update()


# In[11]:


# vtkPolyData is a data object that is a concrete implementation of vtkDataSet.
# vtkPolyData represents a geometric structure consisting of vertices, lines,
# polygons, and/or triangle strips
polygon = vtk.vtkPolyData()
polygon.SetPoints(points)
polygon.SetLines(lines)
#polygon.GetCellData().SetScalars(scalars)

tubeFilter = vtk.vtkTubeFilter()
tubeFilter.SetInputData(polygon)
tubeFilter.SetNumberOfSides(5);
tubeFilter.SetVaryRadiusToVaryRadiusOff()
tubeFilter.SetRadius(0.1)

tubeMapper = vtk.vtkPolyDataMapper()
tubeMapper.SetInputConnection(tubeFilter.GetOutputPort())
tubeMapper.Update()


actor = vtk.vtkActor()
actor.SetMapper(tubeMapper)
#actor.SetPosition(point)
actor.VisibilityOn()
renderer.AddActor(actor)
    


# In[12]:


#sphere = []
#for spherePosition in atomsCoordinatesDataset:
#    sphere = vtkSphereSource()
#    sphere.SetRadius(scalars.GetValue(0))
#    #polygon = sphere.GetOutput()

#print(sphere)


# In[13]:


# outline
outline = vtk.vtkOutlineFilter()
if vtk.VTK_MAJOR_VERSION <= 5:
    outline.SetInputData(tubeFilter)
else:
    outline.SetInputConnection(tubeFilter.GetOutputPort())
mapper2 = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper2.SetInput(outline.GetOutput())
else:
    mapper2.SetInputConnection(outline.GetOutputPort())
    
actor2 = vtk.vtkActor()
actor2.GetProperty().SetColor(0, 0, 0)
actor2.SetMapper(mapper2)

renderer.AddActor(actor2)


# In[14]:


# vtkPolyDataMapper is a class that maps polygonal data (i.e., vtkPolyData)
# to graphics primitives
'''polygonMapper = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    polygonMapper.SetInputConnection(polygon.GetProducerPort())
else:
    polygonMapper.SetInputData(polygon)
    polygonMapper.Update()
''' 


# In[15]:


# Create an actor to represent the polygon. The actor orchestrates rendering of
# the mapper's graphics primitives. An actor also refers to properties via a
# vtkProperty instance, and includes an internal transformation matrix. We
# set this actor's mapper to be polygonMapper which we created above.
#polygonActor = vtk.vtkActor()
#polygonActor.SetMapper(polygonMapper)
#polygonActor.GetProperty().SetColor(1, 1, 1)


# In[16]:


#glyph = vtk.vtkGlyph3D()
#glyph.SetInputData(polygon)


# In[17]:


# Create the Renderer and assign actors to it. A renderer is like a
# viewport. It is part or all of a window on the screen and it is
# responsible for drawing the actors it has.  We also set the
# background color here.
#renderer = vtk.vtkRenderer()


# In[18]:


#renderer.AddActor(polygonActor)


# In[19]:


renderer.SetBackground(0.3, 0.3, 0.3)


# In[20]:


# Automatically set up the camera based on the visible actors.
# The camera will reposition itself to view the center point of the actors,
# and move along its initial view plane normal
# (i.e., vector defined from camera position to focal point) so that all of the
# actors can be seen.
renderer.ResetCamera()


# In[21]:


# Finally we create the render window which will show up on the screen
# We put our renderer into the render window using AddRenderer. We
# also set the size to be 300 pixels by 300.
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(800, 600)
 
# The vtkRenderWindowInteractor class watches for events (e.g., keypress,
# mouse) in the vtkRenderWindow. These events are translated into
# event invocations that VTK understands (see VTK/Common/vtkCommand.h
# for all events that VTK processes). Then observers of these VTK
# events can process them as appropriate.
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()
 
# There is no explicit need to free any objects at this point.
# Once Python exits, memory is automatically freed.

