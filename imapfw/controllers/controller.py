# The MIT License (MIT).
# Copyright (c) 2015-2018, Nicolas Sebrecht & contributors.

"""

A controller is defined in a repository to control its end-driver.

Controllers can be chained to each others so that the flows pass through each.

They can either be passive or active. Passive controllers follow-up the requests
and return results as-is. Active controllers changes the flow to achieve their
tasks. IOW, each controller can only view what the underlying controller accepts
to show. The order in the chain is relevant.

The controller base "Controller" is a passive controller (see code below).


SCHEMATIC OVERVIEW EXAMPLE (right side)
---------------------------------------

                 (filter)      (tracker)      (encoder)
+----------+   +----------+   +----------+   +----------+   +----------+
|          |-->|          |-->|          |-->|          |-->|          |
|  engine  |   |controller+   |controller|   |controller|   |  driver  |
|          |<--|          |<--|          |<--|          |<--|          |
+----------+   +----------+   +----------+   +----------+   +----------+
                 [active]       [passive]      [active]
                              notifications,  UTF-7/UTF-8
                                debugging


"""


class Controller(object):
    def __init__(self, repositoryName, repositoryConf, conf):
        self.repositoryName = repositoryName
        # Merge the repository configuration with the controller configuration.
        self.conf = repositoryConf.copy()
        self.conf.update(conf.copy())

        self.driver = None

    def __getattr__(self, name):
        return getattr(self.driver, name)

    def fw_drive(self, driver):
        self.driver = driver

    def getClassName(self):
        return self.__class__.__name__

    def initialize(self):
        """Override this method to make initialization in your app."""
