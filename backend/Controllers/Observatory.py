class ObservatoryController:

    def __init__(self,mount_controller):

        self.mount_controller = mount_controller

    def emergency_stop(self):
        if self.mount_controller.is_connected():
            self.mount_controller.stop_motion()

    def shutdown(self):
        if self.mount_controller.is_connected():
            self.mount_controller.disconnect()
