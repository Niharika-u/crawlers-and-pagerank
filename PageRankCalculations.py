from neo4j import GraphDatabase


class PageRankCalculations:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def calculate_page_rank(self):
        with self.driver.session() as session:
            self._convert_graph_to_pagerank(session)
            self._get_page_rank(session)

    @staticmethod
    def _convert_graph_to_pagerank(session):
        result = session.run("""
            CALL gds.graph.project(
              'page_rank',
              'Page',
              'LINKS',
              {
                relationshipProperties: 'weight'
              }
            )
        """)
        print(result)

    @staticmethod
    def _get_page_rank(session):
        result = session.run("""
           CALL gds.pageRank.stream('page_rank')
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).name AS name, score
            ORDER BY score DESC, name ASC
        """)
        for record in result:
            print(record)



