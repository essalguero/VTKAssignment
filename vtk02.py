from vtk import *
import math


reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("Wind.vtk")
reader.Update()

a,b = reader.GetOutput().GetScalarRange()
xmi, xma, ymi, yma, zmi, zma = reader.GetOutput().GetBounds()

ctf = vtk.vtkLookupTable()
ctf.SetHueRange(0.667, 0.0)
ctf.SetValueRange(1.0, 1.0)
ctf.SetSaturationRange(0.0, 1.0)
ctf.SetTableRange(a,b)



plane = vtk.vtkPlaneSource()
plane.SetOrigin(xmi,math.ceil(ymi),zmi)
plane.SetPoint1(xma,math.ceil(ymi),zmi)
plane.SetPoint2(xmi,math.ceil(ymi),zma)
plane.SetXResolution(4)
plane.SetYResolution(6)
plane.Update()


stream = vtk.vtkStreamTracer()
stream.SetSourceConnection(plane.GetOutputPort())
stream.SetInputConnection(reader.GetOutputPort())
stream.SetIntegrationDirectionToForward()
stream.SetIntegrator(vtk.vtkRungeKutta4())
#stream.SetStepLength(0.05)

stream.SetInitialIntegrationStep(0.02)
stream.SetMinimumIntegrationStep(0.05)
stream.SetMaximumIntegrationStep(10)

print(stream)

streamMapper = vtk.vtkPolyDataMapper()
streamMapper.SetLookupTable(ctf)
streamMapper.SetInputConnection(stream.GetOutputPort())
streamMapper.SetScalarRange(a,b)
streamActor = vtk.vtkActor()
streamActor.SetMapper(streamMapper)
streamActor.GetProperty().SetLineWidth(3.0)



'''outline = vtk.vtkOutlineFilter()


outline.SetInputData(reader.GetOutput())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputData(outline.GetOutput())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(0.8, 0.8, 0.8)
outlineActor.GetProperty().SetLineWidth(2.0)
'''

boundingBox = vtk.vtkOutlineFilter()
boundingBox.SetInputConnection(reader.GetOutputPort())
boundingBoxMapper = vtk.vtkPolyDataMapper()
boundingBoxMapper.SetInputConnection(boundingBox.GetOutputPort())
boundingBoxActor = vtk.vtkActor()
boundingBoxActor.SetMapper(boundingBoxMapper)
boundingBoxActor.GetProperty().SetColor(0.0,0.0,1.0)
boundingBoxActor.GetProperty().SetLineWidth(2.0)

ren = vtk.vtkRenderer()
ren.SetBackground(0.2, 0.2, 0.2)
ren.AddActor(streamActor)
ren.AddActor(boundingBoxActor)
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName("Wind as Streamlines")
renWin.SetSize(800, 600)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()
