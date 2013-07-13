#!/bin/python
# -*- coding:utf-8 -*-
"""
unit test for toodledo2growl.tasks
"""

import os
import sys
from datetime import datetime
import unittest
from mock import MagicMock, patch

sys.path.insert(0, os.path.abspath('../'))
import tasks


class TestHotList(unittest.TestCase):
    """ test HotList """
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestRetrieveNormal(TestHotList):
    """ normal retrieve() """
    def setUp(self):
        self.patcher = patch('tasks.ApiClient')
        self.apic = self.patcher.start()
        self.apic.return_value = MagicMock(name='ApiClient',
                spec=tasks.ApiClient)
        self.apic.return_value.authenticate = MagicMock(name='authenticate')
        self.apic.return_value.getAccountInfo = MagicMock(name='getAccountInfo')
        del self.apic.return_value.getAccountInfo.return_value.hotlistduedate
        self.apic.return_value.getTasks = MagicMock(name='getTasks')

    def tearDown(self):
        self.patcher.stop()

    def test_retrieve_one(self):
        mock_task = MagicMock(name='mocked_task')
        attr = {'duedate': None,
                'star': None,
                'priority': 5,
                'status': 1,
                'title': 'retrieve one'
               }
        mock_task.configure_mock(**attr)
        del mock_task.completed
        self.apic.return_value.getTasks.return_value = [mock_task, ]
        hotlist = tasks.HotList()
        result = list(hotlist.retrieve())
        self.assertEqual(result, [mock_task])

    def test_retrieve_multi(self):
        mock_task_1st = MagicMock(name='mocked_task_1st')
        attr_1st = {'duedate': None,
                    'star': None,
                    'priority': 5,
                    'status': 1,
                    'title': 'retrieve one'
                   }
        mock_task_1st.configure_mock(**attr_1st)
        del mock_task_1st.completed
        mock_task_2nd = MagicMock(name='mocked_task_2nd')
        attr_2nd = {'duedate': None,
                    'star': None,
                    'priority': 5,
                    'status': 1,
                    'title': 'retrieve two'
                   }
        mock_task_2nd.configure_mock(**attr_2nd)
        del mock_task_2nd.completed
        self.apic.return_value.getTasks.return_value = [mock_task_1st, mock_task_2nd]
        hotlist = tasks.HotList()
        result = list(hotlist.retrieve())
        self.assertEqual(result, [mock_task_1st, mock_task_2nd])

    def test_retrieve_empty(self):
        self.apic.return_value.getTasks.return_value = []
        hotlist = tasks.HotList()
        result = list(hotlist.retrieve())
        self.assertEqual(result, [])


class TestRetrieveError(TestHotList):
    """ retrieve() error """
    def setUp(self):
        self.patcher = patch('tasks.ApiClient')
        self.apic = self.patcher.start()
        self.apic.return_value = MagicMock(name='ApiClient',
                spec=tasks.ApiClient)
        self.apic.return_value.authenticate = MagicMock(name='authenticate')
        self.apic.return_value.getAccountInfo = MagicMock(name='getAccountInfo')
        del self.apic.return_value.getAccountInfo.return_value.hotlistduedate
        self.apic.return_value.getTasks = MagicMock(name='getTasks')

    def tearDown(self):
        self.patcher.stop()

    def test_retrieve_error(self):
        self.apic.return_value.getTasks.side_effect = Exception('error on server')
        hotlist = tasks.HotList()
        with self.assertRaisesRegexp(Exception, r'error on server'):
            result = list(hotlist.retrieve())


