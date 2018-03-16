#Author-Steven Kraemer
#Description-Connect sketch points that are very close.

import adsk.core, adsk.fusion, adsk.cam, traceback, time

def centerPoint(point):
    ret = False

    try:
        if point.connectedEntities: #IF the point is connected to anything...
            for item in point.connectedEntities: #Get the connected objects
                #If a circle or Arc...
                if isinstance(item, adsk.fusion.SketchArc) or isinstance(item, adsk.fusion.SketchCircle):
                    if item.centerSketchPoint == point: #If the point is a center, return true.
                        ret = True
    except:
        #Unknown...
        print('exception')
    return ret
        
def validatePoint(point):
    ret = False
    if point.isValid and point.connectedEntities and not centerPoint(point):
        ret = True
    return ret
        

def run(context):
    ui = None
    threshold_distance = 0.09
    merge_count = 0
    error_count = 0
    t0 = time.clock()
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        selection = ui.activeSelections.all
        points = adsk.core.ObjectCollection.create()
        
        #Add only sketchpoints to the points collection
        [points.add(item) for item in selection if isinstance(item, adsk.fusion.SketchPoint)]
        print(len(points))
        #Enumerate (add an index to the )
        for index,point in enumerate(points): 
            #Ignore invalid points, points that aren't connected to objects, and aren't center points for circles, arcs, and curves... 
            if validatePoint(point):
                for merge in points[index+1:]:
                    if validatePoint(merge):
                        distance = point.geometry.distanceTo(merge.geometry)
                        if 0.0 <= distance < threshold_distance:
                            try:
                                point.merge(merge)
                            except:
                                error_count += 1
                            merge_count += 1
                            adsk.doEvents()
        duration = time.clock() - t0
        ui.messageBox("ConnectTheDots has completed !\nConnected " + str(merge_count) + " dots of " + str(points.count) + " selected.\nThere were " + str(error_count) + " errors.\nDuration (seconds): " + str(duration) )

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
