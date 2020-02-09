import json
import graphene as g
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id
from app.message.models import Message


# 0. create type
class UserType(DjangoObjectType):
    class Meta:
        model = User


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        filter_fields = {'message': ['icontains']}
        interfaces = (g.Node, )


# 1. create query
class Query(g.AbstractType):
    current_user = g.Field(UserType)
    message = g.Field(MessageType, id=g.ID())
    all_messages = DjangoFilterConnectionField(MessageType)

    def resolve_current_user(self, args, context, info):
        if not context.user.is_authenticated():
            return None
        return context.user

    def resolve_message(self, args, context, info):
        rid = from_global_id(args.get('id'))
        return Message.objects.get(pk=rid[1])

    def resolve_all_messages(self, args, context, info):
        return Message.objects.all()


# 2. create mutation
class CreateMessageMutation(g.Mutation):
    class Input:
        message = g.String()

    status = g.Int()
    formErrors = g.String()
    message = g.Field(MessageType)

    @staticmethod
    def mutate(root, args, context, info):
        if not context.user.is_authenticated():
            return CreateMessageMutation(status=403)
        message = args.get('message', '').strip()
        if not message:
            return CreateMessageMutation(
                status=400,
                formErrors=json.dumps(
                    {'message': ['Please enter a message.']}))
        obj = Message.objects.create(
            user=context.user, message=message
        )
        return CreateMessageMutation(status=200, message=obj)


class Mutation(g.AbstractType):
    create_message = CreateMessageMutation.Field()



