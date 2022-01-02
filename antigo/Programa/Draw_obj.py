import pandas as pd
import numpy as  np
import imageio
import sys

# Load the shape model. The first column lists whether the row is a vertex or face. The second,
# third and fourth column list the coordiantes (vertex) and vertex indices (faces)
COMET_67P_SHAPE_OBJ = pd.read_csv('data/hirestoutatis.OBJ', delim_whitespace=True, \
                                  names=['TYPE', 'X1', 'X2', 'X3'])

# Assign the vertices and faces
VERTICES = COMET_67P_SHAPE_OBJ.loc[COMET_67P_SHAPE_OBJ['TYPE'] == 'v'][['X1', 'X2', 'X3']].values \
               .tolist()
faces = COMET_67P_SHAPE_OBJ.loc[COMET_67P_SHAPE_OBJ['TYPE'] == 'f'][['X1', 'X2', 'X3']].values

# The index in the faces sub set starts at 1. For Python, it needs to start at 0.
faces = faces - 1

# Convert the indices to integer
faces = faces.astype(int)

# Convert the numpy array to a Python list
faces = faces.tolist()


# Now we need to define a main window class that is needed to set a window size / resolution.
from PyQt5.QtWidgets import QWidget, QHBoxLayout

# Import visvis
import visvis as vv

# Define the class
class MainWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.fig = vv.backends.backend_pyqt5.Figure(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.fig._widget)
        self.setLayout(layout)
        self.setWindowTitle('Rosetta')
        self.show()

####################---Create Object---####################

# Create visvis application
app = vv.use()
app.Create()


# Create main window frame and set a resolution.
main_w = MainWindow()
main_w.resize(1200, 800)

# Create the 3 D shape model as a mesh. verticesPerFace equals 3 since triangles define the
# mesh's surface in this case
vv.mesh(vertices=VERTICES, faces=faces, verticesPerFace=3)

# Get figure
#figure = vv.gcf() # se usar figure.DrawNow()

# Get axes objects
axes = vv.gca()

# Set a black background
axes.bgcolor = 'White'

# Deactivate the grid and make the x, y, z axes invisible
axes.axis.showGrid = False
axes.axis.visible = False

# Set some camera settings
# Please note: if you want to "fly" arond the comet with w, a, s, d (translation) and i, j, k, l
# (tilt) replace '3d' with 'fly'
axes.camera = '3d'

# Field of view in degrees
axes.camera.fov = 60

# Set default azmiuth and elevation angle in degrees
axes.camera.azimuth = 120
axes.camera.elevation = 25

# Draw figure
#figure.DrawNow()

# Save image of Object
#image = vv.getframe(vv.gca())
#image = (image*255).astype(np.uint8)
#imageio.imwrite('Comet67P.png', image)

# Run the application!
app.Run()


####################---Make GIF---####################

# Create visvis application
app = vv.use()
app.Create()

# Create main window frame and set a resolution.
main_w = MainWindow()
main_w.resize(700, 320)

# Create the 3 D shape model as a mesh. verticesPerFace equals 3 since triangles define the
# mesh's surface in this case
shape_obj = vv.mesh(vertices=VERTICES, faces=faces, verticesPerFace=3)
shape_obj.specular = 0.0
shape_obj.diffuse = 0.9

# Get figure
figure = vv.gcf()

# Get axes objects and set figure parameters
axes = vv.gca()

# Set a black background
axes.bgcolor = 'black'

# Deactivate the grid and make the x, y, z axes invisible
axes.axis.showGrid = False
axes.axis.visible = False

# Set camera settings
axes.camera = '3d'
axes.camera.fov = 60
axes.camera.zoom = 0.2

# Turn off the main light
axes.light0.Off()

# Create a fixed light source
light_obj = axes.lights[1]
light_obj.On()
light_obj.position = (5.0, 5.0, 5.0, 0.0)

# Empty array that contains all images of the comet's rotation
comet_images = []

# Rotate camera in 300 steps in azimuth
for azm_angle in range(300):

    # Change azimuth angle of the camera
    axes.camera.azimuth = 360 * float(azm_angle) / 300

    # Draw the axes and figure
    axes.Draw()
    figure.DrawNow()

    # Get the current image
    temp_image = vv.getframe(vv.gca())

    # Apped the current image in 8 bit integer
    comet_images.append((temp_image*255).astype(np.uint8))

# Close Window
main_w.close()

# Save the images as an animated GIF
print('Saving GIF ...')
imageio.mimsave('Comet67P.gif', comet_images, duration=0.04)
input('Enter to exit...')