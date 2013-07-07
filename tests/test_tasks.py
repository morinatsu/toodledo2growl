#!/bin/python
# -*- coding:utf-8 -*-
"""
unit test for toodledo2growl.tasks
"""

import os
import sys
import unittest
from mock import MagicMock, patch
from poodledo import apiclient

sys.path.insert(0, os.path.abspath('../'))


def _dummy_config_get(section, item):
    if (section == 'credential') and (item == 'app_id'):
        return 'testoftasks'
    elif (section == 'credential') and (item == 'app_token'):
        return 'apptokenfortasks'
    elif (section == 'credential') and (item == 'email'):
        return 'emailfortasks'
    elif (section == 'credential') and (item == 'password'):
        return 'passwordfortasks'
    else:
        pass


class TestHotList(unittest.TestCase):
    """ test HotList """
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestRetrieveNormal(TestHotList):
    """ normal retrieve() """
    @patch('poodledo.apiclient.ApiClient')
    def test_retrieve_one(self, apic):
        apic.return_value = MagicMock(name='ApiClient',
                spec=apiclient.ApiClient)
        apic.return_value.authenticate = MagicMock(name='authenticate')
        apic.return_value.getAccountInfo = MagicMock(name='getAccountInfo')
        del apic.return_value.getAccountInfo.return_value.hotlistduedate
        apic.return_value.getTasks = MagicMock(name='getTasks')
        mock_task = MagicMock(name='mocked_task')
        attr = {'duedate': None,
                'star': None,
                'priority': 5,
                'status': 1,
                'title': 'retrieve one'
               }
        mock_task.configure_mock(**attr)
        del mock_task.completed
        apic.return_value.getTasks.return_value = [mock_task, ]
        import tasks
        hotlist = tasks.HotList()
        result = list(hotlist.retrieve())
        self.assertEqual(result, [mock_task])

    def test_retrieve_multi(self):
        pass

    def test_retrieve_empty(self):
        pass


class TestRetrieveError(TestHotList):
    """ retrieve() error """
    def test_retrieve_error(self):
        pass


class TestIsHot(TestHotList):
    """ normal retrieve() """
    def test_hot(self):
        pass

    def test_low_priority(self):
        pass

    def test_no_priority(self):
        pass

    def test_not_started(self):
        pass

    def test_no_duedate(self):
        pass

    def test_no_star(self):
        pass

    def test_unstared(self):
        pass

    def test_has_not_status(self):
        pass

    def test_is_not_next_action(self):
        pass


if __name__ == '__main__':
    unittest.main()
