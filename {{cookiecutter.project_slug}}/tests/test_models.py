#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase

from {{cookiecutter.package_name}} import factories, models


class TestSampleModel(TestCase):

    def test_something(self):
        self.assertIsNotNone(models)

    def test_user_factory(self):
        user = factories.UserFactory()
        self.assertIsNotNone(user)
