import graphene as g
import app.message.schema


class Query(app.message.schema.Query, g.ObjectType):
    pass


class Mutation(app.message.schema.Mutation, g.ObjectType,):
    pass


schema = g.Schema(query=Query, mutation=Mutation)
