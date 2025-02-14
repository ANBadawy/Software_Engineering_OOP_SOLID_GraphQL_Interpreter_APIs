import graphene
from kpi_app.schema import Query, Mutation

class Query(Query, graphene.ObjectType):
    pass

class Mutation(Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
