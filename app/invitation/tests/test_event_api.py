# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from django.test import TestCase
# from django.utils import timezone
#
# from rest_framework import status
# from rest_framework.test import APIClient
#
# from core.models import Event
#
# from invitation.serializers import EventSerializer
#
# EVENT_URL = reverse('invitation:event-list')
#
#
# class PublicIngredientsApiTests(TestCase):
#     """Test the publically available Events API"""
#
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_login_required(self):
#         """Test that login is required to access this endpoint"""
#         res = self.client.get(EVENT_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class PrivateIngredientsAPITests(TestCase):
#     """Test events can be retrieved by authorized user"""
#
#     def setUp(self):
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             firstname='TestFirstName',
#             middlename="TestMiddleName",
#             lastname="TestLastName",
#             phonenumber='1234567890',
#             emailid="test@testmail.com",
#             dob="1900-01-01",
#             gender="Not Disclosed",
#             firebaseuserid="qwerty123456asdfgh0987"
#         )
#         self.client.force_authenticate(self.user)
#
#     def test_retrieve_event_list(self):
#         """Test retrieving a list of events"""
#         Event.objects.create(eventtype='MR',
#                              eventdatetimestamp=timezone.now(),
#                              eventdescription='Big fat wedding',
#                              venueid='001',
#                              user=self.user)
#         Event.objects.create(eventtype='BD',
#                              eventdatetimestamp=timezone.now(),
#                              eventdescription='Birthday Party',
#                              venueid='002',
#                              user=self.user)
#
#         res = self.client.get(EVENT_URL)
#
#         event = Event.objects.all().order_by('-eventid')
#         serializer = EventSerializer(event, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)
#
#     def test_event_limited_to_user(self):
#         """Test that only events for authenticated user are returned"""
#         user2 = get_user_model().objects.create_user(
#             firstname='Test2FirstName',
#             middlename="Test2MiddleName",
#             lastname="Test2LastName",
#             phonenumber='1234567899',
#             emailid="test2@testmail.com",
#             dob="1900-02-02",
#             gender="Not Disclosed",
#             firebaseuserid="qwerty123456asdfgh7890"
#         )
#         Event.objects.create(eventtype='MR',
#                              eventdatetimestamp=timezone.now(),
#                              eventdescription='Big fat wedding',
#                              venueid='001',
#                              user=user2)
#
#         event = Event.objects.create(eventtype='BD',
#                                      eventdatetimestamp=timezone.now(),
#                                      eventdescription='Birthday Party',
#                                      venueid='002',
#                                      user=self.user)
#
#         res = self.client.get(EVENT_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(res.data), 1)
#         self.assertEqual(res.data[0]['eventdescription'],
#                          event.eventdescription)
