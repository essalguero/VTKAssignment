import vtk

# Definir la función para procesar los eventos de teclado
def Keypress(obj, event):
    # Utilizar las variables definidas en el script
    global isosurface_value, renWin, isosurface, textActor, text_props
    
    #Mirar la tecla pulsada
    key = obj.GetKeySym()
    if key == "a":
        if isosurface_value < 1.0:
            isosurface_value = isosurface_value + 0.01
    elif key == "s":
        if isosurface_value > 0.0:
            isosurface_value = isosurface_value - 0.01

    # Actualiza el texto en la ventana con el nuevo valor (si se ha actualizado)
    isosurface.SetValue(0,isosurface_value)
    textActor.SetInput("%4.2f" %(isosurface_value))
    text_props.SetColor(lut.GetColor(isosurface_value))

    # renderiza la ventana
    renWin.Render()

# Leer el fichero con los datos
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName("hydrogen.vtk")

# Crear una tabla para los colores a utilizar en funcion del valor
lut = vtk.vtkColorTransferFunction()
lut.AddRGBPoint(0,1,0,0)
lut.AddRGBPoint(0.5,1,1,0)
lut.AddRGBPoint(1,0,1,0)

# Inicializar el valor de isosuperficie
isosurface_value=0.5

# Crear un Contour filter para dibujarlo en pantalla
isosurface = vtk.vtkContourFilter()
isosurface.SetInputConnection(reader.GetOutputPort())
isosurface.SetValue(0,isosurface_value)

# Crear un mapper para la isosuperficie y conectarla con los datos
isosurfaceMapper = vtk.vtkPolyDataMapper()
isosurfaceMapper.SetInputConnection(isosurface.GetOutputPort())

# Crear un actor y asociarle el mapper
isosurfaceActor = vtk.vtkActor()
isosurfaceActor.SetMapper(isosurfaceMapper)

# Fijar la tabla para los colores
isosurfaceMapper.SetLookupTable(lut)


# Crear propiedades para mostrar el valor de la isosuperficie
text_props = vtk.vtkTextProperty()
text_props.BoldOn()
text_props.ItalicOn()
text_props.ShadowOn()
text_props.SetFontSize(60)

# Crear un actor para el texto
textActor = vtk.vtkTextActor()
textActor.SetTextProperty(text_props)

# Obtener las coordenadas para poner el texto
text_position = textActor.GetPositionCoordinate()
text_position.SetCoordinateSystemToNormalizedViewport()
text_position.SetValue(0.8,0.9)


# Crear la barra con la escala
scalarBar = vtk.vtkScalarBarActor()
scalarBar.SetLookupTable(isosurfaceMapper.GetLookupTable())

scalarBar.SetTitle("Probability")
scalarBar.GetLabelTextProperty().SetColor(0,0,1)
scalarBar.GetTitleTextProperty().SetColor(0,0,1)

# Fijar el tamaño con el que mostrar la escala
scalarBar.SetWidth(.15)
scalarBar.SetHeight(.90)

# Obtener las coordenadas para poner la barra
scale_position = scalarBar.GetPositionCoordinate()
scale_position.SetCoordinateSystemToNormalizedViewport()
scale_position.SetValue(0.05,0.05)


# Crear el bounding box
boundingBox = vtk.vtkOutlineFilter()
boundingBox.SetInputConnection(reader.GetOutputPort())

# Crear su mapper
boundingBoxMapper = vtk.vtkPolyDataMapper()
boundingBoxMapper.SetInputConnection(boundingBox.GetOutputPort())

# Crear el actor para añadirlo al renderer
boundingBoxActor = vtk.vtkActor()
boundingBoxActor.SetMapper(boundingBoxMapper)
boundingBoxActor.GetProperty().SetColor(0.0,0.0,1.0)
boundingBoxActor.GetProperty().SetLineWidth(5.0)

# Iniciar el texto con el valor del isosurface_value
textActor.SetInput("%4.2f" %(isosurface_value))
text_props.SetColor(lut.GetColor(isosurface_value))

#Crear el renderer
ren = vtk.vtkRenderer()
ren.SetBackground(.8, .8, .8)

# Añadir todos los actores
ren.AddActor(boundingBoxActor)
ren.AddActor(isosurfaceActor)
ren.AddActor(scalarBar)
ren.AddActor(textActor)

# Crear la ventana de renderizado
renWin = vtk.vtkRenderWindow()
renWin.SetWindowName("Hydrogen Visualization")
renWin.SetSize(800, 600)
renWin.AddRenderer(ren)

# Crear la ventana interactiva y fijar el event manager de las teclas
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.AddObserver("KeyPressEvent", Keypress)
iren.Initialize()
iren.Start()
