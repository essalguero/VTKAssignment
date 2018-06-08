import vtk

from vtk import *

import numpy as np


# Leer los ficheros
with open('atoms-radius.txt') as f:
    radiusDataset = f.read().splitlines()
f.close()

with open('atoms-coordinates.txt') as f:
    atomsCoordinatesDataset = f.read().splitlines()
f.close()

with open('atoms-connections.txt') as f:
    atomsConnectionsDataset = f.read().splitlines()
f.close()


# Borrar la primera fila de cada dataset (Es una cabecera)
del radiusDataset[0]
del atomsCoordinatesDataset[0]
del atomsConnectionsDataset[0]


# Separar las coordenadas de los puntos y guardar los puntos en una estructura (de listas)
points = vtk.vtkPoints()
for coord in atomsCoordinatesDataset:
    pointData = coord.split(' ')
    numPointData = [float(pointData[0]), float(pointData[1]), float(pointData[2])]
    points.InsertNextPoint(numPointData[:])


# Separar las conexiones entre puntos y guardarlas en una estructura
lines = vtk.vtkCellArray()
for line in atomsConnectionsDataset:
    stringList = line.split(' ')
    position = int(stringList[0])
    value = int(stringList[1])

    lines.InsertNextCell(2)
    lines.InsertCellPoint(position)
    lines.InsertCellPoint(value)


# Guardar los radios en una estructura
scalars = vtk.vtkFloatArray()
for valueStr in radiusDataset:
    value = float(valueStr)
    scalars.InsertNextValue(value)


# Crear el renderer
renderer = vtk.vtkRenderer()

# Crear la estructura para pintar los datos
glyph = vtk.vtkGlyph3D()
glyph.SetScaleFactor(0.1)


# Crear LUT para colorear las esferas
lut = vtkColorTransferFunction()
lut.SetColorSpaceToRGB()
lut.AddRGBPoint(0.3,1,1,1)
lut.AddRGBPoint(0.7,1,0,0)
lut.AddRGBPoint(0.78,0,0,1)
lut.AddRGBPoint(2,0,1,0)
lut.SetScaleToLinear()


# Crear variables mapper y actor para usarlas en el resto del script
mapper = []
actor = []

# Crear una esfera por cada punto
for i in range(0, points.GetNumberOfPoints()):
    point = points.GetPoint(i)
    
    # Crear una esfera utilizando el tamaño del radio
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(scalars.GetValue(i) / 2)
    
    # Fijar la conexion con el glyph
    glyph.SetInputConnection(sphere.GetOutputPort())
    
    # Crear un PolyDataMapper para cada esfera
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphere.GetOutputPort())
    mapper.SetColorModeToMapScalars();
    mapper.SetLookupTable(lut)
    
    # Crear un actor para cada esfera
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetPosition(point)
    actor.VisibilityOn()
    
    # Fijar el color de la esfera basándose en el LUT definido
    actor.GetProperty().SetColor(lut.GetColor(scalars.GetValue(i)))
    
    # Añadir el actor al renderer para pintarlo
    renderer.AddActor(actor)



# In[11]:


# vtkPolyData represents a geometric structure consisting of vertices, lines, polygons, and/or triangle strips
polygon = vtk.vtkPolyData()
polygon.SetPoints(points)
polygon.SetLines(lines)

# Crear filtro para las conexiones entre esferas (átomos)
tubeFilter = vtk.vtkTubeFilter()
tubeFilter.SetInputData(polygon)
tubeFilter.SetNumberOfSides(5);
tubeFilter.SetVaryRadiusToVaryRadiusOff()
tubeFilter.SetRadius(0.1)

# Crear un mapper para el filtro
tubeMapper = vtk.vtkPolyDataMapper()
tubeMapper.SetInputConnection(tubeFilter.GetOutputPort())
tubeMapper.Update()

# Crear un actor para incorporarlo al renderer
actor = vtk.vtkActor()
actor.SetMapper(tubeMapper)
actor.VisibilityOn()
renderer.AddActor(actor)
    

# Crear el bounding box
boundingBox = vtk.vtkOutlineFilter()

# La forma de crearlo depende de la version de vtk
if vtk.VTK_MAJOR_VERSION <= 5:
    boundingBox.SetInputData(tubeFilter)
else:
    boundingBox.SetInputConnection(tubeFilter.GetOutputPort())

# Crear su mapper
mapper = vtk.vtkPolyDataMapper()

# La forma de asociar el boundingbox al mapper depende de la version de vtk
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper.SetInput(boundingBox.GetOutput())
else:
    mapper.SetInputConnection(boundingBox.GetOutputPort())

# Crear el actor para añadirlo al renderer
actor = vtk.vtkActor()
actor.GetProperty().SetColor(0, 0, 0)
actor.SetMapper(mapper)

renderer.AddActor(actor)

#Preparar la renderizacion

# Fijar el color de fondo
renderer.SetBackground(0.3, 0.3, 0.3)

# Resetear la camara
renderer.ResetCamera()

#Crear la ventana de renderizado
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(800, 600)
 
# Fijar la ventana como interactiva
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()