class TestIsHot(TestHotList):
    """ normal retrieve() """
    def setUp(self):
        self.patcher = patch('tasks.ApiClient')
        self.apic = self.patcher.start()
        self.apic.return_value = MagicMock(name='ApiClient',
                spec=tasks.ApiClient)
        self.apic.return_value.authenticate = MagicMock(name='authenticate')
        self.apic.return_value.getAccountInfo = MagicMock(name='getAccountInfo')
        del self.apic.return_value.getAccountInfo.return_value.hotlistduedate
        self.apic.return_value.getAccountInfo.return_value.hotlistpriority = 3
        self.apic.return_value.getTasks = MagicMock(name='getTasks')

    def tearDown(self):
        self.patcher.stop()

    def test_hot(self):
        mock_task = MagicMock(name='mocked_task')
        attr = {'duedate': None,
                'star': None,
                'priority': 5,
                'status': 1,
                'title': 'retrieve one'
               }
        mock_task.configure_mock(**attr)
        del mock_task.completed
        self.apic.return_value.getTasks.return_value = [mock_task, ]
        hotlist = tasks.HotList()
        result = list(hotlist.retrieve())
        self.assertEqual(result, [mock_task])

    def test_low_priority(self):
        mock_task = MagicMock(name='mocked_task')
        attr = {'duedate': None,
                'star': None,
                'priority': 1,
                'status': 1,
                'title': 'retrieve one'
               }
        mock_task.configure_mock(**attr)
        del mock_task.completed
        self.apic.return_value.getTasks.return_value = [mock_task, ]
        hotlist = tasks.HotList()
        result = list(hotlist.retrieve())
        self.assertEqual(result, [])

    def test_no_priority(self):
        del self.apic.return_value.getAccountInfo.return_value.hotlistpriority
        mock_task = MagicMock(name='mocked_task')
        attr = {'duedate': None,
                'star': None,
                'priority': 1,
                'status': 1,
                'title': 'retrieve one'
               }
        mock_task.configure_mock(**attr)
        del mock_task.completed
        self.apic.return_value.getTasks.return_value = [mock_task, ]
        hotlist = tasks.HotList()
        result = list(hotlist.retrieve())
        self.assertEqual(result, [mock_task])

    def test_not_started(self):
        self.apic.return_value.getAccountInfo.return_value.hotliststar= '1'
        mock_task = MagicMock(name='mocked_task')
        attr = {'duedate': None,
                'star': '0',
                'priority': 5,
                'status': 1,
                'title': 'retrieve one'
               }
        mock_task.configure_mock(**attr)
        del mock_task.completed
        self.apic.return_value.getTasks.return_value = [mock_task, ]
        hotlist = tasks.HotList()
        result = list(hotlist.retrieve())
        self.assertEqual(result, [])

    def test_no_duedate(self):
        mock_task = MagicMock(name='mocked_task')
        attr = {'duedate': datetime.today(),
                'star': '1',
                'priority': 5,
                'status': 1,
                'title': 'retrieve one'
               }
        mock_task.configure_mock(**attr)
        del mock_task.completed
        self.apic.return_value.getTasks.return_value = [mock_task, ]
        hotlist = tasks.HotList()
        result = list(hotlist.retrieve())
        self.assertEqual(result, [mock_task])

    def test_no_star(self):
        mock_task = MagicMock(name='mocked_task')
        attr = {'duedate': None,
                'star': '0',
                'priority': 5,
                'status': 1,
                'title': 'retrieve one'
               }
        mock_task.configure_mock(**attr)
        del mock_task.completed
        self.apic.return_value.getTasks.return_value = [mock_task, ]
        hotlist = tasks.HotList()
        result = list(hotlist.retrieve())
        self.assertEqual(result, [mock_task, ])

    def test_has_not_status(self):
        del self.apic.return_value.getAccountInfo.return_value.hotliststatus
        mock_task = MagicMock(name='mocked_task')
        attr = {'duedate': None,
                'star': None,
                'priority': 5,
                'status': 1,
                'title': 'retrieve one'
               }
        mock_task.configure_mock(**attr)
        del mock_task.completed
        self.apic.return_value.getTasks.return_value = [mock_task, ]
        hotlist = tasks.HotList()
        result = list(hotlist.retrieve())
        self.assertEqual(result, [mock_task])

    def test_is_not_next_action(self):
        self.apic.return_value.getAccountInfo.return_value.hotliststatus = '1'
        mock_task = MagicMock(name='mocked_task')
        attr = {'duedate': None,
                'star': None,
                'priority': 5,
                'status': 2,
                'title': 'retrieve one'
               }
        mock_task.configure_mock(**attr)
        del mock_task.completed
        self.apic.return_value.getTasks.return_value = [mock_task, ]
        hotlist = tasks.HotList()
        result = list(hotlist.retrieve())
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
