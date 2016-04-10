
import sys


#
#   Class: Driver
#       Base class for drivers
#
class DriverBase:

    #
    #   Constructor:
    #       The constructor
    #
    #   Parameters:
    #       self - Self
    #       settings - Settings to initialize the driver with
    #
    def __init__(self, settings):
        self.machine_name = 'null'
        self.name = "NullDriver"
        self.settings = settings

    #
    #   Function: clone
    #       Clone services that are marked to be cloned
    #
    #   Parameters:
    #       self - Self
    #
    def clone(self):
        self.log("Clone not implemented")

    #
    #   Function: build
    #       Build services
    #
    #   Parameters:
    #       self - Self
    #
    def build(self):
        self.log("Build not implemented")

    #
    #   Function: start
    #       Start services
    #
    #   Parameters:
    #       self - Self
    #
    def start(self):
        self.log("Start not implemented")

    #
    #   Function: stop
    #       Stop running services
    #
    #   Parameters:
    #       self - Self
    #
    def stop(self):
        self.log("Stop not implemented")

    #
    #   Function: log
    #       Log a message
    #
    #   Parameters:
    #       self - Self
    #       msg - Message to log
    #
    #   Returns:
    #       def
    #
    def log(self, msg):
        print "\033[92m" + self.name + " \033[0m" + msg
        sys.stdout.flush()

    #
    #   Function: set_branch_container
    #       Set the <BranchContainer> for this driver.
    #
    #   Parameters:
    #       self - Self
    #       container - Set the container
    #
    def set_branch_container(self, container):
        self.branch_container = container
