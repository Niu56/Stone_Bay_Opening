# Import javascript modules
from js import THREE, window, document, Object
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math

#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUAL SETUP
    # Declare the variables
    global renderer, scene, camera, controls, composer, axesHelper
    
    #Set up the renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

    # Set up the scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0.1,0.1,0.1)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.z = 50
    scene.add(camera)

    # Set the axis helper
    axesHelper = THREE.AxesHelper.new(5)
    scene.add( axesHelper )


    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation
    global brick_params, bricks_left, bricks_right, brick_line_right, brick_line_left, beam_list, beam_line_list
    bricks_right = []
    bricks_left = []
    brick_line_right = []
    brick_line_left = []
    beam_list = []
    beam_line_list = []
    brick_params = {
            "length" : 32,
            "width" : 12,
            "y" : 3,
            "x" : 5 
            }
    brick_params = Object.fromEntries(to_js(brick_params))

    global extrude_settings
    extrude_settings = {
        "steps": 2,
        "depth": 16,
        "bevelEnabled": True,
        "bevelThickness": 1,
        "bevelSize": 1,
        "bevelOffset": 0,
        "bevelSegments": 1
        }
    extrude_settings = Object.fromEntries(to_js(extrude_settings))    
    
    global material, line_material
    color = THREE.Color.new(224/255,199/255,173/255)
    material = THREE.MeshBasicMaterial.new()
    material.transparent = True
    material.opacity = 1
    material.color = color

    line_color = THREE.Color.new(162/255,119/255,66/255)
    line_material = THREE.LineBasicMaterial.new()
    line_material.color = line_color
    line_material.linewidth = 50
    

    global shape1
    shape1 = THREE.Shape.new()
    shape1.moveTo( 0, 0 )
    shape1.lineTo( 0, brick_params.width )
    shape1.lineTo( brick_params.length, brick_params.width )
    shape1.lineTo( brick_params.length, 0 )
    shape1.lineTo( 0, 0 )

    global shape2
    shape2 = THREE.Shape.new()
    shape2.moveTo( 0, 0 )
    shape2.lineTo( 0, brick_params.length )
    shape2.lineTo( brick_params.width, brick_params.length )
    shape2.lineTo( brick_params.width, 0 )
    shape2.lineTo( 0, 0 )

    global shape3
    shape3 = THREE.Shape.new()
    shape3.moveTo( 0, 0 )
    shape3.lineTo( 0, brick_params.width )
    shape3.lineTo( brick_params.length, brick_params.width )
    shape3.lineTo( brick_params.length, 0 )
    shape3.lineTo( 0, 0 )

    global shape4
    shape4 = THREE.Shape.new()
    shape4.moveTo( 0, 0 )
    shape4.lineTo( 0, brick_params.length )
    shape4.lineTo( brick_params.width, brick_params.length )
    shape4.lineTo( brick_params.width, 0 )
    shape4.lineTo( 0, 0 )    

    global beam
    beam = THREE.Shape.new()
    beam.moveTo( 0, 0 )
    beam.lineTo( 0, brick_params.width )
    beam.lineTo( 10 * brick_params.x + 2 * brick_params.length, brick_params.width )
    beam.lineTo( 10 * brick_params.x + 2 * brick_params.length, 0 )
    beam.lineTo( 0, 0 )        

# -----------------------------------------------------------------------------
    # Pillar 1 (Left)

    for i in range(brick_params.y):
        geometry = THREE.ExtrudeGeometry.new( shape1, extrude_settings )

        geometry.translate( 0, (2 * (brick_params.width + 2) * i) + (brick_params.width + 2), 0)

        brick1 = THREE.Mesh.new( geometry, material )
        bricks_left.append( brick1 )
        scene.add( brick1 )

        edges = THREE.EdgesGeometry.new( brick1.geometry )
        line_left = THREE.LineSegments.new( edges, line_material )
        brick_line_left.append( line_left )
        scene.add( line_left )

    for j in range(brick_params.y):
        geometry = THREE.ExtrudeGeometry.new( shape2, extrude_settings )

        geometry.translate((2 * (brick_params.width + 2) * j), 0, 0)
        geometry.rotateZ(math.radians(90))
        geometry.rotateY(math.radians(90))

        brick2 = THREE.Mesh.new( geometry, material )
        bricks_left.append( brick2 )
        scene.add( brick2 )

        edges = THREE.EdgesGeometry.new( brick2.geometry )
        line = THREE.LineSegments.new( edges, line_material )
        brick_line_left.append( line_left )
        scene.add( line_left )

