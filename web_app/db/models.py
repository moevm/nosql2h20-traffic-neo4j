from neomodel import StringProperty
from neomodel import IntegerProperty
from neomodel import FloatProperty
from neomodel import StructuredNode
from neomodel import db


class WayNode(StructuredNode):
    id = IntegerProperty(required=True)
    lat = FloatProperty(required=True)
    lon = FloatProperty(required=True)

    @classmethod
    def match(cls, lat=0.0, lon=0.0):
        query = f'''
            match (n:{cls.__name__})
            where {lat-0.002} <= n.lat and n.lat <= {lat+0.002} and
	              {lon-0.002} <= n.lon and n.lon <= {lon+0.002}
            with collect(n) as w_nodes
            unwind w_nodes as w_node
            with point({{longitude: w_node.lon, latitude: w_node.lat}}) as p1,
                 point({{longitude: {lon}, latitude: {lat}}}) as p2,
                 w_nodes
            with collect(distance(p1, p2)) as dists, min(distance(p1, p2)) as min_dist, w_nodes
            return w_nodes[[i in range(0, size(dists)-1) where dists[i] = min_dist][0]]
        '''

        results, _ = db.cypher_query(query=query)
        return WayNode.inflate(results[0][0])

    @classmethod
    def kShortestPaths(cls, id0, id1, k=1):
        query = f'''
            match (s:{cls.__name__} {{id: {id0}}}),
                  (f:{cls.__name__} {{id: {id1}}})
            call gds.alpha.kShortestPaths.stream( {{
                startNode: s,
                endNode: f,
                k: {k},
                path: true,
                relationshipWeightProperty: 'distance',
                nodeProjection: 'WayNode',
                relationshipProjection: {{
                    Way: {{
                        type: 'Way',
                        properties: 'distance'
                    }}
                }}
            }})
            yield nodeIds, costs
            return [node in gds.util.asNodes(nodeIds) | node] AS nodes,
                   reduce(acc = 0.0, cost in costs | acc + cost) AS distance
        '''
        results, _ = db.cypher_query(query=query)
        return [[WayNode.inflate(node) for node in path[0]] for path in results],\
               [result[1] for result in results]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, lat={self.lat}, lon={self.lon})'


class Building(StructuredNode):
    id = IntegerProperty(required=True)
    street = StringProperty(required=True)
    housenumber = StringProperty(required=True)
    lat = FloatProperty(required=True)
    lon = FloatProperty(required=True)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, street={self.street}, housenumber={self.housenumber}, lat={self.lat}, lon={self.lon})'