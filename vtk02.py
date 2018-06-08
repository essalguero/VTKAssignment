import vtk
from vtk import *

import math

# Leer los datos del fichero
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("Wind.vtk")
reader.Update()


# Leer los rangos del fichero
min_value, max_value = reader.GetOutput().GetScalarRange()
min_x, max_x, min_y, max_y, min_z, max_z = reader.GetOutput().GetBounds()

# Crear una LUT para los colores y fijar los rangos de valores
lut = vtk.vtkLookupTable()
lut.SetHueRange(0.0, 0.0)
lut.SetValueRange(1.0, 1.0)
lut.SetSaturationRange(0.20, 1.0)


# Crear el plano para pintar los datos - Sacado de internet
plane = vtk.vtkPlaneSource()
plane.SetOrigin(min_x, math.ceil(min_y), min_z)
plane.SetPoint1(max_x, math.ceil(min_y), min_z)
plane.SetPoint2(min_x, math.ceil(min_y), max_z)


# Fijar el numero de lineas a pintar por eje
plane.SetXResolution(4 * 4)
plane.SetYResolution(6 * 2)
plane.Update()


# Crear un StreamTracer para pintar las lineas con los datos
stream = vtk.vtkStreamTracer()
stream.SetSourceConnection(plane.GetOutputPort())
stream.SetInputConnection(reader.GetOutputPort())


# Fijar tipo de integracion y método -> Sacado de internet
stream.SetIntegrationDirectionToForward()
stream.SetIntegrator(vtk.vtkRungeKutta4())


# Fijar los parámetros para la integración
stream.SetInitialIntegrationStep(0.1)
stream.SetMinimumIntegrationStep(10)
stream.SetMaximumIntegrationStep(10)
stream.SetMaximumPropagation(10000)


# Crear un mapper para el StreamTracer
streamMapper = vtk.vtkPolyDataMapper()
streamMapper.SetLookupTable(lut)
streamMapper.SetInputConnection(stream.GetOutputPort())
streamMapper.SetScalarRange(min_value, max_value)


# Crear un actor para añadirlo al renderer
streamActor = vtk.vtkActor()


# Fijar el mapper al actor
streamActor.SetMapper(streamMapper)
streamActor.GetProperty().SetLineWidth(3.5)


# Crear el bounding box en la pantalla. Depende de los datos leidos
boundingBox = vtk.vtkOutlineFilter()
boundingBox.SetInputConnection(reader.GetOutputPort())


# Crear un mapper para el bounding box
boundingBoxMapper = vtk.vtkPolyDataMapper()
boundingBoxMapper.SetInputConnection(boundingBox.GetOutputPort())


# Crear un actor para añadirlo al renderer
boundingBoxActor = vtk.vtkActor()
boundingBoxActor.SetMapper(boundingBoxMapper)
boundingBoxActor.GetProperty().SetColor(0.9, 0.9, 0.9)
boundingBoxActor.GetProperty().SetLineWidth(2.0)

# Crear el renderer
ren = vtk.vtkRenderer()
ren.SetBackground(0.2, 0.2, 0.4)

# Añadir los actores al renderer
ren.AddActor(streamActor)
ren.AddActor(boundingBoxActor)

# Crear la ventana de renderizado
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("Wind")
renWin.SetSize(800, 600)

# Crear la ventana interactiva
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()
