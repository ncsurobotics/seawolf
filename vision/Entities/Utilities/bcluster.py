import matplotlib.pyplot as plt
import math
import Queue
import random
import pdb


class ClusterPt:
    def __init__(self, x, y, idx):
        self.x = x
        self.y = y
        self.idx = idx
        self.found = False

#pts = [ [1,2], [2,1], [10, 3], [ 10,2], [1,4] ]

"""
Clustering algorithm where all points in each cluster has to be within a maximum distance from another point in it.
Author: Ben Fisher
"""

def findClusters(pts, maxDist):

    #for i in range(5):
    #    pts.append( [random.randint(0,5), random.randint(0,5)] )
    #    pts.append( [random.randint(15,20), random.randint(15,20)] )

    #X = []
    #Y = []


    #make x and y data structures, just X: [ [coord, ptIdx], ... ], Y: [ coord, ...]
    cpts = []
    i = 0
    for i in range(len(pts)):
        cpts.append(ClusterPt(pts[i][0], pts[i][1], i))
    pts = cpts
    #sort pts by x
    def getFirst(elem):
        return elem.x

    pts.sort(key=getFirst)
    #print pts
    #print "-----------------------------------------------------------"

    for i in range(len(pts)):
        pts[i].idx = i

    ptIdx = 0
    foundCount = 0
    queue = Queue.Queue()

    ptCount = len(pts)

    clusters = [[]]
    clusterIdx = 0
    #pdb.set_trace()
    while foundCount < ptCount:
        #get neighbors
        #move right
        pts[ptIdx].found = True
        clusters[clusterIdx].append(pts[ptIdx])
        foundCount += 1
        idx = ptIdx + 1
        while idx < ptCount and abs(pts[idx].x - pts[ptIdx].x) <= maxDist:
            if math.sqrt( (pts[ptIdx].x - pts[idx].x) ** 2 + (pts[ptIdx].y - pts[idx].y) ** 2 ) <= maxDist and (not pts[idx].found):
                queue.put_nowait(pts[idx])
            idx += 1
        idx = ptIdx - 1
        #move left
        while idx > 0 and abs(pts[idx].x - pts[ptIdx].x) <= maxDist:
            if math.sqrt( (pts[ptIdx].x - pts[idx].x) ** 2 + (pts[ptIdx].y - pts[idx].y) ** 2 ) <= maxDist and (not pts[idx].found):
                queue.put_nowait(pts[idx])
            idx -= 1
        #skip found neighbors and set next in queue to ptidx
        found = True
        while found and (not queue.empty()):
            pt = queue.get_nowait()
            ptIdx = pt.idx
            found = pt.found
        if found:
            #find next point
            for pt in pts:
                if not pt.found:
                    ptIdx = pt.idx
                    clusters.append([])
                    clusterIdx += 1
                    break
        
    #ptTypes = [ 'ro', 'bs', 'gs', 'bo', 'go', 'gs' ]
    clusterIdx = 0
    for cluster in clusters:
        #ptType = ptTypes[clusterIdx % len(ptTypes)]
        #print ptType
        clusterIdx += 1
        #x = []
        #y = []
        for i in range(len(cluster)):
            cluster[i] = [cluster[i].x, cluster[i].y ]
            #x.append(pt.x)
            #y.append(pt.y)
        #plt.plot(x, y, ptType)
    #plt.axis([-1, 21, -1, 21])
    #plt.show()
    #print clusters
    def biggestCluster(cluster):
        return -len(cluster)
    clusters.sort(key=biggestCluster)
    return clusters
#print findClusters(pts, 4) 
