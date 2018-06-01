
# coding: utf-8

# In[1]:


import vtk

reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("hydrogen.vtk")

#Set the isovalue and create the Contour filter.
isovalue=0.5
isosurface = vtk.vtkContourFilter()
isosurface.SetInputConnection(reader.GetOutputPort())
isosurface.SetValue(0,isovalue)
isosurfaceMapper = vtk.vtkPolyDataMapper()
isosurfaceMapper.SetInputConnection(isosurface.GetOutputPort())
isosurfaceActor = vtk.vtkActor()
isosurfaceActor.SetMapper(isosurfaceMapper)

#Create a colour transfer function so the data will change colour for different isovalues.
lut=vtk.vtkColorTransferFunction()
lut.AddRGBPoint(0,1,0,0)
lut.AddRGBPoint(0.5,1,1,0)
lut.AddRGBPoint(1,0,1,0)

# Set the LookupTable of the isosurface
isosurfaceMapper.SetLookupTable(lut)

#Display the current value
textActor = vtk.vtkTextActor()
tp = vtk.vtkTextProperty()
tp.BoldOn()
tp.ShadowOn()
tp.ItalicOn()
tp.SetColor(1.0,0.2,0.3)
tp.SetFontFamilyToArial()
tp.SetFontSize(50)
textActor.SetTextProperty(tp)

#Place the value at the correct position
position = textActor.GetPositionCoordinate()
position.SetCoordinateSystemToNormalizedViewport()
position.SetValue(0.8,0.9)


# Create the bar with the scale
scalarBar = vtk.vtkScalarBarActor()
scalarBar.SetLookupTable(isosurfaceMapper.GetLookupTable())

scalarBar.SetTitle("Probability")
scalarBar.GetLabelTextProperty().SetColor(0,0,1)
scalarBar.GetTitleTextProperty().SetColor(0,0,1)

scalarBar.SetWidth(.20)
scalarBar.SetHeight(.90)

position = scalarBar.GetPositionCoordinate()
position.SetCoordinateSystemToNormalizedViewport()
position.SetValue(0.05,0.05)


#Create a bounding box
boundingBox = vtk.vtkOutlineFilter()
boundingBox.SetInputConnection(reader.GetOutputPort())
boundingBoxMapper = vtk.vtkPolyDataMapper()
boundingBoxMapper.SetInputConnection(boundingBox.GetOutputPort())
boundingBoxActor = vtk.vtkActor()
boundingBoxActor.SetMapper(boundingBoxMapper)
boundingBoxActor.GetProperty().SetColor(0.0,0.0,1.0)
boundingBoxActor.GetProperty().SetLineWidth(2.0)

def Keypress(obj, event):
    global isovalue, renWin
    key = obj.GetKeySym()
    if key == "i":
        if isovalue < 1.0:
            isovalue = isovalue + 0.01
            isosurface.SetValue(0,isovalue)
            textActor.SetInput("%4.2f" %(isovalue))
            tp.SetColor(lut.GetColor(isovalue))
            renWin.Render()
    elif key == "o":
        if isovalue > 0.0:
            isovalue = isovalue - 0.01
            isosurface.SetValue(0,isovalue)
            textActor.SetInput("%4.2f" %(isovalue))
            tp.SetColor(lut.GetColor(isovalue))
            renWin.Render()



#Create the renderer and render window.
ren = vtk.vtkRenderer()
ren.SetBackground(.8, .8, .8)
ren.AddActor(boundingBoxActor)
ren.AddActor(isosurfaceActor)
ren.AddActor(scalarBar)
ren.AddActor(textActor)
renWin = vtk.vtkRenderWindow()
renWin.SetWindowName("Hydrogen Visualization")
renWin.SetSize(800, 600)
renWin.AddRenderer(ren)


iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.AddObserver("KeyPressEvent", Keypress)
iren.Initialize()
iren.Start()