# -----------------------------------------------------------------------------
    # Pillar 2 (Right)

    for k in range(brick_params.y):
        geometry = THREE.ExtrudeGeometry.new( shape3, extrude_settings )

        geometry.translate( 0, 2 * (brick_params.width + 2) * k, 0)
        
        brick3 = THREE.Mesh.new( geometry, material )
        bricks_right.append( brick3 )
        scene.add( brick3 )

        edges = THREE.EdgesGeometry.new( brick3.geometry )
        line_right = THREE.LineSegments.new( edges, line_material )
        brick_line_right.append( line_right )
        scene.add( line_right )

    for l in range(brick_params.y):
        geometry = THREE.ExtrudeGeometry.new( shape4, extrude_settings )

        geometry.translate(((2 * (brick_params.width + 2) * l) + (brick_params.width + 2)), 0, 0)
        geometry.rotateZ(math.radians(90))
        geometry.rotateY(math.radians(90))

        brick4 = THREE.Mesh.new( geometry, material )
        bricks_right.append( brick4 )
        scene.add( brick4 )

        edges = THREE.EdgesGeometry.new( brick4.geometry )
        line_right = THREE.LineSegments.new( edges, line_material )
        brick_line_right.append( line_right )
        scene.add( line_right )

# -----------------------------------------------------------------------------
    # Beam 

    for n in range(brick_params.y):
        geometry = THREE.ExtrudeGeometry.new( beam, extrude_settings )

        if n == brick_params.y-1:
            geometry.translate( - brick_params.length, (2 * (brick_params.width + 2) * n) + 2 * (brick_params.width + 2), 0)

        beam_geom = THREE.Mesh.new( geometry, material )
        beam_list.append( beam_geom )
        scene.add( beam_geom )

        edges = THREE.EdgesGeometry.new( beam_geom.geometry )
        line_beam = THREE.LineSegments.new( edges, line_material )
        beam_line_list.append( line_beam )
        scene.add( line_beam )

    #-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Set up GUI
    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    param_folder.add(brick_params, 'length', 8, 32, 1)
    param_folder.add(brick_params, 'y', 1, 10, 1)
    param_folder.add(brick_params, 'x', 5, 15, 1)
    param_folder.add(extrude_settings, 'depth', 1, 16, 1)
    param_folder.open()
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Update bricks

