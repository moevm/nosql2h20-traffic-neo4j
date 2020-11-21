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
            MATCH (n:{cls.__name__})
            WHERE {lat-0.002} <= n.lat and n.lat <= {lat+0.002} AND
	              {lon-0.002} <= n.lon and n.lon <= {lon+0.002}
            WITH n, distance(point({{longitude:n.lon,latitude:n.lat}}), point({{latitude: 59.8644123, longitude: 30.3490114}})) as dist
            ORDER BY dist ASC
            RETURN n limit 1
        '''

        results, _ = db.cypher_query(query=query)
        return WayNode.inflate(results[0][0])

    @classmethod
    def kShortestPaths(cls, id0, id1, k=1):
        query = f'''
            MATCH (s:{cls.__name__} {{id: {id0}}}),
                  (f:{cls.__name__} {{id: {id1}}})
            CALL gds.alpha.kShortestPaths.stream( {{
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
            YIELD nodeIds, costs
            RETURN gds.util.asNodes(nodeIds) AS nodes,
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