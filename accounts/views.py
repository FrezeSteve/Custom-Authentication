# from django.shortcuts import get_object_or_404
# from .serializers import AccountSerializer
# from . import models
# from rest_framework import viewsets, authtoken
# from rest_framework.response import Response
# from rest_framework.authentication import TokenAuthentication
# from django.utils.decorators import method_decorator
#
#
# # TODO: Integrate with third-party identity providers eg Google, Facebook and Twitter
# # TODO: Let users delete their accounts
#
#
# class AccountViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """S
#     authentication_classes = [TokenAuthentication]
#
#     @staticmethod
#     def list(request):
#         queryset = models.User.objects.all()
#         serializer = AccountSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     @staticmethod
#     def retrieve(request, pk=None):
#         queryset = models.User.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = AccountSerializer(user)
#         return Response(serializer.data)
#
#     # endpoint to create a user
#     @method_decorator
#     def create(self, request):
#         return Response()
#
#     # endpoint to update user details
#     def update(self, request, pk=None):
#         return Response()
#
#     # endpoint to delete a user
#     def destroy(self, request, pk=None):
#         return Response()
#
#
# # class TokenAuth(authtoken):
# #     pass