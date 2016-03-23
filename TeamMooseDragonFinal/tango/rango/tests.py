from django.test import TestCase, TransactionTestCase
from django.test.client import Client
from rango.models import User, UserProfile, Review, Er_Room
from rango.forms import UserForm, UserProfileForm
from rango.parser import Parse

import unittest
import logging
import os
import sqlite3 as lite

LOGGER = logging.getLogger(name='profile')


class UserTest(TestCase):
    """Test Case for User Profile"""
    
    LOGGER.debug("User & UserProfile Tests setUp")
    def setUp(self):
        self.leo = User.objects.create_user('leothelion','leothelion@hotmail.com', 'rawr',
                                            first_name="Leo", last_name="Lion")

        self.hippo = User.objects.create_user(first_name="Hungry", last_name="Hippo",
                                              username="hungryhippo", email="hungryhungry@hotmail.com", 
                                              password="food")


        self.leoprofile = UserProfile.objects.update_or_create(user=User.objects.get(username='leothelion'),
                                                      website="http://leo.com",
                                                      show_email=True,
                                                      posts=0)
        
        self.hippoprofile = UserProfile.objects.update_or_create(user=User.objects.get(username='hungryhippo'),
                                                      website="http://hippo.com",
                                                      show_email=False,
                                                      posts=0)
        
        self.client = Client()
    
    def test_user_created(self):
        print User.objects.all()

        self.assertEqual(User.objects.get(username='leothelion').first_name, "Leo")
        self.assertEqual(User.objects.get(username='leothelion').last_name, "Lion")
        self.assertEqual(User.objects.get(username='leothelion').email, "leothelion@hotmail.com")
        self.assertEqual(User.objects.count(), 2)
    
    def test_user_profile_created(self):
        print User.objects.all()
        print UserProfile.objects.all()
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertTrue(UserProfile.objects.get(user=User.objects.get(username='leothelion')).show_email)
        self.assertFalse(UserProfile.objects.get(user=User.objects.get(username='hungryhippo')).show_email)

    
    def test_view_profile(self):
        """Test to see if profile for leothelion can be viewed anon and logged in"""
        LOGGER.debug("Test GET /rango/view/leothelion/ for anon user")
        anon_view_response = self.client.get('/rango/view/leothelion/')
        self.assertContains(anon_view_response, "leothelion@hotmail.com")
 
        LOGGER.debug("Test GET /rango/view/leothelion/ for logged in user")
        self.client.login(username='leothelion', password='rawr')
        logged_in_view_response = self.client.get('/rango/view/leothelion/')
        self.assertContains(logged_in_view_response, "leothelion@hotmail.com")
        
        """Test to see if profile for hungryhippo can be viewed anon and logged in"""
        LOGGER.debug("Test GET /rango/view/hungyhippo/ for anon user")
        anon_view_response = self.client.get('/rango/view/hungryhippo/')
        self.assertNotContains(anon_view_response, "hungryhungry@hotmail.com")
        self.assertContains(anon_view_response, "Hungry")
 
        LOGGER.debug("Test GET /rango/view/hungryhippo/ for logged in user")
        self.client.login(username='hungryhippo', password='food')
        logged_in_view_response = self.client.get('/rango/view/hungryhippo/')
        self.assertContains(logged_in_view_response, "hungryhungry@hotmail.com")
        self.assertContains(anon_view_response, "Hippo")

    def test_edit_profile(self):
        
        """Test to see if profile for user1 can be edited anon and logged in"""
        
        LOGGER.debug("Test GET /rango/edit/ for anon user")
        anon_edit_response = self.client.get('/rango/edit/')
        # redirected to login page
        self.assertEquals(302, anon_edit_response.status_code)
        self.assertRedirects(anon_edit_response, "http://testserver/accounts/login/?next=/rango/edit/")

        LOGGER.debug("Test GET /rango/edit/ for logged in user")
        self.client.login(username='leothelion', password='rawr')
        logged_in_edit_response = self.client.get('/rango/edit/')
        self.assertContains(logged_in_edit_response, "leo")
    
class ReviewTest(TestCase):
    
    LOGGER.debug("Review Tests setUp")
    def setUp(self):
        self.leo = User.objects.create_user('leothelion','leothelion@hotmail.com', 'rawr',
                                            first_name="Leo", last_name="Lion")
        
        er1 = Review(title='ER 1', creator=self.leo)
        er1.save()
        self.assertEqual(er1.title, "ER 1")
    
    def test_post_review(self):
               
        LOGGER.debug("Test GET /rango/post/reply/# for anon user")
        anon_post_response = self.client.get('/rango/post/reply/1/')
        self.assertRedirects(anon_post_response,"http://testserver/accounts/login/?next=/rango/post/reply/1/")
        
        LOGGER.debug("Test GET /rango/post/reply/# for logged user")
        self.client.login(username='leothelion', password='rawr')
        logged_in_post_response = self.client.get('/rango/post/reply/1/')
        self.assertContains(logged_in_post_response, "Busyness")
        


class ParserTest(TestCase):
    
    LOGGER.debug("Parser Test")
    
    def test_parse_file(self):    
        MYDIR = os.path.dirname(__file__)
        filepath = str((os.path.join(MYDIR, '../ERtext.txt')))
        filepathdb = str((os.path.join(MYDIR, '../db.sqlite3')))
        a = Parse()    
        a.parsing(filepath, filepathdb)

        