def update_bricks():

    # Number of bricks on Y axis
    # Pillar left

    global bricks_right, bricks_left, brick_line_left, brick_line_right, material, line_material, geometry, beam_list, beam_line_list
    if len(bricks_left) != 0:
        
        if len(bricks_left) != brick_params.y:
            for brick1 in bricks_left: scene.remove(brick1)
            for brick2 in bricks_left: scene.remove(brick2)
            for line_left in brick_line_left: scene.remove(line_left)
            bricks_left = []
            brick_line_left = []

            for i in range(brick_params.y):
                geometry = THREE.ExtrudeGeometry.new( shape1, extrude_settings )
                
                geometry.translate(0, (2 * (brick_params.width + 2) * i)+ (brick_params.width + 2), 0)
                geometry.rotateY(math.radians(-90))
            

                mesh = THREE.Mesh.new( geometry, material )
                bricks_left.append(mesh)
                scene.add( mesh )

                edges = THREE.EdgesGeometry.new( mesh.geometry )
                line_left = THREE.LineSegments.new( edges, line_material )
                brick_line_left.append(line_left)
                scene.add( line_left )
            
            for j in range(brick_params.y):
                geometry = THREE.ExtrudeGeometry.new( shape2, extrude_settings )
                
                geometry.translate((2 * (brick_params.width + 2) * j), 0, 0)
                geometry.rotateZ(math.radians(90))

                mesh = THREE.Mesh.new( geometry, material )
                bricks_left.append(mesh)
                scene.add( mesh )

                edges = THREE.EdgesGeometry.new( mesh.geometry )
                line_left = THREE.LineSegments.new( edges, line_material )
                brick_line_left.append(line_left)
                scene.add( line_left )

        else:
            for i in range(len(bricks_left)): 
                brick1 = bricks_left[i]
                line_left = brick_line_left[i]

                geometry = THREE.ExtrudeGeometry.new( shape1, extrude_settings )

                geometry.translate(0,(2* (brick_params.width + 2) * i) + (brick_params.width + 2), 0)
                geometry.rotateY(math.radians(-90))
                
                mesh = THREE.Mesh.new( geometry, material )

                brick1.geometry = geometry

                edges = THREE.EdgesGeometry.new( brick1.geometry )
                line_left.geometry = edges

            for j in range(len(bricks_left)): 
                brick2 = bricks_left[j]
                line_left = brick_line_left[j]

                geometry = THREE.ExtrudeGeometry.new( shape2, extrude_settings )

                geometry.translate((2 * (brick_params.width + 2) * j), 0, 0)
                geometry.rotateZ(math.radians(90))
                
                mesh = THREE.Mesh.new( geometry, material )

                brick2.geometry = geometry

                edges = THREE.EdgesGeometry.new( brick2.geometry )
                line_left.geometry = edges


    # Distance between pillars and number of bricks on Y axis in 2nd pillar
    # Pillar Right


        if len(bricks_right) != 0:
            
            for m in range(brick_params.x):

                if len(bricks_right) != brick_params.y:
                    for brick3 in bricks_right: scene.remove(brick3)
                    for brick4 in bricks_right: scene.remove(brick4)
                    for line_right in brick_line_right: scene.remove(line_right)
                    bricks_right = []
                    brick_line_right = []

                    for k in range(brick_params.y):
                        geometry = THREE.ExtrudeGeometry.new( shape3, extrude_settings )
                        
                        geometry.translate(0, 2 * (brick_params.width + 2) * k, 0)
                        geometry.translate(10 * m, 0, 0)

                        mesh = THREE.Mesh.new( geometry, material )
                        bricks_right.append(mesh)
                        scene.add( mesh )

                        edges = THREE.EdgesGeometry.new( mesh.geometry )
                        line_right = THREE.LineSegments.new( edges, line_material )
                        brick_line_right.append(line_right)
                        scene.add( line_right )
                    
                    for l in range(brick_params.y):
                        geometry = THREE.ExtrudeGeometry.new( shape4, extrude_settings )
                        
                        geometry.translate(((2 * (brick_params.width + 2) * l) + (brick_params.width + 2)), 0, 0)
                        geometry.translate(0, 0, 10 * m)
                        geometry.rotateZ(math.radians(90))
                        geometry.rotateY(math.radians(90))

                        mesh = THREE.Mesh.new( geometry, material )
                        bricks_right.append(mesh)
                        scene.add( mesh )

                        edges = THREE.EdgesGeometry.new( mesh.geometry )
                        line_right = THREE.LineSegments.new( edges, line_material )
                        brick_line_right.append(line_right)
                        scene.add( line_right )

                else:
                    for k in range(len(bricks_right)): 
                        brick3 = bricks_right[k]
                        line_right = brick_line_right[k]

                        geometry = THREE.ExtrudeGeometry.new( shape3, extrude_settings )

                        geometry.translate(0, (brick_params.width + 2) * k, 0)
                        geometry.translate(10 * m, 0, 0)
                        
                        mesh = THREE.Mesh.new( geometry, material )

                        brick3.geometry = geometry

                        edges = THREE.EdgesGeometry.new( brick3.geometry )
                        line_right.geometry = edges

                    for l in range(len(bricks_right)): 
                        brick4 = bricks_right[l]
                        line_right = brick_line_right[l]

                        geometry = THREE.ExtrudeGeometry.new( shape4, extrude_settings )

                        geometry.translate(((2 * (brick_params.width + 2) * l) + (brick_params.width + 2)), 0, 0)
                        geometry.translate(0, 0, 10 * m)
                        geometry.rotateZ(math.radians(90))
                        geometry.rotateY(math.radians(90))
                        
                        mesh = THREE.Mesh.new( geometry, material )

                        brick4.geometry = geometry

                        edges = THREE.EdgesGeometry.new( brick4.geometry )
                        line_right.geometry = edges
        
        if len(beam_list) != 0:

            for p in range(brick_params.x):

                global beam
                beam = THREE.Shape.new()
                beam.moveTo( 0, 0 )
                beam.lineTo( 0, brick_params.width )
                beam.lineTo( 10*p + 2 * brick_params.length, brick_params.width )
                beam.lineTo( 10*p + 2 * brick_params.length, 0 )
                beam.lineTo( 0, 0 )        


                if len(beam_list) != brick_params.y:
                    for beam_geom in beam_list: scene.remove(beam_geom)
                    for line_beam in beam_line_list : scene.remove(line_beam)
                    beam_list = []
                    beam_line_list = []

                    for n in range(brick_params.y):
                        geometry = THREE.ExtrudeGeometry.new( beam, extrude_settings )
                        
                        if n == brick_params.y-1:

                            geometry.translate( - brick_params.length, (2 * (brick_params.width + 2) * n) + 2 * (brick_params.width + 2), 0)

                        beam_geom = THREE.Mesh.new( geometry, material )
                        beam_list.append( beam_geom )
                        scene.add( beam_geom )

                        edges = THREE.EdgesGeometry.new( beam_geom.geometry )
                        line_beam = THREE.LineSegments.new( edges, line_material )
                        beam_line_list.append( line_beam )
                        scene.add( line_beam )

                else:
                    for n in range(len(beam_list)):
                        beam_geom = beam_list[n]
                        line_beam = beam_line_list[n]

                        geometry = THREE.ExtrudeGeometry.new( beam, extrude_settings )

                        if n == brick_params.y-1:
                            geometry.translate( - brick_params.length, (2 * (brick_params.width + 2) * n) + 2 * (brick_params.width + 2), 0)

                        mesh = THREE.Mesh.new( geometry, material )

                        beam_geom.geometry = geometry

                        edges = THREE.EdgesGeometry.new( beam_geom.geometry )
                        line_beam.geometry = edges


# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update_bricks()
    controls.update()
    #renderer.render(scene, camera)
    composer.render()

# Graphical post-processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()